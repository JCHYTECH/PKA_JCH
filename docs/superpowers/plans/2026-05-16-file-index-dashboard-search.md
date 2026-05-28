# File Index Dashboard Search Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an elegant `file_index` search block to the PKA hub dashboard with keyword search, project/component filters, direct file open, and parent-folder open.

**Architecture:** Extend `scripts/dashboard_server.py` with small JSON endpoints backed by `scripts/rebuild_file_index.py`, then render a compact search section inside `JCH_Inbox/01_DASHBOARDS/hub.html` with lightweight client-side filtering state. Keep the backend authoritative for result ranking and keep the frontend focused on presentation and interaction.

**Tech Stack:** [[Python]] 3, [[SQLite]], 

---

### Task 1: Add backend tests for file-index dashboard endpoints

**Files:**
- Modify: `tests/test_dashboard_kanban_endpoints.py`
- Reference: `scripts/dashboard_server.py`

- [ ] **Step 1: Write the failing tests**

Add these tests to `tests/test_dashboard_kanban_endpoints.py`:

```python
    def test_file_index_search_endpoint_uses_backend_search(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/file-index/search?q=wild&project_key=03_WILDNEXUS&component=03.01%20BIOACOUSTIC"
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
            dashboard_server.rebuild_file_index,
            "search_index",
            return_value=[{"filename": "WildNexus_MASTER_ARCHITECTURE.md", "file_path": "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/WildNexus_MASTER_ARCHITECTURE.md"}],
        ) as search_mock:
            dashboard_server.DashboardHandler.do_GET(handler)

        search_mock.assert_called_once_with(
            dashboard_server.TEAM_DB,
            "wild",
            project_key="03_WILDNEXUS",
            component="03.01 BIOACOUSTIC",
            limit=20,
        )
        self.assertEqual(payloads[0][0], 200)
        self.assertEqual(payloads[0][1]["results"][0]["filename"], "WildNexus_MASTER_ARCHITECTURE.md")

    def test_file_index_filters_endpoint_returns_projects_and_components(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/file-index/filters"
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
            dashboard_server.rebuild_file_index,
            "available_filters",
            return_value={
                "projects": ["03_WILDNEXUS", "06_PHOTO_NATURE"],
                "components": {
                    "03_WILDNEXUS": ["03.01 BIOACOUSTIC", "03.02 FAUNE_AUTOUR_APP"],
                    "06_PHOTO_NATURE": [],
                },
            },
        ):
            dashboard_server.DashboardHandler.do_GET(handler)

        self.assertEqual(payloads[0][0], 200)
        self.assertIn("03_WILDNEXUS", payloads[0][1]["projects"])
        self.assertIn("03.01 BIOACOUSTIC", payloads[0][1]["components"]["03_WILDNEXUS"])
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_dashboard_kanban_endpoints -v
```

Expected: FAIL because `dashboard_server` does not yet expose file-index endpoints or `rebuild_file_index` helpers.

- [ ] **Step 3: Commit failing-test checkpoint**

```bash
git add tests/test_dashboard_kanban_endpoints.py
git commit -m "test: cover dashboard file index endpoints"
```

### Task 2: Extend file-index backend helpers for dashboard use

**Files:**
- Modify: `scripts/rebuild_file_index.py`
- Test: `tests/test_rebuild_file_index.py`

- [ ] **Step 1: Write the failing helper tests**

Add these tests to `tests/test_rebuild_file_index.py`:

```python
    def test_search_supports_component_filter(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")
        results = rebuild_file_index.search_index(
            self.db_path,
            "faune",
            project_key="03_WILDNEXUS",
            component="03.02 FAUNE_AUTOUR_APP",
        )
        self.assertEqual(results[0]["component"], "03.02 FAUNE_AUTOUR_APP")

    def test_available_filters_lists_projects_and_components(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")
        filters = rebuild_file_index.available_filters(self.db_path)
        self.assertIn("03_WILDNEXUS", filters["projects"])
        self.assertIn("03.01 BIOACOUSTIC", filters["components"]["03_WILDNEXUS"])
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_rebuild_file_index -v
```

