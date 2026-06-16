#!/usr/bin/env python3
"""
wildlens_weekly.py — Rapport hebdomadaire WildLens + générateur d'édition.

Deux modes :
  python3 scripts/wildlens_weekly.py report   → rapport d'activité WildLens
  python3 scripts/wildlens_weekly.py edition  → template pour la prochaine édition
  python3 scripts/wildlens_weekly.py stats    → stats Ghost (nécessite ADMIN_API_KEY)

Tourne le dimanche à 10h (launchd com.dobby.wildlens-weekly).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTEON_DIR = ROOT / "JCH_Inbox" / "03_PROJECTS" / "02_ARTEON"
WILDLENS_DIR = ARTEON_DIR / "wildlens"
EDITIONS_DIR = WILDLENS_DIR / "editions"
REPORTS_DIR = WILDLENS_DIR / "reports"

GHOST_API_URL = "https://wildlens.ghost.io/ghost/api/admin"


def list_editions() -> list[Path]:
    """Return all edition files sorted by date."""
    if not EDITIONS_DIR.is_dir():
        return []
    files = sorted(EDITIONS_DIR.glob("WildLens-*.md"))
    return files


def get_edition_number(path: Path) -> int:
    """Extract edition number from filename like WildLens-2026-04-18.md → 1."""
    # Simple: count editions before this one + 1
    editions = list_editions()
    for i, p in enumerate(editions, 1):
        if p == path:
            return i
    return len(editions) + 1


def next_edition_date() -> date:
    """Next Saturday (or today if Saturday)."""
    today = date.today()
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0:
        return today
    return today + timedelta(days=days_until_saturday)


def cmd_report(args):
    """Generate WildLens activity report."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    editions = list_editions()
    today = date.today()
    last_sunday = today - timedelta(days=today.weekday() + 1) if today.weekday() != 6 else today - timedelta(days=7)

    report = f"""# WildLens Weekly Report — {today.isoformat()}

## État de la colonne

- **Éditions publiées :** {len(editions)}
- **Dernière édition :** {editions[-1].name if editions else 'Aucune'}
- **Prochaine édition :** {next_edition_date().isoformat()} (Edition #{len(editions) + 1})
- **Jours depuis dernière publication :** {(today - date.fromisoformat(editions[-1].stem.split('-', 1)[1])).days if editions else '∞'}

## Fichiers d'édition

| # | Date | Fichier |
|---|------|---------|
"""
    for i, p in enumerate(editions, 1):
        dt = p.stem.split('-', 1)[1] if '-' in p.stem else '?'
        size = p.stat().st_size
        report += f"| {i} | {dt} | {p.name} ({size:,} B) |\n"

    report += f"""
## Prochaine édition (Edition #{len(editions) + 1})

- **Date cible :** {next_edition_date().isoformat()}
- **Template :** lancer `python3 scripts/wildlens_weekly.py edition`
- **5 segments requis :** Éditorial · Science · Technique · Competition · Field Assignment

## Ghost Stats

⚠️  Admin API Key non configurée. Pour activer les stats Ghost :
1. Ghost Admin → Settings → Integrations → Add custom integration
2. Copier Admin API Key dans Keychain : `security add-generic-password -s "GHOST_ADMIN_KEY" -a "wildlens" -w "la_clé"`
3. Relancer `python3 scripts/wildlens_weekly.py stats`

## Actions recommandées

"""
    if not editions:
        report += "- [ ] **URGENT** — Aucune édition publiée. La colonne est inactive.\n"
    elif (today - date.fromisoformat(editions[-1].stem.split('-', 1)[1])).days > 14:
        report += f"- [ ] **URGENT** — Dernière édition il y a {(today - date.fromisoformat(editions[-1].stem.split('-', 1)[1])).days} jours. Reprendre la cadence.\n"
    report += f"- [ ] Générer l'édition #{len(editions) + 1} avant {next_edition_date().isoformat()}\n"
    report += "- [ ] Configurer la clé Ghost Admin API pour les stats automatiques\n"
    report += "- [ ] Vérifier que ghost.io est actif (pas de suspension pour inactivité)\n"

    report += f"""
---
*Rapport généré automatiquement par Dobby le {today.isoformat()}*
"""

    out_path = REPORTS_DIR / f"WildLens-weekly-{today.isoformat()}.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"✅ Rapport → {out_path}")
    print(report)


