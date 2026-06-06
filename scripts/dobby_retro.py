#!/usr/bin/env python3
"""
dobby_retro.py  🦉  — Rétrospective multi-source auto-apprenante

Lit les transcripts de TOUS les outils utilisés par JCH (DeepSeek TUI,
Claude Code, composer_history), en extrait des patterns localement,
puis produit une rétrospective cross-session enrichie.

Usage :
    python3 scripts/dobby_retro.py                        # aujourd'hui
    python3 scripts/dobby_retro.py --days 7               # 7 derniers jours
    python3 scripts/dobby_retro.py --all                  # toutes les sessions
    python3 scripts/dobby_retro.py --dry-run              # extraction locale seulement
    python3 scripts/dobby_retro.py --provider openrouter   # LLM via OpenRouter

Dépendances : sqlite3, json, re, collections (stdlib).
              requests pour OpenRouter (pip install requests si utilisé).
"""

import json
import os
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

# ── CONFIG ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
PKA_DIR = BASE_DIR.parent
DB_PATH = PKA_DIR / "TEAM" / "team.db"
RETRO_DIR = PKA_DIR / "wiki" / "Daily"
SECRETS_DIR = Path.home() / ".config" / "pka-jch"

# Sources de transcripts
DEEPSEEK_SESSIONS_DIR = Path.home() / ".deepseek" / "sessions"
DEEPSEEK_COMPOSER_HISTORY = Path.home() / ".deepseek" / "composer_history.txt"
CLAUDE_SESSIONS_DIR = Path.home() / ".claude" / "projects" / "-Users-jchavauxm5"
CODEX_HISTORY = Path.home() / ".codex" / "history.jsonl"

# Limites
MAX_SESSION_CHARS = 15000       # chars max par session avant troncature
MAX_CONTEXT_CHARS = 50000       # chars max total envoyé au LLM
MAX_RETRO_DAYS = 30             # fenêtre max de rétrospective (jours)

# Patterns de détection locale
DECISION_PATTERNS = [
    r"(on\s+va|je\s+(vais|décide|choisis?|opte)|décision\s*[::]|choix\s*[:])",
    r"(validé|approuvé|confirmé|retenu|adopté)",
    r"(pas\s+la\s+peine|abandonné|annulé|rejeté)",
]
FAILURE_PATTERNS = [
    r"(erreur\s*:|bug|crash|plante|marche\s+pas|ne\s+fonctionne\s+pas)",
    r"(blocked|stuck|bloqué|coincé|échec|fail)",
    r"(timeout|404|500|exception|traceback)",
]
QUESTION_PATTERNS = [
    r"comment\s+(faire|configurer|installer|utiliser|lancer)",
    r"c['']est\s+quoi|qu['']est-ce\s+que|c['']est\s+comment",
    r"(pourquoi|quelle\s+est\s+la\s+différence|à\s+quoi\s+sert)",
]
ENTITY_PATTERNS = {
    "projet": [
        r"(?i)\b(WILDNEXUS|ARTEON|VETALYX|WILDLENS|WILDMESH|FAUNE\s*AUTOUR|DIM3|HOME\s*ASSISTANT)\b",
    ],
    "outil": [
        r"(?i)\b(Ollama|DeepSeek|Claude|GPT|OpenRouter|NVIDIA|Tailscale|Homebridge|Docker|NGINX)\b",
    ],
    "machine": [
        r"(?i)\b(M[15]|RPi|Raspberry\s*Pi|Mac\s*(Mini|Book|Studio|Pro|Air))\b",
    ],
    "membre": [
        r"(?i)\b(Dobby|Bouvier|Furet|Castor|Corbeau|Delphi|Héron|Lynx|Jade|Renard|Iris|Forge|Ariane|Bruno|Sybil|Clio|Sigma|Vega|Trace|Miel|Vasco|Nova|Argus|Pie|Chouette|Milan|Atlas|Hermine|Cigogne)\b",
    ],
}

# ── PROVIDER ABSTRACTION ─────────────────────────────────────────────

