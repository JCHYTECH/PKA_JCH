#!/usr/bin/env python3
"""
pka_skill_generator.py 🦉 — Générateur de skills auto-apprenant PKA

Lit les patterns extraits par dobby_retro.py depuis team.db, identifie les
clusters de problèmes récurrents, et propose des skills candidates (SKILL.md)
via analyse LLM. Inspiré par la boucle d'apprentissage de Hermes Agent.

Boucle : retro_patterns → cluster → LLM → brouillon SKILL.md → TEAM_Inbox/
        → Corbeau (curation) → Dobby (validation) → skills/ (déploiement)

Usage :
    python3 scripts/pka_skill_generator.py                  # analyse + propose
    python3 scripts/pka_skill_generator.py --dry-run        # extraction locale seulement
    python3 scripts/pka_skill_generator.py --days 14        # fenêtre de 14 jours
    python3 scripts/pka_skill_generator.py --auto           # génère + écrit dans TEAM_Inbox/
    python3 scripts/pka_skill_generator.py --provider openrouter  # LLM via OpenRouter

Dépendances : sqlite3, json, re, collections (stdlib). requests pour OpenRouter.

Model: deepseek-v4 (2026-06-12, skill auto-generation pipeline)
"""

import json
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

# ── CONFIG ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
PKA_DIR = BASE_DIR.parent
DB_PATH = PKA_DIR / "TEAM" / "team.db"
SKILLS_DIR = PKA_DIR / "skills"
TEAM_INBOX = PKA_DIR / "TEAM_Inbox"
SKILLS_INDEX = SKILLS_DIR / "INDEX.md"
SECRETS_DIR = Path.home() / ".config" / "pka-jch"

# Seuils
MIN_PATTERN_OCCURRENCES = 3          # occurrences min pour proposer une skill
MIN_CLUSTER_SIMILARITY = 0.55        # similarité min pour grouper deux patterns
MAX_SKILL_PROPOSALS = 3              # max de skills proposées par run

# ── PROVIDER ABSTRACTION ─────────────────────────────────────────────

SYSTEM_PROMPT = """Tu es Dobby 🦉, orchestrateur du système PKA de Jean-Claude Havaux.
Tu analyses des patterns récurrents extraits des sessions de travail multi-outils
(DeepSeek TUI, Claude Code, Codex CLI).

On te fournit :
1. Une liste de questions/échecs/bloqueurs récurrents
2. Les skills PKA existantes (pour éviter les doublons)
3. Le contexte : PKA est un système multi-agents (30 spécialistes + Dobby)
   avec knowledge graph, skills markdown, cron jobs, bots Telegram.

Ta mission : proposer des skills candidates qui transformeraient ces problèmes
récurrents en procédures réutilisables (comme Hermes Agent le fait).

Pour chaque skill candidate, produis UN SEUL bloc exactement au format :

---SKILL---
name: <slug-court>
trigger: <quand déclencher — phrase simple>
description: <1 ligne max 120 car>
body: |
  ## Procédure

  ### Prérequis
  - ...

  ### Étapes
  1. ...
  2. ...
  3. ...

  ### Vérification
  - ...

  ### En cas d'échec
  - ...
---END---

Règles :
- Le name doit être un slug (pka-xxx)
- Le trigger doit mentionner les mots-clés que JCH utiliserait
- La body doit être actionnable, pas théorique
- Ne pas dupliquer une skill existante
- Si aucun pattern ne justifie une skill, retourne explicitement "AUCUNE_SKILL"
- Maximum 3 skills proposées
"""


class SkillGeneratorProvider:
    """Fournisseur LLM pour la génération de skills."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def generate(self, context: str) -> str:
        raise NotImplementedError


class OpenRouterProvider(SkillGeneratorProvider):
    """OpenRouter — compatible DeepSeek, Claude, Qwen, etc."""

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, context: str) -> str:
        import requests
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": context},
            ],
            "max_tokens": 3000,
            "temperature": 0.4,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(self.API_URL, json=payload, headers=headers, timeout=90)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


# ── LECTURE DES PATTERNS DEPUIS TEAM.DB ─────────────────────────────

def load_patterns(days: int = 14) -> dict[str, list[str]]:
    """Lit les patterns depuis retro_patterns dans team.db."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        cutoff = (date.today() - timedelta(days=days)).isoformat()
        c.execute(
            """SELECT pattern_type, content FROM retro_patterns
               WHERE date >= ? AND resolved_at IS NULL
               ORDER BY date DESC""",
            (cutoff,),
        )
        rows = c.fetchall()
        conn.close()

        patterns: dict[str, list[str]] = defaultdict(list)
        for ptype, content in rows:
            if content and content.strip():
                patterns[ptype].append(content.strip())

        return dict(patterns)
    except (OSError, sqlite3.DatabaseError) as exc:
        print(f"[DB] Lecture patterns impossible : {exc}")
        return {}


