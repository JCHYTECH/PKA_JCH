# PKA Kanban Card List Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an operable card-list view for the PKA kanban so JCH can inspect normalized Plane cards with filters by project, status, owner, and JCH decision queue.

**Architecture:** Reuse Plane as the external source of truth and extend the current local read-only kanban stack. Add one service-layer list builder in Python, expose lightweight JSON endpoints from the dashboard server, then add a dedicated dashboard page that renders a compact, filterable card list without introducing a second task database.

**Tech Stack:** Python 3 standard library, existing `scripts/pka_plane_adapter.py`, `scripts/pka_kanban_service.py`, `scripts/dashboard_server.py`, vanilla HTML/CSS/JS, `unittest`

---

## File Structure

- Modify: `scripts/pka_kanban_service.py`
  Add normalized list-oriented helpers on top of the existing summary logic.
- Modify: `tests/test_pka_kanban_service.py`
  Cover filtering, owner aggregation, and awaiting-JCH selection.
- Modify: `scripts/dashboard_server.py`
  Expose JSON endpoints for kanban card list and list filters.
- Modify: `tests/test_dashboard_kanban_endpoints.py`
  Cover new endpoints and payload contracts.
- Create: `JCH_Inbox/01_DASHBOARDS/kanban.html`
  Dedicated list-view dashboard for kanban cards.
- Optional reference only: `JCH_Inbox/01_DASHBOARDS/hub.html`
  Add one link to the new view if needed after the page exists.

### Task 1: Extend the kanban service for list-oriented filtering

**Files:**
- Modify: `tests/test_pka_kanban_service.py`
- Modify: `scripts/pka_kanban_service.py`
- Reference: `scripts/pka_kanban_schema.py`

- [ ] **Step 1: Write the failing tests**

Add these tests to `tests/test_pka_kanban_service.py`:

```python
    def test_build_card_list_filters_by_project_status_owner_and_awaiting_jch(self):
        cards = [
            {
                "title": "Prepare ARTEON palette",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Dobby",
                "priority": "normale",
                "status": "En validation",
                "description": "Needs JCH sign-off",
                "labels": ["branding", "en-attente-jch"],
            },
            {
                "title": "Ship WildNexus field notes",
                "project": "03_WILDNEXUS",
                "type": "document",
                "owner": "Forge",
                "priority": "normale",
                "status": "En cours",
                "description": "Ongoing implementation",
                "labels": ["tech"],
            },
            {
                "title": "Review legal clause",
                "project": "08_VETALYX",
                "type": "decision",
                "owner": "Renard",
                "priority": "haute",
                "status": "En attente",
                "description": "Blocked by external answer",
                "labels": ["legal", "bloque-externe"],
            },
        ]

        filtered = pka_kanban_service.build_card_list(
            cards,
            project="02_ARTEON",
            status="En validation",
            owner="Dobby",
            awaiting_jch_only=True,
        )

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Prepare ARTEON palette")
        self.assertTrue(filtered[0]["awaiting_jch"])

    def test_build_card_list_sorts_by_status_then_title(self):
        cards = [
            {
                "title": "Zulu",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Dobby",
                "priority": "normale",
                "status": "En cours",
                "description": "Later alpha",
            },
            {
                "title": "Alpha",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Dobby",
                "priority": "normale",
                "status": "En cours",
                "description": "First alpha",
            },
        ]

        ordered = pka_kanban_service.build_card_list(cards)

        self.assertEqual([card["title"] for card in ordered], ["Alpha", "Zulu"])

    def test_available_card_filters_returns_projects_statuses_and_owners(self):
        cards = [
            {
                "title": "Prepare ARTEON palette",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Dobby",
                "priority": "normale",
                "status": "En validation",
                "description": "Needs JCH sign-off",
            },
            {
                "title": "Ship WildNexus field notes",
                "project": "03_WILDNEXUS",
                "type": "document",
                "owner": "Forge",
                "priority": "normale",
                "status": "En cours",
                "description": "Ongoing implementation",
            },
        ]

        filters = pka_kanban_service.available_card_filters(cards)

        self.assertEqual(filters["projects"], ["02_ARTEON", "03_WILDNEXUS"])
        self.assertIn("En validation", filters["statuses"])
        self.assertEqual(filters["owners"], ["Dobby", "Forge"])
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_pka_kanban_service -v
```