class RetroProvider:
    """CLASSE ABSTRAITE — fournisseur LLM pour l'analyse rétrospective."""

    SYSTEM_PROMPT = """Tu es Dobby 🦉, orchestrateur du système PKA de Jean-Claude Havaux.
Tu analyses les transcripts de sessions de travail multi-outils (DeepSeek TUI, Claude Code, Codex CLI).
Ton objectif : identifier les inefficacités, les décisions non documentées, les échecs ouverts,
les questions récurrentes, et les patterns de travail.

Tu reçois :
1. Un résumé des patterns extraits localement par Dobby
2. Les extraits de transcript les plus pertinents

Produis une rétrospective structurée en markdown avec ces sections (obligatoires) :

## Décisions prises
## Échecs ouverts / bloqueurs
## Questions récurrentes (signe de lacune documentaire)
## Nouveaux patterns détectés
## Efficacités / inefficacités
## Ce qu'il faut garder en mémoire pour les prochaines sessions
## Recommandations

Sois direct et précis. Cite des exemples concrets. Ne te ménage pas.
Output : markdown pur, prêt à écrire dans un fichier."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def analyze(self, transcript: str, today_str: str) -> str:
        raise NotImplementedError


class AnthropicProvider(RetroProvider):
    """Fournisseur Anthropic Claude."""

    def analyze(self, transcript: str, today_str: str) -> str:
        try:
            import anthropic
        except ImportError:
            return self._fallback_retro(today_str, "anthropic indisponible (pip install anthropic)")

        client = anthropic.Anthropic(api_key=self.api_key)
        prompt = (
            f"Voici le transcript des sessions du {today_str} entre JCH et ses assistants :\n\n"
            f"{transcript}\n\n"
            f"Produis la rétrospective de ces sessions."
        )
        try:
            response = client.messages.create(
                model=self.model,
                max_tokens=3000,
                system=self.SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as exc:
            return self._fallback_retro(today_str, f"Erreur Anthropic: {exc}")

    def _fallback_retro(self, today_str: str, reason: str) -> str:
        return (
            f"## Rétrospective locale — {today_str}\n\n"
            f"**Note :** L'analyse LLM n'a pas pu être produite ({reason}).\n"
            f"Les patterns locaux ont été extraits et archivés dans team.db.\n"
            f"Relance avec `--provider openrouter` ou vérifie la clé API."
        )


class OpenRouterProvider(RetroProvider):
    """Fournisseur OpenRouter — compatible DeepSeek, Qwen, Claude, etc."""

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def analyze(self, transcript: str, today_str: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": (
                    f"Voici le transcript des sessions du {today_str} entre JCH et ses assistants :\n\n"
                    f"{transcript}\n\n"
                    f"Produis la rétrospective de ces sessions."
                )},
            ],
            "max_tokens": 3000,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            import requests
            resp = requests.post(self.API_URL, json=payload, headers=headers, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except ImportError:
            return self._fallback_retro(today_str, "requests non installé (pip install requests)")
        except Exception as exc:
            return self._fallback_retro(today_str, f"Erreur OpenRouter: {exc}")

    def _fallback_retro(self, today_str: str, reason: str) -> str:
        return (
            f"## Rétrospective locale — {today_str}\n\n"
            f"**Note :** L'analyse LLM n'a pas pu être produite ({reason}).\n"
            f"Les patterns locaux ont été extraits et archivés dans team.db."
        )

# ── LECTURE MULTI-SOURCE ─────────────────────────────────────────────

def read_deepseek_sessions(cutoff: datetime | None = None) -> list[dict]:
    """Lit les sessions DeepSeek TUI depuis ~/.deepseek/sessions/"""
    exchanges: list[dict] = []
    if not DEEPSEEK_SESSIONS_DIR.is_dir():
        return exchanges

    for fpath in sorted(DEEPSEEK_SESSIONS_DIR.glob("*.json"),
                        key=lambda f: f.stat().st_mtime, reverse=True):
        mtime = datetime.fromtimestamp(fpath.stat().st_mtime)
        if cutoff and mtime < cutoff:
            break  # plus ancien

        try:
            with open(fpath) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        meta = data.get("metadata", {})
        model = meta.get("model", "unknown")
        session_id = meta.get("id", fpath.stem)
        messages = data.get("messages", [])

        for msg in messages:
            role = msg.get("role", "")
            if role not in ("user", "assistant"):
                continue
            content = msg.get("content", "")
            text = ""
            if isinstance(content, str):
                text = content.strip()
            elif isinstance(content, list):
                parts = [c.get("text", "") for c in content
                         if isinstance(c, dict) and c.get("type") == "text"]
                text = " ".join(parts).strip()

            if text:
                exchanges.append({
                    "source": "deepseek",
                    "session_id": session_id,
                    "model": model,
                    "role": "user" if role == "user" else "assistant",
                    "text": text[:MAX_SESSION_CHARS],
                })
    return exchanges


def read_claude_sessions(cutoff: datetime | None = None) -> list[dict]:
    """Lit les sessions Claude Code depuis ~/.claude/projects/"""
    exchanges: list[dict] = []
    if not CLAUDE_SESSIONS_DIR.is_dir():
        return exchanges

    for fpath in sorted(CLAUDE_SESSIONS_DIR.glob("*.jsonl"),
                        key=lambda f: f.stat().st_mtime, reverse=True):
        mtime = datetime.fromtimestamp(fpath.stat().st_mtime)
        if cutoff and mtime < cutoff:
            break

        with open(fpath) as f:
            for line in f:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue

                t = d.get("type", "")
                if t not in ("user", "assistant"):
                    continue

                msg = d.get("message", {})
                content = msg.get("content", "")
                text = ""
                if isinstance(content, list):
                    parts = [c.get("text", "") for c in content
                             if isinstance(c, dict) and c.get("type") == "text"]
                    text = " ".join(parts).strip()
                else:
                    text = str(content).strip()

                if text:
                    exchanges.append({
                        "source": "claude",
                        "session_id": fpath.stem,
                        "model": msg.get("model", "claude"),
                        "role": t,
                        "text": text[:MAX_SESSION_CHARS],
                    })
    return exchanges


def read_composer_history(cutoff: datetime | None = None) -> list[dict]:
    """Lit le composer_history DeepSeek (requêtes utilisateur uniquement)."""
    exchanges: list[dict] = []
    if not DEEPSEEK_COMPOSER_HISTORY.is_file():
        return exchanges

    mtime = datetime.fromtimestamp(DEEPSEEK_COMPOSER_HISTORY.stat().st_mtime)
    if cutoff and mtime < cutoff:
        return exchanges

    with open(DEEPSEEK_COMPOSER_HISTORY) as f:
        for line in f:
            line = line.strip()
            if line:
                exchanges.append({
                    "source": "composer_history",
                    "session_id": "composer",
                    "model": "deepseek-v4",
                    "role": "user",
                    "text": line[:MAX_SESSION_CHARS],
                })
    return exchanges


def read_codex_history(cutoff: datetime | None = None) -> list[dict]:
    """Lit le history.jsonl de Codex CLI."""
    exchanges: list[dict] = []
    if not CODEX_HISTORY.is_file():
        return exchanges

    mtime = datetime.fromtimestamp(CODEX_HISTORY.stat().st_mtime)
    if cutoff and mtime < cutoff:
        return exchanges

    with open(CODEX_HISTORY) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue

            ts = d.get("ts", 0)
            if isinstance(ts, str):
                try:
                    ts_int = int(ts)
                except ValueError:
                    ts_int = 0
            else:
                ts_int = int(ts)

            if ts_int:
                msg_dt = datetime.fromtimestamp(ts_int)
                if cutoff and msg_dt < cutoff:
                    continue

            text = d.get("text", "").strip()
            if text:
                exchanges.append({
                    "source": "codex",
                    "session_id": d.get("session_id", "codex_unknown"),
                    "model": "codex-cli",
                    "role": "user",
                    "text": text[:MAX_SESSION_CHARS],
                })
    return exchanges


def load_all_transcripts(days: int = 1) -> list[dict]:
    """Charge tous les transcripts des N derniers jours, toutes sources."""
    cutoff = datetime.now() - timedelta(days=days) if days < 365 else None

    all_exchanges = []
    all_exchanges.extend(read_deepseek_sessions(cutoff))
    all_exchanges.extend(read_claude_sessions(cutoff))
    all_exchanges.extend(read_composer_history(cutoff))
    all_exchanges.extend(read_codex_history(cutoff))

    return all_exchanges


# ── EXTRACTION LOCALE DE PATTERNS ──────────────────────────────────────

def extract_local_patterns(exchanges: list[dict]) -> dict[str, Any]:
    """Analyse locale : décisions, échecs, questions, entités, répétitions."""

    decisions: list[str] = []
    failures: list[str] = []
    questions: list[str] = []
    entities: Counter = Counter()
    user_msgs: list[str] = []
    session_ids: set = set()
    models_used: set = set()

    for ex in exchanges:
        session_ids.add(ex["session_id"])
        models_used.add(ex["model"])
        text = ex["text"]

        if ex["role"] == "user":
            user_msgs.append(text)

            for pat in DECISION_PATTERNS:
                for match in re.finditer(pat, text, re.IGNORECASE):
                    context = text[max(0, match.start()-40):match.end()+60].strip()
                    decisions.append(context[:120])
                    break

            for pat in FAILURE_PATTERNS:
                for match in re.finditer(pat, text, re.IGNORECASE):
                    context = text[max(0, match.start()-40):match.end()+60].strip()
                    failures.append(context[:120])
                    break

            for pat in QUESTION_PATTERNS:
                for match in re.finditer(pat, text, re.IGNORECASE):
                    context = text[max(0, match.start()-40):match.end()+80].strip()
                    questions.append(context[:150])
                    break

        for cat, pats in ENTITY_PATTERNS.items():
            for pat in pats:
                for match in re.finditer(pat, text):
                    entities[(cat, match.group(0))] += 1

    question_keywords = Counter()
    for q in questions:
        words = [w.lower() for w in q.split()
                 if len(w) > 3 and w.lower() not in ("comment", "pourquoi", "quelle", "qu'est", "c'est")]
        question_keywords.update(words)

    recurring_questions = [
        q for q in questions if any(
            w in q.lower() for w, c in question_keywords.most_common(10)
            if c >= 3
        )
    ]
    seen_questions = set()
    unique_recurring = []
    for q in recurring_questions:
        key = q.lower()[:60]
        if key not in seen_questions:
            seen_questions.add(key)
            unique_recurring.append(q)

    return {
        "session_count": len(session_ids),
        "models_used": sorted(models_used),
        "total_exchanges": len(exchanges),
        "user_messages": len(user_msgs),
        "decisions": list(set(decisions))[:20],
        "failures": list(set(failures))[:20],
        "questions": list(set(questions))[:20],
        "recurring_questions": unique_recurring[:10],
        "top_entities": {
            cat: [(name, count) for (c, name), count in entities.most_common(20) if c == cat][:10]
            for cat in ("projet", "outil", "machine", "membre")
        },
    }


def build_context(exchanges: list[dict], patterns: dict) -> str:
    """Construit le contexte pour le LLM : patterns + extraits pertinents."""
    lines = ["# RÉSUMÉ DES PATTERNS EXTRAITS LOCALEMENT", ""]

    def add_section(title, items):
        if items:
            lines.append(f"## {title}")
            for item in items[:10]:
                lines.append(f"- {item}")
            lines.append("")

    add_section("Décisions détectées", patterns["decisions"])
    add_section("Échecs / bloqueurs", patterns["failures"])
    add_section("Questions posées", patterns["questions"])
    add_section("Questions récurrentes", patterns["recurring_questions"])

    lines.append("## Entités mentionnées")
    for cat, items in patterns["top_entities"].items():
        if items:
            names = ", ".join(f"{n} ({c}x)" for n, c in items)
            lines.append(f"- **{cat}** : {names}")
    lines.append("")

    lines.append(f"## Statistiques")
    lines.append(f"- Sessions : {patterns['session_count']}")
    lines.append(f"- Échanges : {patterns['total_exchanges']}")
    lines.append(f"- Messages utilisateur : {patterns['user_messages']}")
    lines.append(f"- Modèles utilisés : {', '.join(patterns['models_used'])}")
    lines.append("")

    lines.append("# EXTRAITS DE TRANSCRIPT")
    lines.append("")

    user_msgs = sorted(
        [e for e in exchanges if e["role"] == "user"],
        key=lambda x: len(x["text"]), reverse=True
    )[:8]
    for ex in user_msgs:
        label = f"[{ex['source']}] JCH"
        text = ex["text"][:600]
        lines.append(f"**{label}** : {text}")
        lines.append("")

    total = "\n".join(lines)
    if len(total) > MAX_CONTEXT_CHARS:
        total = total[:MAX_CONTEXT_CHARS] + "\n\n[... tronqué ...]"
    return total


# ── STOCKAGE DB ───────────────────────────────────────────────────────

def _init_retro_schema(conn: sqlite3.Connection):
    """Crée les tables de rétrospective si elles n'existent pas."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS retro_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            pattern_type TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT,
            session_count INTEGER DEFAULT 1,
            resolved_at TEXT,
            resolved_by TEXT,
            auto_resolved INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_retro_date ON retro_patterns(date);
        CREATE INDEX IF NOT EXISTS idx_retro_type ON retro_patterns(pattern_type);
        CREATE INDEX IF NOT EXISTS idx_retro_unresolved ON retro_patterns(resolved_at)
            WHERE resolved_at IS NULL;

        CREATE TABLE IF NOT EXISTS retro_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            report_path TEXT,
            exchange_count INTEGER DEFAULT 0,
            session_count INTEGER DEFAULT 0,
            model_used TEXT,
            provider TEXT,
            status TEXT DEFAULT 'analyzed',
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS retro_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            content TEXT NOT NULL,
            assignee TEXT DEFAULT 'dobby',
            status TEXT DEFAULT 'open',
            resolved_at TEXT,
            resolved_by TEXT,
            session_ref INTEGER,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_recommendations_status ON retro_recommendations(status);
        CREATE INDEX IF NOT EXISTS idx_recommendations_date ON retro_recommendations(date);
    """)
    _migrate_retro_schema(conn)


def _migrate_retro_schema(conn: sqlite3.Connection):
    """Migration sécurisée — ajoute les colonnes manquantes sans perte de données."""
    migrations = [
        ("retro_patterns", "resolved_at", "TEXT"),
        ("retro_patterns", "resolved_by", "TEXT"),
        ("retro_patterns", "auto_resolved", "INTEGER DEFAULT 0"),
        ("retro_sessions", "session_count", "INTEGER DEFAULT 0"),
    ]
    c = conn.cursor()
    for table, column, col_type in migrations:
        try:
            c.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
        except sqlite3.OperationalError:
            pass  # column already exists, safe to ignore
    conn.commit()


def store_patterns(patterns: dict, today_str: str):
    """Stocke les patterns extraits dans team.db + auto-résolution des anciens."""
    try:
        conn = sqlite3.connect(DB_PATH)
        _init_retro_schema(conn)
        c = conn.cursor()

        for decision in patterns.get("decisions", []):
            c.execute(
                "INSERT INTO retro_patterns (date, pattern_type, content, source) VALUES (?, 'decision', ?, 'auto-extract')",
                (today_str, decision),
            )
        for failure in patterns.get("failures", []):
            c.execute(
                "INSERT INTO retro_patterns (date, pattern_type, content, source) VALUES (?, 'failure', ?, 'auto-extract')",
                (today_str, failure),
            )
        for question in patterns.get("questions", []):
            c.execute(
                "INSERT INTO retro_patterns (date, pattern_type, content, source) VALUES (?, 'question', ?, 'auto-extract')",
                (today_str, question),
            )
        for recurring in patterns.get("recurring_questions", []):
            c.execute(
                "INSERT INTO retro_patterns (date, pattern_type, content, source) VALUES (?, 'recurring_question', ?, 'auto-extract')",
                (today_str, recurring),
            )

        # Auto-résolution : marquer les patterns 'failure' passés qui n'apparaissent plus
        # On garde une fenêtre de 14 jours pour éviter de marquer des patterns très récents
        if today_sessions := patterns.get("session_count", 0):
            today_failure_snippets = set(
                f[:80].lower() for f in patterns.get("failures", [])
            )
            c.execute(
                """SELECT id, date, content FROM retro_patterns
                   WHERE pattern_type = 'failure'
                     AND resolved_at IS NULL
                     AND date < ?
                   ORDER BY date ASC""",
                (today_str,),
            )
            old_unresolved = c.fetchall()
            resolved_count = 0
            for pid, pdate, pcontent in old_unresolved:
                # Si le contenu du pattern ancien n'est plus mentionné aujourd'hui
                snippet = pcontent[:80].lower()
                if snippet and snippet not in today_failure_snippets:
                    # Vérifier si pattern a plus de 3 jours (pour éviter faux positifs récents)
                    from datetime import datetime as dt
                    try:
                        pattern_age = (dt.strptime(today_str, "%Y-%m-%d")
                                       - dt.strptime(pdate, "%Y-%m-%d")).days
                    except ValueError:
                        pattern_age = 1
                    if pattern_age >= 3:
                        c.execute(
                            "UPDATE retro_patterns SET resolved_at = ?, resolved_by = 'auto', auto_resolved = 1 WHERE id = ?",
                            (today_str, pid),
                        )
                        resolved_count += 1
            if resolved_count:
                print(f"[Auto-résolution] {resolved_count} anciens patterns marqués résolus.")

        conn.commit()
        conn.close()
    except (OSError, sqlite3.DatabaseError) as exc:
        print(f"[DB] stockage patterns impossible : {exc}")


def store_retro_report(today_str: str, report_path: str | None,
                       exchange_count: int, session_count: int,
                       models: str, provider: str):
    """Enregistre la session de rétrospective."""
    try:
        conn = sqlite3.connect(DB_PATH)
        _init_retro_schema(conn)
        conn.execute(
            "INSERT INTO retro_sessions (date, report_path, exchange_count, session_count, model_used, provider, status) VALUES (?, ?, ?, ?, ?, ?, 'analyzed')",
            (today_str, report_path, exchange_count, session_count, models, provider),
        )
        conn.commit()
        conn.close()
    except (OSError, sqlite3.DatabaseError) as exc:
        print(f"[DB] enregistrement session impossible : {exc}")


# ── MÉTRIQUES D'EFFICACITÉ ────────────────────────────────────────────


def compute_resolution_rate(date_from: str, date_to: str) -> dict:
    """Métrique 1 — Taux de résolution : combien de failures/bloqueurs
    identifiés entre date_from et date_to ont été résolus via auto-détection."""
    try:
        conn = sqlite3.connect(DB_PATH)
        _init_retro_schema(conn)
        c = conn.cursor()

        c.execute(
            """SELECT COUNT(*) FROM retro_patterns
               WHERE pattern_type IN ('failure', 'recurring_question')
                 AND date >= ? AND date <= ?
                 AND resolved_at IS NULL""",
            (date_from, date_to),
        )
        still_open = c.fetchone()[0]

        c.execute(
            """SELECT COUNT(*) FROM retro_patterns
               WHERE pattern_type IN ('failure', 'recurring_question')
                 AND date >= ? AND date <= ?""",
            (date_from, date_to),
        )
        total = c.fetchone()[0]

        c.execute(
            """SELECT COUNT(*) FROM retro_patterns
               WHERE pattern_type IN ('failure', 'recurring_question')
                 AND date >= ? AND date <= ?
                 AND resolved_at IS NOT NULL
                 AND resolved_by = 'auto'""",
            (date_from, date_to),
        )
        auto_resolved = c.fetchone()[0]

        c.execute(
            """SELECT COUNT(*) FROM retro_patterns
               WHERE pattern_type IN ('failure', 'recurring_question')
                 AND date >= ? AND date <= ?
                 AND resolved_by NOT NULL AND resolved_by != 'auto'""",
            (date_from, date_to),
        )
        manual_resolved = c.fetchone()[0]

        conn.close()

        resolved = auto_resolved + manual_resolved
        rate = (resolved / total * 100) if total > 0 else 0.0
        return {
            "total_patterns": total,
            "still_open": still_open,
            "auto_resolved": auto_resolved,
            "manual_resolved": manual_resolved,
            "resolved_total": resolved,
            "resolution_rate": round(rate, 1),
        }
    except (OSError, sqlite3.DatabaseError) as exc:
        print(f"[DB] resolution_rate impossible : {exc}")
        return {"error": str(exc)}


def compute_volume_trend(window_days: int = 14) -> dict:
    """Métrique 2 — Évolution du volume : tendance des échanges/session
    sur les N derniers jours."""
    try:
        conn = sqlite3.connect(DB_PATH)
        _init_retro_schema(conn)
        c = conn.cursor()

        c.execute(
            """SELECT date, exchange_count, session_count FROM retro_sessions
               WHERE status = 'analyzed'
                 AND session_count > 0
               ORDER BY date ASC
               LIMIT ?""",
            (window_days,),
        )
        rows = c.fetchall()
        conn.close()

        if len(rows) < 2:
            return {"enough_data": False, "message": "Pas assez de points (min 2 sessions requises)"}

        recent = rows[-1]
        oldest = rows[0]

        recent_ratio = recent[1] / recent[2] if recent[2] > 0 else 0
        oldest_ratio = oldest[1] / oldest[2] if oldest[2] > 0 else 0

        # Tendance sur la période
        trend_pct = round(
            ((recent_ratio - oldest_ratio) / oldest_ratio * 100) if oldest_ratio > 0 else 0,
            1,
        )

        # Moyenne mobile sur les 3 derniers jours vs les 3 premiers
        if len(rows) >= 6:
            recent3 = [r for r in rows[-3:]]
            oldest3 = [r for r in rows[:3]]
            avg_recent = sum(r[1] / r[2] for r in recent3) / 3
            avg_oldest = sum(r[1] / r[2] for r in oldest3) / 3
            trend_3d_pct = round(
                ((avg_recent - avg_oldest) / avg_oldest * 100) if avg_oldest > 0 else 0,
                1,
            )
        else:
            avg_recent = recent_ratio
            avg_oldest = oldest_ratio
            trend_3d_pct = trend_pct

        return {
            "enough_data": True,
            "days": len(rows),
            "avg_exchanges_per_session_recent": round(recent_ratio, 1),
            "avg_exchanges_per_session_oldest": round(oldest_ratio, 1),
            "trend_pct": trend_pct,
            "trend_3d_pct": trend_3d_pct,
            "direction": "down" if trend_pct < 0 else ("up" if trend_pct > 0 else "stable"),
        }
    except (OSError, sqlite3.DatabaseError) as exc:
        return {"error": str(exc)}


def compute_application_rate(today_str: str, window_days: int = 7) -> dict:
    """Métrique 3 — Taux d'application : combien de patterns 'question'
    et 'recurring_question' d'il y a window_days jours ne réapparaissent plus
    aujourd'hui (signe que le sujet a été traité/documenté)."""
    from datetime import datetime as dt, timedelta

    try:
        then_date = (dt.strptime(today_str, "%Y-%m-%d") - timedelta(days=window_days)).isoformat()

        conn = sqlite3.connect(DB_PATH)
        _init_retro_schema(conn)
        c = conn.cursor()

        # Questions qui existaient il y a window_days jours
        c.execute(
            """SELECT id, content FROM retro_patterns
               WHERE pattern_type IN ('question', 'recurring_question')
                 AND date = ?
                 AND resolved_at IS NULL""",
            (then_date,),
        )
        old_questions = c.fetchall()

        # Questions d'aujourd'hui
        c.execute(
            """SELECT content FROM retro_patterns
               WHERE pattern_type IN ('question', 'recurring_question')
                 AND date = ?""",
            (today_str,),
        )
        today_questions = set(q[0][:80].lower() for q in c.fetchall())

        conn.close()

        if not old_questions:
            return {
                "enough_data": False,
                "message": f"Aucune question identifiée il y a {window_days} jours",
            }

        still_present = 0
        applied_ids = []
        for qid, qcontent in old_questions:
            snippet = qcontent[:80].lower()
            # On considère "appliqué" si le sujet n'est plus posé textuellement
            if snippet and snippet not in today_questions:
                still_present += 1
            else:
                applied_ids.append(qid)

        total = len(old_questions)
        applied = total - still_present
        rate = round(applied / total * 100, 1) if total > 0 else 0.0

        return {
            "enough_data": True,
            "total_questions_before": total,
            "still_recurring": still_present,
            "applied_implicitly": applied,
            "application_rate": rate,
        }
    except (OSError, sqlite3.DatabaseError) as exc:
        return {"error": str(exc)}


