#!/usr/bin/env python3
"""
PKA MEMORY.md Generator — régénère MEMORY.md à partir de team.db.

Lit les tables knowledge, retro_patterns, members et produit un MEMORY.md
structuré, lisible par des humains et des LLM.

Usage:
    python3 scripts/pka_generate_memory.py              # régénère MEMORY.md
    python3 scripts/pka_generate_memory.py --dry-run    # affiche sans écrire
    python3 scripts/pka_generate_memory.py --diff       # montre les changements

Part of PKA Memory Layer — docs/system/pka-memory-layer.md
"""

import os
import sqlite3
import sys
from datetime import datetime, timedelta

# ─── Configuration ───────────────────────────────────────────────

PKA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PKA_ROOT, "TEAM", "team.db")
MEMORY_PATH = os.path.join(PKA_ROOT, "MEMORY.md")
DAYS_DECISIONS = 60  # Jours de décisions à inclure
DAYS_FAILURES = 90   # Jours d'échecs à inclure


# ─── Lecture DB ───────────────────────────────────────────────────

def fetch_profile(conn):
    """Lit le profil JCH depuis la table members."""
    row = conn.execute(
        "SELECT name, role, status FROM members WHERE name LIKE '%JCH%' OR name LIKE '%Jean%' LIMIT 1"
    ).fetchone()
    if row:
        return {"name": row[0], "role": row[1], "status": row[2]}
    return None


def fetch_decisions(conn, days=DAYS_DECISIONS):
    """Lit les décisions récentes."""
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = conn.execute(
        """SELECT title, body, created_at, tags
           FROM knowledge
           WHERE type IN ('fact', 'insight')
             AND status = 'active'
             AND created_at >= ?
           ORDER BY created_at DESC
           LIMIT 50""",
        (cutoff,)
    ).fetchall()
    return [{"title": r[0], "body": r[1], "date": r[2], "project": r[3]} for r in rows]


def fetch_facts(conn, days=30):
    """Lit les faits récents."""
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = conn.execute(
        """SELECT title, body, created_at, tags
           FROM knowledge
           WHERE type = 'fact'
             AND status = 'active'
             AND created_at >= ?
           ORDER BY created_at DESC
           LIMIT 30""",
        (cutoff,)
    ).fetchall()
    return [{"title": r[0], "body": r[1], "date": r[2], "project": r[3]} for r in rows]


def fetch_failures(conn, days=DAYS_FAILURES):
    """Lit les échecs/blocages."""
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = conn.execute(
        """SELECT pattern_type, content, date, resolved_at, auto_resolved
           FROM retro_patterns
           WHERE pattern_type IN ('blocker', 'failure', 'échec')
             AND date >= ?
           ORDER BY date DESC
           LIMIT 20""",
        (cutoff,)
    ).fetchall()
    return [{
        "type": r[0], "content": r[1], "date": r[2],
        "resolved": r[3], "auto": r[4]
    } for r in rows]


def fetch_access_info(conn):
    """Lit les informations d'accès technique."""
    rows = conn.execute(
        """SELECT title, body, created_at
           FROM knowledge
           WHERE type IN ('note', 'fact') AND (title LIKE '%accès%' OR title LIKE '%Accès%' OR tags LIKE '%access%')
             AND status = 'active'
           ORDER BY created_at DESC
           LIMIT 20"""
    ).fetchall()
    return [{"title": r[0], "body": r[1], "date": r[2]} for r in rows]


def fetch_feedback(conn, days=30):
    """Lit le feedback récent."""
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = conn.execute(
        """SELECT feedback_type, context, user_response, created_at, incorporated
           FROM dobby_feedback
           WHERE created_at >= ?
           ORDER BY created_at DESC
           LIMIT 20""",
        (cutoff,)
    ).fetchall()
    return [{
        "type": r[0], "context": r[1], "response": r[2],
        "date": r[3], "incorporated": r[4]
    } for r in rows]


def fetch_projects(conn):
    """Détecte les projets actifs depuis knowledge."""
    rows = conn.execute(
        """SELECT DISTINCT tags, COUNT(*) as cnt
           FROM knowledge
           WHERE status = 'active'
             AND tags IS NOT NULL AND tags != ''
           GROUP BY tags
           ORDER BY cnt DESC
           LIMIT 15"""
    ).fetchall()
    return [{"name": r[0], "count": r[1]} for r in rows]


# ─── Génération ───────────────────────────────────────────────────

