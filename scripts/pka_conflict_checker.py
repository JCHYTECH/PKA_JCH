#!/usr/bin/env python3
"""
PKA Conflict Checker — détection de contradictions entre opinions de spécialistes.

Inspiré de OctoChains ConflictChecker : agents isolés → analyse parallèle →
détection structurée des conflits avant synthèse.

Deux modes :
  --heuristic  : regex + patterns (local, gratuit)
  --llm        : via LLM (précis, nécessite API)

Usage:
  python3 scripts/pka_conflict_checker.py report1.md report2.md report3.md
  python3 scripts/pka_conflict_checker.py --heuristic *.md
  python3 scripts/pka_conflict_checker.py --llm --json *.md
  python3 scripts/pka_conflict_checker.py --from-db --topic "WILDNEXUS deep sleep"

Sortie structurée JSON :
  { "has_conflicts": true,
    "summary": "...",
    "conflicts": [{"description":"...", "agents":["A","B"], "severity":"critical"}] }
"""

import json
import os
import re
import sqlite3
import sys
from collections import defaultdict

# ─── Configuration ───────────────────────────────────────────────

PKA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PKA_ROOT, "TEAM", "team.db")


# ─── Heuristic Conflict Detection ────────────────────────────────

# Patterns de contradiction factuelle
FACT_PATTERNS = [
    # Contradictions numériques explicites
    (r"(\d+[\.,]?\d*)\s*(€|euros?|USD|\$)", "numeric"),
    # Affirmation vs négation sur le même sujet
    (r"\b(fonctionne|marche|opérationnel|OK|validé)\b", "positive_claim"),
    (r"\b(ne\s+marche\s+pas|ne\s+fonctionne\s+pas|défaillant|inopérant|échec|bloqué)\b", "negative_claim"),
    # Délais contradictoires
    (r"\b(\d+)\s*(jours?|semaines?|mois)\b", "timeline"),
    # Recommandations opposées
    (r"\b(recommande|préconise|suggère|conseille)\b", "recommendation"),
    (r"\b(déconseille|éviter|contre-indiqué|risque)\b", "warning"),
]


def extract_claims(text, source_name):
    """Extrait les affirmations structurées d'un texte."""
    claims = []
    # Numérique
    for match in re.finditer(r"(\d+[\.,]?\d*)\s*(€|euros?|USD|\$|mA|µA|V|MHz|jours?|semaines?|mois)", text):
        claims.append({
            "type": "numeric",
            "value": match.group(0),
            "context": text[max(0, match.start()-80):match.end()+80],
            "source": source_name
        })

    # Affirmations de vérité
    for match in re.finditer(r"\b(est|sont|sera|coûte|prend|nécessite)\s+(\w+(?:\s+\w+){0,5})", text):
        claims.append({
            "type": "assertion",
            "value": match.group(0),
            "context": text[max(0, match.start()-60):match.end()+60],
            "source": source_name
        })

    # Recommandations
    for match in re.finditer(r"\b(recommande|préconise|suggère|conseille|il faut|on doit)\s+(.{10,120}?)[.!?]", text):
        claims.append({
            "type": "recommendation",
            "value": match.group(0),
            "context": match.group(0),
            "source": source_name
        })

    return claims


def detect_numeric_conflicts(claims_by_source):
    """Détecte les conflits entre affirmations numériques."""
    conflicts = []
    sources = list(claims_by_source.keys())
    for i in range(len(sources)):
        for j in range(i+1, len(sources)):
            src_a, src_b = sources[i], sources[j]
            nums_a = [c for c in claims_by_source[src_a] if c["type"] == "numeric"]
            nums_b = [c for c in claims_by_source[src_b] if c["type"] == "numeric"]

            for ca in nums_a:
                for cb in nums_b:
                    # Cherche des valeurs numériques proches mais contradictoires
                    val_a_match = re.search(r"(\d+[\.,]?\d*)", ca["value"])
                    val_b_match = re.search(r"(\d+[\.,]?\d*)", cb["value"])
                    if val_a_match and val_b_match:
                        try:
                            va = float(val_a_match.group(1).replace(",", "."))
                            vb = float(val_b_match.group(1).replace(",", "."))
                            # Même ordre de grandeur mais valeurs très différentes (>2x)
                            if va > 0 and vb > 0:
                                ratio = max(va, vb) / min(va, vb)
                                if ratio > 2.0:
                                    # Vérifie si les unités sont similaires
                                    unit_a = ca["value"].replace(val_a_match.group(1), "")
                                    unit_b = cb["value"].replace(val_b_match.group(1), "")
                                    if unit_a == unit_b:
                                        conflicts.append({
                                            "description": f"Écart numérique {ratio:.1f}x : {src_a} = {ca['value']} vs {src_b} = {cb['value']}",
                                            "agents": [src_a, src_b],
                                            "severity": "high" if ratio > 5 else "moderate"
                                        })
                        except ValueError:
                            pass
    return conflicts