def build_metrics_section(today_str: str) -> str:
    """Produit la section markdown des 3 métriques pour le rapport."""
    from datetime import datetime as dt, timedelta

    lines = ["## 📊 Métriques d'efficacité\n"]

    # Métrique 1 — Résolution
    week_ago = (dt.strptime(today_str, "%Y-%m-%d") - timedelta(days=7)).isoformat()
    resolution = compute_resolution_rate(week_ago, today_str)
    if "error" not in resolution:
        lines.append("### Taux de résolution (7 jours glissants)")
        lines.append(f"- Patterns détectés : {resolution['total_patterns']}")
        lines.append(f"- Résolus automatiquement : {resolution['auto_resolved']}")
        lines.append(f"- Résolus manuellement : {resolution['manual_resolved']}")
        lines.append(f"- Encore ouverts : {resolution['still_open']}")
        lines.append(f"- **Taux : {resolution['resolution_rate']}%**\n")
    else:
        lines.append(f"### Taux de résolution\n- {resolution['error']}\n")

    # Métrique 2 — Volume
    volume = compute_volume_trend()
    if volume.get("enough_data"):
        direction_icon = "📈" if volume["direction"] == "up" else ("📉" if volume["direction"] == "down" else "➡️")
        lines.append("### Évolution du volume (tendance)")
        lines.append(f"- {direction_icon} Direction : {volume['direction']}")
        lines.append(f"- Échanges/session récent : {volume['avg_exchanges_per_session_recent']}")
        lines.append(f"- Échanges/session début fenêtre : {volume['avg_exchanges_per_session_oldest']}")
        lines.append(f"- Tendance globale : {volume['trend_pct']}%")
        lines.append(f"- Tendance 3j-3j : {volume['trend_3d_pct']}%\n")
    elif "error" in volume:
        lines.append(f"### Évolution du volume\n- {volume['error']}\n")
    else:
        lines.append(f"### Évolution du volume\n- {volume['message']}\n")

    # Métrique 3 — Application
    application = compute_application_rate(today_str)
    if application.get("enough_data"):
        lines.append("### Taux d'application implicite")
        lines.append(f"- Questions J-7 : {application['total_questions_before']}")
        lines.append(f"- Encore posées : {application['still_recurring']}")
        lines.append(f"- Non réapparues (signe de résolution) : {application['applied_implicitly']}")
        lines.append(f"- **Taux d'application : {application['application_rate']}%**\n")
    elif "error" in application:
        lines.append(f"### Taux d'application implicite\n- {application['error']}\n")
    else:
        lines.append(f"### Taux d'application implicite\n- {application['message']}\n")

    return "\n".join(lines)


