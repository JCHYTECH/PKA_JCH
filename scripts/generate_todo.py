#!/usr/bin/env python3
"""Generate todo-jch.html from todo-jch.json — JCH's personal task dashboard.

Usage:
    python scripts/generate_todo.py                    # write JCH_Inbox/todo-jch.html
    python scripts/generate_todo.py --check            # check if HTML matches JSON
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "JCH_Inbox" / "todo-jch.json"
HTML_PATH = ROOT / "JCH_Inbox" / "todo-jch.html"

URGENCY_LABELS = {"critique": "Critique", "urgent": "Urgent", "important": "Important", "long": "Long terme"}
URGENCY_COLORS = {"critique": "var(--rouge-alert)", "urgent": "#e67e22", "important": "#d4ac0d", "long": "var(--vert-ok)"}

# Project buttons derived dynamically in generate_html()


def load_tasks() -> dict:
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


STATUS_LABELS = {"todo": "À faire", "in_progress": "En cours", "waiting": "En attente", "done": "Terminé"}
STATUS_CSS = {"todo": "", "in_progress": "in-progress", "waiting": "waiting", "done": "done"}


def html_card(task: dict) -> str:
    status = task.get("status", "todo")
    is_done = status == "done"
    extra_cls = f' {STATUS_CSS[status]}' if STATUS_CSS[status] else ""
    checked = 'checked' if is_done else ""
    label = "Terminée ✓" if is_done else "Marquer comme fait"
    status_badge = f' <span class="status-badge {STATUS_CSS[status]}">{STATUS_LABELS[status]}</span>' if not is_done and status != "todo" else ""
    project_label = f"{task['project']} · {task['project_sub']}" if task.get("project_sub") else task["project"]

    deps_html = ""
    for dep in task.get("deps", []):
        deps_html += f'<div class="dep-tag">{dep}</div>'

    return f"""\
  <div class="card{extra_cls}" data-urgency="{task['urgency']}" data-project="{task['project']}" data-status="{status}">
    <div class="card-top">
      <div class="card-title">{task['title']}{status_badge}</div>
      <div class="badge-urgency {task['urgency']}">{URGENCY_LABELS[task['urgency']]}</div>
    </div>
    <div class="card-context">{task['context']}</div>
    <div class="card-meta">
      <div class="card-project">{project_label}</div>
      <div class="card-deps">{deps_html}</div>
      <div class="card-who">{task.get('role', 'Responsable')} : <strong>{task['who']}</strong></div>
    </div>
    <div class="card-check"><input type="checkbox" id="{task['id']}" onchange="toggleDoneCard(this)" {checked}><label for="{task['id']}">{label}</label></div>
  </div>"""


def generate_html(data: dict) -> str:
    meta = data["meta"]
    tasks = data["tasks"]

    cards = "\n\n".join(html_card(t) for t in tasks)
    # Derive project buttons from data (ordered by frequency)
    proj_counts = {}
    for t in tasks:
        p = t["project"]
        proj_counts[p] = proj_counts.get(p, 0) + 1
    sorted_projects = sorted(proj_counts, key=lambda p: (-proj_counts[p], p))
    project_buttons = "\n".join(
        f'  <button class="filter-btn" data-filter="project" data-value="{p}" onclick="filterProject(this)">{p}</button>'
        for p in sorted_projects
    )

    today = date.today().isoformat()

    return f"""\
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta['title']}</title>
<link rel="stylesheet" href="01_DASHBOARDS/assets/pka-theme.css">
<style>
  :root {{
    --critique: var(--rouge-alert);
    --urgent:   #e67e22;
    --important:#d4ac0d;
    --long:     var(--vert-ok);
  }}
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Space Grotesk', sans-serif; background: var(--fond-global); color: var(--texte-clair); min-height: 100vh; }}

  /* ── Header ── */
  .header {{
    background: var(--carte-bg); color: var(--texte-clair);
    padding: 24px 40px; display: flex; align-items: baseline; justify-content: space-between;
    position: sticky; top: 0; z-index: 100; border-bottom: 1px solid var(--bordure);
  }}
  .header-title {{ font-size: 18px; font-weight: 300; letter-spacing: 0.1em; }}
  .header-title span {{ color: var(--ocre); }}
  .header-count {{ font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--texte-mute); }}

  /* ── Toolbar ── */
  .toolbar {{
    background: var(--fond-global); border-bottom: 1px solid var(--bordure);
    padding: 14px 40px; display: flex; gap: 12px; flex-wrap: wrap; align-items: center;
  }}
  .toolbar-label {{ font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--texte-mute); margin-right: 4px; }}
  .filter-btn {{
    font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 500;
    padding: 5px 14px; border: 1px solid var(--bordure); background: var(--carte-bg); color: var(--texte-gris);
    cursor: pointer; letter-spacing: 0.04em; transition: all 0.15s; border-radius: 4px;
  }}
  .filter-btn:hover {{ background: var(--bordure); color: var(--texte-clair); }}
  .filter-btn.active {{ background: var(--bordure); color: var(--texte-clair); border-color: var(--texte-gris); }}
  
  .filter-btn.u-critique.active {{ background: var(--rouge-alert); color: white; border-color: var(--rouge-alert); }}
  .filter-btn.u-urgent.active {{ background: #E67E22; color: white; border-color: #E67E22; }}
  .filter-btn.u-important.active {{ background: #D4AC0D; border-color: #D4AC0D; color: var(--fond-global); }}
  .filter-btn.u-long.active {{ background: var(--vert-ok); border-color: var(--vert-ok); color: var(--fond-global); }}
  
  .sep {{ width: 1px; height: 24px; background: var(--bordure); margin: 0 4px; }}

  /* ── Grid ── */
  .grid {{ padding: 32px 40px; display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }}

  /* ── Card ── */
  .card {{
    background: var(--carte-bg); padding: 20px 22px; cursor: default;
    border: 1px solid var(--bordure);
    border-left: 4px solid var(--bordure); transition: opacity 0.2s, transform 0.2s;
    display: flex; flex-direction: column; gap: 12px; border-radius: 8px;
  }}
  .card:hover {{ transform: translateY(-2px); border-color: var(--texte-mute); }}
  .card.hidden {{ display: none; }}
  .card.done {{ opacity: 0.4; border-left-color: var(--bordure) !important; }}
  .card.done .card-title {{ text-decoration: line-through; color: var(--texte-mute); }}

  .card[data-urgency="critique"] {{ border-left-color: var(--rouge-alert); }}
  .card[data-urgency="urgent"]   {{ border-left-color: #e67e22; }}
  .card[data-urgency="important"]{{ border-left-color: #d4ac0d; }}
  .card[data-urgency="long"]     {{ border-left-color: var(--vert-ok); }}

  .card-top {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }}
  .card-title {{ font-size: 15px; font-weight: 600; line-height: 1.35; color: var(--texte-clair); }}
  .badge-urgency {{
    font-size: 9px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 3px 10px; border-radius: 3px; white-space: nowrap; flex-shrink: 0;
  }}
  .badge-urgency.critique {{ background: var(--rouge-alert); color: white; }}
  .badge-urgency.urgent   {{ background: #E67E22; color: white; }}
  .badge-urgency.important{{ background: #D4AC0D; color: var(--fond-global); }}
  .badge-urgency.long     {{ background: var(--vert-ok); color: var(--fond-global); }}

  .status-badge {{
    font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 3px;
    margin-left: 8px; white-space: nowrap; display: inline-block;
  }}
  .status-badge.in-progress {{ background: #2c6fce; color: white; }}
  .status-badge.waiting {{ background: #6b5b3a; color: #e0d5c0; }}
  .card.in-progress {{ border-left-color: #2c6fce !important; }}
  .card.waiting {{ border-left-color: #6b5b3a !important; opacity: 0.75; }}

  .card-context {{ font-size: 13px; line-height: 1.55; color: var(--texte-gris); }}
  .card-meta {{ display: flex; flex-direction: column; gap: 6px; margin-top: auto; }}
  .card-project {{ font-size: 11px; font-family: 'IBM Plex Mono', monospace; color: var(--ocre); }}
  .card-deps {{ display: flex; flex-wrap: wrap; gap: 4px; }}
  .dep-tag {{
    font-size: 10px; padding: 2px 8px; background: var(--bordure);
    color: var(--texte-mute); border-radius: 3px;
  }}
  .card-who {{ font-size: 12px; color: var(--texte-mute); }}

  .card-check {{ margin-top: auto; padding-top: 8px; border-top: 1px solid var(--bordure); font-size: 13px; }}
  .card-check input {{ margin-right: 8px; cursor: pointer; }}
  .card-check label {{ cursor: pointer; user-select: none; }}

  /* ── Stats bar ── */
  .statsbar {{
    background: var(--carte-bg); border-top: 1px solid var(--bordure);
    padding: 14px 40px; display: flex; gap: 24px; font-size: 13px;
    position: sticky; bottom: 0; z-index: 100;
  }}
  .stat-dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }}
  .stat-dot.critique {{ background: var(--rouge-alert); }}
  .stat-dot.urgent   {{ background: #E67E22; }}
  .stat-dot.important{{ background: #D4AC0D; }}
  .stat-dot.long     {{ background: var(--vert-ok); }}
</style>
</head>
<body>

<div class="header">
  <div class="header-title">JCH<span> — Things To Do</span></div>
  <div class="header-count"><span id="visible-count">—</span> · généré le {today}</div>
</div>

<div class="toolbar">
  <span class="toolbar-label">Urgence</span>
  <button class="filter-btn u-critique active" data-filter="urgency" data-value="critique" onclick="toggleFilter(this)">Critique</button>
  <button class="filter-btn u-urgent active" data-filter="urgency" data-value="urgent" onclick="toggleFilter(this)">Urgent</button>
  <button class="filter-btn u-important active" data-filter="urgency" data-value="important" onclick="toggleFilter(this)">Important</button>
  <button class="filter-btn u-long active" data-filter="urgency" data-value="long" onclick="toggleFilter(this)">Long terme</button>
  <div class="sep"></div>
  <span class="toolbar-label">Projet</span>
  <button class="filter-btn active" data-filter="project" data-value="all" onclick="filterProject(this)">Tous</button>
{project_buttons}
  <div class="sep"></div>
  <button class="filter-btn" onclick="toggleDone()">Masquer terminées</button>
</div>

<div class="grid" id="grid">

{cards}

</div>

<div class="statsbar">
  <div class="stat"><span class="stat-dot critique"></span><strong id="cnt-critique">—</strong> critiques</div>
  <div class="stat"><span class="stat-dot urgent"></span><strong id="cnt-urgent">—</strong> urgentes</div>
  <div class="stat"><span class="stat-dot important"></span><strong id="cnt-important">—</strong> importantes</div>
  <div class="stat"><span class="stat-dot long"></span><strong id="cnt-long">—</strong> long terme</div>
  <div class="stat" style="margin-left:auto;">Mis à jour : {today}</div>
</div>

<script>
  const activeUrgency = new Set(['critique','urgent','important','long']);
  let activeProject = 'all';
  let hideDone = false;

  function toggleFilter(btn) {{
    const val = btn.dataset.value;
    if (activeUrgency.has(val)) {{
      if (activeUrgency.size === 1) return;
      activeUrgency.delete(val);
      btn.classList.remove('active');
    }} else {{
      activeUrgency.add(val);
      btn.classList.add('active');
    }}
    applyFilters();
  }}

  function filterProject(btn) {{
    document.querySelectorAll('[data-filter="project"]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeProject = btn.dataset.value;
    applyFilters();
  }}

  function toggleDone() {{
    hideDone = !hideDone;
    applyFilters();
  }}

  function applyFilters() {{
    const cards = document.querySelectorAll('.card');
    let visible = 0;
    const counts = {{critique:0, urgent:0, important:0, long:0}};

    cards.forEach(card => {{
      const u = card.dataset.urgency;
      const p = card.dataset.project;
      const isDone = card.classList.contains('done');

      const urgencyOk = activeUrgency.has(u);
      const projectOk = activeProject === 'all' || p === activeProject;
      const doneOk = !hideDone || !isDone;

      if (urgencyOk && projectOk && doneOk) {{
        card.classList.remove('hidden');
        visible++;
        if (!isDone) counts[u]++;
      }} else {{
        card.classList.add('hidden');
      }}
    }});

    document.getElementById('visible-count').textContent = visible + ' tâche' + (visible > 1 ? 's' : '');
    document.getElementById('cnt-critique').textContent = counts.critique;
    document.getElementById('cnt-urgent').textContent = counts.urgent;
    document.getElementById('cnt-important').textContent = counts.important;
    document.getElementById('cnt-long').textContent = counts.long;
  }}

  function toggleDoneCard(checkbox) {{
    const card = checkbox.closest('.card');
    if (checkbox.checked) {{
      card.classList.add('done');
      checkbox.nextElementSibling.textContent = 'Terminée ✓';
    }} else {{
      card.classList.remove('done');
      checkbox.nextElementSibling.textContent = 'Marquer comme fait';
    }}
    applyFilters();
  }}

  applyFilters();
</script>
</body>
</html>"""


def generate(check: bool = False) -> int:
    data = load_tasks()
    rendered = generate_html(data)

    if check:
        current = HTML_PATH.read_text(encoding="utf-8") if HTML_PATH.exists() else ""
        if current != rendered:
            print("DRIFT todo-jch.html")
            return 1
        print("todo-jch.html up to date")
        return 0

    HTML_PATH.write_text(rendered, encoding="utf-8")
    print(f"UPDATED {HTML_PATH.name} ({len(data['tasks'])} tasks, {len(rendered):,} bytes)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate JCH todo dashboard")
    parser.add_argument("--check", action="store_true", help="Check drift without writing")
    args = parser.parse_args()
    return generate(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
