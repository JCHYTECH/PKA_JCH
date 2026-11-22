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
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTEON_DIR = ROOT / "JCH_Inbox" / "03_PROJECTS" / "02_ARTEON"
WILDLENS_DIR = ARTEON_DIR / "wildlens"
EDITIONS_DIR = WILDLENS_DIR / "editions"
REPORTS_DIR = WILDLENS_DIR / "reports"
SUGGEST_DIR = WILDLENS_DIR / "suggestions"
THEME_FILE = WILDLENS_DIR / "theme-semaine.md"
THUMB_DIR = ROOT / "PHOTO" / "analyses" / "thumbnails"
VISION_SCAN = ROOT / "scripts" / "pka_vision_scan.py"

GHOST_API_URL = "https://wildlens.arteon.be/ghost/api/admin"


def _frontmatter(path: Path, key: str, default: str = "") -> str:
    """Lit un champ du frontmatter YAML d'une édition (premières ~30 lignes)."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines()[:30]:
            s = line.strip()
            if s.startswith(f"{key}:"):
                return s.split(":", 1)[1].strip()
    except Exception:
        pass
    return default


def _edition_status(path: Path) -> str:
    """Lit le champ `status` du frontmatter d'une édition (défaut : inconnu)."""
    return _frontmatter(path, "status", "inconnu")


def _edition_number(path: Path) -> int:
    """Numéro d'édition depuis le frontmatter `edition:` (défaut : 0)."""
    raw = _frontmatter(path, "edition", "")
    try:
        return int(raw)
    except ValueError:
        return 0


def build_email_summary() -> tuple[str, str]:
    """Construit (sujet, corps) du mail de notification WildLens."""
    editions = list_editions()
    published = [e for e in editions if _edition_status(e) == "published"]
    scheduled = [e for e in editions if _edition_status(e) == "scheduled"]
    nxt = next_edition_date()
    today = date.today()

    lineup = " · ".join(
        f"#{_edition_number(e)} {_edition_status(e)}" for e in editions
    ) or "aucune"

    subject = f"[Dobby] WildLens — rapport hebdo {today.isoformat()}"
    lines = [
        f"WildLens — état de la colonne ({today.isoformat()})",
        "",
        f"• Éditions publiées : {len(published)}",
        f"• Éditions programmées : {len(scheduled)}",
        f"• Prochaine édition : {nxt.isoformat()} (samedi)",
        f"• File : {lineup}",
    ]
    lines += ["", f"Rapport complet : wildlens/reports/WildLens-weekly-{today.isoformat()}.md"]
    return subject, "\n".join(lines)


