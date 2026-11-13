#!/usr/bin/env python3
"""
PKA Session Extractor — extrait décisions, faits et préférences
des JSON de session DeepSeek TUI et les injecte dans team.db.

Usage:
    python3 scripts/pka_session_extract.py <session.json>
    python3 scripts/pka_session_extract.py --batch ~/.deepseek/sessions/
    python3 scripts/pka_session_extract.py --latest   # dernière session

Sorties:
    - knowledge    : décisions, faits, préférences, briefs
    - retro_patterns : blocages, échecs
    - dobby_feedback  : corrections de JCH

Part of PKA Memory Layer — docs/system/pka-memory-layer.md
"""

import json
import re
import sys
import sqlite3
import os
from datetime import datetime
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "TEAM", "team.db")
SESSION_DIR = os.path.expanduser("~/.deepseek/sessions/")

# Patterns pour détecter des décisions dans les messages assistant
DECISION_PATTERNS = [
    r"(?i)\b(décision|décidé|validé|acté)\b[:\s]*(.+)",
    r"(?i)\b(ADR|architecture decision)\b[:\s]*(.+)",
    r"(?i)\b(on va|on a décidé|j'ai décidé)\b[:\s]*(.+)",
    r"(?i)^[\s]*[-*]\s*\[DÉCISION\]\s*(.+)",
    r"(?i)\b(Décision[:])\s*(.+)",
]

# Patterns pour les corrections de JCH (feedback)
FEEDBACK_PATTERNS = [
    (r"(?i)\bnon[,.]?\s*(fais|plutôt|utilise|essaie|corrige)\b", "correction"),
    (r"(?i)\b(fais plutôt|utilise plutôt|plutôt)\b", "correction"),
    (r"(?i)\b(OK|oui|vas-y|lance|parfait|super|bravo)\b", "acceptance"),
    (r"(?i)\b(pas maintenant|laisse tomber|annule|pas la peine)\b", "rejection"),
]

# Patterns pour les faits appris
FACT_PATTERNS = [
    r"(?i)\b(j'ai appris|j'ai découvert|nouveau[:])\s*(.+)",
    r"(?i)\b(info|information|note)[:]\s*(.+)",
]

# ─── Extraction ───────────────────────────────────────────────────

def extract_text_blocks(messages, role="assistant"):
    """Extrait le texte des messages d'un rôle donné (hors thinking)."""
    texts = []
    for msg in messages:
        if msg.get("role") != role:
            continue
        content = msg.get("content", [])
        if isinstance(content, str):
            texts.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    texts.append(block.get("text", ""))
    return texts


def extract_user_requests(messages):
    """Extrait les vraies requêtes utilisateur (hors turn_meta)."""
    requests = []
    for msg in messages:
        if msg.get("role") != "user":
            continue
        content = msg.get("content", [])
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            text = " ".join(
                b.get("text", "")
                for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            )
        # Filtrer les blocs turn_meta et tool_result
        text = re.sub(r"<turn_meta>.*?</turn_meta>", "", text, flags=re.DOTALL)
        text = text.strip()
        if text and len(text) > 5:
            requests.append(text)
    return requests


def extract_decisions(texts):
    """Extrait les décisions depuis un ensemble de textes assistant."""
    decisions = []
    for text in texts:
        for pattern in DECISION_PATTERNS:
            matches = re.findall(pattern, text, re.MULTILINE)
            for match in matches:
                # match peut être un tuple si plusieurs groupes
                if isinstance(match, tuple):
                    decision_text = match[-1].strip()
                else:
                    decision_text = match.strip()
                if len(decision_text) > 10 and len(decision_text) < 500:
                    decisions.append(decision_text)
    return list(set(decisions))  # déduplication basique


def extract_feedback(user_requests):
    """Extrait le feedback JCH depuis les requêtes utilisateur."""
    feedback_items = []
    for req in user_requests:
        for pattern, ftype in FEEDBACK_PATTERNS:
            if re.search(pattern, req):
                feedback_items.append({
                    "type": ftype,
                    "text": req[:300],
                })
                break  # un seul type par requête
    return feedback_items


def extract_facts(texts):
    """Extrait des faits appris depuis les messages assistant."""
    facts = []
    for text in texts:
        for pattern in FACT_PATTERNS:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    fact_text = match[-1].strip()
                else:
                    fact_text = match.strip()
                if 10 < len(fact_text) < 300:
                    facts.append(fact_text)
    return list(set(facts))