def detect_assertion_conflicts(claims_by_source):
    """Détecte les affirmations opposées sur le même sujet."""
    conflicts = []
    sources = list(claims_by_source.keys())
    # Cherche des paires de recommandations opposées
    for i in range(len(sources)):
        for j in range(i+1, len(sources)):
            src_a, src_b = sources[i], sources[j]
            recs_a = [c for c in claims_by_source[src_a] if c["type"] == "recommendation"]
            recs_b = [c for c in claims_by_source[src_b] if c["type"] == "recommendation"]

            for ra in recs_a:
                for rb in recs_b:
                    # Mots-clés opposés
                    oppose_keywords = [
                        ("acheter", "éviter"), ("utiliser", "ne pas utiliser"),
                        ("implémenter", "repousser"), ("urgent", "pas prioritaire"),
                        ("faire", "ne pas faire"), ("lancer", "attendre"),
                    ]
                    for kw_a, kw_b in oppose_keywords:
                        if kw_a in ra["value"].lower() and kw_b in rb["value"].lower():
                            conflicts.append({
                                "description": f"Recommandations opposées : {src_a} dit « {ra['value'][:100]} », {src_b} dit « {rb['value'][:100]} »",
                                "agents": [src_a, src_b],
                                "severity": "critical"
                            })
                            break
    return conflicts


def heuristic_check(texts, source_names=None):
    """Détection heuristique de conflits (sans LLM).

    Args:
        texts: liste de textes (strings)
        source_names: liste de noms de sources (sinon "Source 1", "Source 2"...)

    Returns:
        dict avec has_conflicts, summary, conflicts[]
    """
    if source_names is None:
        source_names = [f"Source {i+1}" for i in range(len(texts))]

    claims_by_source = {}
    for text, name in zip(texts, source_names):
        claims_by_source[name] = extract_claims(text, name)

    all_conflicts = []
    all_conflicts.extend(detect_numeric_conflicts(claims_by_source))
    all_conflicts.extend(detect_assertion_conflicts(claims_by_source))

    # Déduplication
    seen = set()
    unique_conflicts = []
    for c in all_conflicts:
        key = c["description"][:80]
        if key not in seen:
            seen.add(key)
            unique_conflicts.append(c)

    has_conflicts = len(unique_conflicts) > 0
    summary = (
        f"{len(unique_conflicts)} conflit(s) détecté(s) entre "
        f"{len(source_names)} sources — {len([c for c in unique_conflicts if c['severity']=='critical'])} critique(s)"
        if has_conflicts
        else f"Aucun conflit détecté entre {len(source_names)} sources."
    )

    return {
        "has_conflicts": has_conflicts,
        "summary": summary,
        "conflicts": unique_conflicts,
        "mode": "heuristic",
        "sources": source_names
    }


# ─── LLM-based Conflict Detection ────────────────────────────────

def llm_check(texts, source_names=None, model="deepseek-v4-pro"):
    """Détection de conflits via LLM.

    Utilise le prompt matrix d'OctoChains : tous les outputs projetés
    sur une matrice d'évaluation structurée en un seul passage.
    """
    if source_names is None:
        source_names = [f"Source {i+1}" for i in range(len(texts))]

    # Construit le prompt matrix
    sources_block = ""
    for name, text in zip(source_names, texts):
        sources_block += f"\n### {name}\n{text[:1500]}\n"

    prompt = f"""Tu es un auditeur neutre. Analyse les rapports de {len(source_names)} spécialistes ci-dessous.

RAPPORTS INDÉPENDANTS :
{sources_block}

TÂCHE : Détecte TOUTES les contradictions entre ces rapports. Ne lisse rien. Cherche :
1. Contradictions factuelles (chiffres, dates, faits qui s'opposent)
2. Recommandations opposées (l'un dit d'acheter, l'autre d'éviter)
3. Désaccords sur les priorités ou timelines
4. Incohérences logiques (A suppose X, B suppose non-X)

Réponds UNIQUEMENT en JSON :
{{
  "has_conflicts": true/false,
  "summary": "résumé exécutif en 1-2 phrases",
  "conflicts": [
    {{
      "description": "description précise du conflit",
      "agents": ["Nom Source A", "Nom Source B"],
      "severity": "critical/moderate/minor"
    }}
  ]
}}"""

    # Utilise le client OpenAI local ou DeepSeek
    try:
        import openai
        client = openai.OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
            base_url="https://api.deepseek.com/v1"
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2000
        )
        result_text = response.choices[0].message.content
        # Nettoie le markdown éventuel
        result_text = re.sub(r"^```json\s*", "", result_text)
        result_text = re.sub(r"\s*```$", "", result_text)
        result = json.loads(result_text)
        result["mode"] = "llm"
        result["sources"] = source_names
        return result
    except Exception as e:
        # Fallback to heuristic
        print(f"⚠️  LLM indisponible ({e}) — fallback heuristique", file=sys.stderr)
        result = heuristic_check(texts, source_names)
        result["mode"] = "heuristic (llm fallback)"
        return result