def load_recommendations(days: int = 30) -> list[str]:
    """Lit les recommandations ouvertes depuis retro_recommendations."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        cutoff = (date.today() - timedelta(days=days)).isoformat()
        c.execute(
            """SELECT content FROM retro_recommendations
               WHERE date >= ? AND status = 'open'
               ORDER BY date DESC""",
            (cutoff,),
        )
        rows = c.fetchall()
        conn.close()
        return [r[0].strip() for r in rows if r[0] and r[0].strip()]
    except (OSError, sqlite3.DatabaseError) as exc:
        print(f"[DB] Lecture recommandations impossible : {exc}")
        return []


def load_existing_skills() -> set[str]:
    """Lit les skills existantes depuis skills/INDEX.md."""
    if not SKILLS_INDEX.is_file():
        return set()

    existing = set()
    content = SKILLS_INDEX.read_text(encoding="utf-8")
    # Extrait les slugs markdown
    for match in re.finditer(r'\[([a-z][a-z0-9_-]+)\]\(', content):
        existing.add(match.group(1).lower())
    # Extrait les noms depuis le frontmatter
    for match in re.finditer(r'name:\s*([a-z][a-z0-9_-]+)', content):
        existing.add(match.group(1).lower())

    # Ajoute les skills multi-plateformes (.agents/, .claude/, .deepseek/)
    for base in [PKA_DIR / ".agents" / "skills",
                 Path.home() / ".claude" / "skills",
                 Path.home() / ".deepseek" / "skills"]:
        if base.is_dir():
            for d in base.iterdir():
                if d.is_dir():
                    existing.add(d.name.lower())

    return existing


# ── CLUSTERING ───────────────────────────────────────────────────────

def similarity(a: str, b: str) -> float:
    """Calcule la similarité entre deux textes courts."""
    return SequenceMatcher(None, a.lower()[:200], b.lower()[:200]).ratio()


def cluster_patterns(patterns: list[str],
                     min_similarity: float = MIN_CLUSTER_SIMILARITY
                     ) -> list[list[str]]:
    """Groupe les patterns par similarité textuelle (clustering simple)."""
    if len(patterns) <= 1:
        return [patterns] if patterns else []

    # Clustering glouton
    clusters = []
    remaining = list(patterns)

    while remaining:
        seed = remaining.pop(0)
        cluster = [seed]
        i = 0
        while i < len(remaining):
            if similarity(seed, remaining[i]) >= min_similarity:
                cluster.append(remaining.pop(i))
            else:
                i += 1
        clusters.append(cluster)

    return clusters


def find_skill_candidates(patterns: dict[str, list[str]],
                          recommendations: list[str],
                          existing_skills: set[str],
                          min_occurrences: int = MIN_PATTERN_OCCURRENCES,
                          ) -> list[dict]:
    """Identifie les clusters de patterns qui justifient une skill candidate."""
    candidates = []

    # 1. Questions récurrentes
    questions = patterns.get("question", []) + patterns.get("recurring_question", [])
    if questions:
        clusters = cluster_patterns(questions)
        for cluster in clusters:
            if len(cluster) >= min_occurrences:
                candidates.append({
                    "type": "question_recurrente",
                    "patterns": cluster,
                    "count": len(cluster),
                    "sample": cluster[0][:200],
                })

    # 2. Échecs récurrents
    failures = patterns.get("failure", [])
    if failures:
        clusters = cluster_patterns(failures)
        for cluster in clusters:
            if len(cluster) >= min_occurrences:
                candidates.append({
                    "type": "echec_recurrent",
                    "patterns": cluster,
                    "count": len(cluster),
                    "sample": cluster[0][:200],
                })

    # 3. Recommandations non résolues
    for rec in recommendations:
        candidates.append({
            "type": "recommandation_ouverte",
            "patterns": [rec],
            "count": 1,
            "sample": rec[:200],
        })

    # Trier par nombre d'occurrences décroissant
    candidates.sort(key=lambda c: c["count"], reverse=True)

    # Limiter à MAX_SKILL_PROPOSALS
    return candidates[:MAX_SKILL_PROPOSALS]


# ── BUILD CONTEXT ────────────────────────────────────────────────────

def build_llm_context(candidates: list[dict],
                      existing_skills: set[str],
                      ) -> str:
    """Construit le contexte envoyé au LLM pour analyse."""
    lines = [
        "## Patterns récurrents détectés dans les sessions PKA",
        f"Date : {date.today().isoformat()}",
        "",
    ]

    for i, cand in enumerate(candidates, 1):
        lines.append(f"### Candidat #{i} — {cand['type']} ({cand['count']} occurrences)")
        lines.append(f"Échantillon : {cand['sample']}")
        if len(cand['patterns']) > 1:
            lines.append(f"Total patterns dans ce cluster : {len(cand['patterns'])}")
        lines.append("")

    lines.append("## Skills PKA existantes (à ne pas dupliquer)")
    for skill_name in sorted(existing_skills):
        lines.append(f"- {skill_name}")
    lines.append("")

    lines.append("## Instructions")
    lines.append("Propose des skills candidates au format ---SKILL---/---END---.")
    lines.append("Si aucun pattern ne justifie une nouvelle skill, réponds 'AUCUNE_SKILL'.")

    return "\n".join(lines)


# ── PARSE LLM OUTPUT ─────────────────────────────────────────────────

def parse_skill_blocks(llm_output: str) -> list[dict]:
    """Parse les blocs ---SKILL---/---END--- du LLM."""
    skills = []
    pattern = re.compile(r'---SKILL---\s*\n(.*?)\n---END---', re.DOTALL)
    for match in pattern.finditer(llm_output):
        block = match.group(1).strip()
        parsed = {}
        current_key = None
        current_value = []

        for line in block.split("\n"):
            if line.startswith("name:"):
                if current_key:
                    parsed[current_key] = "\n".join(current_value).strip()
                current_key = "name"
                current_value = [line.replace("name:", "").strip()]
            elif line.startswith("trigger:"):
                if current_key:
                    parsed[current_key] = "\n".join(current_value).strip()
                current_key = "trigger"
                current_value = [line.replace("trigger:", "").strip()]
            elif line.startswith("description:"):
                if current_key:
                    parsed[current_key] = "\n".join(current_value).strip()
                current_key = "description"
                current_value = [line.replace("description:", "").strip()]
            elif line.startswith("body:") or line.startswith("body: |"):
                if current_key:
                    parsed[current_key] = "\n".join(current_value).strip()
                current_key = "body"
                current_value = [line.replace("body:", "").replace("|", "").strip()]
            else:
                if current_key:
                    current_value.append(line.strip())
                elif line.strip():
                    if "description" in parsed:
                        parsed["description"] += " " + line.strip()

        if current_key and current_value:
            parsed[current_key] = "\n".join(current_value).strip()

        if "body" in parsed:
            parsed["body"] = parsed["body"].lstrip("\n")

        if "name" in parsed and parsed["name"]:
            skills.append(parsed)

    return skills


# ── FORMATEUR SKILL.MD ───────────────────────────────────────────────

SKILL_TEMPLATE = """---
name: {name}
description: {description}
triggers:
  - "{trigger}"
