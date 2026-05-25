#!/usr/bin/env python3
"""Build the first Obsidian knowledge graph indexes for PKA_JCH."""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/obsidian-knowledge-graph"
INDEX_DIR = OUTPUT_DIR / "indexes"

TECHNOLOGY_TERMS = [
    "Arduino",
    "BirdNET",
    "ChatGPT",
    "Claude",
    "Codex",
    "Docker",
    "ESP32",
    "ESP32-S3",
    "FastAPI",
    "Git",
    "Graphify",
    "LoRa",
    "n8n",
    "Obsidian",
    "PostgreSQL",
    "Qdrant",
    "Raspberry Pi",
    "Raspberry Pi 5",
    "Redis",
    "SQLite",
    "Tailscale",
    "Whisper",
    "Xeno-Canto",
]

AGENT_NAMES = [
    "Dobby",
    "Bouvier",
    "Furet",
    "Castor",
    "Corbeau",
    "Delphi",
    "Heron",
    "Héron",
    "Lynx",
    "Jade",
    "Renard",
    "Iris",
    "Forge",
    "Ariane",
    "Bruno",
    "Sybil",
    "Clio",
    "Sigma",
    "Vega",
    "Trace",
    "Miel",
    "Vasco",
    "Nova",
    "Argus",
    "Pie",
    "Chouette",
    "Milan",
    "Atlas",
    "Hermine",
]

AMBIGUOUS_TERMS = {
    "Claude": "Ambiguous runtime or model reference",
    "ChatGPT": "Ambiguous runtime or product reference",
    "Python": "Ambiguous language, script, or runtime reference",
    "Apple": "Ambiguous company, device, or ecosystem reference",
    "Pi": "Ambiguous shorthand; prefer Raspberry Pi 5 when intended",
}

SKIP_PARTS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "03_AUDIO_DOWNLOADS",
}

GENERATED_OUTPUT_NAMES = {"knowledge_dictionary.md", "review_queue.md"}
@dataclass(frozen=True)
class NoteRecord:
    path: Path
    title: str
    note_type: str = ""
    status: str = ""
    aliases: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    folder: str = ""


@dataclass
class Inventory:
    root: Path
    notes: list[NoteRecord]
    projects: dict[str, list[NoteRecord]]
    agents: dict[str, list[NoteRecord]]
    technologies: dict[str, list[NoteRecord]]
    ambiguous_terms: dict[str, list[NoteRecord]]


@dataclass(frozen=True)
class WikilinkSuggestion:
    note_path: Path
    line_number: int
    terms: list[str]
    original: str
    proposed: str


def should_scan(path: Path) -> bool:
    parts = path.parts
    if "obsidian-knowledge-graph" in parts:
        graph_index = parts.index("obsidian-knowledge-graph")
        if len(parts) > graph_index + 1 and parts[graph_index + 1] == "indexes":
            return False
        if path.name in GENERATED_OUTPUT_NAMES or path.name.startswith("wikilink_dry_run"):
            return False
    return (
        path.suffix.lower() == ".md"
        and not any(part in SKIP_PARTS for part in parts)
        and not any(part.startswith(".") for part in parts)
    )


def parse_scalar_list(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("\"'") for item in value[1:-1].split(",") if item.strip()]
    return [value.strip().strip("\"'")]


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text

    raw = text[4:end].strip("\n")
    body = text[end + 4 :].lstrip("\n")
    data: dict[str, object] = {}
    current_key = ""

    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, [])
            value = line[4:].strip().strip("\"'")
            if isinstance(data[current_key], list):
                data[current_key].append(value)
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        data[current_key] = parse_scalar_list(value) if current_key in {"aliases", "tags"} else value.strip().strip("\"'")

    return data, body


