#!/usr/bin/env python3
"""
pka_memory_capture.py — Capture mémoire unifiée PKA

Mode auto-extraction v0.2 (2026-07-05) — Reconcile auto + Memory Guard + Trust levels.
Primary: Gemma3 12B via Ollama M1. Fallback: DeepSeek V3 API.

Point d'entrée unique pour la capture de faits atomiques dans la mémoire PKA.
Implémente le format {fact, category, importance} avec :
- Déduplication avant écriture
- Routage automatique (team.db, MEMORY.md, user_model)
- Résolution de conflits + auto-reconcile
- Memory guard (pre-write injection scan)
- Niveaux de confiance (trust: internal/external/untrusted)

Usage:
    pka_memory_capture.py --fact "JC utilise le port 8123 pour HA M5" --category semantic --importance 4
    pka_memory_capture.py --auto-extract transcript.txt
    pka_memory_capture.py --auto-extract - < conversation.txt
    pka_memory_capture.py --json '{"fact": "...", "category": "procedural", "importance": 3}'
    cat facts.json | pka_memory_capture.py --stdin
    pka_memory_capture.py --fact "..." --category semantic --importance 3 --trust external

Catégories:
    semantic   — Faits stables (noms, URLs, architectures, technos)
    procedural — Règles et préférences (formatage, workflows, habitudes)
    episodic   — Événements datés (décisions, sessions, statuts)

Importance:
    1 — Basse (anecdotique, contexte)
    2 — Faible (nice-to-have)
    3 — Moyenne (utile, standard)
    4 — Haute (contrainte projet, préférence forte)
    5 — Critique (sécurité, architecture, ne doit jamais expirer)

Source Trust:
    internal  — Fait généré par Dobby ou un spécialiste PKA (défaut)
    external  — Fait provenant d'une source externe (web, transcript, document)
    untrusted — Contenu utilisateur non vérifié (upload, inbox brut)
    Les faits external/untrusted sont scannés par memory guard avant écriture
    et marqués dans la colonne trust de memory_capture.
"""

import argparse
import json
import sqlite3
import sys
import os
import re
from datetime import datetime
from pathlib import Path
import subprocess
import urllib.request
import urllib.error

DB_PATH = os.path.expanduser("~/PKA_JCH/TEAM/team.db")
MEMORY_PATH = os.path.expanduser("~/PKA_JCH/MEMORY.md")
USER_PATH = os.path.expanduser("~/PKA_JCH/USER.md")
PKABASE = os.path.expanduser("~/PKA_JCH")

# Auto-extraction config
OLLAMA_M1_URL = "http://100.73.212.110:11434"
OLLAMA_MODEL = "gemma3:12b-it-qat"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# Prompt guard script path
GUARD_SCRIPT = os.path.join(PKABASE, "scripts", "pka_prompt_guard.py")

EXTRACTION_PROMPT = """You are a fact extraction engine for a personal knowledge system (PKA).

From the conversation below, extract ALL noteworthy atomic facts. Follow this schema exactly:
- fact: One self-contained statement (single sentence, in the original language)
- category: Exactly one of: "semantic" (stable facts: URLs, names, architectures, ports, versions),
            "procedural" (rules, preferences, workflows, habits),
            "episodic" (dated events, decisions, status changes, deliveries)
- importance: 1 (trivia) to 5 (critical: security, architecture, irreversible decisions)

RULES:
1. Extract ONLY new or noteworthy information. Skip greetings, trivialities, repetitions.
2. If someone states a preference (e.g., "I prefer X over Y"), category=procedural, importance>=3.
3. If a decision changes system state (e.g., "let's deploy to X"), category=episodic, importance>=4.
4. If a factual statement about infrastructure (e.g., "the server runs on port 8123"), category=semantic, importance>=3.
5. Output a JSON array ONLY, no markdown, no explanation. Example:
[{"fact":"JC prefers simple systems over complex pipelines","category":"procedural","importance":4}]

CONVERSATION:
{transcript}"""