def _send_summary_email(subject: str, body: str) -> bool:
    """Envoie le mail de notification via Gmail SMTP (best-effort, non bloquant)."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from dobby_notify_email import send_email
        return send_email(subject, body)
    except Exception as e:
        print(f"⚠️  Notification mail non envoyée : {e}", file=sys.stderr)
        return False


def list_editions() -> list[Path]:
    """Retourne les éditions canoniques (editions/final/*.md), triées par numéro."""
    final_dir = EDITIONS_DIR / "final"
    if not final_dir.is_dir():
        return []
    return sorted(final_dir.glob("*.md"), key=_edition_number)


def get_edition_number(path: Path) -> int:
    """Numéro d'édition d'un fichier (frontmatter `edition:`, sinon 0)."""
    return _edition_number(path)


def next_edition_date() -> date:
    """Next Saturday (or today if Saturday)."""
    today = date.today()
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0:
        return today
    return today + timedelta(days=days_until_saturday)


def read_theme() -> str | None:
    """Lit le thème de la semaine depuis theme-semaine.md (première ligne utile)."""
    if not THEME_FILE.exists():
        return None
    for line in THEME_FILE.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and not s.startswith("#") and not s.startswith(">"):
            return s
    return None


def suggest_photo(theme: str) -> str | None:
    """Scanne les vignettes avec un modèle vision pour le thème ; renvoie la sortie."""
    if not THUMB_DIR.is_dir() or not VISION_SCAN.exists():
        return None
    try:
        r = subprocess.run(
            [sys.executable, str(VISION_SCAN), str(THUMB_DIR), theme],
            capture_output=True, text=True, timeout=240)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def cmd_suggest(args) -> None:
    """Suggère une photo pour le thème de la semaine (vision OpenRouter)."""
    theme = args.theme or read_theme()
    if not theme:
        print("Aucun thème — définis-le dans theme-semaine.md ou passe --theme.")
        return
    print(f"Thème : {theme}")
    out = suggest_photo(theme)
    if not out:
        print("Aucune suggestion (vision indisponible ou aucune correspondance).")
        return
    print(out)
    SUGGEST_DIR.mkdir(parents=True, exist_ok=True)
    path = SUGGEST_DIR / f"{date.today().isoformat()}-suggestion.md"
    path.write_text(
        f"# Photo de la semaine — {date.today().isoformat()}\n\n"
        f"**Thème :** {theme}\n\n```\n{out}\n```\n",
        encoding="utf-8")
    print(f"Suggestion → {path}")


def cmd_report(args):
    """Generate WildLens activity report."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    editions = list_editions()
    published = [e for e in editions if _edition_status(e) == "published"]
    scheduled = [e for e in editions if _edition_status(e) == "scheduled"]
    today = date.today()
    nxt = next_edition_date()

    report = f"""# WildLens Weekly Report — {today.isoformat()}

## État de la colonne

- **Éditions publiées :** {len(published)}
- **Éditions programmées :** {len(scheduled)}
- **Prochaine édition :** {nxt.isoformat()} (samedi)

## Fichiers d'édition

| # | Statut | Fichier |
|---|--------|---------|
"""
    for e in editions:
        report += f"| {_edition_number(e)} | {_edition_status(e)} | {e.name} |\n"

    report += f"""
## Prochaine édition

- **Date cible :** {nxt.isoformat()}
- **Structure v2 :** ① Le Cadre · ② Le Virage · ③ L'Objectif · ④ Le Constat (voir `ref/architecture-editoriale-v2.md`)

## Ghost Stats

⚠️  Admin API Key non configurée. Pour activer les stats Ghost :
1. Ghost Admin → Settings → Integrations → Add custom integration
2. Copier Admin API Key dans Keychain : `security add-generic-password -s "GHOST_ADMIN_KEY" -a "wildlens" -w "la_clé"`
3. Relancer `python3 scripts/wildlens_weekly.py stats`

## Actions recommandées

"""
    if not published:
        report += "- [ ] **URGENT** — Aucune édition publiée. Publier l'édition #1.\n"
    elif len(scheduled) < 2:
        report += "- [ ] **Prévoir** — moins de 2 éditions programmées, rédiger la suivante.\n"
    report += f"- [ ] Préparer l'édition de {nxt.isoformat()}\n"
    report += "- [ ] Configurer la clé Ghost Admin API pour les stats automatiques\n"
    report += "- [ ] Vérifier que wildlens.arteon.be est actif (pas de suspension pour inactivité)\n"

    theme = read_theme()
    if theme:
        report += f"\n## Photo de la semaine\n\n**Thème :** {theme}\n\n"
        sugg = suggest_photo(theme)
        report += (sugg + "\n") if sugg else "_(suggestion vision non disponible)_\n"

    report += f"""
---
*Rapport généré automatiquement par Dobby le {today.isoformat()}*
"""

    out_path = REPORTS_DIR / f"WildLens-weekly-{today.isoformat()}.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"✅ Rapport → {out_path}")
    print(report)

    if not getattr(args, "no_email", False):
        subject, body = build_email_summary()
        _send_summary_email(subject, body)


def cmd_edition(args):
    """Génère le template de la prochaine édition (architecture v2 — 4 sections)."""
    edition_num = max([_edition_number(e) for e in list_editions()] or [0]) + 1
    pub_date = next_edition_date()

    template = f"""---
date: {pub_date.isoformat()}
source: editorial-dobby
domain: arteon/blogging
project: WildLens
edition: {edition_num}
tone: militant
status: draft
---
# WildLens — Édition #{edition_num}

> **Thème : « … »** — une phrase qui porte le propos.

**Mots-clés :** …

## ① Le Cadre — (400-600 mots)

*Photo de JC · matériel · © JC Havaux / ARTEON*

…

## ② Le Virage — (200-300 mots)

…

## ③ L'Objectif — (300-400 mots)

…

## ④ Le Constat — (100-150 mots)

…

---
*À publier le {pub_date.isoformat()} (samedi).*
"""

    out_dir = EDITIONS_DIR / "final"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"wildlens-edition-{edition_num}-template.md"
    if out_path.exists():
        print(f"⚠️  Edition #{edition_num} existe déjà : {out_path}")
        return

    out_path.write_text(template, encoding="utf-8")
    print(f"📝 Template → {out_path}")
    print(f"   Edition #{edition_num} — publication prévue le {pub_date.isoformat()}")
    print(f"   4 sections (Cadre · Virage · Objectif · Constat) à remplir avant samedi")


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

def cmd_notify(args):
    """Envoie le mail de notification d'état WildLens (sans régénérer le rapport)."""
    subject, body = build_email_summary()
    print(body)
    if _send_summary_email(subject, body):
        print("✅ Mail envoyé")

def main():
    parser = argparse.ArgumentParser(description="WildLens Weekly — rapport + générateur d'édition")
    sub = parser.add_subparsers(dest="command")

    p_report = sub.add_parser("report", help="Rapport d'activité WildLens (+ photo de la semaine)")
    p_report.add_argument("--no-email", action="store_true", help="Ne pas envoyer le mail de notification")
    sub.add_parser("edition", help="Générer le template pour la prochaine édition")
    sub.add_parser("stats", help="Stats Ghost (nécessite ADMIN_API_KEY)")
    sub.add_parser("notify", help="Envoyer le mail d'état WildLens (sans régénérer le rapport)")
    p_suggest = sub.add_parser("suggest", help="Suggérer une photo pour le thème de la semaine")
    p_suggest.add_argument("--theme", help="Thème (défaut : lit theme-semaine.md)")

    args = parser.parse_args()

    if args.command == "report":
        cmd_report(args)
    elif args.command == "edition":
        cmd_edition(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "notify":
        cmd_notify(args)
    elif args.command == "suggest":
        cmd_suggest(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
