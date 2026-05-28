"""wikilink_patcher — détecte et insère les wikilinks Obsidian manquants."""

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
    """Lit TEAM/team.db → SELECT name FROM members WHERE status='active'."""
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT name FROM members WHERE status='active'"
        ).fetchall()
    return [row[0] for row in rows]


def patch_text(text: str, members: list[str], known_files: list[str]) -> str:
    """Wrappe les mentions de membres et fichiers connus en [[wikilinks]].

    Ne touche pas :
    - blocs code (```...```)
    - code inline entre backticks
    - URLs (https?://)
    - [[wikilinks]] existants
    - frontmatter YAML (bloc --- en début de fichier)
    """
    if not members and not known_files:
        return text

    # Split the text into segments: protected (code blocks, frontmatter, etc.)
    # and processable.
    # Strategy: tokenise into alternating safe/unsafe segments, only process unsafe ones.

    tokens = _tokenise(text)
    terms = sorted(members + known_files, key=len, reverse=True)

    result_parts: list[str] = []
    for segment, is_safe in tokens:
        if is_safe:
            result_parts.append(segment)
        else:
            result_parts.append(_wrap_terms(segment, terms))

    return "".join(result_parts)


def _tokenise(text: str) -> list[tuple[str, bool]]:
    """Split text into (segment, is_safe) pairs.

    Safe segments must not be modified:
    - YAML frontmatter (leading --- block)
    - fenced code blocks (```...```)
    - inline code (`...`)
    - URLs
    - existing [[wikilinks]]
    """
    # Pattern matching safe segments
    safe_pattern = re.compile(
        r"(?P<frontmatter>(?s:\A---\n.*?\n---\n?))"  # YAML frontmatter at start
        r"|(?P<fenced>```[\s\S]*?```)"                # fenced code blocks
        r"|(?P<inline>`[^`\n]+`)"                     # inline code
        r"|(?P<url>https?://\S+)"                     # URLs
        r"|(?P<wikilink>\[\[[^\]]*\]\])",              # existing [[wikilinks]]
        re.MULTILINE,
    )

    tokens: list[tuple[str, bool]] = []
    pos = 0
    for m in safe_pattern.finditer(text):
        start, end = m.span()
        if pos < start:
            tokens.append((text[pos:start], False))
        tokens.append((text[start:end], True))
        pos = end
    if pos < len(text):
        tokens.append((text[pos:], False))

    return tokens


def _wrap_terms(segment: str, terms: list[str]) -> str:
    """Wrap each term occurrence in [[...]] within a processable segment."""
    for term in terms:
        # Match whole word only (word boundary), case-sensitive
        pattern = re.compile(r"(?<!\[)\b" + re.escape(term) + r"\b(?!\])")
        segment = pattern.sub(f"[[{term}]]", segment)
    return segment


def patch_file(path: Path, members: list[str], known_files: list[str]) -> bool:
    """Patche un fichier MD en place. Retourne True si modifié.

    Exclut les fichiers dans EXCLUDED_FILES.
    """
    if path.suffix != ".md":
        return False

    if path.name in EXCLUDED_FILES:
        return False

    original = path.read_text(encoding="utf-8")
    patched = patch_text(original, members, known_files)

    if patched == original:
        return False

    path.write_text(patched, encoding="utf-8")
    return True


def run(root: Path, db_path: Path | None = None) -> list[Path]:
    """Scanne JCH_Inbox/, TEAM/, TEAM_Inbox/, docs/ récursivement.

    Exclut .obsidian/, __pycache__/, node_modules/, .git/.
    Retourne la liste des fichiers modifiés.
    """
    if db_path is None:
        db_path = root / "TEAM" / "team.db"

    members = load_active_members(db_path)

    # Collect known file stems from the scanned directories
    scan_dirs = ["JCH_Inbox", "TEAM", "TEAM_Inbox", "docs"]
    all_md_files: list[Path] = []

    for dir_name in scan_dirs:
        scan_root = root / dir_name
        if not scan_root.exists():
            continue
        for md_file in scan_root.rglob("*.md"):
            # Skip files inside excluded dirs
            if any(part in EXCLUDED_DIRS for part in md_file.parts):
                continue
            all_md_files.append(md_file)

    known_files = [f.stem for f in all_md_files]

    modified: list[Path] = []
    for md_file in all_md_files:
        if patch_file(md_file, members, known_files):
            modified.append(md_file)

    return modified