Expected: FAIL because `build_card_list` and `available_card_filters` do not exist yet.

- [ ] **Step 3: Write minimal implementation**

Update `scripts/pka_kanban_service.py` with:

```python
from collections import Counter, defaultdict

from scripts import pka_kanban_schema


def validate_card(card: dict) -> dict:
    schema = pka_kanban_schema.load_schema()

    for field in schema["required_fields"]:
        if not card.get(field):
            raise ValueError(f"missing required field: {field}")

    if card["status"] not in schema["statuses"]:
        raise ValueError(f"unknown status: {card['status']}")

    return card


def _status_rank(status: str) -> int:
    schema = pka_kanban_schema.load_schema()
    return schema["statuses"].index(status)


def _normalized_card(raw_card: dict) -> dict:
    card = validate_card(raw_card)
    labels = sorted(label for label in card.get("labels", []) if isinstance(label, str))
    normalized = dict(card)
    normalized["labels"] = labels
    normalized["awaiting_jch"] = card["status"] == "En validation" and "en-attente-jch" in labels
    normalized["blocked"] = card["status"] == "En attente"
    return normalized


def build_summary(cards: list[dict]) -> dict:
    schema = pka_kanban_schema.load_schema()
    totals = Counter({status: 0 for status in schema["statuses"]})
    by_project = defaultdict(lambda: {"total": 0})
    blocked = 0
    awaiting_jch = 0

    for raw_card in cards:
        card = _normalized_card(raw_card)
        totals[card["status"]] += 1
        by_project[card["project"]]["total"] += 1

        if card["blocked"]:
            blocked += 1
        if card["awaiting_jch"]:
            awaiting_jch += 1

    return {
        "totals": dict(totals),
        "blocked": blocked,
        "awaiting_jch": awaiting_jch,
        "by_project": dict(by_project),
    }


def build_card_list(
    cards: list[dict],
    project: str | None = None,
    status: str | None = None,
    owner: str | None = None,
    awaiting_jch_only: bool = False,
) -> list[dict]:
    normalized = [_normalized_card(card) for card in cards]
    filtered = []
    for card in normalized:
        if project and card["project"] != project:
            continue
        if status and card["status"] != status:
            continue
        if owner and card["owner"] != owner:
            continue
        if awaiting_jch_only and not card["awaiting_jch"]:
            continue
        filtered.append(card)
    return sorted(filtered, key=lambda card: (_status_rank(card["status"]), card["title"].lower()))


def available_card_filters(cards: list[dict]) -> dict:
    normalized = [_normalized_card(card) for card in cards]
    return {
        "projects": sorted({card["project"] for card in normalized}),
        "statuses": [status for status in pka_kanban_schema.load_schema()["statuses"] if any(card["status"] == status for card in normalized)],
        "owners": sorted({card["owner"] for card in normalized}),
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```bash
python3 -m unittest tests.test_pka_kanban_service -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_pka_kanban_service.py scripts/pka_kanban_service.py
git commit -m "feat: add kanban card list service"
```

### Task 2: Add dashboard endpoints for kanban cards and filters

**Files:**
- Modify: `tests/test_dashboard_kanban_endpoints.py`
- Modify: `scripts/dashboard_server.py`
- Reference: `scripts/pka_plane_adapter.py`
- Reference: `scripts/pka_kanban_service.py`

- [ ] **Step 1: Write the failing tests**

Add these tests to `tests/test_dashboard_kanban_endpoints.py`:

```python
    def test_kanban_cards_endpoint_returns_filtered_card_list(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/kanban/cards?project=03_WILDNEXUS&status=En%20cours&owner=Forge&awaiting_jch=0"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = mock.Mock()
        handler.send_response = mock.Mock()
        handler.send_header = mock.Mock()
        handler.end_headers = mock.Mock()
        handler.is_authorized_request = mock.Mock(return_value=True)
        handler.is_local_request = mock.Mock(return_value=True)
        payloads = []
        handler.send_json = lambda payload, status=200: payloads.append((status, payload))

        with mock.patch.object(dashboard_server, "kanban_cards_payload", return_value={"ok": True, "cards": [{"title": "Ship WildNexus field notes"}]}) as payload_mock:
            dashboard_server.DashboardHandler.do_GET(handler)

        payload_mock.assert_called_once_with("03_WILDNEXUS", "En cours", "Forge", False)
        self.assertEqual(payloads[0][0], 200)
        self.assertEqual(payloads[0][1]["cards"][0]["title"], "Ship WildNexus field notes")

    def test_kanban_filters_endpoint_returns_available_filters(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/kanban/filters"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = mock.Mock()
        handler.send_response = mock.Mock()
        handler.send_header = mock.Mock()
        handler.end_headers = mock.Mock()
        handler.is_authorized_request = mock.Mock(return_value=True)
        handler.is_local_request = mock.Mock(return_value=True)
        payloads = []
        handler.send_json = lambda payload, status=200: payloads.append((status, payload))

        with mock.patch.object(
            dashboard_server,
            "kanban_filters_payload",
            return_value={"ok": True, "projects": ["02_ARTEON"], "statuses": ["En validation"], "owners": ["Dobby"]},
        ):
            dashboard_server.DashboardHandler.do_GET(handler)

        self.assertEqual(payloads[0][0], 200)
        self.assertTrue(payloads[0][1]["ok"])
        self.assertEqual(payloads[0][1]["owners"], ["Dobby"])
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_dashboard_kanban_endpoints -v
```

Expected: FAIL because `/api/kanban/cards` and `/api/kanban/filters` do not exist yet.

- [ ] **Step 3: Write minimal implementation**

Update `scripts/dashboard_server.py` with:

```python
def _all_kanban_cards() -> list[dict]:
    ensure_plane_api_token()
    config = pka_plane_adapter.load_config()
    cards = []
    for project_key in sorted(config["projects"]):
        cards.extend(pka_plane_adapter.fetch_project_issues(project_key))
    return cards


def kanban_cards_payload(
    project: str | None,
    status: str | None,
    owner: str | None,
    awaiting_jch_only: bool,
) -> dict:
    try:
        cards = _all_kanban_cards()
        return {
            "ok": True,
            "cards": pka_kanban_service.build_card_list(
                cards,
                project=project or None,
                status=status or None,
                owner=owner or None,
                awaiting_jch_only=awaiting_jch_only,
            ),
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc), "cards": []}


def kanban_filters_payload() -> dict:
    try:
        cards = _all_kanban_cards()
        return {"ok": True, **pka_kanban_service.available_card_filters(cards)}
    except Exception as exc:
        return {"ok": False, "error": str(exc), "projects": [], "statuses": [], "owners": []}
```

Inside `DashboardHandler.do_GET`, add:

```python
        if path == "/api/kanban/cards":
            params = parse_qs(parsed.query)
            awaiting_jch = params.get("awaiting_jch", ["0"])[0] == "1"
            payload = kanban_cards_payload(
                params.get("project", [""])[0] or None,
                params.get("status", [""])[0] or None,
                params.get("owner", [""])[0] or None,
                awaiting_jch,
            )
            self.send_json(payload, HTTPStatus.OK if payload.get("ok", True) else HTTPStatus.SERVICE_UNAVAILABLE)
            return

        if path == "/api/kanban/filters":
            payload = kanban_filters_payload()
            self.send_json(payload, HTTPStatus.OK if payload.get("ok", True) else HTTPStatus.SERVICE_UNAVAILABLE)
            return
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```bash
python3 -m unittest tests.test_dashboard_kanban_endpoints -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_dashboard_kanban_endpoints.py scripts/dashboard_server.py
git commit -m "feat: add dashboard kanban card endpoints"
```

### Task 3: Add a dedicated kanban list dashboard page

**Files:**
- Create: `JCH_Inbox/01_DASHBOARDS/kanban.html`
- Reference: `JCH_Inbox/01_DASHBOARDS/hub.html`

- [ ] **Step 1: Write the page shell**

Create `JCH_Inbox/01_DASHBOARDS/kanban.html` with:

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PKA · Kanban</title>
<link rel="stylesheet" href="assets/pka-theme.css">
<style>
  :root {
    --noir: #0D0B09;
    --ivoire: #F8F5F0;
    --ocre: #C17F3A;
    --ardoise: #4A5568;
    --sable: #E8E2DA;
    --gris: #6B6560;
    --brun: #2A2420;
    --vert: #3D5A3E;
    --rouge: #C0392B;
  }
  body { margin: 0; font-family: 'Space Grotesk', sans-serif; background: var(--ivoire); color: var(--noir); }
  .header { background: var(--brun); color: white; padding: 28px 40px; display: flex; justify-content: space-between; align-items: end; }
  .header-title { font-size: 28px; font-weight: 300; letter-spacing: 0.08em; }
  .header-sub { margin-top: 6px; color: rgba(255,255,255,0.55); font-size: 13px; }
  .main { max-width: 1200px; margin: 0 auto; padding: 40px 40px 72px; }
  .toolbar { display: grid; grid-template-columns: minmax(220px, 1fr) repeat(3, minmax(180px, 0.7fr)); gap: 10px; margin-bottom: 18px; }
  .field { display: grid; gap: 6px; }
  .label { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--gris); text-transform: uppercase; letter-spacing: 0.08em; }
  select, input { min-height: 40px; border: 1px solid var(--sable); background: white; padding: 0 12px; font: inherit; }
  .toggle { display: flex; align-items: center; gap: 8px; padding-top: 24px; font-size: 12px; color: var(--gris); }
  .statusline { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--ocre); margin-bottom: 14px; min-height: 14px; }
  .cards { display: grid; gap: 10px; }
  .card { background: white; border: 1px solid var(--sable); border-left: 4px solid var(--sable); padding: 16px; }
  .card.blocked { border-left-color: var(--rouge); }
  .card.awaiting-jch { border-left-color: var(--ocre); }
  .card-head { display: flex; justify-content: space-between; gap: 12px; margin-bottom: 8px; }
  .card-title { font-size: 15px; font-weight: 700; }
  .meta { display: flex; flex-wrap: wrap; gap: 6px; }
  .chip { font-family: 'IBM Plex Mono', monospace; font-size: 9px; background: var(--sable); border-radius: 999px; padding: 4px 7px; text-transform: uppercase; }
  .desc { color: var(--gris); font-size: 12px; line-height: 1.55; margin-bottom: 10px; }
  .labels { display: flex; gap: 6px; flex-wrap: wrap; }
  .empty { background: white; border: 1px dashed var(--sable); color: var(--gris); padding: 16px; }
  .back { color: rgba(255,255,255,0.8); text-decoration: none; font-family: 'IBM Plex Mono', monospace; font-size: 11px; }
  @media (max-width: 840px) { .toolbar { grid-template-columns: 1fr; } }