def extract_briefs(texts):
    """Détecte les briefs émis vers les spécialistes."""
    briefs = []
    for text in texts:
        # Cherche les patterns de brief dans les calls checklist ou agent_open
        if "brief" in text.lower() and ("créé" in text.lower() or "émis" in text.lower() or "envoyé" in text.lower()):
            # Extrait le contexte autour de "brief"
            briefs.append(text[:300])
    return briefs


def detect_project(texts):
    """Détecte le projet principal de la session."""
    project_keywords = {
        "WILDNEXUS": ["wildnexus", "esp32", "lora", "caméra-piège", "ppk2", "bom"],
        "VETALYX": ["vetalyx", "allergie", "vétérinaire", "diagnostic"],
        "ARTEON": ["arteon", "shopify", "wildlens", "whitewall"],
        "PHOTO_AI_JURY": ["argus", "photo.*jury", "critique.*photo"],
        "PHOTO_NATURE": ["photo.*nature", "faune", "oiseau"],
        "TRAVELS": ["travel", "vanlife", "voyage", "cigogne"],
        "IOT": ["iot", "home.?assistant", "zigbee", "domotique"],
        "AI_IT_TOOLS": ["ai.*tool", "it.*tool", "kanban", "hermes"],
    }
    all_text = " ".join(texts).lower()
    scores = {}
    for project, keywords in project_keywords.items():
        score = sum(1 for kw in keywords if re.search(kw, all_text))
        if score > 0:
            scores[project] = score
    if scores:
        return max(scores, key=scores.get)
    return None


# ─── Storage ──────────────────────────────────────────────────────

def store_knowledge(conn, title, body, ktype, source, project_key):
    """Insère une entrée dans la table knowledge. Retourne l'ID."""
    cursor = conn.execute(
        """INSERT INTO knowledge (title, body, type, source, status, tags, created_by, created_at)
           VALUES (?, ?, ?, ?, 'active', ?, 'Dobby', datetime('now'))
           RETURNING id""",
        (title[:200], body[:2000], ktype, source, project_key or "")
    )
    row = cursor.fetchone()
    return row[0] if row else None