# ── AUTO-APPRENTISSAGE ──────────────────────────────────────────────


def parse_llm_discoveries(retro_text: str, local_patterns: dict) -> dict:
    discoveries = {"decisions": [], "failures": [], "questions": [], "recurring_questions": []}
    if not retro_text:
        return discoveries
    section_patterns = {
        "decisions": r"## Décisions prises\s*\n(.*?)(?=\n##|\Z)",
        "failures": r"## Échecs ouverts\s*/?\s*bloqueurs\s*\n(.*?)(?=\n##|\Z)",
        "questions": r"## Questions récurrentes\s*\n(.*?)(?=\n##|\Z)",
    }
    local_snippets: dict[str, set] = {}
    for cat in ("decisions", "failures", "questions"):
        local_snippets[cat] = set(l[:80].lower() for l in local_patterns.get(cat, []))
    seen: set = set()
    for cat, pat in section_patterns.items():
        m = re.search(pat, retro_text, re.DOTALL)
        if not m:
            continue
        items = re.findall(r"[-*]\s+(.+?)(?:\n|$)", m.group(1))
        items += re.findall(r"\d+\.\s+(.+?)(?:\n|$)", m.group(1))
        for item in items:
            item = item.strip().strip('"').strip("*")
            if not item or len(item) < 20:
                continue
            # Clean: remove leading dashes/bold markers from LLM output
            item = re.sub(r"^[-*]\s*\*{0,2}", "", item).strip()
            if not item or len(item) < 20:
                continue
            key = item[:80].lower()
            if key in seen:
                continue
            seen.add(key)
            is_local = any(key in ls or any(key[:40] in l for l in ls) for ls in local_snippets.values())
            if not is_local:
                discoveries[cat].append(item)
    return discoveries


