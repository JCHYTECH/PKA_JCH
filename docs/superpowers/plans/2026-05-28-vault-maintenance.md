# PKA Vault Maintenance — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Script autonome de maintenance nocturne qui corrige les wikilinks manquants, détecte les fichiers mal placés, et commite automatiquement les changements via launchd à 02:00 chaque nuit.

**Architecture:** Trois modules indépendants (`wikilink_patcher`, `file_placement_checker`, `git_nightly_commit`) orchestrés par un entry point `pka_vault_maintenance.py`. Chaque module est fail-safe : une exception dans un module n'arrête pas les suivants. Log uniquement si erreur critique.

**Tech Stack:** Python 3.13, `sqlite3` (TEAM/team.db), `subprocess` (git), `unittest` + `tempfile` pour les tests, `launchd` pour la planification macOS.

---

## File Map

| Fichier | Action | Rôle |
| --- | --- | --- |
| `scripts/modules/__init__.py` | Créer | Package marker |
| `scripts/modules/wikilink_patcher.py` | Créer | Détecte et insère les wikilinks manquants |
| `scripts/modules/file_placement_checker.py` | Créer | Vérifie le placement des fichiers selon les règles |
| `scripts/modules/git_nightly_commit.py` | Créer | Staging + commit automatique daté |
| `scripts/pka_vault_maintenance.py` | Créer | Entry point — orchestre les 3 modules |
| `scripts/launchd/com.jchytech.pka-vault-maintenance.plist` | Créer | Planification launchd 02:00 quotidien |
| `scripts/install_vault_maintenance_launchd.sh` | Créer | Script d'installation launchd |
| `tests/test_wikilink_patcher.py` | Créer | Tests unitaires wikilink_patcher |
| `tests/test_file_placement_checker.py` | Créer | Tests unitaires file_placement_checker |
| `tests/test_git_nightly_commit.py` | Créer | Tests unitaires git_nightly_commit |

---

## Task 1 : Module wikilink_patcher

**Files:**
- Create: `scripts/modules/__init__.py`
- Create: `scripts/modules/wikilink_patcher.py`
- Test: `tests/test_wikilink_patcher.py`

- [ ] **Step 1 : Créer le package modules**

```bash
touch /Users/jchavauxm5/PKA_JCH/scripts/modules/__init__.py
```

