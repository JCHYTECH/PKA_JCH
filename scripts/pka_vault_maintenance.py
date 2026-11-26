#!/usr/bin/env python3
"""Entry point — maintenance nocturne du vault PKA_JCH.

Étapes:
  1. wikilink_patcher — correction automatique des wikilinks
  2. file_placement_checker — vérification emplacement des fichiers
  3. git_nightly_commit — commit nocturne automatique
  4. dedup_detector — détection de notes en doublon (v0.1 — 2026-07-13)
  5. broken_link_scanner — détection de wikilinks cassés (v0.1 — 2026-07-13)
  6. orphan_detector — détection de notes orphelines (v0.1 — 2026-07-13)

Patterns 4-6 inspirés de « I Replaced Apple Notes With AI » (Sanja, 2026).
"""

from __future__ import annotations

import hashlib
import logging
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # racine du vault
LOG_PATH = ROOT / "scripts" / "logs" / "vault_maintenance.log"
MAX_FILES_SILENT = 50
MAX_ORPHAN_REPORT = 30
WIKILINK_PATTERN = re.compile(r'\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]')

try:
    from scripts.modules import wikilink_patcher, file_placement_checker, git_nightly_commit
except ModuleNotFoundError:
    from modules import wikilink_patcher, file_placement_checker, git_nightly_commit


def find_duplicates(root, log):
    """Détecte les notes en doublon par hash de contenu (hors frontmatter)."""
    seen = {}  # hash → [paths]
    for md_file in root.rglob("*.md"):
        if any(skip in str(md_file) for skip in [".git/", ".quarantine/", "node_modules/", "_local/"]):
            continue
        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
            # Ignorer le frontmatter (entre --- et ---)
            if content.startswith("---"):
                parts = content.split("---", 2)
                body = parts[2] if len(parts) > 2 else content
            else:
                body = content
            h = hashlib.sha256(body.encode()).hexdigest()
            seen.setdefault(h, []).append(str(md_file.relative_to(root)))
        except (IOError, OSError):
            continue

    dups = {h: paths for h, paths in seen.items() if len(paths) > 1}
    if dups:
        log.warning("dedup_detector: %d groupes de doublons détectés", len(dups))
        group_id = 0
        for h, paths in dups.items():
            group_id += 1
            log.warning("  Groupe #%d (%d fichiers):", group_id, len(paths))
            for p in paths[:5]:  # max 5 par groupe
                log.warning("    - %s", p)
    return dups


def find_broken_links(root, log):
    """Détecte les [[wikilinks]] qui pointent vers des fichiers inexistants."""
    # Construire l'index de tous les fichiers .md (sans extension)
    all_files = set()
    for md_file in root.rglob("*.md"):
        if any(skip in str(md_file) for skip in [".git/", ".quarantine/", "node_modules/", "_local/"]):
            continue
        rel = str(md_file.relative_to(root))
        all_files.add(rel)
        all_files.add(rel.replace(".md", ""))  # sans extension

    broken = []
    for md_file in root.rglob("*.md"):
        if any(skip in str(md_file) for skip in [".git/", ".quarantine/", "node_modules/", "_local/"]):
            continue
        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except (IOError, OSError):
            continue

        for match in WIKILINK_PATTERN.finditer(content):
            target = match.group(1).strip()
            target_md = target + ".md" if not target.endswith(".md") else target
            if target not in all_files and target_md not in all_files:
                broken.append({
                    "source": str(md_file.relative_to(root)),
                    "target": target,
                })

    if broken:
        log.warning("broken_link_scanner: %d liens cassés détectés", len(broken))
        for b in broken[:20]:  # max 20 rapportés
            log.warning("  %s → [[%s]]", b["source"], b["target"])
    return broken


def find_orphans(root, log):
    """Détecte les notes sans lien entrant (orphelines)."""
    # Construire le graphe des liens entrants
    incoming = Counter()  # target → count
    all_notes = set()

    for md_file in root.rglob("*.md"):
        if any(skip in str(md_file) for skip in [".git/", ".quarantine/", "node_modules/", "_local/", "archive"]):
            continue
        rel = str(md_file.relative_to(root))
        all_notes.add(rel)

        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except (IOError, OSError):
            continue

        for match in WIKILINK_PATTERN.finditer(content):
            target = match.group(1).strip()
            target_md = target + ".md" if not target.endswith(".md") else target
            incoming[target] += 1
            incoming[target_md] += 1

    orphans = []
    for note in sorted(all_notes):
        # Skip fichiers système et index
        if any(s in note for s in ["INDEX.md", "index.md", "README", "SOUL.md", "USER.md", "MEMORY.md",
                                     "AGENTS.md", "CLAUDE.md", "ADAPTER-PROMPT.md", "BOOTSTRAP.md"]):
            continue
        if note.startswith("JCH_Inbox/00_INBOX/"):
            continue
        if note.startswith("_local/"):
            continue
        note_no_ext = note.replace(".md", "")
        if incoming.get(note, 0) == 0 and incoming.get(note_no_ext, 0) == 0:
            orphans.append(note)

    if orphans:
        log.warning("orphan_detector: %d notes orphelines détectées", len(orphans))
        for o in orphans[:MAX_ORPHAN_REPORT]:
            log.warning("  - %s", o)
        if len(orphans) > MAX_ORPHAN_REPORT:
            log.warning("  ... et %d autres", len(orphans) - MAX_ORPHAN_REPORT)
    return orphans


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(LOG_PATH, encoding="utf-8")],
    )
    log = logging.getLogger(__name__)

    errors = 0
    today = date.today().isoformat()

    # Étape 1 — wikilink_patcher
    try:
        modified = wikilink_patcher.run(ROOT)
        if len(modified) > MAX_FILES_SILENT:
            log.warning("wikilink_patcher: %d fichiers modifiés (> %d)", len(modified), MAX_FILES_SILENT)
    except Exception as exc:
        log.error("wikilink_patcher failed: %s", exc)
        errors += 1

    # Étape 2 — file_placement_checker
    try:
        anomalies = file_placement_checker.check(ROOT)
        for anomaly in anomalies:
            log.warning("file_placement_checker anomaly: path=%s expected=%s", anomaly.get("path"), anomaly.get("expected"))
    except Exception as exc:
        log.error("file_placement_checker failed: %s", exc)
        errors += 1

    # Étape 3 — git_nightly_commit
    try:
        result = git_nightly_commit.run(date_str=today, root=ROOT)
        if result.get("error"):
            log.error("git_nightly_commit error: %s", result["error"])
            errors += 1
    except Exception as exc:
        log.error("git_nightly_commit failed: %s", exc)
        errors += 1

    # Étape 4 — dedup_detector (v0.1)
    try:
        dups = find_duplicates(ROOT, log)
    except Exception as exc:
        log.error("dedup_detector failed: %s", exc)
        errors += 1

    # Étape 5 — broken_link_scanner (v0.1)
    try:
        broken = find_broken_links(ROOT, log)
    except Exception as exc:
        log.error("broken_link_scanner failed: %s", exc)
        errors += 1

    # Étape 6 — orphan_detector (v0.1)
    try:
        orphans = find_orphans(ROOT, log)
    except Exception as exc:
        log.error("orphan_detector failed: %s", exc)
        errors += 1

    return 1 if errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