def store_retro_discoveries(discoveries: dict, today_str: str) -> int:
    cat_map = {"decisions": "llm_discovered_decision", "failures": "llm_discovered_failure", "questions": "llm_discovered_question"}
    total = 0
    try:
        conn = sqlite3.connect(DB_PATH)
        _init_retro_schema(conn)
        c = conn.cursor()
        for local_cat, db_type in cat_map.items():
            for item in discoveries.get(local_cat, []):
                c.execute("SELECT id FROM retro_patterns WHERE date = ? AND pattern_type = ? AND content = ?",
                          (today_str, db_type, item))
                if not c.fetchone():
                    c.execute("INSERT INTO retro_patterns (date, pattern_type, content, source) VALUES (?, ?, ?, 'llm_discovery')",
                              (today_str, db_type, item))
                    total += 1
        conn.commit()
        conn.close()
        if total:
            print(f"[Auto-apprentissage] {total} nouveaux patterns découverts par LLM.")
        return total
    except (OSError, sqlite3.DatabaseError) as exc:
        print(f"[DB] stockage découvertes impossible : {exc}")
        return 0


def compute_pattern_frequency(today_str: str, window_days: int = 14) -> dict:
    from datetime import datetime as dt, timedelta
    try:
        since = (dt.strptime(today_str, "%Y-%m-%d") - timedelta(days=window_days)).isoformat()
        conn = sqlite3.connect(DB_PATH)
        _init_retro_schema(conn)
        c = conn.cursor()
        c.execute("""SELECT pattern_type, COUNT(DISTINCT date) as days, COUNT(*) as total
                     FROM retro_patterns WHERE date >= ? AND pattern_type NOT LIKE 'llm_discovered%'
                     GROUP BY pattern_type ORDER BY days DESC""", (since,))
        per_type = {row[0]: {"days": row[1], "total": row[2]} for row in c.fetchall()}
        c.execute("""SELECT pattern_type, content, COUNT(DISTINCT date) as days
                     FROM retro_patterns WHERE date >= ?
                     GROUP BY pattern_type, substr(content, 1, 60)
                     HAVING days >= 3 ORDER BY days DESC""", (since,))
        recurring = [{"type": r[0], "content": r[1][:80], "days": r[2]} for r in c.fetchall()]
        conn.close()
        return {"per_type": per_type, "recurring": recurring[:15]}
    except (OSError, sqlite3.DatabaseError) as exc:
        return {"error": str(exc)}