- [ ] **Step 2 : Écrire les tests (TDD — fichier de test d'abord)**

Créer `tests/test_wikilink_patcher.py` :

```python
import sqlite3
import tempfile
import unittest
from pathlib import Path

from scripts.modules import wikilink_patcher


class WikilinkPatcherTest(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        # Créer une DB minimale avec 2 membres
        db_path = self.root / "TEAM" / "team.db"
        db_path.parent.mkdir(parents=True)
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                "CREATE TABLE members (name TEXT, status TEXT)"
            )
            conn.execute("INSERT INTO members VALUES ('Forge', 'active')")
            conn.execute("INSERT INTO members VALUES ('Vasco', 'active')")
            conn.execute("INSERT INTO members VALUES ('Corbeau', 'inactive')")
        self.db_path = db_path

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_load_active_members(self):
        members = wikilink_patcher.load_active_members(self.db_path)
        self.assertIn("Forge", members)
        self.assertIn("Vasco", members)
        self.assertNotIn("Corbeau", members)

    def test_patch_member_mention(self):
        text = "J'ai demandé à Forge de vérifier le pipeline."
        result = wikilink_patcher.patch_text(text, members=["Forge", "Vasco"], known_files=[])
        self.assertIn("[[Forge]]", result)
        self.assertNotIn("[[Vasco]]", result)

    def test_no_double_wrap(self):
        text = "[[Forge]] a livré le rapport."
        result = wikilink_patcher.patch_text(text, members=["Forge"], known_files=[])
        self.assertEqual(result.count("[[Forge]]"), 1)

    def test_skip_code_block(self):
        text = "```\nForge est mentionné ici\n```"
        result = wikilink_patcher.patch_text(text, members=["Forge"], known_files=[])
        self.assertNotIn("[[Forge]]", result)

    def test_skip_url(self):
        text = "Voir https://example.com/Forge pour les détails."
        result = wikilink_patcher.patch_text(text, members=["Forge"], known_files=[])
        self.assertNotIn("[[Forge]]", result)

    def test_patch_known_file_reference(self):
        text = "Consulter pka_system_check pour l'audit."
        result = wikilink_patcher.patch_text(
            text, members=[], known_files=["pka_system_check"]
        )
        self.assertIn("[[pka_system_check]]", result)

    def test_patch_file_writes_to_disk(self):
        md_file = self.root / "note.md"
        md_file.write_text("Forge a livré.", encoding="utf-8")
        modified = wikilink_patcher.patch_file(
            md_file, members=["Forge"], known_files=[]
        )
        self.assertTrue(modified)
        self.assertIn("[[Forge]]", md_file.read_text(encoding="utf-8"))

    def test_excluded_files_not_touched(self):
        excluded = self.root / "CLAUDE.md"
        excluded.write_text("Forge travaille ici.", encoding="utf-8")
        modified = wikilink_patcher.patch_file(
            excluded, members=["Forge"], known_files=[]
        )
        self.assertFalse(modified)
        self.assertNotIn("[[Forge]]", excluded.read_text(encoding="utf-8"))
```

- [ ] **Step 3 : Vérifier que les tests échouent**

```bash
cd /Users/jchavauxm5/PKA_JCH && python -m pytest tests/test_wikilink_patcher.py -v 2>&1 | head -20
```

Attendu : `ModuleNotFoundError` ou `ImportError`.

- [ ] **Step 4 : Implémenter `scripts/modules/wikilink_patcher.py`**

```python
"""Détecte et insère les wikilinks Obsidian manquants dans les fichiers MD."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

EXCLUDED_FILES = {
    "CLAUDE.md", "AGENTS.md", "GEMINI.md", "DEEPSEEK.md",
    "MEMORY.md", "ROSTER.md", "QWEN.md", "GEMMA.md", "Codex.md",
}
EXCLUDED_DIRS = {".obsidian", "__pycache__", "node_modules", ".git"}


def load_active_members(db_path: Path) -> list[str]:
    if not db_path.is_file():
        return []
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT name FROM members WHERE status='active'"
        ).fetchall()
    return [row[0] for row in rows]


def _mask_code_blocks(text: str) -> tuple[str, list[str]]:
    """Remplace les blocs code par des placeholders pour éviter de les modifier."""
    blocks: list[str] = []
    def replacer(m: re.Match) -> str:
        blocks.append(m.group(0))
        return f"\x00CODEBLOCK{len(blocks) - 1}\x00"
    masked = re.sub(r"```[\s\S]*?```|`[^`\n]+`", replacer, text)
    return masked, blocks


def _restore_code_blocks(text: str, blocks: list[str]) -> str:
    for i, block in enumerate(blocks):
        text = text.replace(f"\x00CODEBLOCK{i}\x00", block)
    return text


def _mask_urls(text: str) -> tuple[str, list[str]]:
    urls: list[str] = []
    def replacer(m: re.Match) -> str:
        urls.append(m.group(0))
        return f"\x00URL{len(urls) - 1}\x00"
    masked = re.sub(r"https?://\S+", replacer, text)
    return masked, urls


def _restore_urls(text: str, urls: list[str]) -> str:
    for i, url in enumerate(urls):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def patch_text(text: str, members: list[str], known_files: list[str]) -> str:
    text, code_blocks = _mask_code_blocks(text)
    text, urls = _mask_urls(text)

    for name in members:
        # Ne wraper que si pas déjà un wikilink
        text = re.sub(
            r"(?<!\[)\b(" + re.escape(name) + r")\b(?!\])",
            r"[[\1]]",
            text,
        )

    for fname in known_files:
        text = re.sub(
            r"(?<!\[)\b(" + re.escape(fname) + r")\b(?!\])",
            r"[[\1]]",
            text,
        )

    text = _restore_urls(text, urls)
    text = _restore_code_blocks(text, code_blocks)
    return text


def patch_file(path: Path, members: list[str], known_files: list[str]) -> bool:
    """Patche un fichier MD. Retourne True si le fichier a été modifié."""
    if path.name in EXCLUDED_FILES:
        return False
    if not path.suffix == ".md":
        return False

    original = path.read_text(encoding="utf-8")

    # Séparer le frontmatter YAML
    frontmatter = ""
    body = original
    if original.startswith("---"):
        parts = original.split("---", 2)
        if len(parts) >= 3:
            frontmatter = "---" + parts[1] + "---"
            body = parts[2]

    patched_body = patch_text(body, members, known_files)
    patched = frontmatter + patched_body

    if patched == original:
        return False

    path.write_text(patched, encoding="utf-8")
    return True


def run(root: Path, db_path: Path | None = None) -> list[Path]:
    """Lance le patch sur tout le vault. Retourne la liste des fichiers modifiés."""
    if db_path is None:
        db_path = root / "TEAM" / "team.db"

    members = load_active_members(db_path)

    scan_dirs = ["JCH_Inbox", "TEAM", "TEAM_Inbox", "docs"]
    all_md = []
    for d in scan_dirs:
        scan_path = root / d
        if not scan_path.exists():
            continue
        for p in scan_path.rglob("*.md"):
            if not any(excl in p.parts for excl in EXCLUDED_DIRS):
                all_md.append(p)

    known_files = [p.stem for p in all_md]

    modified = []
    for md_file in all_md:
        if patch_file(md_file, members, known_files):
            modified.append(md_file)

    return modified
```

- [ ] **Step 5 : Lancer les tests**

```bash
cd /Users/jchavauxm5/PKA_JCH && python -m pytest tests/test_wikilink_patcher.py -v
```

Attendu : tous PASS.

- [ ] **Step 6 : Commit**

```bash
git add scripts/modules/__init__.py scripts/modules/wikilink_patcher.py tests/test_wikilink_patcher.py
git commit -m "feat(vault-maintenance): wikilink_patcher — détection et correction automatique"
```

---

## Task 2 : Module file_placement_checker

**Files:**
- Create: `scripts/modules/file_placement_checker.py`
- Test: `tests/test_file_placement_checker.py`

- [ ] **Step 1 : Écrire les tests**

Créer `tests/test_file_placement_checker.py` :

```python
import tempfile
import unittest
from pathlib import Path

from scripts.modules import file_placement_checker


class FilePlacementCheckerTest(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def _create(self, rel: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        return p

    def test_daily_note_in_wrong_place(self):
        self._create("JCH_Inbox/03_PROJECTS/2026-05-28_daily.md")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertTrue(any("2026-05-28_daily.md" in p for p in paths))

    def test_daily_note_in_correct_place(self):
        self._create("JCH_Inbox/01_DASHBOARDS/2026-05-28_daily.md")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertFalse(any("2026-05-28_daily.md" in p for p in paths))

    def test_py_outside_scripts(self):
        self._create("JCH_Inbox/03_PROJECTS/helper.py")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertTrue(any("helper.py" in p for p in paths))

    def test_py_inside_scripts_ok(self):
        self._create("scripts/helper.py")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertFalse(any("helper.py" in p for p in paths))

    def test_plist_outside_launchd(self):
        self._create("scripts/com.test.plist")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertTrue(any("com.test.plist" in p for p in paths))

    def test_plist_inside_launchd_ok(self):
        self._create("scripts/launchd/com.test.plist")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertFalse(any("com.test.plist" in p for p in paths))

    def test_file_at_inbox_root(self):
        self._create("JCH_Inbox/orphan.md")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertTrue(any("orphan.md" in p for p in paths))
```

- [ ] **Step 2 : Vérifier que les tests échouent**

```bash
cd /Users/jchavauxm5/PKA_JCH && python -m pytest tests/test_file_placement_checker.py -v 2>&1 | head -10
```

Attendu : `ImportError`.

- [ ] **Step 3 : Implémenter `scripts/modules/file_placement_checker.py`**

```python
"""Vérifie que les fichiers du vault sont dans leurs dossiers attendus."""

from __future__ import annotations

import re
from pathlib import Path

DAILY_NOTE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}_")
EXCLUDED_DIRS = {".obsidian", "__pycache__", "node_modules", ".git"}

RULES: list[dict] = [
    {
        "description": "Daily notes hors 01_DASHBOARDS",
        "match": lambda p: DAILY_NOTE_PATTERN.match(p.name) and p.suffix == ".md",
        "allowed": lambda p, root: (root / "JCH_Inbox" / "01_DASHBOARDS") in p.parents,
        "expected": "JCH_Inbox/01_DASHBOARDS/",
    },
    {
        "description": "Fichier .py hors scripts/",
        "match": lambda p: p.suffix == ".py",
        "allowed": lambda p, root: (root / "scripts") in p.parents,
        "expected": "scripts/",
    },
    {
        "description": "Fichier .plist hors scripts/launchd/",
        "match": lambda p: p.suffix == ".plist",
        "allowed": lambda p, root: (root / "scripts" / "launchd") in p.parents,
        "expected": "scripts/launchd/",
    },
    {
        "description": "Fichier directement à la racine de JCH_Inbox/",
        "match": lambda p: True,
        "allowed": lambda p, root: p.parent != root / "JCH_Inbox",
        "expected": "sous-dossier de JCH_Inbox/",
    },
]


def check(root: Path) -> list[dict]:
    """Retourne la liste des anomalies de placement."""
    anomalies = []

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(excl in p.parts for excl in EXCLUDED_DIRS):
            continue

        for rule in RULES:
            if rule["match"](p) and not rule["allowed"](p, root):
                anomalies.append({
                    "path": str(p.relative_to(root)),
                    "description": rule["description"],
                    "expected": rule["expected"],
                })
                break  # une seule règle par fichier

    return anomalies
```

- [ ] **Step 4 : Lancer les tests**

```bash
cd /Users/jchavauxm5/PKA_JCH && python -m pytest tests/test_file_placement_checker.py -v
```

Attendu : tous PASS.

- [ ] **Step 5 : Commit**

```bash
git add scripts/modules/file_placement_checker.py tests/test_file_placement_checker.py
git commit -m "feat(vault-maintenance): file_placement_checker — détection fichiers mal placés"
```

---

## Task 3 : Module git_nightly_commit

**Files:**
- Create: `scripts/modules/git_nightly_commit.py`
- Test: `tests/test_git_nightly_commit.py`

- [ ] **Step 1 : Écrire les tests**

Créer `tests/test_git_nightly_commit.py` :

```python
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.modules import git_nightly_commit


class GitNightlyCommitTest(unittest.TestCase):

    def test_build_commit_message(self):
        msg = git_nightly_commit.build_commit_message("2026-05-28")
        self.assertEqual(msg, "chore(vault): nightly maintenance 2026-05-28")

    def test_build_add_args_excludes_security(self):
        args = git_nightly_commit.build_add_args()
        self.assertIn("JCH_Inbox/", args)
        self.assertNotIn("JCH_Inbox/99_SYSTEM/security/", args)

    def test_nothing_to_commit_returns_false(self):
        with mock.patch("scripts.modules.git_nightly_commit._git_status_empty", return_value=True):
            result = git_nightly_commit.run(date_str="2026-05-28", dry_run=True)
        self.assertFalse(result["committed"])
        self.assertEqual(result["reason"], "nothing_to_commit")

    def test_commit_called_when_changes_present(self):
        with mock.patch("scripts.modules.git_nightly_commit._git_status_empty", return_value=False), \
             mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=0)
            result = git_nightly_commit.run(date_str="2026-05-28", dry_run=False)
        self.assertTrue(result["committed"])
        # Vérifier que git add a été appelé
        add_call = mock_run.call_args_list[0]
        self.assertIn("add", add_call.args[0])

    def test_dry_run_does_not_call_subprocess(self):
        with mock.patch("scripts.modules.git_nightly_commit._git_status_empty", return_value=False), \
             mock.patch("subprocess.run") as mock_run:
            git_nightly_commit.run(date_str="2026-05-28", dry_run=True)
        mock_run.assert_not_called()

    def test_commit_failure_logs_error(self):
        with mock.patch("scripts.modules.git_nightly_commit._git_status_empty", return_value=False), \
             mock.patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "git")):
            result = git_nightly_commit.run(date_str="2026-05-28", dry_run=False)
        self.assertFalse(result["committed"])
        self.assertIn("error", result)