</style>
</head>
<body>
  <div class="header">
    <div>
      <div class="header-title">PKA · Kanban</div>
      <div class="header-sub">Vue liste transversale des cartes Plane normalisées</div>
    </div>
    <a class="back" href="/hub.html">retour hub</a>
  </div>
  <main class="main">
    <div class="toolbar">
      <label class="field">
        <span class="label">Projet</span>
        <select id="filter-project"><option value="">Tous les projets</option></select>
      </label>
      <label class="field">
        <span class="label">Statut</span>
        <select id="filter-status"><option value="">Tous les statuts</option></select>
      </label>
      <label class="field">
        <span class="label">Owner</span>
        <select id="filter-owner"><option value="">Tous les owners</option></select>
      </label>
      <label class="toggle">
        <input id="filter-awaiting-jch" type="checkbox">
        <span>Attente JCH uniquement</span>
      </label>
    </div>
    <div class="statusline" id="kanban-status">Chargement...</div>
    <div class="cards" id="kanban-cards">
      <div class="empty">Chargement des cartes...</div>
    </div>
  </main>
  <script src="assets/kanban.js"></script>
</body>
</html>
```

- [ ] **Step 2: Commit shell checkpoint**

```bash
git add JCH_Inbox/01_DASHBOARDS/kanban.html
git commit -m "feat: add kanban dashboard shell"
```

### Task 4: Add client-side kanban list controller

**Files:**
- Modify: `JCH_Inbox/01_DASHBOARDS/kanban.html`

- [ ] **Step 1: Add minimal controller**

Append this script block at the end of `JCH_Inbox/01_DASHBOARDS/kanban.html` and remove the external `assets/kanban.js` reference:

```html
  <script>
    function escapeHtml(value) {
      return String(value || "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      }[character]));
    }

    function renderCards(payload) {
      const statusline = document.getElementById("kanban-status");
      const container = document.getElementById("kanban-cards");
      if (!payload.ok) {
        statusline.textContent = "Erreur";
        container.innerHTML = `<div class="empty">${escapeHtml(payload.error || "Kanban indisponible")}</div>`;
        return;
      }
      const cards = payload.cards || [];
      statusline.textContent = `${cards.length} carte${cards.length > 1 ? "s" : ""}`;
      if (!cards.length) {
        container.innerHTML = `<div class="empty">Aucune carte correspondant aux filtres.</div>`;
        return;
      }
      container.innerHTML = cards.map(card => `
        <article class="card ${card.blocked ? "blocked" : ""} ${card.awaiting_jch ? "awaiting-jch" : ""}">
          <div class="card-head">
            <div class="card-title">${escapeHtml(card.title)}</div>
            <div class="meta">
              <span class="chip">${escapeHtml(card.project)}</span>
              <span class="chip">${escapeHtml(card.status)}</span>
              <span class="chip">${escapeHtml(card.owner)}</span>
            </div>
          </div>
          <div class="desc">${escapeHtml(card.description || "Sans description")}</div>
          <div class="labels">
            ${(card.labels || []).map(label => `<span class="chip">${escapeHtml(label)}</span>`).join("")}
          </div>
        </article>
      `).join("");
    }

    async function loadFilters() {
      const response = await fetch("/api/kanban/filters");
      const payload = await response.json();
      if (!response.ok || !payload.ok) {
        throw new Error(payload.error || "Filtres indisponibles");
      }
      document.getElementById("filter-project").innerHTML =
        `<option value="">Tous les projets</option>` +
        (payload.projects || []).map(project => `<option value="${escapeHtml(project)}">${escapeHtml(project)}</option>`).join("");
      document.getElementById("filter-status").innerHTML =
        `<option value="">Tous les statuts</option>` +
        (payload.statuses || []).map(status => `<option value="${escapeHtml(status)}">${escapeHtml(status)}</option>`).join("");
      document.getElementById("filter-owner").innerHTML =
        `<option value="">Tous les owners</option>` +
        (payload.owners || []).map(owner => `<option value="${escapeHtml(owner)}">${escapeHtml(owner)}</option>`).join("");
    }

    async function loadCards() {
      const params = new URLSearchParams();
      const project = document.getElementById("filter-project").value;
      const status = document.getElementById("filter-status").value;
      const owner = document.getElementById("filter-owner").value;
      const awaiting = document.getElementById("filter-awaiting-jch").checked;
      if (project) params.set("project", project);
      if (status) params.set("status", status);
      if (owner) params.set("owner", owner);
      if (awaiting) params.set("awaiting_jch", "1");
      document.getElementById("kanban-status").textContent = "Chargement...";
      const response = await fetch(`/api/kanban/cards?${params.toString()}`);
      const payload = await response.json();
      renderCards(payload);
    }

    async function boot() {
      try {
        await loadFilters();
        await loadCards();
      } catch (error) {
        renderCards({ ok: False, error: String(error) });
      }
    }

    document.getElementById("filter-project").addEventListener("change", () => { loadCards().catch(() => {}); });
    document.getElementById("filter-status").addEventListener("change", () => { loadCards().catch(() => {}); });
    document.getElementById("filter-owner").addEventListener("change", () => { loadCards().catch(() => {}); });
    document.getElementById("filter-awaiting-jch").addEventListener("change", () => { loadCards().catch(() => {}); });
    boot().catch(() => {});
  </script>
```

- [ ] **Step 2: Fix the `False` typo and ensure the final script is valid**

Update the `boot()` catch block so the final code is:

```html
    async function boot() {
      try {
        await loadFilters();
        await loadCards();
      } catch (error) {
        renderCards({ ok: false, error: String(error) });
      }
    }
```

- [ ] **Step 3: Commit**

```bash
git add JCH_Inbox/01_DASHBOARDS/kanban.html
git commit -m "feat: add kanban list dashboard controller"
```

### Task 5: Link the new kanban page from the hub

**Files:**
- Modify: `JCH_Inbox/01_DASHBOARDS/hub.html`

- [ ] **Step 1: Add the navigation card**

Add this card inside the `Navigation superviseur` grid in `JCH_Inbox/01_DASHBOARDS/hub.html`:

```html
      <a class="dash-card" href="kanban.html">
        <div class="dash-card-icon">🗃️</div>
        <div class="dash-card-title">Liste Kanban</div>
        <div class="dash-card-desc">Vue filtrable des cartes Plane normalisées par projet, statut, owner et attente JCH.</div>
        <div class="dash-card-tag">kanban.html</div>
      </a>
```

- [ ] **Step 2: Commit**

```bash
git add JCH_Inbox/01_DASHBOARDS/hub.html
git commit -m "feat: link kanban list from hub"
```

### Task 6: Final verification

**Files:**
- Test: `tests/test_pka_kanban_service.py`
- Test: `tests/test_dashboard_kanban_endpoints.py`
- Runtime: `scripts/dashboard_server.py`
- Runtime: `JCH_Inbox/01_DASHBOARDS/kanban.html`

- [ ] **Step 1: Run the full automated checks**

Run:

```bash
python3 -m unittest tests.test_pka_kanban_service tests.test_dashboard_kanban_endpoints tests.test_pka_plane_adapter
```

Expected: PASS

- [ ] **Step 2: Run the local server and verify endpoints**

Run:

```bash
python3 scripts/dashboard_server.py --host 127.0.0.1 --port 8792
```

In another shell, run:

```bash
curl --silent --show-error "http://127.0.0.1:8792/api/kanban/filters"
curl --silent --show-error "http://127.0.0.1:8792/api/kanban/cards?awaiting_jch=1"
```

Expected:
- first payload includes `projects`, `statuses`, `owners`
- second payload includes `{ "ok": true, "cards": [...] }`

- [ ] **Step 3: Open the dashboard page and verify manual behavior**

Open:

```bash
open http://127.0.0.1:8792/kanban.html
```

Manual checks:
- filters load without JS error
- card count updates after filter changes
- awaiting-JCH toggle narrows the list
- empty state renders cleanly when no card matches

- [ ] **Step 4: Commit final integration**

```bash
git add tests/test_pka_kanban_service.py tests/test_dashboard_kanban_endpoints.py scripts/pka_kanban_service.py scripts/dashboard_server.py JCH_Inbox/01_DASHBOARDS/kanban.html JCH_Inbox/01_DASHBOARDS/hub.html
git commit -m "feat: add pka kanban card list dashboard"
```