Expected: FAIL because `search_index` does not yet accept `component` and `available_filters` does not exist.

- [ ] **Step 3: Write minimal implementation**

Update `scripts/rebuild_file_index.py`:

```python
def search_index(
    db_path: Path,
    query: str,
    project_key: str | None = None,
    component: str | None = None,
    limit: int = 20,
) -> list[dict]:
    needle = f"%{query.lower()}%"
    sql = """
        SELECT
            filename,
            file_path,
            category,
            project_key,
            component,
            CASE
                WHEN lower(filename) = ? THEN 300
                WHEN lower(filename) LIKE ? THEN 200
                WHEN lower(file_path) LIKE ? THEN 100
                ELSE 0
            END AS rank
        FROM file_index
        WHERE exists_on_disk = 1
          AND (lower(filename) LIKE ? OR lower(file_path) LIKE ? OR lower(COALESCE(tags, '')) LIKE ?)
    """
    params: list[object] = [query.lower(), needle, needle, needle, needle, needle]
    if project_key:
        sql += " AND project_key = ?"
        params.append(project_key)
    if component:
        sql += " AND component = ?"
        params.append(component)
    sql += " ORDER BY rank DESC, filename ASC LIMIT ?"
    params.append(limit)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, params).fetchall()
    return [dict(row) for row in rows]


def available_filters(db_path: Path) -> dict:
    with sqlite3.connect(db_path) as conn:
        projects = [
            row[0]
            for row in conn.execute(
                "SELECT DISTINCT project_key FROM file_index WHERE exists_on_disk = 1 AND project_key IS NOT NULL ORDER BY project_key"
            )
        ]
        components: dict[str, list[str]] = {}
        for project_key in projects:
            components[project_key] = [
                row[0]
                for row in conn.execute(
                    "SELECT DISTINCT component FROM file_index WHERE exists_on_disk = 1 AND project_key = ? AND component IS NOT NULL ORDER BY component",
                    (project_key,),
                )
            ]
    return {"projects": projects, "components": components}
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```bash
python3 -m unittest tests.test_rebuild_file_index -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/rebuild_file_index.py tests/test_rebuild_file_index.py
git commit -m "feat: add file index search filters"
```

### Task 3: Add dashboard server JSON endpoints

**Files:**
- Modify: `scripts/dashboard_server.py`
- Test: `tests/test_dashboard_kanban_endpoints.py`

- [ ] **Step 1: Implement helper responders**

Add near the other dashboard helpers in `scripts/dashboard_server.py`:

```python
from scripts import rebuild_file_index


def file_index_search_payload(query: str, project_key: str | None, component: str | None, limit: int = 20) -> dict:
    cleaned_query = query.strip()
    if len(cleaned_query) < 2:
        return {"ok": True, "results": []}
    results = rebuild_file_index.search_index(
        TEAM_DB,
        cleaned_query,
        project_key=project_key or None,
        component=component or None,
        limit=max(1, min(limit, 50)),
    )
    return {"ok": True, "results": results}


def file_index_filters_payload() -> dict:
    filters = rebuild_file_index.available_filters(TEAM_DB)
    return {"ok": True, **filters}
```

- [ ] **Step 2: Wire GET routes**

Inside `DashboardHandler.do_GET`, add:

```python
        if path == "/api/file-index/search":
            params = parse_qs(parsed.query)
            payload = file_index_search_payload(
                params.get("q", [""])[0],
                params.get("project_key", [""])[0] or None,
                params.get("component", [""])[0] or None,
                int(params.get("limit", ["20"])[0] or 20),
            )
            self.send_json(payload)
            return

        if path == "/api/file-index/filters":
            self.send_json(file_index_filters_payload())
            return
```

- [ ] **Step 3: Run endpoint tests**

Run:

```bash
python3 -m unittest tests.test_dashboard_kanban_endpoints -v
```

Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add scripts/dashboard_server.py tests/test_dashboard_kanban_endpoints.py
git commit -m "feat: expose file index dashboard endpoints"
```

### Task 4: Add the dashboard search block markup and styling

**Files:**
- Modify: `JCH_Inbox/01_DASHBOARDS/hub.html`