def cmd_edition(args):
    """Generate template for next edition."""
    edition_num = len(list_editions()) + 1
    pub_date = next_edition_date()

    template = f"""# WildLens — Edition #{edition_num}
**Publication :** {pub_date.isoformat()} (Saturday)
**Status :** draft

---

## 1. Éditorial

> *Thème de la semaine — une idée qui relie les 4 sections suivantes.*

<!-- 200-300 mots -->

---

## 2. Science Spotlight

> *Une découverte scientifique récente qui change notre façon de photographier le vivant.*

<!-- 150-250 mots + lien vers le papier -->

---

## 3. Technique Deep-Dive

> *Une technique photo décortiquée — pourquoi elle marche, quand l'utiliser.*

<!-- 200-300 mots + diagramme SVG -->

---

## 4. Competition Frame

> *Une image de concours qui mérite d'être étudiée — ce qu'elle fait bien, ce qu'on peut apprendre.*

<!-- 150-200 mots + image embed -->

---

## 5. Field Assignment

> *Un exercice de terrain pour les lecteurs cette semaine.*

<!-- 100-150 mots + contraintes -->

---

## Notes de publication

- [ ] Texte complet relu
- [ ] Images embed avec crédits
- [ ] Diagramme SVG pour la section Technique
- [ ] Tags Ghost : wildlife-photography, field-technique, science, competition
- [ ] URL canonique : wildlens.ghost.io/edition-{edition_num:03d}

---
*Template généré le {date.today().isoformat()} · Prochaine édition : {pub_date.isoformat()}*
"""

    out_path = EDITIONS_DIR / f"WildLens-{pub_date.isoformat()}.md"
    if out_path.exists():
        print(f"⚠️  Edition #{edition_num} existe déjà : {out_path}")
        return

    EDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(template, encoding="utf-8")
    print(f"📝 Template → {out_path}")
    print(f"   Edition #{edition_num} — publication prévue le {pub_date.isoformat()}")
    print(f"   5 sections à remplir avant samedi")


def cmd_stats(args):
    """Fetch Ghost stats via Admin API."""
    import subprocess

    # Try Keychain
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", "GHOST_ADMIN_KEY", "-w"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            api_key = result.stdout.strip()
        else:
            print("❌ Clé Ghost Admin API non trouvée dans le Keychain.")
            print("   Config : security add-generic-password -s 'GHOST_ADMIN_KEY' -a 'wildlens' -w 'la_clé'")
            sys.exit(1)
    except Exception:
        print("❌ Impossible de lire le Keychain.")
        sys.exit(1)

    # Fetch stats via Ghost Admin API
    import urllib.request
    import urllib.error

    endpoints = {
        "site": f"{GHOST_API_URL}/site/",
        "members": f"{GHOST_API_URL}/members/?limit=1",
        "posts": f"{GHOST_API_URL}/posts/?limit=10&order=published_at%20desc&formats=title,url,published_at",
    }

    print(f"\n📊 WildLens Ghost Stats — {date.today().isoformat()}\n")

    for name, url in endpoints.items():
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Ghost {api_key}")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                if name == "members":
                    print(f"👥 Subscribers : {len(data.get('members', []))} (total; limit=1 query)")
                elif name == "posts":
                    posts = data.get("posts", [])
                    print(f"📝 Posts : {len(posts)} récents")
                    for p in posts[:5]:
                        pub = p.get("published_at", "?")[:10]
                        print(f"   {pub} — {p.get('title', '?')[:60]}")
                elif name == "site":
                    site = data.get("site", {})
                    print(f"🌐 Site : {site.get('title', '?')}")
                    print(f"   URL  : {site.get('url', '?')}")
        except urllib.error.HTTPError as e:
            print(f"⚠️  {name} : HTTP {e.code}")
        except Exception as e:
            print(f"⚠️  {name} : {e}")

    print()

def main():
    parser = argparse.ArgumentParser(description="WildLens Weekly — rapport + générateur d'édition")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("report", help="Rapport d'activité WildLens")
    sub.add_parser("edition", help="Générer le template pour la prochaine édition")
    sub.add_parser("stats", help="Stats Ghost (nécessite ADMIN_API_KEY)")

    args = parser.parse_args()

    if args.command == "report":
        cmd_report(args)
    elif args.command == "edition":
        cmd_edition(args)
    elif args.command == "stats":
        cmd_stats(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