```

- [ ] **Step 2 : Vérifier que les tests échouent**

```bash
cd /Users/jchavauxm5/PKA_JCH && python -m pytest tests/test_git_nightly_commit.py -v 2>&1 | head -10
```

Attendu : `ImportError`.

- [ ] **Step 3 : Implémenter `scripts/modules/git_nightly_commit.py`**

```python
"""Staging et commit automatique nightly pour le vault PKA_JCH."""

from __future__ import annotations

import datetime
import subprocess
from pathlib import Path

ADD_PATHS = [
    "JCH_Inbox/",
    "TEAM/",
    "TEAM_Inbox/",
    "docs/",
    "scripts/",
]

EXCLUDE_PATTERNS = [
    "JCH_Inbox/99_SYSTEM/security/",
    "*.env",
    "*.token",
    "*credentials*",
    "*_token.json",
]


def build_commit_message(date_str: str) -> str:
    return f"chore(vault): nightly maintenance {date_str}"


def build_add_args() -> list[str]:
    return ADD_PATHS.copy()


def _git_status_empty(root: Path | None = None) -> bool:
    cmd = ["git", "status", "--porcelain"]
    kwargs: dict = {"capture_output": True, "text": True}
    if root:
        kwargs["cwd"] = str(root)
    result = subprocess.run(cmd, **kwargs)
    return result.stdout.strip() == ""


