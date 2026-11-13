#!/usr/bin/env python3
"""Sauvegarde manuelle d'une session PKA.

Equivalent pragmatique du /save Claude : ajoute une section dans la daily note
du jour et une ligne dans wiki/log.md. Peut être utilisé en mode interactif ou
avec arguments.
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


PKA_DIR = Path(__file__).resolve().parents[1]
DAILY_DIR = PKA_DIR / "wiki" / "Daily"
LOG_PATH = PKA_DIR / "wiki" / "log.md"
TEAM_DB = PKA_DIR / "TEAM" / "team.db"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9àâäçéèêëîïôöùûüÿñæœ]+", "-", text, flags=re.IGNORECASE)
    text = text.strip("-")
    return text[:60] or "session"


def prompt_multiline(label: str) -> str:
    print(f"\n{label}")
    print("Termine par une ligne contenant seulement '.'")
    lines: list[str] = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if line.strip() == ".":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def prompt_single(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default or ""


def daily_path(day: datetime, title: str) -> Path:
    dest_dir = DAILY_DIR / day.strftime("%Y") / day.strftime("%m")
    dest_dir.mkdir(parents=True, exist_ok=True)
    return dest_dir / f"{day.strftime('%Y-%m-%d')}-{slugify(title)}.md"


def build_section(
    now: datetime,
    title: str,
    summary: str,
    actions: str,
    decisions: str,
    next_steps: str,
    model: str = "",
    project: str = "",
) -> str:
    parts = [
        f"## Session — {now.strftime('%H:%M')} — {title}",
        "",
    ]
    context = []
    if model:
        context.append(f"- Modèle : {model}")
    if project:
        context.append(f"- Projet : {project}")
    if context:
        parts.extend(["### Contexte", *context, ""])
    parts.extend([
        "### Résumé",
        summary or "- À compléter.",
    ])
    if actions:
        parts.extend(["", "### Actions", actions])
    if decisions:
        parts.extend(["", "### Décisions", decisions])
    if next_steps:
        parts.extend(["", "### Prochaines étapes", next_steps])
    return "\n".join(parts).rstrip() + "\n"


def ensure_daily_file(path: Path, now: datetime, title: str) -> None:
    if path.exists():
        return
    header = "\n".join([
        "---",
        f"date: {now.strftime('%Y-%m-%d')}",
        "tags: [daily, PKA, session]",
        "type: daily",
        "status: active",
        "---",
        "",
        f"# {now.strftime('%Y-%m-%d')} — {title}",
        "",
    ])
    path.write_text(header, encoding="utf-8")


def append_log(now: datetime, title: str, summary: str, path: Path, model: str = "", project: str = "") -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        LOG_PATH.write_text("# Log PKA\n\n---\n", encoding="utf-8")
    one_line = " ".join(summary.split())
    if len(one_line) > 180:
        one_line = one_line[:177].rstrip() + "..."
    rel = path.relative_to(PKA_DIR)
    context = []
    if model:
        context.append(f"model={model}")
    if project:
        context.append(f"project={project}")
    context_text = f" [{' ; '.join(context)}]" if context else ""
    entry = f"\n{now.strftime('%Y-%m-%d %H:%M')} — Save Codex{context_text} : {title} ({one_line}) — `{rel}`\n"
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(entry)


def save_session(args: argparse.Namespace) -> Path:
    now = datetime.now()
    title = args.title
    summary = args.summary
    actions = args.actions
    decisions = args.decisions
    next_steps = args.next_steps
    model = args.model
    project = args.project

    if args.interactive or not title:
        print("Dobby — sauvegarde session PKA")
        title = prompt_single("Titre", title or "session-codex")
        model = prompt_single("Modèle", model)
        project = prompt_single("Projet", project)
        summary = summary or prompt_multiline("Résumé")
        actions = actions or prompt_multiline("Actions réalisées")
        decisions = decisions or prompt_multiline("Décisions")
        next_steps = next_steps or prompt_multiline("Prochaines étapes")

    if not title:
        raise SystemExit("Titre requis.")
    if not summary:
        raise SystemExit("Résumé requis.")

    path = Path(args.file).expanduser() if args.file else daily_path(now, title)
    if not path.is_absolute():
        path = PKA_DIR / path
    path.parent.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print("DRY RUN — aucune écriture.")
        print(f"Fichier cible : {path}")
        print(build_section(now, title, summary, actions, decisions, next_steps, model=model, project=project))
        return path

    ensure_daily_file(path, now, title)
    section = build_section(now, title, summary, actions, decisions, next_steps, model=model, project=project)
    with path.open("a", encoding="utf-8") as fh:
        fh.write("\n" + section)

    append_log(now, title, summary, path, model=model, project=project)
    _log_to_memory_log(now, title, summary, decisions, model=model, project=project)
    return path


def _log_to_memory_log(
    now: datetime,
    title: str,
    summary: str,
    decisions: str,
    model: str = "",
    project: str = "",
) -> None:
    body_parts = [summary]
    if decisions:
        body_parts.append(f"Décisions: {decisions}")
    body = " | ".join(p.strip() for p in body_parts if p.strip())
    if len(body) > 500:
        body = body[:497] + "..."
    try:
        with sqlite3.connect(TEAM_DB) as con:
            con.execute(
                """INSERT INTO memory_log
                   (memory_file, memory_name, memory_type, model, event_type, body, project_key, created_at)
                   VALUES (?, ?, 'session', ?, 'save', ?, ?, ?)""",
                (
                    f"wiki/Daily/{now.strftime('%Y/%m/%Y-%m-%d')}-{title}.md",
                    f"save-{now.strftime('%Y%m%d-%H%M')}",
                    model or "unknown",
                    body,
                    project or None,
                    now.strftime("%Y-%m-%d"),
                ),
            )
    except (OSError, sqlite3.DatabaseError):
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Sauvegarde manuelle d'une session PKA")
    parser.add_argument("--title")
    parser.add_argument("--summary")
    parser.add_argument("--actions", default="")
    parser.add_argument("--decisions", default="")
    parser.add_argument("--next-steps", default="")
    parser.add_argument("--model", default="", help="Modèle ou runtime utilisé: codex, claude, gemini, deepseek...")
    parser.add_argument("--project", default="", help="Projet PKA concerné: WILDNEXUS, ARTEON, VETALYX...")
    parser.add_argument("--file", help="Chemin daily note cible. Défaut: wiki/Daily/YYYY/MM/date-title.md")
    parser.add_argument("-i", "--interactive", action="store_true", help="Mode interactif")
    parser.add_argument("--dry-run", action="store_true", help="Affiche la sauvegarde sans écrire")
    args = parser.parse_args()

    try:
        path = save_session(args)
    except KeyboardInterrupt:
        print("\nSauvegarde annulée.")
        sys.exit(130)

    if args.dry_run:
        print("\nDry run terminé.")
    else:
        print(f"\nSauvegarde écrite : {path}")
        print(f"Log mis à jour : {LOG_PATH}")


if __name__ == "__main__":
    main()