def title_from_body(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def read_note(root: Path, path: Path) -> NoteRecord:
    text = path.read_text(encoding="utf-8", errors="ignore")
    frontmatter, body = parse_frontmatter(text)
    rel = path.relative_to(root)
    title = str(frontmatter.get("title") or title_from_body(path, body))
    aliases = frontmatter.get("aliases", [])
    tags = frontmatter.get("tags", [])
    return NoteRecord(
        path=rel,
        title=title,
        note_type=str(frontmatter.get("type", "")),
        status=str(frontmatter.get("status", "")),
        aliases=list(aliases) if isinstance(aliases, list) else parse_scalar_list(str(aliases)),
        tags=list(tags) if isinstance(tags, list) else parse_scalar_list(str(tags)),
        folder=str(rel.parent),
    )


def term_in_note(term: str, note: NoteRecord, body_cache: dict[Path, str], root: Path) -> bool:
    if term.lower() in note.title.lower():
        return True
    text = body_cache.get(note.path)
    if text is None:
        text = (root / note.path).read_text(encoding="utf-8", errors="ignore")
        body_cache[note.path] = text
    pattern = r"(?<![\w-])" + re.escape(term) + r"(?![\w-])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def project_name_for(note: NoteRecord) -> str | None:
    parts = note.path.parts
    if len(parts) >= 3 and parts[0] == "JCH_Inbox" and parts[1] == "03_PROJECTS":
        return parts[2]
    if note.note_type.lower() in {"project", "projet"}:
        return note.title
    return None


def build_inventory(root: Path = PROJECT_ROOT) -> Inventory:
    root = root.resolve()
    md_files = sorted(path for path in root.rglob("*.md") if should_scan(path.relative_to(root)))
    notes = [read_note(root, path) for path in md_files]

    projects: dict[str, list[NoteRecord]] = defaultdict(list)
    for note in notes:
        project = project_name_for(note)
        if project:
            projects[project].append(note)

    body_cache: dict[Path, str] = {}
    agents: dict[str, list[NoteRecord]] = defaultdict(list)
    technologies: dict[str, list[NoteRecord]] = defaultdict(list)
    ambiguous: dict[str, list[NoteRecord]] = defaultdict(list)

    for note in notes:
        for agent in AGENT_NAMES:
            if term_in_note(agent, note, body_cache, root):
                agents[agent].append(note)
        for term in TECHNOLOGY_TERMS:
            if term_in_note(term, note, body_cache, root):
                technologies[term].append(note)
        for term in AMBIGUOUS_TERMS:
            if term_in_note(term, note, body_cache, root):
                ambiguous[term].append(note)

    return Inventory(
        root=root,
        notes=notes,
        projects=dict(sorted(projects.items())),
        agents=dict(sorted(agents.items())),
        technologies=dict(sorted(technologies.items())),
        ambiguous_terms=dict(sorted(ambiguous.items())),
    )


def header(title: str) -> list[str]:
    return [
        "---",
        f"date: {date.today().isoformat()}",
        "model: GPT-5 Codex",
        "type: index",
        "status: generated",
        "---",
        "",
        f"# {title}",
        "",
        "> Generated inventory. Do not edit by hand; update the scanner and regenerate.",
        "",
    ]


def render_note_index(inventory: Inventory) -> str:
    lines = header("Note Index")
    lines.extend(["| Title | Type | Status | Tags | Path |", "|---|---|---|---|---|"])
    for note in inventory.notes:
        tags = ", ".join(note.tags)
        lines.append(f"| {note.title} | {note.note_type} | {note.status} | {tags} | `{note.path}` |")
    lines.append("")
    return "\n".join(lines)


def render_project_index(inventory: Inventory) -> str:
    lines = header("Project Index")
    lines.extend(["| Project | Notes | Representative Paths |", "|---|---:|---|"])
    for project, notes in inventory.projects.items():
        paths = "<br>".join(f"`{note.path}`" for note in notes[:5])
        lines.append(f"| {project} | {len(notes)} | {paths} |")
    lines.append("")
    return "\n".join(lines)


def render_agent_index(inventory: Inventory) -> str:
    lines = header("Agent Index")
    lines.extend(["| Agent | Mentions | Representative Paths |", "|---|---:|---|"])
    for agent, notes in inventory.agents.items():
        paths = "<br>".join(f"`{note.path}`" for note in notes[:8])
        lines.append(f"| {agent} | {len(notes)} | {paths} |")
    lines.append("")
    return "\n".join(lines)


def render_technology_index(inventory: Inventory) -> str:
    lines = header("Technology Index")
    lines.extend(["| Technology | Mentions | Representative Paths |", "|---|---:|---|"])
    for term, notes in inventory.technologies.items():
        paths = "<br>".join(f"`{note.path}`" for note in notes[:8])
        lines.append(f"| {term} | {len(notes)} | {paths} |")
    lines.append("")
    return "\n".join(lines)


def representative_folder(name: str, category: str, notes: list[NoteRecord]) -> str:
    if not notes:
        return ""

    if category == "agent":
        if any(note.folder == "TEAM" for note in notes):
            return "TEAM"
        for note in notes:
            if note.folder.startswith("TEAM_Inbox"):
                return note.folder

    if category == "project":
        for note in notes:
            if project_name_for(note) == name and len(note.path.parts) >= 3:
                return "/".join(note.path.parts[:3])

    stable_folders = [
        note.folder
        for note in notes
        if note.folder and note.folder != "." and not note.folder.startswith("wiki/Daily")
    ]
    folders = Counter(stable_folders or [note.folder for note in notes])
    return folders.most_common(1)[0][0]


def render_knowledge_dictionary(inventory: Inventory) -> str:
    lines = [
        "---",
        f"date: {date.today().isoformat()}",
        "model: GPT-5 Codex",
        "type: dictionary",
        "status: draft",
        "---",
        "",
        "# Knowledge Dictionary",
        "",
        "> Draft dictionary for JCH validation before automated wikilinking.",
        "",
    ]

    entries: list[tuple[str, str, list[NoteRecord]]] = []
    entries.extend((project, "project", notes) for project, notes in inventory.projects.items())
    entries.extend((agent, "agent", notes) for agent, notes in inventory.agents.items())
    entries.extend((term, "technology", notes) for term, notes in inventory.technologies.items())

    seen: set[str] = set()
    for name, category, notes in sorted(entries, key=lambda item: (item[1], item[0].lower())):
        key = f"{category}:{name}"
        if key in seen:
            continue
        seen.add(key)
        folder = representative_folder(name, category, notes)
        lines.extend(
            [
                f"## {name}",
                "",
                f"- canonical: {name}",
                "- aliases:",
                f"  - {name}",
                f"- category: {category}",
                f"- folder: `{folder}`",
                "- ambiguity: none recorded",
                "",
            ]
        )
    return "\n".join(lines)


def render_review_queue(inventory: Inventory) -> str:
    lines = [
        "---",
        f"date: {date.today().isoformat()}",
        "model: GPT-5 Codex",
        "type: review-queue",
        "status: generated",
        "---",
        "",
        "# Review Queue",
        "",
        "> Ambiguous candidates. Do not wikilink these automatically.",
        "",
    ]
    if not inventory.ambiguous_terms:
        lines.extend(["No ambiguous candidates detected.", ""])
        return "\n".join(lines)

    for term, notes in inventory.ambiguous_terms.items():
        reason = AMBIGUOUS_TERMS[term]
        paths = "\n".join(f"  - `{note.path}`" for note in notes[:10])
        lines.extend(
            [
                f"## {term}",
                "",
                f"- reason: {reason}",
                "- candidate paths:",
                paths,
                "- decision:",
                "",
            ]
        )
    return "\n".join(lines)


def linkable_terms(inventory: Inventory) -> list[str]:
    terms = set(inventory.projects) | set(inventory.agents) | set(inventory.technologies)
    terms -= set(AMBIGUOUS_TERMS)
    return sorted(terms, key=lambda term: (-len(term), term.lower()))


def wiki_link_spans(line: str) -> list[tuple[int, int]]:
    return [(match.start(), match.end()) for match in re.finditer(r"\[\[[^\]]+\]\]", line)]


def markdown_code_spans(line: str) -> list[tuple[int, int]]:
    return [(match.start(), match.end()) for match in re.finditer(r"`[^`]*`", line)]


def overlaps(start: int, end: int, spans: list[tuple[int, int]]) -> bool:
    return any(start < span_end and end > span_start for span_start, span_end in spans)


def propose_line(line: str, terms: list[str]) -> tuple[str, list[str]]:
    blocked_spans = wiki_link_spans(line) + markdown_code_spans(line)
    replacements: list[tuple[int, int, str]] = []

    for term in terms:
        pattern = r"(?<![\w-])" + re.escape(term) + r"(?![\w-])"
        for match in re.finditer(pattern, line, flags=re.IGNORECASE):
            if overlaps(match.start(), match.end(), blocked_spans):
                continue
            if overlaps(match.start(), match.end(), [(start, end) for start, end, _ in replacements]):
                continue
            replacements.append((match.start(), match.end(), term))

    if not replacements:
        return line, []

    replacements.sort(key=lambda item: item[0])
    chunks: list[str] = []
    cursor = 0
    used_terms: list[str] = []
    for start, end, term in replacements:
        chunks.append(line[cursor:start])
        chunks.append(f"[[{term}]]")
        used_terms.append(term)
        cursor = end
    chunks.append(line[cursor:])
    return "".join(chunks), used_terms


def is_wikilink_dry_run_candidate(note: NoteRecord) -> bool:
    return len(note.path.parts) > 1


def propose_wikilinks(inventory: Inventory, max_files: int = 5) -> list[WikilinkSuggestion]:
    terms = linkable_terms(inventory)
    suggestions: list[WikilinkSuggestion] = []
    files_with_suggestions: set[Path] = set()

    for note in inventory.notes:
        if not is_wikilink_dry_run_candidate(note):
            continue
        if len(files_with_suggestions) >= max_files and note.path not in files_with_suggestions:
            break

        text = (inventory.root / note.path).read_text(encoding="utf-8", errors="ignore")
        in_code_block = False
        note_suggestions: list[WikilinkSuggestion] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            proposed, used_terms = propose_line(line, terms)
            if used_terms:
                note_suggestions.append(
                    WikilinkSuggestion(
                        note_path=note.path,
                        line_number=line_number,
                        terms=used_terms,
                        original=line,
                        proposed=proposed,
                    )
                )

        if note_suggestions:
            files_with_suggestions.add(note.path)
            suggestions.extend(note_suggestions)

    return suggestions


def render_wikilink_dry_run(inventory: Inventory, suggestions: list[WikilinkSuggestion], max_files: int = 5) -> str:
    lines = [
        "---",
        f"date: {date.today().isoformat()}",
        "model: GPT-5 Codex",
        "type: wikilink-dry-run",
        "status: proposal",
        "---",
        "",
        f"# Wikilink Dry Run - {max_files} files",
        "",
        "> Proposal only. No source note has been modified.",
        "",
        f"- scanned notes: {len(inventory.notes)}",
        f"- files with suggestions: {len({suggestion.note_path for suggestion in suggestions})}",
        f"- line suggestions: {len(suggestions)}",
        "",
    ]

    by_file: dict[Path, list[WikilinkSuggestion]] = defaultdict(list)
    for suggestion in suggestions:
        by_file[suggestion.note_path].append(suggestion)

    for note_path, file_suggestions in by_file.items():
        lines.extend([f"## `{note_path}`", ""])
        for suggestion in file_suggestions:
            terms = ", ".join(suggestion.terms)
            lines.extend(
                [
                    f"### Line {suggestion.line_number}",
                    "",
                    f"- terms: {terms}",
                    "- before:",
                    f"  `{suggestion.original}`",
                    "- after:",
                    f"  `{suggestion.proposed}`",
                    "",
                ]
            )

    return "\n".join(lines)


def write_outputs(inventory: Inventory, output_dir: Path = OUTPUT_DIR) -> None:
    index_dir = output_dir / "indexes"
    index_dir.mkdir(parents=True, exist_ok=True)
    (index_dir / "note_index.md").write_text(render_note_index(inventory), encoding="utf-8")
    (index_dir / "project_index.md").write_text(render_project_index(inventory), encoding="utf-8")
    (index_dir / "agent_index.md").write_text(render_agent_index(inventory), encoding="utf-8")
    (index_dir / "technology_index.md").write_text(render_technology_index(inventory), encoding="utf-8")
    (output_dir / "knowledge_dictionary.md").write_text(render_knowledge_dictionary(inventory), encoding="utf-8")
    (output_dir / "review_queue.md").write_text(render_review_queue(inventory), encoding="utf-8")
    suggestions = propose_wikilinks(inventory, max_files=5)
    (output_dir / "wikilink_dry_run_5.md").write_text(render_wikilink_dry_run(inventory, suggestions, max_files=5), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Obsidian knowledge graph inventory files.")
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    inventory = build_inventory(args.root)
    write_outputs(inventory, args.output)
    print(f"notes={len(inventory.notes)} projects={len(inventory.projects)} agents={len(inventory.agents)} technologies={len(inventory.technologies)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