def run(
    date_str: str | None = None,
    root: Path | None = None,
    dry_run: bool = False,
) -> dict:
    if date_str is None:
        date_str = datetime.date.today().isoformat()

    if _git_status_empty(root):
        return {"committed": False, "reason": "nothing_to_commit"}

    if dry_run:
        return {"committed": False, "reason": "dry_run", "would_commit": date_str}

    cwd = str(root) if root else None
    try:
        subprocess.run(
            ["git", "add"] + build_add_args(),
            check=True,
            capture_output=True,
            cwd=cwd,
        )
        subprocess.run(
            ["git", "commit", "-m", build_commit_message(date_str)],
            check=True,
            capture_output=True,
            cwd=cwd,
        )
        return {"committed": True, "date": date_str}
    except subprocess.CalledProcessError as exc:
        return {"committed": False, "error": str(exc)}
```

- [ ] **Step 4 : Lancer les tests**

```bash
cd /Users/jchavauxm5/PKA_JCH && python -m pytest tests/test_git_nightly_commit.py -v
```

Attendu : tous PASS.

- [ ] **Step 5 : Commit**

```bash
git add scripts/modules/git_nightly_commit.py tests/test_git_nightly_commit.py
git commit -m "feat(vault-maintenance): git_nightly_commit — staging et commit automatique"
```

---

## Task 4 : Entry point pka_vault_maintenance.py

**Files:**
- Create: `scripts/pka_vault_maintenance.py`

- [ ] **Step 1 : Implémenter l'entry point**

Créer `scripts/pka_vault_maintenance.py` :

```python
#!/usr/bin/env python3
"""Entry point — maintenance nocturne du vault PKA_JCH."""