def generate_markdown(conn):
    """Génère le contenu complet de MEMORY.md."""
    now = datetime.now().strftime("%Y-%m-%d")

    sections = []

    # En-tête
    sections.append(f"""# MEMORY — PKA_JCH
> Miroir portable de la mémoire accumulée par Dobby.
> Généré automatiquement depuis `team.db` — {now}
> Source de vérité : `TEAM/team.db` — ne pas éditer manuellement.

---

## Profil JCH
""")

    # Profil
    profile = fetch_profile(conn)
    if profile:
        sections.append(f"- **Nom :** Jean-Claude Havaux (JC)")
        sections.append(f"- **Statut DB :** {profile['name']} — {profile['role']}")
    else:
        sections.append("- Profil JCH — voir `TEAM/team.db` table `members`")

    sections.append("")

    # Projets actifs
    sections.append("## Projets actifs\n")
    projects = fetch_projects(conn)
    if projects:
        for p in projects:
            sections.append(f"- **{p['name']}** ({p['count']} entrées knowledge)")
    else:
        sections.append("- Aucun projet actif détecté dans knowledge")

    sections.append("")

    # Décisions récentes
    sections.append(f"## Décisions récentes ({DAYS_DECISIONS} jours)\n")
    decisions = fetch_decisions(conn)
    if decisions:
        for d in decisions:
            date = d['date'][:10] if d['date'] else "?"
            proj = f" [{d['project']}]" if d['project'] else ""
            sections.append(f"- [{date}]{proj} : {d['title']}")
            if d['body']:
                sections.append(f"  {d['body'][:200]}")
    else:
        sections.append("- Aucune décision récente dans knowledge")
    sections.append("")

    # Échecs / Blocages
    sections.append(f"## Échecs récents ({DAYS_FAILURES} jours)\n")
    failures = fetch_failures(conn)
    if failures:
        for f in failures:
            status = "✅ résolu" if f['resolved'] else ("🔄 auto-résolu" if f['auto'] else "🔴 ouvert")
            sections.append(f"- [{f['date']}] [{status}] : {f['content'][:200]}")
    else:
        sections.append("- Aucun échec récent dans retro_patterns")
    sections.append("")

    # Feedback Dobby
    sections.append("## Feedback Dobby (30 jours)\n")
    feedback = fetch_feedback(conn)
    if feedback:
        for fb in feedback:
            icon = {"correction": "🔧", "acceptance": "👍", "rejection": "👎", "preference": "💡"}.get(fb['type'], "📝")
            incorp = "✅" if fb['incorporated'] else "⏳"
            sections.append(f"- [{fb['date'][:10]}] {icon} {incorp} {fb['type']}: {fb['response'][:150]}")
    else:
        sections.append("- Aucun feedback récent")
    sections.append("")

    # Accès techniques
    sections.append("## Accès techniques\n")
    access = fetch_access_info(conn)
    if access:
        sections.append("| Service | Accès |")
        sections.append("|---------|-------|")
        for a in access:
            sections.append(f"| {a['title'][:40]} | {a['body'][:80] if a['body'] else '—'} |")
    else:
        sections.append("- Aucune information d'accès dans knowledge")
    sections.append("")

    # Faits récents
    sections.append("## Faits récents (30 jours)\n")
    facts = fetch_facts(conn)
    if facts:
        for f in facts:
            proj = f" [{f['project']}]" if f['project'] else ""
            sections.append(f"- [{f['date'][:10]}]{proj} : {f['title']}")
    else:
        sections.append("- Aucun fait récent")
    sections.append("")

    # Footer
    sections.append("---\n")
    sections.append(f"*Généré par `scripts/pka_generate_memory.py` le {now} — source : `TEAM/team.db`*\n")

    return "\n".join(sections)


# ─── Main ─────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv
    show_diff = "--diff" in sys.argv

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        new_content = generate_markdown(conn)
    finally:
        conn.close()

    if dry_run:
        print(new_content)
    elif show_diff:
        if os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH) as f:
                old = f.read()
            if old == new_content:
                print("✅ Aucun changement — MEMORY.md est à jour.")
            else:
                print(f"📝 Changements détectés ({len(new_content) - len(old)} octets de diff)")
                # Affiche les sections qui ont changé
                old_lines = set(old.split("\n"))
                new_lines = set(new_content.split("\n"))
                added = new_lines - old_lines
                removed = old_lines - new_lines
                if added:
                    print(f"   +{len(added)} lignes ajoutées")
                if removed:
                    print(f"   -{len(removed)} lignes supprimées")
        else:
            print("📄 MEMORY.md n'existe pas encore. Utilisez sans --diff pour le créer.")
    else:
        with open(MEMORY_PATH, "w") as f:
            f.write(new_content)
        print(f"✅ MEMORY.md régénéré ({len(new_content)} caractères)")


if __name__ == "__main__":
    main()