def count_active_days(today_str: str, window_days: int = 14) -> int:
    from datetime import datetime as dt, timedelta
    try:
        since = (dt.strptime(today_str, "%Y-%m-%d") - timedelta(days=window_days)).isoformat()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(DISTINCT date) FROM retro_patterns WHERE date >= ?", (since,))
        n = c.fetchone()[0]
        conn.close()
        return n
    except (OSError, sqlite3.DatabaseError):
        return 0


def build_learning_section(today_str: str) -> str:
    from datetime import datetime as dt, timedelta
    lines = ["## 🧠 Auto-apprentissage\n"]
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT pattern_type, content FROM retro_patterns WHERE date = ? AND source = 'llm_discovery' ORDER BY pattern_type", (today_str,))
        discoveries = c.fetchall()
        conn.close()
    except (OSError, sqlite3.DatabaseError):
        discoveries = []

    if discoveries:
        lines.append("### Nouveaux patterns découverts aujourd'hui")
        lines.append("*(identifiés par le LLM, non détectés par l'extraction locale)*\n")
        for ptype, content in discoveries:
            label = ptype.replace("llm_discovered_", "").capitalize()
            lines.append(f"- [{label}] {content[:150]}")
        lines.append("")
    else:
        lines.append("*Aucun nouveau pattern découvert par le LLM aujourd'hui.*\n")

    freq = compute_pattern_frequency(today_str)
    if "error" not in freq and freq.get("per_type"):
        lines.append("### Fréquence des patterns (14 jours)")
        for ptype, stats in freq["per_type"].items():
            label = ptype.replace("_", " ").capitalize()
            lines.append(f"- **{label}** : {stats['days']} jours, {stats['total']} occurrences")
        lines.append("")

    if "error" not in freq and freq.get("recurring"):
        lines.append("### Patterns confirmés (3+ jours d'apparition)")
        lines.append("*(assez fréquents pour mériter une action documentaire)*\n")
        for p in freq["recurring"]:
            label = p["type"].replace("_", " ").capitalize()
            lines.append(f"- [{label}] ({p['days']}x) {p['content']}")
        lines.append("")
        high_freq = [p for p in freq["recurring"] if p["days"] >= 5]
        if high_freq:
            lines.append("### 📝 Suggestions de documentation automatique")
            for p in high_freq:
                lines.append(f"- [ ] Documenter : **{p['content']}**")
            lines.append("")

    active_days = count_active_days(today_str)
    lines.append("### Bilan apprentissage")
    lines.append(f"- Nouveaux patterns appris aujourd'hui : {len(discoveries)}")
    lines.append(f"- Jours d'observation : {active_days}")
    lines.append(f"- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.\n")
    return "\n".join(lines)


# ── RECOMMANDATIONS ASSIGNABLES ──────────────────────────────────────


ASSIGNEE_KEYWORDS = {
    "forge": ["forge", "script", "automatis", "déploiement", "cron", "monitor", "build"],
    "renard": ["légal", "juridique", "contrat", "pacte"],
    "sybil": ["consolidat", "daily", "rapport", "dashboard"],
    "furet": ["recherche", "étude", "analyse", "benchmark"],
    "corbeau": ["graphify", "knowledge", "wiki"],
}


def auto_assign(content: str) -> str:
    """Assigne automatiquement une recommandation selon son contenu."""
    lower = content.lower()
    for specialist, keywords in ASSIGNEE_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return specialist
    return "dobby"