# ─── DB Integration ───────────────────────────────────────────────

def check_from_db(topic, db_path=DB_PATH, limit=5):
    """Récupère les entrées knowledge récentes sur un topic et les compare."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """SELECT title, body, type, tags, created_by
           FROM knowledge
           WHERE status = 'active'
             AND (title LIKE ? OR body LIKE ? OR tags LIKE ?)
           ORDER BY created_at DESC
           LIMIT ?""",
        (f"%{topic}%", f"%{topic}%", f"%{topic}%", limit)
    ).fetchall()
    conn.close()

    if len(rows) < 2:
        print(f"⚠️  Moins de 2 entrées trouvées pour '{topic}' — impossible de comparer.")
        return None

    texts = []
    names = []
    for r in rows:
        text = f"## {r['title']}\n{r['body'] or ''}\nType: {r['type']} | Tags: {r['tags']}"
        texts.append(text)
        names.append(f"{r['created_by'] or 'inconnu'} ({r['type']})")

    print(f"📊 Comparaison de {len(texts)} entrées knowledge sur '{topic}'...")
    return heuristic_check(texts, names)


# ─── Storage ─────────────────────────────────────────────────────

def store_conflict_report(conn, report, topic="", source="pka_conflict_checker"):
    """Stocke le rapport de conflit dans retro_patterns."""
    if report.get("has_conflicts"):
        for c in report.get("conflicts", []):
            conn.execute(
                """INSERT INTO retro_patterns
                   (date, pattern_type, content, source, created_at)
                   VALUES (date('now'), ?, ?, ?, datetime('now'))""",
                ("conflict_detected",
                 f"[{c['severity']}] {c['description']} — entre: {', '.join(c.get('agents', []))}",
                 source)
            )
        conn.commit()


# ─── Main ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PKA Conflict Checker")
    parser.add_argument("files", nargs="*", help="Fichiers à comparer")
    parser.add_argument("--heuristic", "-H", action="store_true",
                        default=True, help="Mode heuristique (défaut)")
    parser.add_argument("--llm", "-L", action="store_true",
                        help="Mode LLM (plus précis)")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Sortie JSON uniquement")
    parser.add_argument("--from-db", "-d", type=str, metavar="TOPIC",
                        help="Comparer les entrées knowledge sur un topic")
    parser.add_argument("--severity", "-s", type=str, default="all",
                        choices=["critical", "high", "moderate", "minor", "all"],
                        help="Filtrer par sévérité")

    args = parser.parse_args()

    result = None

    if args.from_db:
        result = check_from_db(args.from_db)
    elif args.files:
        texts = []
        names = []
        for fpath in args.files:
            if os.path.exists(fpath):
                with open(fpath) as f:
                    texts.append(f.read())
                names.append(os.path.splitext(os.path.basename(fpath))[0])
            else:
                # Traite comme du texte inline
                texts.append(fpath)
                names.append(f"Input {len(names)+1}")

        if args.llm:
            result = llm_check(texts, names)
        else:
            result = heuristic_check(texts, names)
    else:
        # Mode interactif : lit depuis stdin
        print("Colle les textes à comparer (Ctrl+D pour terminer, '---' entre les sources) :")
        raw = sys.stdin.read()
        parts = [p.strip() for p in raw.split("\n---\n") if p.strip()]
        if len(parts) < 2:
            print("⚠️  Au moins 2 sources requises.")
            sys.exit(1)
        result = heuristic_check(parts)
        result["sources"] = [f"Source {i+1}" for i in range(len(parts))]

    if result is None:
        sys.exit(1)

    # Filtrage par sévérité
    if args.severity != "all" and result.get("conflicts"):
        result["conflicts"] = [c for c in result["conflicts"]
                                if c.get("severity") == args.severity]
        result["has_conflicts"] = len(result["conflicts"]) > 0

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        severity_icons = {"critical": "🔴", "high": "🟠", "moderate": "🟡", "minor": "🟢"}
        print(f"\n{'='*60}")
        print(f"🔍 PKA Conflict Checker — {result.get('mode', '?')}")
        print(f"{'='*60}")
        print(f"\n{result['summary']}\n")
        if result.get("conflicts"):
            for i, c in enumerate(result["conflicts"], 1):
                icon = severity_icons.get(c.get("severity", ""), "📝")
                print(f"{i}. {icon} [{c.get('severity', '?')}] {c['description'][:200]}")
                if c.get("agents"):
                    print(f"   👥 {', '.join(c['agents'])}")
                print()
        if not result.get("has_conflicts"):
            print("✅ Consensus — aucune contradiction détectée.")
        print(f"{'='*60}\n")

    # Store in DB if conflicts found
    if result and result.get("has_conflicts") and result.get("conflicts"):
        try:
            conn = sqlite3.connect(DB_PATH)
            store_conflict_report(conn, result, args.from_db or "")
            conn.close()
        except Exception:
            pass  # storage is optional