---

# Skill — {name}

> {description}

## Déclencheur
- {trigger}

{body}

---
*Skill auto-générée par pka_skill_generator.py le {date}. En attente de curation par Corbeau et validation Dobby.*
"""


def write_skill_draft(skill: dict, dry_run: bool = False) -> Path | None:
    """Écrit un brouillon SKILL.md dans TEAM_Inbox/."""
    today = date.today().isoformat()
    safe_name = re.sub(r'[^a-z0-9_-]', '-', skill.get("name", "unknown"))
    filename = f"{today}_skill-candidate_{safe_name}.md"
    filepath = TEAM_INBOX / filename

    content = SKILL_TEMPLATE.format(
        name=skill.get("name", "unknown"),
        description=skill.get("description", skill.get("trigger", "")),
        trigger=skill.get("trigger", ""),
        body=skill.get("body", "## Procédure\n\nEn attente de définition détaillée."),
        date=today,
    )

    if dry_run:
        print(f"\n[Dry-run] Serait écrit dans : {filepath}")
        print(f"[Dry-run] Contenu ({len(content)} chars) :")
        print("-" * 60)
        print(content[:500])
        if len(content) > 500:
            print(f"... ({len(content) - 500} chars tronqués)")
        print("-" * 60)
        return None

    filepath.write_text(content, encoding="utf-8")
    print(f"[✓] Skill candidate écrite : {filepath}")
    return filepath


# ── MAIN ─────────────────────────────────────────────────────────────

def get_api_key(provider: str) -> str:
    """Récupère la clé API pour le provider demandé."""
    key_file = SECRETS_DIR / "openrouter_key.txt"
    if key_file.is_file():
        return key_file.read_text().strip()

    # Fallback : api_keys
    keys_file = SECRETS_DIR / "api_keys"
    if keys_file.is_file():
        for line in keys_file.read_text().splitlines():
            if line.startswith("OPENROUTER") or line.startswith("openrouter"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    return parts[1].strip().strip('"').strip("'")

    return ""


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="pka_skill_generator.py — Générateur de skills auto-apprenant PKA"
    )
    parser.add_argument("--days", type=int, default=14,
                        help="Fenêtre d'analyse en jours (défaut: 14)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Extraction locale seulement, pas d'appel LLM ni écriture")
    parser.add_argument("--auto", action="store_true",
                        help="Génère les brouillons SKILL.md dans TEAM_Inbox/")
    parser.add_argument("--provider", type=str, default="openrouter",
                        help="Provider LLM (défaut: openrouter)")
    parser.add_argument("--model", type=str, default="deepseek/deepseek-chat",
                        help="Modèle LLM (défaut: deepseek/deepseek-chat)")
    parser.add_argument("--min-occurrences", type=int, default=MIN_PATTERN_OCCURRENCES,
                        help=f"Occurrences min pour proposer une skill (défaut: {MIN_PATTERN_OCCURRENCES})")
    args = parser.parse_args()

    print("=" * 60)
    print("🦉 pka_skill_generator.py — Générateur de skills auto-apprenant")
    print(f"   Fenêtre : {args.days} jours | Provider : {args.provider} | Modèle : {args.model}")
    print("=" * 60)

    # 1. Charger les patterns
    print(f"\n[1/5] Lecture des patterns depuis team.db (retro_patterns)...")
    patterns = load_patterns(days=args.days)
    total = sum(len(v) for v in patterns.values())
    if total == 0:
        print("       Aucun pattern trouvé dans la période.")
        return
    print(f"       {total} patterns chargés :")
    for ptype, items in sorted(patterns.items()):
        print(f"         - {ptype}: {len(items)}")

    # 2. Charger les recommandations ouvertes
    print(f"\n[2/5] Lecture des recommandations ouvertes...")
    recommendations = load_recommendations(days=max(args.days, 30))
    print(f"       {len(recommendations)} recommandations ouvertes")

    # 3. Charger les skills existantes
    print(f"\n[3/5] Inventaire des skills existantes...")
    existing = load_existing_skills()
    print(f"       {len(existing)} skills recensées")

    # 4. Identifier les candidats
    print(f"\n[4/5] Clustering et identification des candidats...")
    candidates = find_skill_candidates(patterns, recommendations, existing,
                                       min_occurrences=args.min_occurrences)
    if not candidates:
        print("       Aucun cluster ne dépasse le seuil d'occurrences.")
        print("       → Pas de nouvelle skill à proposer pour le moment.")
        return

    print(f"       {len(candidates)} candidat(s) identifié(s) :")
    for c in candidates:
        print(f"         - [{c['type']}] {c['count']} occurrences → \"{c['sample'][:80]}...\"")

    # 5. Analyse LLM
    if args.dry_run:
        print(f"\n[5/5] DRY-RUN — Pas d'appel LLM.")
        context = build_llm_context(candidates, existing)
        print(f"       Contexte préparé : {len(context)} chars")
        print(f"       Serait envoyé à {args.provider}/{args.model}")
        print("\n--- Contexte LLM (début) ---")
        print(context[:800])
        print("...")
        return

    print(f"\n[5/5] Analyse LLM via {args.provider}/{args.model}...")
    api_key = get_api_key(args.provider)
    if not api_key:
        print("       ⚠️  Aucune clé API trouvée. Utilisez --dry-run ou configurez une clé.")
        print(f"       Vérifier : {SECRETS_DIR}/openrouter_key.txt")
        return

    provider = OpenRouterProvider(api_key, args.model)
    context = build_llm_context(candidates, existing)
    print(f"       Contexte : {len(context)} chars envoyés...")

    try:
        llm_output = provider.generate(context)
    except Exception as exc:
        print(f"       ⚠️  Erreur LLM : {exc}")
        print(f"       Fallback : les candidats sont listés ci-dessus, à traiter manuellement.")
        return

    if "AUCUNE_SKILL" in llm_output.upper():
        print("       → Le LLM juge qu'aucune skill n'est justifiée pour le moment.")
        return

    # Parser les skills
    skills = parse_skill_blocks(llm_output)
    if not skills:
        print("       ⚠️  Aucun bloc SKILL valide trouvé dans la réponse LLM.")
        print(f"       Réponse brute ({len(llm_output)} chars) :")
        print(llm_output[:500])
        return

    print(f"       → {len(skills)} skill(s) proposée(s) par le LLM :")
    for s in skills:
        print(f"         - {s.get('name', '?')}: {s.get('description', '?')[:80]}")

    # Écrire les brouillons
    if args.auto:
        print(f"\n--- Écriture des brouillons dans TEAM_Inbox/ ---")
        for skill in skills:
            write_skill_draft(skill, dry_run=False)
        print(f"\n📥 {len(skills)} brouillon(s) dans TEAM_Inbox/ — en attente de curation.")
        print("   Prochaine étape : Corbeau → curation → Dobby → validation → skills/")
    else:
        print(f"\n💡 Mode preview. Pour écrire les brouillons, relance avec --auto")
        for skill in skills:
            write_skill_draft(skill, dry_run=True)


if __name__ == "__main__":
    main()
