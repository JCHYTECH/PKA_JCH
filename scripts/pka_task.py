#!/usr/bin/env python3
"""
pka_task.py — Gestion des tâches JCH via CLI.

Usage:
  python3 scripts/pka_task.py list                          # lister toutes les tâches
  python3 scripts/pka_task.py list --project WILDNEXUS      # filtrer par projet
  python3 scripts/pka_task.py list --status todo             # filtrer par statut
  python3 scripts/pka_task.py status t1 done                 # changer le statut
  python3 scripts/pka_task.py status t3 in_progress          # idem
  python3 scripts/pka_task.py toggle t1                      # toggle todo ↔ done
  python3 scripts/pka_task.py regen                          # régénérer les HTML

Statuts : todo, in_progress, waiting, done
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "JCH_Inbox" / "todo-jch.json"

STATUS_EMOJI = {
    "todo": "⚪",
    "in_progress": "🔵",
    "waiting": "⏳",
    "done": "✅",
}

URGENCY_EMOJI = {
    "critique": "🔴",
    "urgent": "🟠",
    "important": "🟡",
    "long": "🟢",
}


def load():
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def save(data):
    JSON_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def regen_html():
    """Regenerate both HTML views from JSON."""
    scripts = ROOT / "scripts"
    for script in ["generate_todo.py", "generate_kanban.py"]:
        result = subprocess.run(
            [sys.executable, str(scripts / script)],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        if result.returncode != 0:
            print(f"⚠️  {script} failed: {result.stderr[:200]}")
            return False
    return True


def cmd_list(args):
    data = load()
    tasks = data["tasks"]

    if args.status:
        tasks = [t for t in tasks if t.get("status", "todo") == args.status]
    if args.project:
        tasks = [t for t in tasks if t.get("project", "").upper() == args.project.upper()]
    if args.not_done:
        tasks = [t for t in tasks if t.get("status", "todo") != "done"]

    if not tasks:
        print("Aucune tâche trouvée.")
        return

    # Header
    print(f"\n{'ID':4s} {'St':3s} {'U':2s} {'Projet':20s} Titre")
    print("-" * 80)

    counts = {}
    for t in tasks:
        tid = t["id"]
        status = t.get("status", "todo")
        urgency = t.get("urgency", "important")
        project = t.get("project", "?")[:19]
        title = t["title"][:50]

        s_emoji = STATUS_EMOJI.get(status, "⚪")
        u_emoji = URGENCY_EMOJI.get(urgency, "⚪")

        print(f"{tid:4s} {s_emoji}  {u_emoji} {project:20s} {title}")

        counts[status] = counts.get(status, 0) + 1

    # Summary
    print("-" * 80)
    parts = [f"{STATUS_EMOJI.get(s, s)} {c} {s}" for s, c in sorted(counts.items())]
    print(f"{len(tasks)} tâche(s) : {' · '.join(parts)}")


def cmd_status(args):
    data = load()
    task = next((t for t in data["tasks"] if t["id"] == args.id), None)
    if not task:
        print(f"❌ Tâche '{args.id}' introuvable.")
        sys.exit(1)

    old_status = task.get("status", "todo")
    if old_status == args.status:
        print(f"ℹ️  {args.id} déjà en '{args.status}'")
        return

    task["status"] = args.status
    task["done"] = (args.status == "done")
    data["meta"]["last_updated"] = __import__("datetime").date.today().isoformat()
    save(data)

    print(f"{STATUS_EMOJI.get(args.status, '→')} {args.id} : {old_status} → {args.status}")

    if not args.no_regen:
        if regen_html():
            print("   HTML régénérés")


def cmd_toggle(args):
    data = load()
    task = next((t for t in data["tasks"] if t["id"] == args.id), None)
    if not task:
        print(f"❌ Tâche '{args.id}' introuvable.")
        sys.exit(1)

    current = task.get("status", "todo")
    new_status = "todo" if current == "done" else "done"
    task["status"] = new_status
    task["done"] = (new_status == "done")
    data["meta"]["last_updated"] = __import__("datetime").date.today().isoformat()
    save(data)

    emoji = STATUS_EMOJI.get(new_status, "→")
    print(f"{emoji} {args.id} : {current} → {new_status} — {task['title'][:60]}")

    if not args.no_regen:
        if regen_html():
            print("   HTML régénérés")


def cmd_regen(args):
    if regen_html():
        print("✅ todo-jch.html + kanban.html régénérés")


# ═══════════════════════════════════════════════════════════════════
# Serveur HTTP interactif — kanban avec contrôles de statut live
# ═══════════════════════════════════════════════════════════════════

KANBAN_HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PKA — Kanban Live</title>
<style>
  :root {
    --bg: #1a1a2e; --card: #16213e; --border: #2a2a4a;
    --text: #e0e0e0; --muted: #888; --accent: #d4a017;
    --red: #e74c3c; --orange: #e67e22; --yellow: #d4ac0d; --green: #27ae60;
    --blue: #2c6fce; --wait: #6b5b3a;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, system-ui, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
  .header {
    background: var(--card); padding: 12px 24px; display: flex; align-items: center;
    justify-content: space-between; border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 10;
  }
  .header h1 { font-size: 16px; font-weight: 400; letter-spacing: 0.05em; }
  .header h1 span { color: var(--accent); }
  .header .info { font-size: 11px; color: var(--muted); }
  .filters { padding: 10px 24px; display: flex; gap: 6px; flex-wrap: wrap; background: var(--bg); border-bottom: 1px solid var(--border); }
  .filters button {
    font-size: 11px; padding: 4px 10px; border: 1px solid var(--border);
    background: var(--card); color: var(--muted); cursor: pointer; border-radius: 3px; transition: all 0.15s;
  }
  .filters button:hover, .filters button.active { background: var(--border); color: var(--text); }
  .board { display: flex; gap: 0; padding: 16px; overflow-x: auto; }
  .col {
    flex: 1; min-width: 240px; max-width: 380px; background: var(--card);
    margin: 0 6px; border-radius: 8px; border: 1px solid var(--border);
    display: flex; flex-direction: column; max-height: calc(100vh - 130px); overflow-y: auto;
  }
  .col-header {
    padding: 12px 14px; border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 6px; position: sticky; top: 0; background: var(--card);
  }
  .col-header .count { font-family: monospace; font-size: 12px; color: var(--muted); margin-left: auto; }
  .cards { padding: 8px 10px; display: flex; flex-direction: column; gap: 6px; }
  .card {
    background: var(--bg); border: 1px solid var(--border); border-left: 3px solid var(--border);
    padding: 10px 12px; border-radius: 5px;
  }
  .card.critique { border-left-color: var(--red); }
  .card.urgent { border-left-color: var(--orange); }
  .card.important { border-left-color: var(--yellow); }
  .card.long { border-left-color: var(--green); }
  .card-top { display: flex; align-items: flex-start; gap: 6px; margin-bottom: 4px; }
  .card-title { font-size: 13px; font-weight: 600; flex: 1; line-height: 1.3; }
  .badge {
    font-size: 8px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;
    padding: 2px 6px; border-radius: 2px; white-space: nowrap;
  }
  .badge.critique { background: var(--red); color: white; }
  .badge.urgent { background: var(--orange); color: white; }
  .badge.important { background: var(--yellow); color: var(--bg); }
  .badge.long { background: var(--green); color: var(--bg); }
  .card-context { font-size: 11px; color: var(--muted); line-height: 1.4; margin-bottom: 6px; }
  .card-meta { display: flex; justify-content: space-between; align-items: center; font-size: 10px; }
  .card-project { color: var(--accent); font-family: monospace; }
  .card-who { color: var(--muted); }
  .card-status-row { margin-top: 6px; padding-top: 6px; border-top: 1px solid var(--border); display: flex; align-items: center; gap: 6px; }
  .card-status-row select {
    font-size: 11px; padding: 3px 6px; border: 1px solid var(--border);
    background: var(--card); color: var(--text); border-radius: 3px; cursor: pointer;
  }
  .card-status-row .saved { font-size: 10px; color: var(--green); opacity: 0; transition: opacity 0.3s; }
  .card-status-row .saved.show { opacity: 1; }
  .empty { text-align: center; color: var(--muted); padding: 40px 0; font-size: 18px; }
  .stats { padding: 8px 24px; font-size: 11px; color: var(--muted); border-top: 1px solid var(--border); }
  .toast {
    position: fixed; top: 16px; right: 16px; background: var(--green); color: var(--bg);
    padding: 8px 16px; border-radius: 4px; font-size: 12px; z-index: 999;
    opacity: 0; transform: translateY(-10px); transition: all 0.3s;
  }
  .toast.show { opacity: 1; transform: translateY(0); }
  .toast.error { background: var(--red); color: white; }
</style>
</head>
<body>

<div class="header">
  <h1>PKA <span>Kanban Live</span></h1>
  <div class="info" id="status-line">Chargement...</div>
</div>

<div class="filters" id="filters"></div>

<div class="board" id="board"></div>

<div class="stats" id="stats"></div>
<div class="toast" id="toast"></div>

<script>
const STATUSES = ['todo','in_progress','waiting','done'];
const STATUS_LABELS = {todo:'À faire', in_progress:'En cours', waiting:'En attente', done:'Terminé'};
const STATUS_ICONS = {todo:'○', in_progress:'◉', waiting:'⏳', done:'✓'};
const COLORS = {todo:'var(--muted)', in_progress:'var(--blue)', waiting:'var(--wait)', done:'var(--green)'};

let allTasks = [];
let activeProject = 'all';

async function load() {
  try {
    const r = await fetch('/api/tasks');
    allTasks = await r.json();
    buildFilters();
    render();
    document.getElementById('status-line').textContent = allTasks.length + ' tâches';
  } catch(e) {
    document.getElementById('status-line').textContent = '⚠️ Serveur injoignable';
  }
}

function buildFilters() {
  const projects = [...new Set(allTasks.map(t => t.project))].sort();
  const f = document.getElementById('filters');
  f.innerHTML = '<button class="active" onclick="filterProject(\'all\',this)">Tous</button>';
  for (const p of projects) {
    f.innerHTML += `<button onclick="filterProject('${p}',this)">${p}</button>`;
  }
}

function filterProject(p, btn) {
  activeProject = p;
  document.querySelectorAll('.filters button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  render();
}

function render() {
  const board = document.getElementById('board');
  board.innerHTML = '';
  const cols = {};
  for (const s of STATUSES) cols[s] = [];

  for (const t of allTasks) {
    if (activeProject !== 'all' && t.project !== activeProject) continue;
    cols[t.status || 'todo'].push(t);
  }

  for (const s of STATUSES) {
    const tasks = cols[s];
    board.innerHTML += `
      <div class="col">
        <div class="col-header">
          <span style="color:${COLORS[s]}">${STATUS_ICONS[s]}</span>
          <span style="font-weight:600;font-size:14px">${STATUS_LABELS[s]}</span>
          <span class="count">${tasks.length}</span>
        </div>
        <div class="cards">
          ${tasks.length === 0 ? '<div class="empty">—</div>' : tasks.map(t => cardHTML(t)).join('')}
        </div>
      </div>`;
  }

  const visible = Object.values(cols).reduce((a,b) => a+b.length, 0);
  document.getElementById('stats').textContent =
    `${visible} tâche(s) visibles` + (activeProject !== 'all' ? ` · ${activeProject}` : '');
}

function cardHTML(t) {
  const status = t.status || 'todo';
  return `
    <div class="card ${t.urgency}">
      <div class="card-top">
        <span class="card-title">${t.title}</span>
        <span class="badge ${t.urgency}">${t.urgency}</span>
      </div>
      <div class="card-context">${t.context || ''}</div>
      <div class="card-meta">
        <span class="card-project">${t.project}${t.project_sub ? ' · ' + t.project_sub : ''}</span>
        <span class="card-who">${t.who}</span>
      </div>
      <div class="card-status-row">
        <select onchange="changeStatus('${t.id}', this.value, this)" value="${status}">
          ${STATUSES.map(s => `<option value="${s}" ${s === status ? 'selected' : ''}>${STATUS_LABELS[s]}</option>`).join('')}
        </select>
        <span class="saved">✓ Sauvé</span>
      </div>
    </div>`;
}

async function changeStatus(id, newStatus, selectEl) {
  const savedEl = selectEl.parentElement.querySelector('.saved');
  try {
    const r = await fetch('/api/task/' + id, {
      method: 'PATCH',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({status: newStatus})
    });
    if (r.ok) {
      const task = allTasks.find(t => t.id === id);
      if (task) task.status = newStatus;
      savedEl.classList.add('show');
      setTimeout(() => savedEl.classList.remove('show'), 1500);
      render();
      toast('Statut mis à jour');
    } else {
      selectEl.value = allTasks.find(t => t.id === id)?.status || 'todo';
      toast('Erreur', true);
    }
  } catch(e) {
    selectEl.value = allTasks.find(t => t.id === id)?.status || 'todo';
    toast('Erreur réseau', true);
  }
}

function toast(msg, isError) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'toast ' + (isError ? 'error' : '') + ' show';
  setTimeout(() => el.classList.remove('show'), 2000);
}

load();
</script>
</body>
</html>"""