- [ ] **Step 1: Add failing frontend expectation notes**

Document the expected DOM hooks in a temporary checklist comment near the dashboard sections:

```html
<!-- file-index dashboard block requires:
  #file-index-query
  #file-index-project
  #file-index-component
  #file-index-results
-->
```

- [ ] **Step 2: Add minimal markup**

Insert a new section above the project portfolio:

```html
  <div class="section">
    <div class="section-title">
      <span>Index fichiers PKA</span>
      <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--ocre);">Recherche + filtres</span>
    </div>
    <div class="file-index-shell">
      <div class="file-index-toolbar">
        <input id="file-index-query" class="file-index-input" type="search" placeholder="Retrouver un fichier PKA">
        <select id="file-index-project" class="file-index-select"><option value="">Tous les projets</option></select>
        <select id="file-index-component" class="file-index-select"><option value="">Tous les composants</option></select>
      </div>
      <div id="file-index-results" class="file-index-results">
        <div class="file-index-empty">Tape au moins 2 caracteres pour lancer la recherche.</div>
      </div>
    </div>
  </div>
```

- [ ] **Step 3: Add compact styles**

Add CSS near the other section/block styles:

```css
  .file-index-shell {
    background: white;
    border: 1px solid var(--sable);
    box-shadow: 0 8px 28px rgba(42,36,32,0.06);
    padding: 18px;
  }
  .file-index-toolbar {
    display: grid;
    grid-template-columns: minmax(260px, 1.4fr) minmax(180px, 0.8fr) minmax(180px, 0.8fr);
    gap: 10px;
    margin-bottom: 14px;
  }
  .file-index-input,
  .file-index-select {
    min-height: 42px;
    border: 1px solid var(--sable);
    background: #fbfaf8;
    padding: 0 12px;
    font: inherit;
    color: var(--noir);
  }
  .file-index-results {
    display: grid;
    gap: 10px;
  }
  .file-index-result {
    border-left: 3px solid var(--sable);
    background: #fbfaf8;
    padding: 12px 14px;
  }
  .file-index-head {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 6px;
  }
  .file-index-name {
    font-size: 13px;
    font-weight: 600;
  }
  .file-index-meta,
  .file-index-path,
  .file-index-empty {
    color: var(--gris);
    font-size: 11px;
    line-height: 1.5;
  }
  .file-index-actions {
    display: flex;
    gap: 8px;
    margin-top: 8px;
  }
  .file-index-action {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    text-decoration: none;
    color: var(--ocre);
  }
```

- [ ] **Step 4: Commit**

```bash
git add JCH_Inbox/01_DASHBOARDS/hub.html
git commit -m "feat: add file index dashboard block layout"
```

### Task 5: Add the frontend search controller

**Files:**
- Modify: `JCH_Inbox/01_DASHBOARDS/hub.html`

- [ ] **Step 1: Add minimal JavaScript controller**

Append a focused script near the existing `loadHealth()` / dashboard JS:

```javascript
  let fileIndexFilters = { projects: [], components: {} };
  let fileIndexTimer = null;

  function escapeHtml(value) {
    return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;');
  }

  function parentHref(filePath) {
    const parent = filePath.split('/').slice(0, -1).join('/');
    return '/' + parent;
  }

  function fileHref(filePath) {
    return '/' + filePath;
  }

  function renderFileIndexResults(results) {
    const root = document.getElementById('file-index-results');
    if (!results.length) {
      root.innerHTML = '<div class="file-index-empty">Aucun fichier correspondant</div>';
      return;
    }
    root.innerHTML = results.map((row) => `
      <div class="file-index-result">
        <div class="file-index-head">
          <div class="file-index-name">${escapeHtml(row.filename)}</div>
          <div class="file-index-meta">${escapeHtml(row.category || '')}</div>
        </div>
        <div class="file-index-meta">${escapeHtml(row.project_key || 'PKA')} ${row.component ? '· ' + escapeHtml(row.component) : ''}</div>
        <div class="file-index-path">${escapeHtml(row.file_path)}</div>
        <div class="file-index-actions">
          <a class="file-index-action" href="${fileHref(row.file_path)}">ouvrir fichier</a>
          <a class="file-index-action" href="${parentHref(row.file_path)}">ouvrir dossier</a>
        </div>
      </div>
    `).join('');
  }

  function syncComponentOptions() {
    const project = document.getElementById('file-index-project').value;
    const component = document.getElementById('file-index-component');
    const values = project ? (fileIndexFilters.components[project] || []) : [];
    component.innerHTML = '<option value="">Tous les composants</option>' + values.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`).join('');
  }

  async function loadFileIndexFilters() {
    const response = await fetch('/api/file-index/filters');
    const payload = await response.json();
    fileIndexFilters = payload;
    const project = document.getElementById('file-index-project');
    project.innerHTML = '<option value="">Tous les projets</option>' + payload.projects.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`).join('');
    syncComponentOptions();
  }

  async function runFileIndexSearch() {
    const query = document.getElementById('file-index-query').value.trim();
    if (query.length < 2) {
      document.getElementById('file-index-results').innerHTML = '<div class="file-index-empty">Tape au moins 2 caracteres pour lancer la recherche.</div>';
      return;
    }
    const project = document.getElementById('file-index-project').value;
    const component = document.getElementById('file-index-component').value;
    const params = new URLSearchParams({ q: query });
    if (project) params.set('project_key', project);
    if (component) params.set('component', component);
    const response = await fetch(`/api/file-index/search?${params.toString()}`);
    const payload = await response.json();
    renderFileIndexResults(payload.results || []);
  }
```

- [ ] **Step 2: Add event wiring**

Append:

```javascript
  document.getElementById('file-index-query').addEventListener('input', () => {
    clearTimeout(fileIndexTimer);
    fileIndexTimer = setTimeout(runFileIndexSearch, 180);
  });
  document.getElementById('file-index-project').addEventListener('change', () => {
    syncComponentOptions();
    runFileIndexSearch();
  });
  document.getElementById('file-index-component').addEventListener('change', runFileIndexSearch);
  loadFileIndexFilters();
```

- [ ] **Step 3: Manual verification**

Run the dashboard server, open `hub.html`, and verify:

```bash
python3 scripts/dashboard_server.py
```

Expected:
- block visible and stylistically coherent
- typing `wildnexus` shows results
- project filter narrows results
- component filter narrows results
- `ouvrir fichier` opens the file target
- `ouvrir dossier` opens the parent directory target

- [ ] **Step 4: Commit**

```bash
git add JCH_Inbox/01_DASHBOARDS/hub.html
git commit -m "feat: wire dashboard file index search"
```

### Task 6: Final verification

**Files:**
- Verify: `scripts/dashboard_server.py`
- Verify: `scripts/rebuild_file_index.py`
- Verify: `JCH_Inbox/01_DASHBOARDS/hub.html`
- Verify: `tests/test_rebuild_file_index.py`
- Verify: `tests/test_dashboard_kanban_endpoints.py`

- [ ] **Step 1: Run backend tests**

```bash
python3 -m unittest tests.test_rebuild_file_index tests.test_dashboard_kanban_endpoints tests.test_pka_plane_adapter
```

Expected: PASS

- [ ] **Step 2: Rescan file index**

```bash
python3 scripts/rebuild_file_index.py rescan
```

Expected: non-zero scanned count, no crash

- [ ] **Step 3: Smoke-test dashboard search from CLI**

```bash
python3 scripts/rebuild_file_index.py search wildnexus --project-key 03_WILDNEXUS --limit 5
```

Expected: visible `03_WILDNEXUS` results

- [ ] **Step 4: Commit final integration**

```bash
git add scripts/dashboard_server.py scripts/rebuild_file_index.py JCH_Inbox/01_DASHBOARDS/hub.html tests/test_rebuild_file_index.py tests/test_dashboard_kanban_endpoints.py docs/superpowers/specs/2026-05-16-file-index-dashboard-search-design.md docs/superpowers/plans/2026-05-16-file-index-dashboard-search.md
git commit -m "feat: add dashboard file index search"
```