def parse_recommendations(retro_text: str) -> list[dict]:
    """Parse la section ## Recommandations du rapport LLM."""
    recs: list[dict] = []
    if not retro_text:
        return recs

    m = re.search(r"## Recommandations\s*\n(.*?)(?=\n##|\Z)", retro_text, re.DOTALL)
    if not m:
        return recs

    items = re.findall(r"(?:\d+\.|[-*])\s+(.+?)(?:\n|$)", m.group(1))
    seen: set = set()
    for item in items:
        item = item.strip().strip('"').strip("*").strip("[]")
        if not item or len(item) < 15 or item.lower() in seen:
            continue
        seen.add(item.lower())
        recs.append({
            "content": item,
            "assignee": auto_assign(item),
        })
    return recs


def store_recommendations(recommendations: list[dict], today_str: str, session_id: int | None = None):
    """Stocke les recommandations en DB — saute les doublons exacts."""
    total = 0
    try:
        conn = sqlite3.connect(DB_PATH)
        _init_retro_schema(conn)
        c = conn.cursor()
        for rec in recommendations:
            c.execute(
                "SELECT id FROM retro_recommendations WHERE status = 'open' AND content = ?",
                (rec["content"],),
            )
            if not c.fetchone():
                c.execute(
                    """INSERT INTO retro_recommendations (date, content, assignee, status, session_ref)
                       VALUES (?, ?, ?, 'open', ?)""",
                    (today_str, rec["content"], rec["assignee"], session_id),
                )
                total += 1
        conn.commit()
        conn.close()
        if total:
            print(f"[Recommandations] {total} nouvelles recommandations enregistrées.")
        return total
    except (OSError, sqlite3.DatabaseError) as exc:
        print(f"[DB] stockage recommandations impossible : {exc}")
        return 0


def compute_recommendation_status() -> dict:
    """État global des recommandations."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""SELECT status, COUNT(*) FROM retro_recommendations GROUP BY status""")
        by_status = {row[0]: row[1] for row in c.fetchall()}

        c.execute("""SELECT assignee, COUNT(*) FROM retro_recommendations WHERE status = 'open' GROUP BY assignee""")
        by_assignee = {row[0]: row[1] for row in c.fetchall()}

        c.execute("""SELECT COUNT(*) FROM retro_recommendations WHERE status = 'open' AND date < date('now', '-7 days')""")
        stale = c.fetchone()[0]

        # Last 5 open recommendations
        c.execute("""SELECT id, date, content, assignee FROM retro_recommendations WHERE status = 'open' ORDER BY date DESC LIMIT 5""")
        latest_open = [{"id": r[0], "date": r[1], "content": r[2][:80], "assignee": r[3]} for r in c.fetchall()]

        conn.close()
        return {
            "total": sum(by_status.values()),
            "by_status": by_status,
            "open_by_assignee": by_assignee,
            "stale_7d": stale,
            "latest_open": latest_open,
        }
    except (OSError, sqlite3.DatabaseError) as exc:
        return {"error": str(exc)}


def mark_recommendation_status(rec_id: int, new_status: str, resolved_by: str = "manual"):
    """Met à jour manuellement le statut d'une recommandation."""
    if new_status not in ("open", "in_progress", "done", "wontfix", "stale"):
        return False
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            """UPDATE retro_recommendations SET status = ?, resolved_at = date('now'), resolved_by = ? WHERE id = ?""",
            (new_status, resolved_by, rec_id),
        )
        conn.commit()
        conn.close()
        return True
    except (OSError, sqlite3.DatabaseError):
        return False


def build_recommendations_tracker() -> str:
    """Produit la section état des recommandations pour le rapport."""
    lines = ["## ✅ État des recommandations\n"]
    status = compute_recommendation_status()
    if "error" in status:
        lines.append(f"- {status['error']}\n")
        return "\n".join(lines)

    by_status = status.get("by_status", {})
    open_count = by_status.get("open", 0)
    done_count = by_status.get("done", 0) + by_status.get("wontfix", 0)
    in_progress = by_status.get("in_progress", 0)
    total = status.get("total", 0)

    lines.append(f"**{total}** recommandations au total — "
                 f"**{open_count}** ouvertes — "
                 f"**{in_progress}** en cours — "
                 f"**{done_count}** terminées\n")

    if status.get("stale_7d"):
        lines.append(f"⚠️ {status['stale_7d']} recommandations ouvertes depuis plus de 7 jours.\n")

    assignee = status.get("open_by_assignee", {})
    if assignee:
        lines.append("### Répartition par assigné\n")
        for name, count in sorted(assignee.items(), key=lambda x: -x[1]):
            lines.append(f"- **{name.capitalize()}** : {count}")
        lines.append("")

    latest = status.get("latest_open", [])
    if latest:
        lines.append("### Plus récentes ouvertes\n")
        for r in latest:
            lines.append(f"- [id={r['id']}] ({r['date']}) **{r['assignee'].capitalize()}** : {r['content']}")
        lines.append("")

    if open_count > 0:
        lines.append(f"Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` "
                     f"pour les clôturer.\n")

    return "\n".join(lines)


# ── BUDGET PROVIDER ──────────────────────────────────────────────────


def build_budget_section() -> str:
    """Section budget pour le rapport : soldes API + alertes."""
    lines = ["## 💰 Budget fournisseurs API\n"]
    try:
        from provider_balance import get_balances
    except ImportError:
        lines.append("*Module provider_balance.py non trouvé — budget non vérifié.*\n")
        return "\n".join(lines)

    data = get_balances(with_openai=True)
    if data.get("warnings"):
        lines.append(f"⚠️ **{data['warning_count']} alerte(s) budget détectée(s)**\n")
    else:
        lines.append("✅ Tous les comptes sont en ordre.\n")

    for r in data["results"]:
        prov = r["provider"]
        if r["status"] == "no_key":
            lines.append(f"- {prov:12s} ⚪ pas de clé")
        elif r["status"] == "error":
            lines.append(f"- {prov:12s} 🔴 {r.get('error', '?')}")
        elif prov == "OpenAI":
            lines.append(f"- {prov:12s} 📊 ${r['usage_month']} consommé ce mois")
        else:
            b = r["balance"]
            cur = r.get("currency", "USD")
            low = b is not None and b < data.get("threshold_usd", 10)
            icon = "🔴" if (b is not None and b < data["threshold_usd"] / 2) else ("🟡" if low else "🟢")
            lines.append(f"- {prov:12s} {icon} ${b} {cur}")

    if data["total_balance_usd"]:
        lines.append(f"\n**Total disponible (USD) : ${data['total_balance_usd']}**\n")

    return "\n".join(lines)


# ── RAPPORT MARKDOWN ─────────────────────────────────────────────────

