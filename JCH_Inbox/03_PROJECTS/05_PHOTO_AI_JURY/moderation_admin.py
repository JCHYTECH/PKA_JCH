#!/usr/bin/env python3
"""
Argus — Interface admin modération queue
Lancer : python3 moderation_admin.py
Ouvrir  : http://localhost:8765
"""

import json
import mimetypes
import os
import sqlite3
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DB_PATH = Path(__file__).parent / "argus_critique.db"
PORT = 8765


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def read_file(path):
    with open(path, "rb") as f:
        return f.read()


HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Argus — Modération</title>
<style>
  :root {
    --noir: #0D0B09; --ivoire: #F8F5F0; --ocre: #C17F3A;
    --sable: #E8E2DA; --gris: #6B6560; --brun: #2A2420;
    --vert: #3D5A3E; --rouge: #C0392B; --orange: #E67E22;
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Helvetica Neue', sans-serif; background: #CFCFCF; min-height: 100vh; }

  .header {
    background: var(--brun); color: white;
    padding: 20px 40px; display: flex; align-items: baseline; justify-content: space-between;
    position: sticky; top: 0; z-index: 100;
  }
  .header-title { font-size: 16px; font-weight: 300; letter-spacing: 0.1em; }
  .header-title span { color: var(--ocre); }
  .badge-count {
    font-family: monospace; font-size: 12px;
    background: var(--ocre); color: white;
    padding: 3px 10px; border-radius: 2px;
  }

  .empty {
    text-align: center; padding: 80px 40px;
    font-size: 14px; color: var(--gris); letter-spacing: 0.05em;
  }
  .empty strong { display: block; font-size: 18px; color: var(--noir); margin-bottom: 8px; }

  .grid { padding: 32px 40px; display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 20px; }

  .card {
    background: white; overflow: hidden;
    border-left: 4px solid var(--orange);
    display: flex; flex-direction: column;
  }
  .card.approved { border-left-color: var(--vert); opacity: 0.5; }
  .card.rejected { border-left-color: var(--rouge); opacity: 0.5; }

  .card-img {
    width: 100%; height: 220px; object-fit: cover;
    background: var(--sable); display: block;
  }
  .card-img-placeholder {
    width: 100%; height: 220px; background: var(--sable);
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; color: var(--gris); letter-spacing: 0.05em;
  }

  .card-body { padding: 16px 18px; display: flex; flex-direction: column; gap: 10px; flex: 1; }

  .card-filename { font-size: 13px; font-weight: 600; color: var(--noir); word-break: break-all; }

  .meta { display: flex; gap: 8px; flex-wrap: wrap; }
  .tag {
    font-family: monospace; font-size: 10px; letter-spacing: 0.04em;
    padding: 2px 8px; background: var(--ivoire); color: var(--gris);
    text-transform: uppercase;
  }
  .tag.captive_animal { background: #FEF3CD; color: #8B6914; }
  .tag.doubtful { background: #FDE8D8; color: #8B3E14; }

  .haiku-reason {
    font-size: 12px; color: var(--gris); line-height: 1.5;
    border-left: 2px solid var(--sable); padding-left: 10px;
    font-style: italic;
  }

  .client { font-size: 11px; color: var(--gris); }
  .client strong { color: var(--noir); }

  textarea {
    width: 100%; border: 1px solid var(--sable); padding: 8px 10px;
    font-size: 12px; font-family: inherit; resize: vertical; min-height: 56px;
    color: var(--noir); outline: none;
  }
  textarea:focus { border-color: var(--ocre); }

  .actions { display: flex; gap: 8px; padding-top: 4px; }
  .btn {
    flex: 1; padding: 9px; font-size: 12px; font-weight: 600;
    letter-spacing: 0.06em; text-transform: uppercase; cursor: pointer;
    border: none; transition: opacity 0.15s;
  }
  .btn:hover { opacity: 0.85; }
  .btn-approve { background: var(--vert); color: white; }
  .btn-reject  { background: var(--rouge); color: white; }
  .btn:disabled { opacity: 0.4; cursor: default; }

  .status-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; padding: 6px 0; text-align: center;
  }
  .status-label.approved { color: var(--vert); }
  .status-label.rejected { color: var(--rouge); }

  .date { font-family: monospace; font-size: 10px; color: var(--gris); }
</style>
</head>
<body>

<div class="header">
  <div class="header-title">Argus <span>·</span> Modération queue</div>
  <div id="badge" class="badge-count">…</div>
</div>

<div id="root"></div>

<script>
async function load() {
  const res = await fetch('/api/queue');
  const items = await res.json();

  const badge = document.getElementById('badge');
  const pending = items.filter(i => i.status === 'pending');
  badge.textContent = pending.length + ' en attente';

  const root = document.getElementById('root');
  if (items.length === 0) {
    root.innerHTML = '<div class="empty"><strong>Queue vide</strong>Aucune photo en attente de modération.</div>';
    return;
  }

  root.innerHTML = '<div class="grid" id="grid"></div>';
  const grid = document.getElementById('grid');
  items.forEach(item => grid.appendChild(buildCard(item)));
}

function buildCard(item) {
  const div = document.createElement('div');
  div.className = 'card' + (item.status !== 'pending' ? ' ' + item.status : '');
  div.id = 'card-' + item.id;

  const imgHtml = item.id
    ? `<img class="card-img" src="/api/image/${item.id}" alt="${item.filename || ''}" onerror="this.outerHTML='<div class=card-img-placeholder>Image non disponible</div>'">`
    : `<div class="card-img-placeholder">Pas d'image</div>`;

  const dateStr = item.created_at ? item.created_at.slice(0, 16).replace('T', ' ') : '—';
  const conf = item.confidence ? (item.confidence * 100).toFixed(0) + '%' : '—';

  const actionHtml = item.status === 'pending'
    ? `<textarea id="note-${item.id}" placeholder="Note optionnelle…"></textarea>
       <div class="actions">
         <button class="btn btn-approve" onclick="decide(${item.id}, 'approve')">✓ Approuver</button>
         <button class="btn btn-reject"  onclick="decide(${item.id}, 'reject')">✗ Rejeter</button>
       </div>`
    : `<div class="status-label ${item.status}">${item.status === 'approved' ? '✓ Approuvée' : '✗ Rejetée'} — ${item.validated_at ? item.validated_at.slice(0,16) : ''}</div>`;

  div.innerHTML = `
    ${imgHtml}
    <div class="card-body">
      <div class="card-filename">${item.filename || item.image_path || 'Fichier inconnu'}</div>
      <div class="meta">
        <span class="tag ${item.category}">${item.category || '—'}</span>
        <span class="tag">confiance ${conf}</span>
      </div>
      ${item.haiku_reason ? `<div class="haiku-reason">${item.haiku_reason}</div>` : ''}
      ${item.client_email ? `<div class="client">Client : <strong>${item.client_email}</strong></div>` : ''}
      <div class="date">${dateStr}</div>
      ${actionHtml}
    </div>`;
  return div;
}

async function decide(id, action) {
  const note = document.getElementById('note-' + id);
  const noteVal = note ? note.value.trim() : '';

  const btns = document.querySelectorAll(`#card-${id} .btn`);
  btns.forEach(b => b.disabled = true);

  const res = await fetch(`/api/${action}/${id}`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ note: noteVal })
  });

  if (res.ok) {
    const card = document.getElementById('card-' + id);
    card.className = 'card ' + (action === 'approve' ? 'approved' : 'rejected');
    const actionsDiv = card.querySelector('.actions');
    if (note) note.remove();
    if (actionsDiv) actionsDiv.outerHTML = `<div class="status-label ${action === 'approve' ? 'approved' : 'rejected'}">${action === 'approve' ? '✓ Approuvée' : '✗ Rejetée'}</div>`;
    // update badge
    const badge = document.getElementById('badge');
    const cur = parseInt(badge.textContent) || 0;
    badge.textContent = Math.max(0, cur - 1) + ' en attente';
  } else {
    btns.forEach(b => b.disabled = false);
    alert('Erreur — réessaie.');
  }
}