def cmd_serve(args):
    """Start interactive kanban server on localhost."""
    import http.server
    import threading
    import webbrowser

    PORT = args.port or 8765

    class KanbanHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *a):
            pass  # silent

        def do_GET(self):
            if self.path == '/' or self.path == '/index.html':
                self._serve_html()
            elif self.path == '/api/tasks':
                self._serve_json()
            else:
                self.send_error(404)

        def do_PATCH(self):
            if self.path.startswith('/api/task/'):
                self._patch_task()
            else:
                self.send_error(404)

        def _serve_html(self):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(KANBAN_HTML.encode('utf-8'))

        def _serve_json(self):
            data = load()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data['tasks']).encode('utf-8'))

        def _patch_task(self):
            task_id = self.path.split('/')[-1]
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            new_status = body.get('status')

            if new_status not in ('todo', 'in_progress', 'waiting', 'done'):
                self.send_error(400, 'Invalid status')
                return

            data = load()
            task = next((t for t in data['tasks'] if t['id'] == task_id), None)
            if not task:
                self.send_error(404, 'Task not found')
                return

            task['status'] = new_status
            task['done'] = (new_status == 'done')
            data['meta']['last_updated'] = __import__('datetime').date.today().isoformat()
            save(data)

            # Regenerate HTML in background
            threading.Thread(target=regen_html, daemon=True).start()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': True, 'id': task_id, 'status': new_status}).encode('utf-8'))

    server = http.server.HTTPServer(('127.0.0.1', PORT), KanbanHandler)

    print(f"\n🖥️  Kanban Live → http://localhost:{PORT}")
    print("   Change les statuts par dropdown — sauvegarde instantanée JSON + HTML")
    print("   Ctrl+C pour arrêter\n")

    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Serveur arrêté")