def store_feedback(conn, session_id, ftype, context, action, response, project_key):
    """Insère un feedback dans dobby_feedback."""
    conn.execute(
        """INSERT INTO dobby_feedback
           (session_id, feedback_type, context, dobby_action, user_response, project_key)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (session_id, ftype, context, action, response, project_key)
    )


def store_pattern(conn, ptype, content, source):
    """Insère un pattern dans retro_patterns."""
    # Évite les doublons basiques
    existing = conn.execute(
        "SELECT id FROM retro_patterns WHERE pattern_type=? AND content=?",
        (ptype, content[:500])
    ).fetchone()
    if not existing:
        conn.execute(
            """INSERT INTO retro_patterns (date, pattern_type, content, source, created_at)
               VALUES (date('now'), ?, ?, ?, datetime('now'))""",
            (ptype, content[:1000], source)
        )


# ─── Post-Processing ─────────────────────────────────────────────

def generate_procedural_rules(conn, threshold=3):
    """Génère des règles procédurales à partir du feedback répété.

    Si ≥`threshold` feedbacks non incorporés partagent des mots-clés communs,
    génère automatiquement une entrée knowledge.type='procedure' et marque
    les feedbacks comme incorporés.
    """
    # Récupère tous les feedbacks non incorporés de type correction
    rows = conn.execute(
        """SELECT id, feedback_type, context, user_response, project_key
           FROM dobby_feedback
           WHERE incorporated = 0 AND feedback_type = 'correction'
           ORDER BY created_at DESC"""
    ).fetchall()

    if len(rows) < threshold:
        return 0

    # Regroupe par similarité de contenu (mots-clés communs)
    import collections
    from itertools import combinations

    # Extrait les mots significatifs de chaque feedback
    stopwords = {"le", "la", "les", "de", "du", "des", "un", "une", "et", "ou", "à", "en",
                 "pas", "ne", "que", "qui", "dans", "sur", "ce", "se", "pour", "avec",
                 "est", "plus", "fait", "faire", "non", "oui", "mais", "tout", "bien"}
    feedback_groups = collections.defaultdict(list)

    for row in rows:
        text = (row[3] or "")  # user_response
        words = set(re.findall(r'\b[a-zàâäéèêëîïôöùûüç]{4,}\b', text.lower()))
        words = words - stopwords
        for w in words:
            feedback_groups[w].append(row)

    count = 0
    seen_ids = set()

    for keyword, group in feedback_groups.items():
        if len(group) >= threshold:
            # Vérifie que ce ne sont pas tous les mêmes feedbacks qu'un autre mot-clé
            group_ids = tuple(sorted(r[0] for r in group))
            if group_ids in seen_ids:
                continue
            seen_ids.add(group_ids)

            # Génère la règle procédurale
            responses = [r[3][:200] for r in group if r[3]]
            rule_body = f"Pattern détecté ({len(group)} occurrences) — mot-clé: '{keyword}'.\n"
            rule_body += "Feedbacks JCH :\n"
            for i, resp in enumerate(responses[:5], 1):
                rule_body += f"  {i}. {resp}\n"
            rule_body += "\nRègle inférée automatiquement. À valider par Corbeau."

            project = group[0][4] or ""

            conn.execute(
                """INSERT INTO knowledge (title, body, type, source, status, tags, created_by, created_at)
                   VALUES (?, ?, 'procedure', 'auto:feedback_pattern', 'active', ?, 'Dobby', datetime('now'))""",
                (f"Règle procédurale — {keyword}", rule_body[:2000], project)
            )

            # Marque les feedbacks comme incorporés
            for r in group:
                conn.execute(
                    "UPDATE dobby_feedback SET incorporated = 1 WHERE id = ?",
                    (r[0],)
                )
            count += 1

    return count


def link_new_knowledge(conn, new_ids, max_links=20):
    """Crée des liens Zettelkasten entre nouveaux et anciens knowledge items.

    Pour chaque nouvel ID, cherche les entrées existantes les plus similaires
    (par chevauchement de mots) et crée des knowledge_links bidirectionnels.
    """
    if not new_ids:
        return 0

    count = 0

    # Récupère toutes les entrées knowledge actives sauf les nouvelles
    all_rows = conn.execute(
        """SELECT id, title, body, tags FROM knowledge
           WHERE status = 'active' AND id NOT IN ({})
           ORDER BY created_at DESC LIMIT 200"""
        .format(','.join('?' * len(new_ids))),
        new_ids
    ).fetchall()

    # Récupère les nouvelles entrées
    new_rows = conn.execute(
        """SELECT id, title, body, tags FROM knowledge WHERE id IN ({})"""
        .format(','.join('?' * len(new_ids))),
        new_ids
    ).fetchall()

    # Pour chaque nouvelle entrée, cherche les plus similaires
    for new_row in new_rows:
        new_id, new_title, new_body, new_tags = new_row
        new_text = f"{new_title or ''} {new_body or ''} {new_tags or ''}".lower()
        new_words = set(re.findall(r'\b[a-zàâäéèêëîïôöùûüç0-9_-]{4,}\b', new_text))

        if not new_words:
            continue

        # Score de similarité = intersection / union (Jaccard simplifié)
        scored = []
        for old_row in all_rows:
            old_id, old_title, old_body, old_tags = old_row
            old_text = f"{old_title or ''} {old_body or ''} {old_tags or ''}".lower()
            old_words = set(re.findall(r'\b[a-zàâäéèêëîïôöùûüç0-9_-]{4,}\b', old_text))

            if not old_words:
                continue

            intersection = new_words & old_words
            if len(intersection) >= 3:  # Au moins 3 mots en commun
                jaccard = len(intersection) / len(new_words | old_words)
                scored.append((old_id, jaccard, intersection))

        # Top 3 liens les plus pertinents
        scored.sort(key=lambda x: x[1], reverse=True)
        for old_id, score, common_words in scored[:3]:
            # Vérifie si le lien existe déjà
            existing = conn.execute(
                "SELECT id FROM knowledge_links WHERE from_id=? AND to_id=?",
                (new_id, old_id)
            ).fetchone()
            if not existing:
                relationship = f"related:{','.join(sorted(common_words)[:3])}"
                conn.execute(
                    "INSERT INTO knowledge_links (from_id, to_id, relationship) VALUES (?, ?, ?)",
                    (new_id, old_id, relationship)
                )
                count += 1

    return count


# ─── Main ─────────────────────────────────────────────────────────

def process_session(json_path, db_path=DB_PATH):
    """Traite un fichier JSON de session et extrait la mémoire."""
    if not os.path.exists(json_path):
        print(f"⚠️  Fichier introuvable : {json_path}")
        return 0

    with open(json_path) as f:
        data = json.load(f)

    messages = data.get("messages", [])
    metadata = data.get("metadata", {})
    session_id = metadata.get("id", os.path.basename(json_path))
    model = metadata.get("model", "unknown")
    date = metadata.get("created_at", "")[:10]

    if not messages:
        print(f"⚠️  Session vide : {json_path}")
        return 0

    # Extraction
    asst_texts = extract_text_blocks(messages, "assistant")
    user_requests = extract_user_requests(messages)
    all_texts = asst_texts + user_requests

    decisions = extract_decisions(asst_texts)
    feedback = extract_feedback(user_requests)
    facts = extract_facts(asst_texts)
    briefs = extract_briefs(asst_texts)
    project = detect_project(all_texts)

    # Connexion DB
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")

    count = 0
    new_knowledge_ids = []

    # Stocke les décisions (type: fact — une décision est un fait acté)
    for dec in decisions:
        kid = store_knowledge(conn, f"Décision — {date}", dec, "fact",
                        f"session:{session_id}", project)
        if kid: new_knowledge_ids.append(kid)
        count += 1

    # Stocke les faits
    for fact in facts:
        kid = store_knowledge(conn, f"Fait — {date}", fact, "fact",
                        f"session:{session_id}", project)
        if kid: new_knowledge_ids.append(kid)
        count += 1

    # Stocke les briefs (type: note)
    for brief in briefs:
        kid = store_knowledge(conn, f"Brief — {date}", brief, "note",
                        f"session:{session_id}", project)
        if kid: new_knowledge_ids.append(kid)
        count += 1

    # Stocke le feedback
    for fb in feedback:
        store_feedback(conn, session_id, fb["type"],
                       f"Session du {date}", "", fb["text"], project)
        count += 1

    # Stocke un pattern si blocage détecté
    if any("bloqué" in t.lower() or "échec" in t.lower() or "ne marche pas" in t.lower()
           for t in all_texts):
        store_pattern(conn, "blocker",
                      f"Blocage détecté session {date} — projet {project}",
                      f"session:{session_id}")

    # ─── Post-processing ───────────────────────────────────────
    proc_count = generate_procedural_rules(conn)
    link_count = link_new_knowledge(conn, new_knowledge_ids)
    count += proc_count + link_count

    conn.commit()
    conn.close()

    print(f"✅ {os.path.basename(json_path)} → {count} entrées")
    print(f"   Projet: {project or 'non détecté'} | Modèle: {model}")
    print(f"   Décisions: {len(decisions)} | Faits: {len(facts)} | Feedback: {len(feedback)} | Briefs: {len(briefs)}")
    if proc_count: print(f"   ⚡ Règles procédurales générées: {proc_count}")
    if link_count: print(f"   🔗 Liens Zettelkasten créés: {link_count}")
    return count


def process_latest(db_path=DB_PATH):
    """Traite la session la plus récente."""
    if not os.path.isdir(SESSION_DIR):
        print(f"⚠️  Dossier sessions introuvable : {SESSION_DIR}")
        return 0
    files = sorted(
        [f for f in os.listdir(SESSION_DIR) if f.endswith(".json")],
        key=lambda f: os.path.getmtime(os.path.join(SESSION_DIR, f)),
        reverse=True
    )
    if not files:
        print("⚠️  Aucune session trouvée.")
        return 0
    return process_session(os.path.join(SESSION_DIR, files[0]), db_path)


def process_batch(session_dir=SESSION_DIR, db_path=DB_PATH, limit=10):
    """Traite les N sessions les plus récentes."""
    if not os.path.isdir(session_dir):
        print(f"⚠️  Dossier introuvable : {session_dir}")
        return 0
    files = sorted(
        [f for f in os.listdir(session_dir) if f.endswith(".json")],
        key=lambda f: os.path.getmtime(os.path.join(session_dir, f)),
        reverse=True
    )[:limit]
    total = 0
    for f in files:
        total += process_session(os.path.join(session_dir, f), db_path)
    print(f"\n📊 Total : {total} entrées extraites de {len(files)} sessions")
    return total


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--latest":
        process_latest()
    elif arg == "--batch":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        process_batch(limit=limit)
    elif arg.endswith(".json"):
        process_session(arg)
    elif os.path.isdir(arg):
        process_batch(arg)
    else:
        print(f"⚠️  Argument non reconnu : {arg}")
        print(__doc__)