# ─── Memory guard: pre-write injection scan ─────────────────────────

# Lightweight inline patterns (mirrors pka_prompt_guard.py for zero-dependency scans)
MEMORY_INJECTION_PATTERNS = [
    # Memory poisoning
    (r"(?i)\b(remember|store|save|memorize)\s+(this|the\s+following)\s*(:\s*)?\s*(password|secret|key|token|instruction)", 9, "memory-poison"),
    (r"(?i)\b(from\s+now\s+on|going\s+forward|henceforth)\s*,?\s*(you\s+(must|will|should|are|always))\b", 7, "future-instruction"),
    # Role hijacking in memory
    (r"(?i)\b(ignore|forget|disregard|override)\s+(all|previous|prior|above)\s+(instructions?|prompts?|rules?|guidelines?|context)\b", 9, "role-hijack"),
    (r"(?i)\byou\s+are\s+now\s+(DAN|STAN|jailbroken|unfiltered|an?\s+unrestricted)\b", 9, "role-hijack-DAN"),
    (r"(?i)\bpretend\s+(you\s+are|to\s+be|that)\b", 7, "role-hijack-pretend"),
    # System prompt extraction
    (r"(?i)\b(repeat|print|output|display|show|tell\s+me|reveal|disclose)\s+(your|the)\s+(system\s+prompt|instructions?|rules?|guidelines?|initial\s+prompt)\b", 9, "system-prompt-extract"),
    # Template injection
    (r"\{\{.*?\}\}", 8, "template-injection"),
    (r"\{%\}.*?%\}", 8, "template-injection-jinja"),
    (r"\$\{.*?\}", 7, "template-injection-shell"),
    # Destructive commands in memory
    (r"(?i)\brm\s+-rf\b", 9, "destructive-cmd-rm"),
    (r"(?i)\bDROP\s+TABLE\b", 9, "destructive-cmd-sql"),
    (r"(?i)\b(execute|run)\s+(this|the\s+following)\s+(code|command|script|payload)\b", 8, "execute-payload"),
    # Future instruction persistence
    (r"(?i)\b(you\s+(must|will|should|are)\s+(always|now|from\s+now))\b", 7, "persistent-command"),
    # Silent overrides
    (r"(?i)\b(system\s*:\s*override|new\s+system\s+prompt|developer\s+mode\s+enabled)\b", 9, "system-override"),
]


def scan_fact_for_injection(fact: str) -> dict:
    """
    Lightweight injection scan on a single fact before writing to memory.
    Returns {'risk_score': int, 'verdict': str, 'findings': list}.
    """
    findings = []
    total_severity = 0

    for pattern, severity, category in MEMORY_INJECTION_PATTERNS:
        for match in re.finditer(pattern, fact):
            findings.append({
                "category": category,
                "severity": severity,
                "match": match.group(0)[:100]
            })
            total_severity += severity ** 1.5

    risk_score = min(100, int(total_severity * 1.5))

    if risk_score > 50:
        verdict = "quarantine"
    elif risk_score >= 20:
        verdict = "warn"
    else:
        verdict = "clean"

    return {"risk_score": risk_score, "verdict": verdict, "findings": findings}


def guard_memory_write(fact: str, trust: str = "internal", force: bool = False) -> bool:
    """
    Pre-write security gate for memory facts.
    Returns True if safe to write, False if blocked.

    Rules:
    - internal trust: always allowed (Dobby-generated)
    - external trust: scan, warn if score >= 20, block if >= 50
    - untrusted trust: scan, block if score >= 20
    """
    if trust == "internal":
        return True

    result = scan_fact_for_injection(fact)

    if trust == "untrusted" and result["risk_score"] >= 20:
        if force:
            print(f"  ⚠️  SECURITY: Fait untrusted bloqué par memory guard "
                  f"(score={result['risk_score']}) -- --force actif, écriture forcée")
            return True
        print(f"  🚫 SECURITY: Fait untrusted bloqué par memory guard "
              f"(score={result['risk_score']}/100)")
        for f in result["findings"]:
            print(f"     [{f['severity']}/10] {f['category']}: {f['match']}")
        return False

    if trust == "external" and result["risk_score"] >= 50:
        print(f"  🚫 SECURITY: Fait external bloqué par memory guard "
              f"(score={result['risk_score']}/100)")
        return False

    if result["risk_score"] >= 20:
        print(f"  ⚠️  memory guard: score={result['risk_score']}/100 — écriture autorisée avec warning")

    return True