def main():
    parser = argparse.ArgumentParser(description="Gestion des tâches JCH")
    sub = parser.add_subparsers(dest="command")

    # list
    list_p = sub.add_parser("list", help="Lister les tâches")
    list_p.add_argument("--status", choices=["todo", "in_progress", "waiting", "done"])
    list_p.add_argument("--project")
    list_p.add_argument("--not-done", action="store_true", help="Tâches non terminées")

    # status
    stat_p = sub.add_parser("status", help="Changer le statut d'une tâche")
    stat_p.add_argument("id", help="ID de la tâche (ex: t1)")
    stat_p.add_argument("status", choices=["todo", "in_progress", "waiting", "done"])
    stat_p.add_argument("--no-regen", action="store_true", help="Ne pas régénérer les HTML")

    # toggle
    tog_p = sub.add_parser("toggle", help="Basculer todo ↔ done")
    tog_p.add_argument("id", help="ID de la tâche")
    tog_p.add_argument("--no-regen", action="store_true")

    # regen
    reg_p = sub.add_parser("regen", help="Régénérer les HTML depuis le JSON")

    # serve
    serve_p = sub.add_parser("serve", help="Lancer le kanban interactif (http://localhost:8765)")
    serve_p.add_argument("--port", type=int, default=8765)
    serve_p.add_argument("--no-browser", action="store_true", help="Ne pas ouvrir le navigateur")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "toggle":
        cmd_toggle(args)
    elif args.command == "regen":
        cmd_regen(args)
    elif args.command == "serve":
        cmd_serve(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
