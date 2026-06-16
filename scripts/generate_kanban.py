#!/usr/bin/env python3
"""Generate kanban.html — unified Kanban board from todo-jch.json + team.db inbox.

Usage:
    python scripts/generate_kanban.py                 # write JCH_Inbox/kanban.html
    python scripts/generate_kanban.py --check         # check drift without writing
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "JCH_Inbox" / "todo-jch.json"
DB_PATH = ROOT / "TEAM" / "team.db"
HTML_PATH = ROOT / "JCH_Inbox" / "kanban.html"

# Column definition
COLUMNS = [
    {"id": "todo",        "label": "À faire",    "icon": "○"},
    {"id": "in_progress", "label": "En cours",   "icon": "◉"},
    {"id": "waiting",     "label": "En attente",  "icon": "⏳"},
    {"id": "done",        "label": "Terminé",     "icon": "✓"},
]

STATUS_TO_COLUMN = {
    "todo": "todo", "in_progress": "in_progress", "waiting": "waiting", "done": "done",
    # inbox brief statuses
    "pending": "todo", "delivered": "waiting", "validated": "done", "rejected": "done", "cancelled": "done",
}

URGENCY_LABELS = {"critique": "Critique", "urgent": "Urgent", "important": "Important", "long": "Long terme"}
URGENCY_ORDER = {"critique": 0, "urgent": 1, "important": 2, "long": 3}

# Project extraction heuristics from brief subjects
PROJECT_KEYWORDS = {
    "WILDNEXUS": ["wildnexus", "edge ai", "caméra", "capteur", "esp32", "lora", "ppk2", "bom", "adr-", "wp02", "p0"],
    "ARTEON": ["arteon", "wildlens", "instant lu", "badge", "charte", "cgu", "argus", "photo"],
    "VETALYX": ["vetalyx", "jchytech", "allerg", "kol", "dixun", "canin", "félin"],
    "LEGAL": ["cgu", "dpa", "marque", "srl", "comptable", "banque", "rgpd", "benelux", "dépôt", "boip"],
    "INFRA": ["m1", "headless", "home assistant", "ha ", "ssh", "tailscale", "docker"],
    "FUTURE_INVEST": ["ibrk", "futures", "invest", "trading", "broker"],
    "TRAVELS": ["van", "stylevan", "camping", "voyage"],
    "IOT": ["zigbee", "iot", "mqtt", "sensor"],
}


# Specialist emoji + delegation rules
SPECIALIST_EMOJI = {
    "Forge": "🦦", "Renard": "🦊", "Vega": "🦚", "Vasco": "🐺", "Bruno": "🐻",
    "Sigma": "🐙", "Nova": "🦋", "Argus": "🦅", "Araignée": "🕷️", "Fourmi": "🐜",
    "Chouette": "🦉", "Héron": "🦢", "Lynx": "🐆", "Atlas": "🐘", "Hermine": "⬜",
    "Miel": "🐝", "Trace": "🕷️", "Furet": "🦡", "Clio": "🦜", "Iris": "🦅",
    "Pie": "🐦‍⬛", "Cigogne": "🦩", "Jade": "🦩", "Corbeau": "🐦‍⬛", "Sybil": "🦔",
    "Dobby": "🦉",
}

# Delegation rules: (project_pattern, keyword_in_title) → suggested specialist
DELEGATE_RULES = [
    # WILDNEXUS
    (["WILDNEXUS"], ["benchmark", "test harness", "firmware", "flash"], "Forge"),
    (["WILDNEXUS"], ["caméra", "capteur", "ov5640", "arducam", "image"], "Nova"),
    (["WILDNEXUS"], ["datasheet", "fiche technique", "télécharger", "re-télécharger"], "Furet"),
    (["WILDNEXUS"], ["commande", "achat", "mouser", "panier", "composant"], "Fourmi"),
    (["WILDNEXUS"], ["terrain", "setup", "piège", "déploiement"], "Chouette"),
    (["WILDNEXUS"], ["lora", "mesh", "réseau", "protocole"], "Araignée"),
    # ARTEON / ARGUS
    (["ARTEON", "ARGUS"], ["badge", "visuel", "charte", "brand", "design"], "Vega"),
    (["ARTEON", "ARGUS"], ["impression", "print", "tirage", "papier"], "Héron"),
    (["ARTEON", "ARGUS"], ["retouche", "lightroom", "dxo", "édition"], "Lynx"),
    (["ARTEON", "ARGUS"], ["site", "web", "page", "shopify", "intégration"], "Forge"),
    (["ARTEON", "ARGUS"], ["seo", "référencement", "visibilité"], "Trace"),
    (["ARTEON", "ARGUS"], ["réseau", "social", "communauté", "content"], "Miel"),
    (["ARTEON", "ARGUS"], ["jury", "critique", "photo", "évaluer"], "Argus"),
    # VETALYX
    (["VETALYX", "JCHYTECH"], ["vétérinaire", "clinique", "allerg", "kol", "protocole"], "Vasco"),
    (["VETALYX", "JCHYTECH"], ["réglementaire", "marquage", "ce", "dispositif"], "Hermine"),
    (["VETALYX", "JCHYTECH"], ["budget", "pricing", "compensation", "finance"], "Bruno"),
    (["VETALYX", "JCHYTECH"], ["rapport", "document", "docx", "rédaction"], "Atlas"),
    # LEGAL
    (["LEGAL"], ["marque", "dépôt", "benelux", "boip", "pi"], "Hermine"),
    (["LEGAL"], ["contrat", "cgu", "dpa", "rgpd", "clause"], "Renard"),
    (["LEGAL"], ["comptable", "srl", "structure", "fiscal"], "Bruno"),
    # INFRA
    (["INFRA"], ["ssh", "tailscale", "docker", "serveur", "déploiement"], "Forge"),
    (["INFRA"], ["home assistant", "ha", "domotique", "dashboard"], "Forge"),
    # FUTURE_INVEST
    (["FUTURE_INVEST"], ["trading", "futures", "stratégie", "analyse"], "Sigma"),
    (["FUTURE_INVEST"], ["profil", "questionnaire", "budget", "risque"], "Bruno"),
    # TRAVELS
    (["TRAVELS"], ["van", "itinéraire", "camping", "voyage"], "Cigogne"),
]


def suggest_delegate(task: dict) -> tuple[str, str] | None:
    """Suggest a specialist who could take this task. Returns (name, emoji) or None."""
    who = task.get("who", "")
    # Only suggest if JCH is the primary (not already delegated)
    if "→" in who or "+" in who or "/" in who:
        return None
    if who.strip() != "JCH":
        return None

    title = task.get("title", "").lower()
    project = task.get("project", "")

    for projects, keywords, specialist in DELEGATE_RULES:
        if project in projects:
            for kw in keywords:
                # Word-boundary match to avoid false positives (e.g. "pi" matching "anthropic")
                if f" {kw} " in f" {title} " or title.startswith(kw + " ") or title.endswith(" " + kw) or title == kw:
                    emoji = SPECIALIST_EMOJI.get(specialist, "→")
                    return (specialist, emoji)
    return None


def infer_project(subject: str, body: str = "") -> str:
    """Guess project from brief subject/body using keyword heuristics."""
    text = (subject + " " + (body or "")).lower()
    for proj, keywords in PROJECT_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return proj
    return "AUTRE"


def load_json_tasks() -> list[dict]:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    tasks = []
    for t in data["tasks"]:
        status = t.get("status", "todo")
        col = STATUS_TO_COLUMN.get(status, "todo")
        tasks.append({
            "id": t["id"],
            "title": t["title"],
            "context": t.get("context", ""),
            "urgency": t.get("urgency", "important"),
            "project": t["project"],
            "project_sub": t.get("project_sub", ""),
            "who": t.get("who", "JCH"),
            "role": t.get("role", ""),
            "status": status,
            "column": col,
            "source": "jch",
            "deps": t.get("deps", []),
        })
    return tasks


def load_inbox_tasks() -> list[dict]:
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    rows = db.execute(
        "SELECT id, to_name, subject, body, status, created_at "
        "FROM inbox WHERE direction = 'JCH→TEAM' AND status IN ('pending', 'in_progress') "
        "ORDER BY created_at DESC"
    ).fetchall()
    db.close()

    tasks = []
    for r in rows:
        col = STATUS_TO_COLUMN.get(r["status"], "todo")
        project = infer_project(r["subject"], r["body"] or "")
        # Determine urgency from body PRIORITY field
        urgency = "important"
        if r["body"]:
            for line in r["body"].split("\n"):
                if line.strip().startswith("PRIORITY"):
                    pval = line.split(":", 1)[-1].strip().lower()
                    if pval in ("critique", "critical", "high"):
                        urgency = "critique"
                    elif pval == "medium":
                        urgency = "important"
                    elif pval in ("low", "long"):
                        urgency = "long"
                    break

        tasks.append({
            "id": f"inbox_{r['id']}",
            "title": r["subject"],
            "context": (r["body"] or "")[:200],
            "urgency": urgency,
            "project": project,
            "project_sub": "",
            "who": r["to_name"],
            "role": "Brief équipe",
            "status": r["status"],
            "column": col,
            "source": "inbox",
            "deps": [],
            "created_at": r["created_at"][:10],
        })
    return tasks


def card_html(task: dict) -> str:
    uc = URGENCY_LABELS.get(task["urgency"], "Important")
    project_label = f"{task['project']} · {task['project_sub']}" if task.get("project_sub") else task["project"]
    source_badge = '<span class="src-badge team">TEAM</span>' if task["source"] == "inbox" else ""
    who_clean = task["who"].replace(" + ", "/")

    # Delegate suggestion
    delegate = suggest_delegate(task)
    delegate_badge = ""
    if delegate:
        name, emoji = delegate
        delegate_badge = f'<span class="delegate-badge" title="Déléguable → {name}">{emoji}&nbsp;{name}</span>'

    return f"""\
    <div class="kanban-card" data-column="{task['column']}" data-urgency="{task['urgency']}" data-project="{task['project']}" data-who="{who_clean}">
      <div class="kc-top">
        <span class="kc-title">{task['title']}</span>
        {source_badge}
        {delegate_badge}
        <span class="kc-urgency {task['urgency']}">{uc}</span>
      </div>
      <div class="kc-context">{task['context'][:150]}</div>
      <div class="kc-meta">
        <span class="kc-project">{project_label}</span>
        <span class="kc-who">{who_clean}</span>
      </div>
    </div>"""


def generate_html() -> str:
    json_tasks = load_json_tasks()
    inbox_tasks = load_inbox_tasks()
    all_tasks = json_tasks + inbox_tasks

    # Collect unique filter values
    projects = sorted(set(t["project"] for t in all_tasks), key=lambda p: (-sum(1 for t in all_tasks if t["project"] == p), p))
    people = sorted(set(t["who"].replace(" + ", "/") for t in all_tasks))

    # Build column HTML
    columns_html = ""
    for col in COLUMNS:
        col_tasks = [t for t in all_tasks if t["column"] == col["id"]]
        # Sort: urgency first, then title
        col_tasks.sort(key=lambda t: (URGENCY_ORDER.get(t["urgency"], 9), t["title"]))
        cards = "\n".join(card_html(t) for t in col_tasks)
        count = len(col_tasks)
        empty_msg = '<div class="kc-empty">—</div>' if count == 0 else ""
        columns_html += f"""\
    <div class="kanban-col" id="col-{col['id']}">
      <div class="kc-header">
        <span class="kc-header-icon">{col['icon']}</span>
        <span class="kc-header-label">{col['label']}</span>
        <span class="kc-header-count">{count}</span>
      </div>
      <div class="kc-cards">
        {cards}
        {empty_msg}
      </div>
    </div>"""

    # Build project filter buttons
    proj_btns = '<button class="kf-btn active" data-filter="project" data-value="all" onclick="filterKanban(this)">Tous</button>\n'
    for p in projects:
        proj_btns += f'      <button class="kf-btn" data-filter="project" data-value="{p}" onclick="filterKanban(this)">{p}</button>\n'

    # Build who filter buttons
    who_btns = '<button class="kf-btn active" data-filter="who" data-value="all" onclick="filterKanban(this)">Tous</button>\n'
    for w in people:
        who_btns += f'      <button class="kf-btn" data-filter="who" data-value="{w}" onclick="filterKanban(this)">{w}</button>\n'

    today = date.today().isoformat()
    total = len(all_tasks)
    jch_count = sum(1 for t in all_tasks if t["source"] == "jch")
    team_count = sum(1 for t in all_tasks if t["source"] == "inbox")

    return f"""\
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PKA — Kanban</title>
<link rel="stylesheet" href="01_DASHBOARDS/assets/pka-theme.css">
<style>
  :root {{
    --critique: var(--rouge-alert);
    --urgent:   #e67e22;
    --important:#d4ac0d;
    --long:     var(--vert-ok);
    --in-progress: #2c6fce;
    --waiting: #6b5b3a;
  }}
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Space Grotesk', sans-serif; background: var(--fond-global); color: var(--texte-clair); min-height: 100vh; }}

  .header {{
    background: var(--carte-bg); padding: 16px 32px;
    display: flex; align-items: baseline; justify-content: space-between;
    position: sticky; top: 0; z-index: 100; border-bottom: 1px solid var(--bordure);
  }}
  .header-title {{ font-size: 18px; font-weight: 300; letter-spacing: 0.1em; }}
  .header-title span {{ color: var(--ocre); }}
  .header-sub {{ font-size: 11px; color: var(--texte-mute); margin-left: 16px; }}

  .filters {{
    background: var(--fond-global); border-bottom: 1px solid var(--bordure);
    padding: 10px 32px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center;
  }}
  .filters-label {{ font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--texte-mute); margin-right: 4px; }}
  .kf-btn {{
    font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 500;
    padding: 4px 12px; border: 1px solid var(--bordure); background: var(--carte-bg);
    color: var(--texte-gris); cursor: pointer; border-radius: 4px; transition: all 0.15s;
  }}
  .kf-btn:hover {{ background: var(--bordure); color: var(--texte-clair); }}
  .kf-btn.active {{ background: var(--bordure); color: var(--texte-clair); border-color: var(--texte-gris); }}
  .kf-sep {{ width: 1px; height: 20px; background: var(--bordure); margin: 0 6px; }}

  .board {{
    display: flex; gap: 0; padding: 16px; overflow-x: auto; flex: 1; min-height: 0;
  }}
  .kanban-col {{
    flex: 1; min-width: 260px; max-width: 400px;
    background: var(--carte-bg); margin: 0 8px; border-radius: 8px;
    border: 1px solid var(--bordure); display: flex; flex-direction: column;
    max-height: calc(100vh - 140px); overflow-y: auto;
  }}
  .kc-header {{
    padding: 14px 16px 10px; border-bottom: 1px solid var(--bordure);
    display: flex; align-items: center; gap: 8px; position: sticky; top: 0;
    background: var(--carte-bg); z-index: 10;
  }}
  .kc-header-icon {{ font-size: 16px; }}
  .kc-header-label {{ font-size: 14px; font-weight: 600; letter-spacing: 0.04em; }}
  .kc-header-count {{ font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--texte-mute); margin-left: auto; }}
  #col-todo .kc-header {{ color: var(--texte-mute); }}
  #col-in_progress .kc-header {{ color: var(--in-progress); }}
  #col-waiting .kc-header {{ color: var(--waiting); }}
  #col-done .kc-header {{ color: var(--vert-ok); }}

  .kc-cards {{ padding: 10px 12px; display: flex; flex-direction: column; gap: 8px; }}
  .kc-empty {{ text-align: center; color: var(--texte-mute); padding: 32px 0; font-size: 20px; }}

  .kanban-card {{
    background: var(--fond-global); border: 1px solid var(--bordure);
    border-left: 3px solid var(--bordure); padding: 12px 14px; border-radius: 6px;
    cursor: default; transition: opacity 0.2s; display: flex; flex-direction: column; gap: 8px;
  }}
  .kanban-card.hidden {{ display: none; }}
  .kanban-card[data-urgency="critique"]  {{ border-left-color: var(--rouge-alert); }}
  .kanban-card[data-urgency="urgent"]    {{ border-left-color: #e67e22; }}
  .kanban-card[data-urgency="important"] {{ border-left-color: #d4ac0d; }}
  .kanban-card[data-urgency="long"]      {{ border-left-color: var(--vert-ok); }}

  .kc-top {{ display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }}
  .kc-title {{ font-size: 13px; font-weight: 600; color: var(--texte-clair); line-height: 1.35; flex: 1; min-width: 0; }}
  .kc-urgency {{
    font-size: 8px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
    padding: 2px 6px; border-radius: 2px; white-space: nowrap;
  }}
  .kc-urgency.critique  {{ background: var(--rouge-alert); color: white; }}
  .kc-urgency.urgent    {{ background: #E67E22; color: white; }}
  .kc-urgency.important {{ background: #D4AC0D; color: var(--fond-global); }}
  .kc-urgency.long      {{ background: var(--vert-ok); color: var(--fond-global); }}

  .kc-context {{ font-size: 11px; color: var(--texte-gris); line-height: 1.45; }}
  .kc-meta {{ display: flex; justify-content: space-between; align-items: center; margin-top: auto; }}
  .kc-project {{ font-size: 10px; font-family: 'IBM Plex Mono', monospace; color: var(--ocre); }}
  .kc-who {{ font-size: 10px; color: var(--texte-mute); }}

  .src-badge {{
    font-size: 8px; font-weight: 700; padding: 2px 6px; border-radius: 2px; letter-spacing: 0.04em;
  }}
  .src-badge.team {{ background: #2c6fce20; color: #2c6fce; border: 1px solid #2c6fce40; }}

  .delegate-badge {{
    font-size: 9px; font-weight: 500; padding: 2px 7px; border-radius: 3px;
    background: #3a5a2c20; color: #8fbc6a; border: 1px solid #3a5a2c40;
    cursor: default; white-space: nowrap;
  }}

  .statsbar {{
    background: var(--carte-bg); border-top: 1px solid var(--bordure);
    padding: 10px 32px; display: flex; gap: 20px; font-size: 12px;
    position: sticky; bottom: 0; z-index: 100;
  }}
</style>
</head>
<body>

<div class="header">
  <div class="header-title">PKA<span> — Kanban</span></div>
  <div class="header-sub">{total} fiches · {jch_count} JCH + {team_count} briefs · {today}</div>
</div>

<div class="filters">
  <span class="filters-label">Projet</span>
  {proj_btns}
  <div class="kf-sep"></div>
  <span class="filters-label">Qui</span>
  {who_btns}
</div>

<div class="board">
{columns_html}
</div>

<div class="statsbar" id="statsbar">
</div>

<script>
  let activeProject = 'all';
  let activeWho = 'all';

  function filterKanban(btn) {{
    const ftype = btn.dataset.filter;
    const val = btn.dataset.value;

    document.querySelectorAll(`.kf-btn[data-filter="${{ftype}}"]`).forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    if (ftype === 'project') activeProject = val;
    if (ftype === 'who') activeWho = val;

    applyKanbanFilters();
  }}

  function applyKanbanFilters() {{
    const cards = document.querySelectorAll('.kanban-card');
    let visible = 0;
    const colCounts = {{}};

    cards.forEach(card => {{
      const p = card.dataset.project;
      const w = card.dataset.who;
      const col = card.dataset.column;

      const projectOk = activeProject === 'all' || p === activeProject;
      const whoOk = activeWho === 'all' || w === activeWho || w.split('/').includes(activeWho);

      if (projectOk && whoOk) {{
        card.classList.remove('hidden');
        visible++;
        colCounts[col] = (colCounts[col] || 0) + 1;
      }} else {{
        card.classList.add('hidden');
      }}
    }});

    // Update column counts
    ['todo','in_progress','waiting','done'].forEach(col => {{
      const el = document.querySelector(`#col-${{col}} .kc-header-count`);
      if (el) el.textContent = colCounts[col] || 0;
    }});

    document.getElementById('statsbar').textContent = visible + ' fiche' + (visible > 1 ? 's' : '') + ' visible' + (activeProject !== 'all' ? ' · Projet ' + activeProject : '') + (activeWho !== 'all' ? ' · ' + activeWho : '');
  }}

  applyKanbanFilters();
</script>
</body>
</html>"""


def generate(check: bool = False) -> int:
    rendered = generate_html()

    if check:
        current = HTML_PATH.read_text(encoding="utf-8") if HTML_PATH.exists() else ""
        if current != rendered:
            print("DRIFT kanban.html")
            return 1
        print("kanban.html up to date")
        return 0

    HTML_PATH.write_text(rendered, encoding="utf-8")
    print(f"UPDATED {HTML_PATH.name} ({len(rendered):,} bytes)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate PKA Kanban board")
    parser.add_argument("--check", action="store_true", help="Check drift without writing")
    return generate(check=parser.parse_args().check)


if __name__ == "__main__":
    raise SystemExit(main())