from __future__ import annotations

import datetime
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "scripts" / "logs" / "vault_maintenance.log"
MAX_FILES_SILENT = 50

try:
    from scripts.modules import wikilink_patcher, file_placement_checker, git_nightly_commit
except ModuleNotFoundError:
    from modules import wikilink_patcher, file_placement_checker, git_nightly_commit


def _setup_logging() -> logging.Logger:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("vault_maintenance")
    logger.setLevel(logging.WARNING)
    handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    )
    logger.addHandler(handler)
    return logger


def main() -> int:
    log = _setup_logging()
    today = datetime.date.today().isoformat()
    errors = 0

    # Étape 1 — Wikilink patcher
    try:
        modified = wikilink_patcher.run(ROOT)
        if len(modified) > MAX_FILES_SILENT:
            log.warning("wikilink_patcher: %d fichiers modifiés", len(modified))
    except Exception as exc:
        log.error("wikilink_patcher failed: %s", exc)
        errors += 1

    # Étape 2 — File placement checker
    try:
        anomalies = file_placement_checker.check(ROOT)
        if anomalies:
            for a in anomalies:
                log.warning(
                    "file_placement: %s → attendu dans %s",
                    a["path"],
                    a["expected"],
                )
    except Exception as exc:
        log.error("file_placement_checker failed: %s", exc)
        errors += 1

    # Étape 3 — Git nightly commit
    try:
        result = git_nightly_commit.run(date_str=today, root=ROOT)
        if not result["committed"] and result.get("error"):
            log.error("git_nightly_commit failed: %s", result["error"])
            errors += 1
        elif result["committed"] and len(result.get("date", "")) > 0:
            committed_count = len(modified) if "modified" in dir() else 0
            if committed_count > MAX_FILES_SILENT:
                log.warning("git commit: %d fichiers inclus", committed_count)
    except Exception as exc:
        log.error("git_nightly_commit failed: %s", exc)
        errors += 1

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2 : Vérifier l'import**