def check_m1_available() -> bool:
    """Check if Ollama on M1 is reachable."""
    try:
        req = urllib.request.Request(f"{OLLAMA_M1_URL}/api/tags", method="GET")
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False


def extract_with_ollama(transcript: str) -> list[dict]:
    """Extract facts using Ollama on M1."""
    import json as json_module

    prompt = EXTRACTION_PROMPT.replace("{transcript}", transcript)
    payload = json_module.dumps({
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 2048}
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{OLLAMA_M1_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=120)
    body = json_module.loads(resp.read().decode("utf-8"))
    raw = body.get("message", {}).get("content", "")

    # Parse JSON from response (strip markdown fences if present)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        if raw.endswith("```"):
            raw = raw[:-3]
    return json_module.loads(raw)


def extract_with_deepseek(transcript: str) -> list[dict]:
    """Extract facts using DeepSeek V3 API as fallback."""
    import json as json_module

    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        # Try reading from config file
        key_file = os.path.expanduser("~/.config/pka-jch/api_keys")
        if os.path.exists(key_file):
            with open(key_file) as f:
                for line in f:
                    if line.startswith("DEEPSEEK_API_KEY="):
                        api_key = line.strip().split("=", 1)[1]
                        break

    prompt = EXTRACTION_PROMPT.replace("{transcript}", transcript)
    payload = json_module.dumps({
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 2048
    }).encode("utf-8")

    req = urllib.request.Request(
        DEEPSEEK_API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )
    resp = urllib.request.urlopen(req, timeout=60)
    body = json_module.loads(resp.read().decode("utf-8"))
    raw = body["choices"][0]["message"]["content"].strip()

    # Parse JSON from response
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        if raw.endswith("```"):
            raw = raw[:-3]
    return json_module.loads(raw)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def normalize_fact(fact: str) -> str:
    """Normalize fact for comparison (lowercase, strip)."""
    return " ".join(fact.lower().strip().split())


def find_similar(conn, fact: str, category: str) -> list[dict]:
    """
    Search for similar facts in memory_capture, knowledge, and user_model.
    Returns list of potential matches with similarity info.
    """
    normalized = normalize_fact(fact)
    results = []

    # 1. memory_capture table — exact + fuzzy match
    rows = conn.execute(
        "SELECT id, fact, category, importance, status FROM memory_capture WHERE status='active'"
    ).fetchall()
    for row in rows:
        row_norm = normalize_fact(row["fact"])
        if row_norm == normalized:
            results.append({"source": "memory_capture", "id": row["id"],
                            "fact": row["fact"], "category": row["category"],
                            "importance": row["importance"], "status": row["status"],
                            "match": "identical"})
        elif normalized in row_norm or row_norm in normalized:
            results.append({"source": "memory_capture", "id": row["id"],
                            "fact": row["fact"], "category": row["category"],
                            "importance": row["importance"], "status": row["status"],
                            "match": "substring"})

    # 2. knowledge table — fuzzy via shared words
    fact_words = set(normalized.split())
    if len(fact_words) >= 3:
        kb_rows = conn.execute(
            "SELECT id, title, body, type FROM knowledge"
        ).fetchall()
        for row in kb_rows:
            kb_text = normalize_fact((row["title"] or "") + " " + (row["body"] or ""))
            kb_words = set(kb_text.split())
            overlap = len(fact_words & kb_words) / max(len(fact_words), 1)
            if overlap >= 0.6:
                results.append({"source": "knowledge", "id": row["id"],
                                "fact": (row["title"] or "")[:120],
                                "category": row["type"],
                                "importance": None, "status": "active",
                                "match": "similar", "overlap": round(overlap, 2)})

    # 3. user_model table
    um_rows = conn.execute(
        "SELECT id, category, insight, confidence FROM user_model"
    ).fetchall()
    for row in um_rows:
        um_text = normalize_fact(row["insight"] or "")
        um_words = set(um_text.split())
        overlap = len(fact_words & um_words) / max(len(fact_words), 1)
        if overlap >= 0.5:
            results.append({"source": "user_model", "id": row["id"],
                            "fact": row["insight"][:120],
                            "category": row["category"],
                            "importance": None, "status": "active",
                            "match": "similar", "overlap": round(overlap, 2)})

    return results


def detect_conflict(conn, fact: str, category: str) -> list[dict]:
    """
    Check if the new fact contradicts an existing one.
    Returns list of potential conflicts.
    """
    conflicts = []
    normalized = normalize_fact(fact)

    # Extract structured key=value pairs (only for well-known keys to avoid false positives)
    known_keys = ['port', 'host', 'model', 'version', 'path', 'url', 'endpoint',
                   'runtime', 'tool', 'machine', 'ip', 'user', 'email']
    kv_pattern = re.compile(
        r'\b(' + '|'.join(known_keys) + r')\b\s*(?:est|utilise|use|is|=|:|->|→)\s*(\S+(?:\s+\S+){0,3})',
        re.IGNORECASE
    )

    rows = conn.execute(
        "SELECT id, fact, category, importance FROM memory_capture WHERE status='active' AND category=?", (category,)
    ).fetchall()

    new_kvs = set(kv_pattern.findall(normalized))
    for row in rows:
        existing_norm = normalize_fact(row["fact"])
        existing_kvs = set(kv_pattern.findall(existing_norm))
        # Same key but different value = conflict
        for nk, nv in new_kvs:
            for ek, ev in existing_kvs:
                if normalize_fact(nk) == normalize_fact(ek) and nv.strip() != ev.strip():
                    conflicts.append({
                        "existing_id": row["id"],
                        "existing_fact": row["fact"],
                        "key": nk,
                        "old_value": ev,
                        "new_value": nv
                    })
    return conflicts


def auto_reconcile(conn, fact: str, category: str, importance: int,
                   new_id: int, trust: str = "internal") -> int:
    """
    Auto-reconcile: if a conflicting fact exists with same key but different value,
    supersede the old one if the new fact has equal or higher importance.
    Returns number of conflicts resolved.
    """
    conflicts = detect_conflict(conn, fact, category)
    resolved = 0

    for c in conflicts:
        # Get importance of existing fact
        existing = conn.execute(
            "SELECT importance FROM memory_capture WHERE id=?", (c["existing_id"],)
        ).fetchone()

        if existing and importance >= existing["importance"]:
            supersede_fact(conn, c["existing_id"], new_id)
            print(f"  ↩️  Auto-reconcile: #{c['existing_id']} superseded "
                  f"(key={c['key']}, {c['old_value']} -> {c['new_value']})")
            resolved += 1
        else:
            print(f"  ⚠️  Conflit non résolu (importance insuffisante P{importance} < "
                  f"P{existing['importance']}): {c['key']}={c['old_value']} -> {c['new_value']}")

    return resolved


def ensure_trust_column(conn):
    """Add trust column to memory_capture if it doesn't exist."""
    try:
        conn.execute("SELECT trust FROM memory_capture LIMIT 1")
    except sqlite3.OperationalError:
        conn.execute(
            "ALTER TABLE memory_capture ADD COLUMN trust TEXT DEFAULT 'internal' "
            "CHECK(trust IN ('internal', 'external', 'untrusted'))"
        )
        conn.commit()
        print("  📐 Colonne 'trust' ajoutée à memory_capture")


def write_memory_capture(conn, fact: str, category: str, importance: int,
                         source: str = "manual", trust: str = "internal",
                         model: str = None,
                         project: str = None) -> int:
    """Insert into memory_capture table. Returns new id.

    Args:
        trust: 'internal' (Dobby), 'external' (web/transcript), 'untrusted' (user upload)
    """
    ensure_trust_column(conn)
    cursor = conn.execute(
        """INSERT INTO memory_capture (fact, category, importance, source, trust, model, project)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (fact, category, importance, source, trust, model, project)
    )
    conn.commit()
    return cursor.lastrowid


def supersede_fact(conn, old_id: int, new_id: int):
    """Mark an old fact as superseded by a new one."""
    conn.execute(
        "UPDATE memory_capture SET status='superseded', superseded_by=? WHERE id=?",
        (new_id, old_id)
    )
    conn.commit()


def append_memory_md(fact: str, category: str, importance: int, model: str = None):
    """Append episodic facts to MEMORY.md."""
    today = datetime.now().strftime("%Y-%m-%d")
    model_tag = f" — {model}" if model else ""
    tag = f"[capture/{category}/P{importance}]"
    entry = f"- [{today}]{tag} : {fact}\n"

    if not os.path.exists(MEMORY_PATH):
        print(f"⚠ MEMORY.md introuvable à {MEMORY_PATH}", file=sys.stderr)
        return

    with open(MEMORY_PATH, "r") as f:
        content = f.read()

    # Find the ## Session section for today or create one
    session_header = f"## Session {today}"
    if session_header in content:
        # Insert after the header
        lines = content.split("\n")
        new_lines = []
        inserted = False
        for line in lines:
            new_lines.append(line)
            if line.strip() == session_header and not inserted:
                new_lines.append(entry)
                inserted = True
        new_content = "\n".join(new_lines)
    else:
        # Add new section at the end before the last ---
        new_content = content.rstrip() + f"\n\n{entry}"

    with open(MEMORY_PATH, "w") as f:
        f.write(new_content)


def propose_user_md_diff(fact: str, category: str):
    """Suggest a USER.md update if the fact is about JC."""
    print(f"\n💡 Ce fait pourrait enrichir USER.md (catégorie: {category})")
    print(f"   Fait : {fact}")
    print(f"   → Pour appliquer : éditer USER.md manuellement ou relancer avec --apply-user")
    return False


def main():
    parser = argparse.ArgumentParser(description="Capture mémoire unifiée PKA")
    parser.add_argument("--fact", help="Le fait atomique à capturer")
    parser.add_argument("--category", choices=["semantic", "procedural", "episodic", "all"],
                        help="Catégorie du fait")
    parser.add_argument("--importance", type=int, choices=range(1, 6),
                        help="Importance (1-5)")
    parser.add_argument("--source", default="manual",
                        help="Source du fait (default: manual)")
    parser.add_argument("--trust", choices=["internal", "external", "untrusted"],
                        default="internal", help="Niveau de confiance de la source")
    parser.add_argument("--model", help="Modèle qui capture le fait")
    parser.add_argument("--project", help="Projet associé (optionnel)")
    parser.add_argument("--json", help="Entrée JSON au lieu d'arguments")
    parser.add_argument("--stdin", action="store_true",
                        help="Lire JSON depuis stdin")
    parser.add_argument("--auto-extract", metavar="TRANSCRIPT",
                        help="Extraire automatiquement les faits d'un transcript (fichier ou '-' pour stdin)")
    parser.add_argument("--no-fallback", action="store_true",
                        help="Désactiver le fallback DeepSeek V3 (utiliser Ollama M1 uniquement)")
    parser.add_argument("--max-facts", type=int, default=20,
                        help="Nombre maximum de faits à extraire (default: 20)")
    parser.add_argument("--auto-trust", choices=["internal", "external", "untrusted"],
                        default="external", help="Niveau de confiance pour --auto-extract (défaut: external)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans écrire")
    parser.add_argument("--apply-user", action="store_true",
                        help="Appliquer automatiquement à USER.md si pertinent")
    parser.add_argument("--force", action="store_true",
                        help="Forcer l'écriture même si conflit détecté")
    parser.add_argument("--search", help="Rechercher des faits existants (sans écrire)")
    parser.add_argument("--no-guard", action="store_true",
                        help="Désactiver le memory guard (pre-write injection scan)")
    parser.add_argument("--no-reconcile", action="store_true",
                        help="Désactiver l'auto-reconcile (override automatique)")
    args = parser.parse_args()

    conn = get_db()

    # Search mode
    if args.search:
        print(f"🔍 Recherche : {args.search}\n")
        results = find_similar(conn, args.search, "semantic")
        if not results:
            # Try all categories
            results = find_similar(conn, args.search, "procedural")
            if not results:
                results = find_similar(conn, args.search, "episodic")
        if results:
            for r in results:
                match_type = r.get("match", "")
                overlap = f" (overlap: {r.get('overlap', '')})" if "overlap" in r else ""
                print(f"  [{r['source']}] {r['fact']}{overlap} — {match_type}")
        else:
            print("  Aucun fait dans memory_capture/knowledge/user_model.")

        # FTS5 fallback — search session history
        fts_script = os.path.join(PKABASE, "scripts", "pka_retrieve.py")
        if os.path.exists(fts_script):
            import subprocess
            print(f"\n🔍 FTS5 (historique sessions) :")
            try:
                result = subprocess.run(
                    ["python3", fts_script, "--fts", args.search],
                    capture_output=True, text=True, timeout=15,
                    cwd=PKABASE
                )
                if result.stdout.strip():
                    lines = result.stdout.strip().split("\n")[:8]
                    for line in lines:
                        print(f"  {line}")
                else:
                    print("  Aucun résultat dans l'historique des sessions.")
            except Exception:
                print("  (recherche FTS5 non disponible)")
        conn.close()
        return

    # ── Auto-extract mode ──
    if args.auto_extract:
        # Load transcript
        if args.auto_extract == "-":
            transcript = sys.stdin.read()
            model_label = "stdin"
        else:
            tpath = os.path.expanduser(args.auto_extract)
            if not os.path.exists(tpath):
                print(f"❌ Fichier introuvable : {tpath}", file=sys.stderr)
                conn.close()
                sys.exit(1)
            with open(tpath) as f:
                transcript = f.read()
            model_label = os.path.basename(tpath)

        if not transcript.strip():
            print("❌ Transcript vide.", file=sys.stderr)
            conn.close()
            sys.exit(1)

        # Truncate if too long (Gemma3 context window ~8K, keep ~6K chars for prompt)
        max_chars = 6000
        if len(transcript) > max_chars:
            print(f"⚠ Transcript tronqué à ~{max_chars} caractères (limite modèle)")
            transcript = transcript[:max_chars]

        # Extract
        m1_available = check_m1_available()
        extracted = []
        model_used = None

        if m1_available:
            print(f"🧠 Ollama M1 -> {OLLAMA_MODEL}")
            model_used = OLLAMA_MODEL
            try:
                extracted = extract_with_ollama(transcript)
            except Exception as e:
                print(f"⚠ Ollama échoué : {e}")
                m1_available = False  # Force fallback

        if not m1_available and not args.no_fallback:
            print(f"☁️  Fallback -> DeepSeek V3 API")
            model_used = "deepseek-chat (fallback)"
            try:
                extracted = extract_with_deepseek(transcript)
            except Exception as e:
                print(f"❌ DeepSeek API échoué : {e}", file=sys.stderr)
                conn.close()
                sys.exit(2)
        elif not m1_available and args.no_fallback:
            print("❌ M1 indisponible et --no-fallback actif.", file=sys.stderr)
            conn.close()
            sys.exit(3)

        if not extracted:
            print("ℹ️  Aucun fait extrait.")
            conn.close()
            return

        # Limit to max_facts
        if len(extracted) > args.max_facts:
            extracted = extracted[:args.max_facts]
            print(f"⚠ Limité à {args.max_facts} faits (--max-facts)")

        print(f"\n📋 {len(extracted)} fait(s) extrait(s) par {model_used} :\n")
        for i, e in enumerate(extracted):
            cat = e.get("category", "semantic")
            imp = e.get("importance", 3)
            fact = e.get("fact", "")
            print(f"  {i+1}. [{cat}/P{imp}] {fact}")

        if args.dry_run:
            print("\n🧪 DRY RUN — aucun fait écrit.")
            conn.close()
            return

        # Write each fact
        print(f"\n✍️  Capture...")
        captured = 0
        reconciled = 0
        blocked = 0
        auto_trust = args.auto_trust
        for e in extracted:
            fact = e.get("fact", "").strip()
            cat = e.get("category", "semantic")
            imp = e.get("importance", 3)

            if not fact or cat not in ("semantic", "procedural", "episodic"):
                continue

            # Check dedup
            existing = find_similar(conn, fact, cat)
            identical = [ex for ex in existing if ex.get("match") == "identical"]
            if identical:
                print(f"  ⏭️  Doublon : {fact[:60]}...")
                continue

            # Pre-write memory guard
            if not args.no_guard and not guard_memory_write(fact, auto_trust, args.force):
                blocked += 1
                continue

            new_id = write_memory_capture(conn, fact, cat, imp,
                                          source="auto-extract", trust=auto_trust,
                                          model=model_used)
            captured += 1

            # Auto-reconcile: check for conflicts with existing facts
            if not args.no_reconcile:
                resolved = auto_reconcile(conn, fact, cat, imp, new_id, auto_trust)
                reconciled += resolved

            # Route
            if cat == "episodic":
                if not args.no_guard and not guard_memory_write(fact, auto_trust, args.force):
                    print(f"  ⚠️  Fait #{new_id} écrit en DB mais BLOQUÉ pour MEMORY.md (security guard)")
                    continue
                append_memory_md(fact, cat, imp, model_used)
            if imp >= 4 and cat in ("semantic", "procedural") and auto_trust != "untrusted":
                type_map = {"semantic": "fact", "procedural": "procedure", "episodic": "note"}
                ktype = type_map.get(cat, "note")
                conn.execute(
                    "INSERT INTO knowledge (title, body, type) VALUES (?, ?, ?)",
                    (fact[:200], fact, ktype)
                )
                conn.commit()

        conn.close()
        status_parts = [f"{captured}/{len(extracted)} capturés"]
        if reconciled:
            status_parts.append(f"{reconciled} reconciliés")
        if blocked:
            status_parts.append(f"{blocked} bloqués (security guard)")
        print(f"\n✅ {', '.join(status_parts)}.")
        return

    # Parse input
    if args.stdin:
        data = json.loads(sys.stdin.read())
    elif args.json:
        data = json.loads(args.json)
    elif args.fact and args.category and args.importance:
        data = {"fact": args.fact, "category": args.category, "importance": args.importance}
    else:
        parser.print_help()
        conn.close()
        return

    fact = data.get("fact", "").strip()
    category = data.get("category", "semantic")
    importance = data.get("importance", 3)
    source = data.get("source", args.source)
    model = data.get("model", args.model)
    project = data.get("project", args.project)
    trust = data.get("trust", args.trust)

    if not fact:
        print("❌ Fait vide — rien à capturer.", file=sys.stderr)
        conn.close()
        sys.exit(1)

    # Step 1 — Dedup check
    existing = find_similar(conn, fact, category)
    identical = [e for e in existing if e.get("match") == "identical"]
    if identical:
        print(f"⏭️  Doublon détecté (memory_capture #{identical[0]['id']}) — ignoré.")
        conn.close()
        return

    # Pre-write memory guard
    if not args.no_guard and not guard_memory_write(fact, trust, args.force):
        print("❌ Capture bloquée par memory guard. Utilisez --force ou --no-guard.")
        conn.close()
        sys.exit(3)

    # Step 2 — Conflict detection
    conflicts = detect_conflict(conn, fact, category)
    if conflicts and not args.force:
        print("⚠️  Conflit(s) potentiel(s) détecté(s) :")
        for c in conflicts:
            print(f"   - Clé << {c['key']} >> : existant={c['old_value']} -> nouveau={c['new_value']}")
            print(f"     Fait existant (#{c['existing_id']}) : {c['existing_fact']}")
        print("\n❌ Capture annulée. Utilisez --force pour écraser ou résolvez manuellement.")
        conn.close()
        sys.exit(2)

    # Step 3 — Write
    if args.dry_run:
        print(f"🧪 DRY RUN — serait écrit :")
        print(f"   Fait       : {fact}")
        print(f"   Catégorie  : {category}")
        print(f"   Importance : {importance}")
        print(f"   Projet     : {project or '-'}")
        print(f"   Trust      : {trust}")
        if conflicts:
            print(f"   Conflits   : {len(conflicts)} (--force actif)")
        conn.close()
        return

    new_id = write_memory_capture(conn, fact, category, importance, source, trust, model, project)

    # Supersede conflicting facts if forced
    if conflicts and args.force:
        for c in conflicts:
            supersede_fact(conn, c["existing_id"], new_id)
            print(f"   ↩️  Fait #{c['existing_id']} marqué comme supplanté.")

    # Auto-reconcile if not forced but auto-reconcile is enabled
    reconciled = 0
    if not args.no_reconcile:
        reconciled = auto_reconcile(conn, fact, category, importance, new_id, trust)

    # Step 4 — Route to additional destinations
    routed = []
    if category == "episodic":
        append_memory_md(fact, category, importance, model)
        routed.append("MEMORY.md")
    if importance >= 4 and category in ("semantic", "procedural") and trust != "untrusted":
        # Map PKA category -> knowledge.type (constrained to: note, insight, concept, quote, fact, procedure, framework)
        type_map = {"semantic": "fact", "procedural": "procedure", "episodic": "note"}
        ktype = type_map.get(category, "note")
        conn.execute(
            "INSERT INTO knowledge (title, body, type) VALUES (?, ?, ?)",
            (fact[:200], fact, ktype)
        )
        conn.commit()
        routed.append("knowledge")
    if category == "semantic" and importance >= 3:
        # Propose USER.md update
        if args.apply_user:
            routed.append("USER.md (auto)")
        else:
            propose_user_md_diff(fact, category)

    conn.close()

    # Output
    print(f"✅ Fait capturé (#{new_id})")
    print(f"   Catégorie  : {category}")
    print(f"   Importance : {'🔴' if importance >= 4 else '🟡' if importance >= 2 else '⚪'} P{importance}")
    trust_icon = {'internal': '🔒 internal', 'external': '🌐 external', 'untrusted': '⚠️ untrusted'}
    print(f"   Trust      : {trust_icon.get(trust, trust)}")
    if reconciled:
        print(f"   Reconcilié  : {reconciled} conflit(s) résolu(s)")
    if routed:
        print(f"   Routé vers : {', '.join(routed)}")
    if conflicts:
        print(f"   Conflits résolus : {len(conflicts)}")

    # Return JSON for piping
    result = {"id": new_id, "status": "captured", "category": category,
              "importance": importance, "routed_to": routed, "trust": trust}
    print(json.dumps(result))


if __name__ == "__main__":
    main()