load();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silence request logs

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            body = HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/queue":
            conn = get_db()
            rows = conn.execute(
                "SELECT * FROM moderation_queue ORDER BY created_at DESC"
            ).fetchall()
            conn.close()
            self.send_json([dict(r) for r in rows])
            return

        if path.startswith("/api/image/"):
            item_id = path.split("/")[-1]
            conn = get_db()
            row = conn.execute(
                "SELECT image_path FROM moderation_queue WHERE id = ?", (item_id,)
            ).fetchone()
            conn.close()
            if not row or not row["image_path"]:
                self.send_response(404)
                self.end_headers()
                return
            img_path = Path(row["image_path"])
            if not img_path.exists():
                self.send_response(404)
                self.end_headers()
                return
            mime, _ = mimetypes.guess_type(str(img_path))
            mime = mime or "application/octet-stream"
            data = read_file(img_path)
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        note = body.get("note", "")

        if path.startswith("/api/approve/") or path.startswith("/api/reject/"):
            action = "approved" if "/approve/" in path else "rejected"
            item_id = path.split("/")[-1]
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = get_db()
            conn.execute(
                "UPDATE moderation_queue SET status=?, moderator_note=?, validated_at=?, updated_at=? WHERE id=?",
                (action, note or None, now, now, item_id),
            )
            conn.commit()
            conn.close()
            self.send_json({"ok": True})
            return

        self.send_response(404)
        self.end_headers()


if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"Base de données introuvable : {DB_PATH}")
        raise SystemExit(1)
    print(f"Argus Modération → http://localhost:{PORT}")
    print("Ctrl+C pour arrêter")
    HTTPServer(("localhost", PORT), Handler).serve_forever()