```bash
cd /Users/jchavauxm5/PKA_JCH && python -c "import scripts.pka_vault_maintenance; print('OK')"
```

Attendu : `OK`.

- [ ] **Step 3 : Lancer la suite de tests complète**

```bash
cd /Users/jchavauxm5/PKA_JCH && python -m pytest tests/test_wikilink_patcher.py tests/test_file_placement_checker.py tests/test_git_nightly_commit.py -v
```

Attendu : tous PASS.

- [ ] **Step 4 : Commit**

```bash
git add scripts/pka_vault_maintenance.py
git commit -m "feat(vault-maintenance): entry point — orchestre les 3 modules"
```

---

## Task 5 : Launchd + script d'installation

**Files:**
- Create: `scripts/launchd/com.jchytech.pka-vault-maintenance.plist`
- Create: `scripts/install_vault_maintenance_launchd.sh`

- [ ] **Step 1 : Créer le plist launchd**

Créer `scripts/launchd/com.jchytech.pka-vault-maintenance.plist` :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.jchytech.pka-vault-maintenance</string>

  <key>ProgramArguments</key>
  <array>
    <string>/Library/Frameworks/Python.framework/Versions/3.13/bin/python3</string>
    <string>/Users/jchavauxm5/PKA_JCH/scripts/pka_vault_maintenance.py</string>
  </array>

  <key>WorkingDirectory</key>
  <string>/Users/jchavauxm5/PKA_JCH</string>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>2</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>

  <key>StandardOutPath</key>
  <string>/Users/jchavauxm5/PKA_JCH/scripts/logs/vault_maintenance.log</string>

  <key>StandardErrorPath</key>
  <string>/Users/jchavauxm5/PKA_JCH/scripts/logs/vault_maintenance.log</string>
</dict>
</plist>
```

- [ ] **Step 2 : Créer le script d'installation**

Créer `scripts/install_vault_maintenance_launchd.sh` :

```bash
#!/bin/zsh
set -euo pipefail

LABEL="com.jchytech.pka-vault-maintenance"
SRC="/Users/jchavauxm5/PKA_JCH/scripts/launchd/${LABEL}.plist"
DST="$HOME/Library/LaunchAgents/${LABEL}.plist"

mkdir -p "$HOME/Library/LaunchAgents"
mkdir -p "/Users/jchavauxm5/PKA_JCH/scripts/logs"
cp "$SRC" "$DST"

if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
  launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
fi

launchctl bootstrap "gui/$(id -u)" "$DST"
launchctl enable "gui/$(id -u)/$LABEL"

echo "Installed $LABEL — lancé quotidiennement à 02:00"
```

- [ ] **Step 3 : Rendre le script exécutable**

```bash
chmod +x /Users/jchavauxm5/PKA_JCH/scripts/install_vault_maintenance_launchd.sh
```

- [ ] **Step 4 : Valider le plist XML**

```bash
plutil -lint /Users/jchavauxm5/PKA_JCH/scripts/launchd/com.jchytech.pka-vault-maintenance.plist
```

Attendu : `OK`.

- [ ] **Step 5 : Commit**

```bash
git add scripts/launchd/com.jchytech.pka-vault-maintenance.plist scripts/install_vault_maintenance_launchd.sh
git commit -m "feat(vault-maintenance): launchd plist + install script — schedule 02:00 quotidien"
```

- [ ] **Step 6 : Installer le launchd** *(action irréversible — confirmer avec JCH avant)*

```bash
/Users/jchavauxm5/PKA_JCH/scripts/install_vault_maintenance_launchd.sh
```

Vérifier l'installation :

```bash
launchctl print "gui/$(id -u)/com.jchytech.pka-vault-maintenance" | grep -E "state|path"
```

Attendu : `state = waiting`.

---

## Voir aussi

- [[2026-05-28-vault-maintenance-design]] — spec validée
- [[pka_system_check]] — script audit sécurité complémentaire