def save_retro_md(today_str: str, content: str, patterns: dict,
                  recommendations: list | None = None) -> str:
    """Sauvegarde le rapport markdown enrichi + métriques + auto-apprentissage."""
    year = today_str[:4]
    month = today_str[5:7]
    dest_dir = RETRO_DIR / year / month
    dest_dir.mkdir(parents=True, exist_ok=True)

    filepath = dest_dir / f"{today_str}-dobby-retro.md"

    metrics = build_metrics_section(today_str)
    learning = build_learning_section(today_str)
    recom_tracker = build_recommendations_tracker()
    budget = build_budget_section()

    header = (
        f"---\ndate: {today_str}\ntype: retrospective\nauthor: Dobby\n"
        f"tags: [retro, meta, auto-analyse, apprentissage]\n"
        f"sessions: {patterns['session_count']}\n"
        f"echanges: {patterns['total_exchanges']}\n"
        f"modeles: {', '.join(patterns['models_used'])}\n---\n\n"
        f"# Rétrospective — {today_str}\n\n"
        f"**Sessions analysées :** {patterns['session_count']} | "
        f"**Échanges :** {patterns['total_exchanges']} | "
        f"**Modèles :** {', '.join(patterns['models_used'])}\n\n"
        f"---\n\n"
    )
    filepath.write_text(header + content + "\n\n" + metrics + "\n\n" + learning + "\n\n" + recom_tracker + "\n\n" + budget, encoding="utf-8")
    return str(filepath)


# ── LLM PROVIDER FACTORY ──────────────────────────────────────────────

def get_provider(provider_name: str, model: str | None = None) -> RetroProvider | None:
    """Fabrique le bon fournisseur LLM."""
    secrets = _load_secrets()

    if provider_name == "anthropic":
        api_key = secrets.get("anthropic")
        if not api_key:
            print("[WARN] Clé Anthropic introuvable. Vérifie ~/.config/pka-jch/anthropic_key.txt")
            return None
        return AnthropicProvider(api_key, model or "claude-haiku-4-5-20251001")

    elif provider_name == "openrouter":
        api_key = secrets.get("openrouter")
        if not api_key:
            print("[WARN] Clé OpenRouter introuvable. Vérifie ~/.config/pka-jch/openrouter_key.txt")
            return None
        return OpenRouterProvider(api_key, model or "deepseek/deepseek-v4-flash")

    return None


def _load_secrets() -> dict[str, str]:
    """Charge les clés API depuis le répertoire des secrets."""
    secrets = {}
    key_file = SECRETS_DIR / "anthropic_key.txt"
    if key_file.is_file():
        secrets["anthropic"] = key_file.read_text().strip()
    key_file = SECRETS_DIR / "openrouter_key.txt"
    if key_file.is_file():
        secrets["openrouter"] = key_file.read_text().strip()
    return secrets


# ── CLI ───────────────────────────────────────────────────────────────

def parse_args(argv: list[str]) -> dict:
    args = {
        "days": 1,
        "dry_run": False,
        "provider": "anthropic",
        "model": None,
        "all": False,
    }
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--days", "-d") and i + 1 < len(argv):
            args["days"] = int(argv[i + 1])
            i += 2
        elif a == "--all":
            args["all"] = True
            args["days"] = 365
            i += 1
        elif a == "--dry-run":
            args["dry_run"] = True
            i += 1
        elif a == "--provider":
            args["provider"] = argv[i + 1] if i + 1 < len(argv) else "anthropic"
            i += 2
        elif a == "--model":
            args["model"] = argv[i + 1] if i + 1 < len(argv) else None
            i += 2
        else:
            i += 1
    return args


def main():
    args = parse_args(sys.argv[1:])
    today_str = date.today().isoformat()
    days = args["days"]

    print(f"[Dobby] Rétrospective multi-source — {days} jour(s)…")
    exchanges = load_all_transcripts(days=days)

    if not exchanges:
        print("[Dobby] Aucune session détectée dans la période.")
        return

    sources = set(e["source"] for e in exchanges)
    models = set(e["model"] for e in exchanges)
    print(f"[Dobby] {len(exchanges)} échanges chargés depuis {', '.join(sources)}")
    print(f"[Dobby] Modèles : {', '.join(models)}")

    print("[Dobby] Extraction locale des patterns…")
    patterns = extract_local_patterns(exchanges)
    print(f"        Décisions : {len(patterns['decisions'])} | "
          f"Échecs : {len(patterns['failures'])} | "
          f"Questions : {len(patterns['questions'])}")
    for cat, items in patterns["top_entities"].items():
        if items:
            print(f"        {cat} : {', '.join(n for n, _ in items[:5])}")

    store_patterns(patterns, today_str)
    session_count = patterns.get("session_count", 0)

    if args["dry_run"]:
        print("[Dobby] Dry-run — analyse LLM sautée. Patterns stockés en DB.")
        store_retro_report(today_str, None, len(exchanges), session_count, ",".join(models), "dry-run")
        print("\n--- RÉSUMÉ LOCAL ---")
        print(json.dumps(patterns, indent=2, ensure_ascii=False))
        return

    print(f"[Dobby] Analyse via {args['provider']}…")
    provider = get_provider(args["provider"], args.get("model"))
    if not provider:
        print("[Dobby] Aucun fournisseur disponible. Fallback analyse locale uniquement.")
        store_retro_report(today_str, None, len(exchanges), session_count, ",".join(models), f"{args['provider']}-failed")
        return

    context = build_context(exchanges, patterns)
    retro = provider.analyze(context, today_str)

    # Auto-apprentissage : extraire les patterns LLM que le regex local a ratés
    discoveries = parse_llm_discoveries(retro, patterns)
    n_discovered = store_retro_discoveries(discoveries, today_str)

    # Recommandations : parser, stocker, assigner
    recommendations = parse_recommendations(retro)
    n_recs = store_recommendations(recommendations, today_str)

    filepath = save_retro_md(today_str, retro, patterns)
    store_retro_report(today_str, filepath, len(exchanges), session_count, ",".join(models), args["provider"])

    print(f"[Dobby] ✅ Rétrospective → {filepath}")

    try:
        from pka_memory_log import log_run
        log_run("dobby_retro", "ok",
                f"Rétrospective {today_str} — {len(exchanges)} échanges depuis {', '.join(sources)}"
                f" — {patterns['session_count']} sessions — {len(patterns['decisions'])} décisions extraites",
                project_key="PKA")
    except ImportError:
        pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Dobby] Interrompu.")
    except Exception as exc:
        print(f"[Dobby] ERREUR : {exc}")
        import traceback
        traceback.print_exc()
        try:
            from pka_memory_log import log_run
            log_run("dobby_retro", "error", str(exc)[:200])
        except ImportError:
            pass
