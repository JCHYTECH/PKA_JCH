# PKA Kanban Plane Implementation Plan

> **For agentic workers:** REQUIRED SUB-[[SKILL]]: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Plane-backed transversal kanban layer to PKA with one canonical workflow, governed labels, project mappings, and dashboard visibility.

**Architecture:** Keep Plane as the external source of truth, but codify all PKA semantics locally in versioned schema/config files plus a small [[Python]] adapter/service layer. Extend the existing dashboard server to expose kanban summary APIs and update the hub UI to display normalized project and validation/blocker views without inventing a second task database.

**Tech Stack:** [[Python]] 3 standard library, JSON config files in 

---

### Task 1: Add regression tests and canonical schema files for the PKA kanban vocabulary

**Files:**
- Create: `tests/test_pka_kanban_schema.py`
- Create: `JCH_Inbox/99_SYSTEM/pka_kanban_schema.json`
- Create: `JCH_Inbox/99_SYSTEM/pka_kanban_governance.json`
- Create: `scripts/pka_kanban_schema.py`
- Test: `tests/test_pka_kanban_schema.py`

- [ ] **Step 1: Write the failing tests**

```python
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import pka_kanban_schema


class PkaKanbanSchemaTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        (self.root / "JCH_Inbox" / "99_SYSTEM").mkdir(parents=True)
        (self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_schema.json").write_text(
            json.dumps(
                {
                    "statuses": [
                        "A qualifier",
                        "Pret",
                        "En cours",
                        "En attente",
                        "En validation",
                        "Termine",
                        "Archive",
                    ],
                    "types": ["task", "decision", "document", "bug", "idea", "follow-up", "deliverable"],
                    "required_fields": ["title", "project", "type", "owner", "priority", "status", "description"],
                }
            ),
            encoding="utf-8",
        )
        (self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json").write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["decision", "execution", "research", "document", "follow-up", "bug", "idea"],
                        "domain": ["legal", "finance", "tech", "photo", "branding", "ops", "travel", "science"],
                        "context": ["urgent", "bloque-externe", "en-attente-jch", "delegue", "a-planifier", "quick-win"],
                        "level": ["strategique", "tactique", "operationnel"],
                    }
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_load_schema_returns_expected_statuses(self):
        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            schema = pka_kanban_schema.load_schema()

        self.assertEqual(
            schema["statuses"],
            ["A qualifier", "Pret", "En cours", "En attente", "En validation", "Termine", "Archive"],
        )

    def test_duplicate_labels_are_rejected(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["decision", "decision"],
                        "domain": [],
                        "context": [],
                        "level": [],
                    }
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaises(ValueError):
                pka_kanban_schema.load_governance()


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_pka_kanban_schema -v`
Expected: FAIL because `scripts/pka_kanban_schema.py` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

Create `JCH_Inbox/99_SYSTEM/pka_kanban_schema.json` with this initial content:

```json
{
  "statuses": [
    "A qualifier",
    "Pret",
    "En cours",
    "En attente",
    "En validation",
    "Termine",
    "Archive"
  ],
  "types": [
    "task",
    "decision",
    "document",
    "bug",
    "idea",
    "follow-up",
    "deliverable"
  ],
  "required_fields": [
    "title",
    "project",
    "type",
    "owner",
    "priority",
    "status",
    "description"
  ],
  "recommended_fields": [
    "lead_specialist",
    "model_used",
    "decision_owner",
    "blocking_reason",
    "expected_outcome",
    "source_link"
  ]
}
```

Create `JCH_Inbox/99_SYSTEM/pka_kanban_governance.json` with this initial content:

```json
{
  "labels": {
    "nature": ["decision", "execution", "research", "document", "follow-up", "bug", "idea"],
    "domain": ["legal", "finance", "tech", "photo", "branding", "ops", "travel", "science"],
    "context": ["urgent", "bloque-externe", "en-attente-jch", "delegue", "a-planifier", "quick-win"],
    "level": ["strategique", "tactique", "operationnel"]
  },
  "rules": {
    "lowercase_only": true,
    "separator": "-",
    "state_labels_forbidden": true,
    "creation_roles": ["Dobby", "Forge"]
  }
}
```

Create `scripts/pka_kanban_schema.py` with this minimal implementation:

```python
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSTEM_DIR = ROOT / "JCH_Inbox" / "99_SYSTEM"
SCHEMA_PATH = SYSTEM_DIR / "pka_kanban_schema.json"
GOVERNANCE_PATH = SYSTEM_DIR / "pka_kanban_governance.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schema() -> dict:
    data = _load_json(SCHEMA_PATH)
    if data["statuses"] != [
        "A qualifier",
        "Pret",
        "En cours",
        "En attente",
        "En validation",
        "Termine",
        "Archive",
    ]:
        raise ValueError("canonical status order drift")
    return data


def load_governance() -> dict:
    data = _load_json(GOVERNANCE_PATH)
    labels = []
    for family in data["labels"].values():
        labels.extend(family)
    if len(labels) != len(set(labels)):
        raise ValueError("duplicate labels are forbidden")
    return data
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_pka_kanban_schema -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add tests/test_pka_kanban_schema.py JCH_Inbox/99_SYSTEM/pka_kanban_schema.json JCH_Inbox/99_SYSTEM/pka_kanban_governance.json scripts/pka_kanban_schema.py
  git commit -m "feat: add pka kanban schema and governance"
else
  echo "skip commit: repository not initialized"
fi
```

### Task 2: Add project registry and Plane connection configuration

**Files:**
- Create: `tests/test_pka_plane_adapter.py`
- Create: `JCH_Inbox/99_SYSTEM/pka_plane_config.json`
- Create: `scripts/pka_plane_adapter.py`
- Test: `tests/test_pka_plane_adapter.py`

- [ ] **Step 1: Write the failing tests**

```python
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import pka_plane_adapter


class PkaPlaneAdapterTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        (self.root / "JCH_Inbox" / "99_SYSTEM").mkdir(parents=True)
        (self.root / "JCH_Inbox" / "03_PROJECTS").mkdir(parents=True)
        for key in ("01_AI_IT_TOOLS", "02_ARTEON", "03_FAUNE_AUTOUR", "08_VETALYX"):
            (self.root / "JCH_Inbox" / "03_PROJECTS" / key).mkdir()
        (self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_plane_config.json").write_text(
            json.dumps(
                {
                    "workspace_slug": "pka-jch",
                    "api_base": "https://plane.example/api/v1",
                    "projects": {
                        "01_AI_IT_TOOLS": {"plane_project_id": "ai-tools"},
                        "02_ARTEON": {"plane_project_id": "arteon"},
                        "08_VETALYX": {"plane_project_id": "vetalyx"}
                    }
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_load_config_returns_known_project_mapping(self):
        with mock.patch.object(pka_plane_adapter, "ROOT", self.root):
            config = pka_plane_adapter.load_config()

        self.assertEqual(config["projects"]["02_ARTEON"]["plane_project_id"], "arteon")

    def test_validate_project_registry_detects_missing_mapping(self):
        with mock.patch.object(pka_plane_adapter, "ROOT", self.root):
            self.assertEqual(
                pka_plane_adapter.validate_project_registry(),
                ["03_PROJECTS project directory missing from Plane config: 03_FAUNE_AUTOUR"]
            )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_pka_plane_adapter -v`
Expected: FAIL because `scripts/pka_plane_adapter.py` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

Create `JCH_Inbox/99_SYSTEM/pka_plane_config.json` with this initial content:

```json
{
  "workspace_slug": "pka-jch",
  "api_base": "https://plane.example/api/v1",
  "api_token_env": "PKA_PLANE_API_TOKEN",
  "projects": {
    "01_AI_IT_TOOLS": { "plane_project_id": "" },
    "02_ARTEON": { "plane_project_id": "" },
    "03_FAUNE_AUTOUR": { "plane_project_id": "" },
    "04_NUANCES": { "plane_project_id": "" },
    "05_PHOTO_AI_JURY": { "plane_project_id": "" },
    "06_PHOTO_NATURE": { "plane_project_id": "" },
    "07_TRAVELS": { "plane_project_id": "" },
    "08_VETALYX": { "plane_project_id": "" }
  }
}
```

Create `scripts/pka_plane_adapter.py` with:

```python
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "JCH_Inbox" / "99_SYSTEM" / "pka_plane_config.json"
PROJECTS_DIR = ROOT / "JCH_Inbox" / "03_PROJECTS"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def plane_token() -> str | None:
    config = load_config()
    return os.environ.get(config["api_token_env"])


def validate_project_registry() -> list[str]:
    config = load_config()
    mapped = set(config["projects"].keys())
    findings = []
    for item in sorted(PROJECTS_DIR.iterdir()):
        if item.is_dir() and item.name not in mapped:
            findings.append(f"03_PROJECTS project directory missing from Plane config: {item.name}")
    return findings
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_pka_plane_adapter -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add tests/test_pka_plane_adapter.py JCH_Inbox/99_SYSTEM/pka_plane_config.json scripts/pka_plane_adapter.py
  git commit -m "feat: add plane config and project registry"
else
  echo "skip commit: repository not initialized"
fi
```

### Task 3: Add a normalized kanban service layer and summary tests

**Files:**
- Create: `tests/test_pka_kanban_service.py`
- Create: `scripts/pka_kanban_service.py`
- Test: `tests/test_pka_kanban_service.py`

- [ ] **Step 1: Write the failing tests**

```python
import unittest

from scripts import pka_kanban_service


class PkaKanbanServiceTest(unittest.TestCase):
    def test_build_summary_counts_statuses_and_validation_queue(self):
        cards = [
            {"project": "02_ARTEON", "status": "En cours", "labels": ["branding"], "lead_specialist": "Vega"},
            {"project": "02_ARTEON", "status": "En validation", "labels": ["en-attente-jch"], "lead_specialist": "Dobby"},
            {"project": "08_VETALYX", "status": "En attente", "labels": ["bloque-externe"], "lead_specialist": "Renard"},
        ]

        summary = pka_kanban_service.build_summary(cards)

        self.assertEqual(summary["totals"]["En cours"], 1)
        self.assertEqual(summary["totals"]["En validation"], 1)
        self.assertEqual(summary["blocked"], 1)
        self.assertEqual(summary["awaiting_jch"], 1)
        self.assertEqual(summary["by_project"]["02_ARTEON"]["total"], 2)

    def test_validate_card_rejects_unknown_status(self):
        with self.assertRaises(ValueError):
            pka_kanban_service.validate_card(
                {
                    "title": "Bad card",
                    "project": "02_ARTEON",
                    "type": "task",
                    "owner": "Dobby",
                    "priority": "haute",
                    "status": "Doing",
                    "description": "wrong status"
                }
            )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_pka_kanban_service -v`
Expected: FAIL because `scripts/pka_kanban_service.py` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

Create `scripts/pka_kanban_service.py` with:

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


def build_summary(cards: list[dict]) -> dict:
    totals = Counter()
    by_project = defaultdict(lambda: {"total": 0})
    blocked = 0
    awaiting_jch = 0

    for raw_card in cards:
        card = validate_card(raw_card)
        totals[card["status"]] += 1
        by_project[card["project"]]["total"] += 1
        if card["status"] == "En attente":
            blocked += 1
        if card["status"] == "En validation" and "en-attente-jch" in card.get("labels", []):
            awaiting_jch += 1

    return {
        "totals": dict(totals),
        "blocked": blocked,
        "awaiting_jch": awaiting_jch,
        "by_project": dict(by_project),
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_pka_kanban_service -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add tests/test_pka_kanban_service.py scripts/pka_kanban_service.py
  git commit -m "feat: add normalized kanban summary service"
else
  echo "skip commit: repository not initialized"
fi
```

### Task 4: Add Plane client fetch hooks and local bootstrap verification

**Files:**
- Modify: `scripts/pka_plane_adapter.py`
- Modify: `tests/test_pka_plane_adapter.py`
- Create: `scripts/pka_kanban_bootstrap.py`
- Create: `tests/test_pka_kanban_bootstrap.py`
- Test: `tests/test_pka_plane_adapter.py`
- Test: `tests/test_pka_kanban_bootstrap.py`

- [ ] **Step 1: Write the failing tests**

Append these tests to `tests/test_pka_plane_adapter.py`:

```python
    def test_normalize_issue_maps_plane_fields_to_pka_card(self):
        issue = {
            "name": "Prepare ARTEON palette",
            "state": {"name": "En validation"},
            "label_details": [{"name": "branding"}, {"name": "en-attente-jch"}],
            "assignee": {"display_name": "Dobby"},
        }
        normalized = pka_plane_adapter.normalize_issue("02_ARTEON", issue)
        self.assertEqual(normalized["project"], "02_ARTEON")
        self.assertEqual(normalized["status"], "En validation")
        self.assertEqual(normalized["owner"], "Dobby")
```

Create `tests/test_pka_kanban_bootstrap.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import pka_kanban_bootstrap


class PkaKanbanBootstrapTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        (self.root / "JCH_Inbox" / "03_PROJECTS").mkdir(parents=True)
        for key in ("01_AI_IT_TOOLS", "02_ARTEON"):
            (self.root / "JCH_Inbox" / "03_PROJECTS" / key).mkdir()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_build_manifest_lists_all_project_boards(self):
        with mock.patch.object(pka_kanban_bootstrap, "ROOT", self.root):
            manifest = pka_kanban_bootstrap.build_manifest()

        self.assertEqual(
            manifest["projects"],
            [
                {"key": "01_AI_IT_TOOLS", "name": "01_AI_IT_TOOLS"},
                {"key": "02_ARTEON", "name": "02_ARTEON"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_pka_plane_adapter tests.test_pka_kanban_bootstrap -v`
Expected: FAIL because `normalize_issue()` and `scripts/pka_kanban_bootstrap.py` do not exist yet.

- [ ] **Step 3: Write minimal implementation**

Extend `scripts/pka_plane_adapter.py` with:

```python
from urllib import request


def normalize_issue(project_key: str, issue: dict) -> dict:
    labels = [item["name"] for item in issue.get("label_details", [])]
    return {
        "title": issue["name"],
        "project": project_key,
        "type": "task",
        "owner": issue.get("assignee", {}).get("display_name", "Unassigned"),
        "priority": "normale",
        "status": issue["state"]["name"],
        "description": issue.get("description_html") or issue.get("description_stripped") or "",
        "labels": labels,
    }


def fetch_project_issues(project_key: str) -> list[dict]:
    raise NotImplementedError("Plane API fetch to be implemented against real workspace credentials")
```

Create `scripts/pka_kanban_bootstrap.py` with:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "JCH_Inbox" / "03_PROJECTS"


def build_manifest() -> dict:
    return {
        "projects": [
            {"key": item.name, "name": item.name}
            for item in sorted(PROJECTS_DIR.iterdir())
            if item.is_dir()
        ]
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_pka_plane_adapter tests.test_pka_kanban_bootstrap -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add tests/test_pka_plane_adapter.py tests/test_pka_kanban_bootstrap.py scripts/pka_plane_adapter.py scripts/pka_kanban_bootstrap.py
  git commit -m "feat: add plane issue normalization and bootstrap manifest"
else
  echo "skip commit: repository not initialized"
fi
```

### Task 5: Extend the dashboard server with kanban summary endpoints

**Files:**
- Modify: `scripts/dashboard_server.py`
- Create: `tests/test_dashboard_kanban_endpoints.py`
- Test: `tests/test_dashboard_kanban_endpoints.py`

- [ ] **Step 1: Write the failing tests**

```python
import unittest
from unittest import mock

from scripts import dashboard_server


class DashboardKanbanEndpointsTest(unittest.TestCase):
    def test_dashboard_health_includes_kanban_stub(self):
        with mock.patch.object(dashboard_server, "kanban_snapshot", return_value={"totals": {"En cours": 2}, "blocked": 1, "awaiting_jch": 1}):
            health = dashboard_server.dashboard_health()

        self.assertEqual(health["kanban"]["blocked"], 1)
        self.assertEqual(health["kanban"]["awaitingJch"], 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_dashboard_kanban_endpoints -v`
Expected: FAIL because `dashboard_health()` does not yet expose kanban data and `kanban_snapshot()` does not exist.

- [ ] **Step 3: Write minimal implementation**

Add these functions near the other dashboard helpers in `scripts/dashboard_server.py`:

```python
from scripts import pka_kanban_service


def kanban_snapshot() -> dict:
    return {
        "totals": {},
        "blocked": 0,
        "awaiting_jch": 0,
        "by_project": {},
    }
```

Then update `dashboard_health()` to return:

```python
    kanban = kanban_snapshot()
    return {
        "ok": True,
        "teamActive": active_team_count(),
        "inboxPending": len(inbox),
        "projectsActive": len(projects),
        "latestDaily": latest_daily_note(),
        "latestDeliverable": latest[0]["name"] if latest else None,
        "kanban": {
            "blocked": kanban["blocked"],
            "awaitingJch": kanban["awaiting_jch"],
            "totals": kanban["totals"],
        },
    }
```

Add a new GET route:

```python
        if path == "/api/kanban/summary":
            self.send_json(kanban_snapshot())
            return
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_dashboard_kanban_endpoints -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add tests/test_dashboard_kanban_endpoints.py scripts/dashboard_server.py
  git commit -m "feat: expose kanban summary via dashboard api"
else
  echo "skip commit: repository not initialized"
fi
```

### Task 6: Add a kanban section to the PKA hub dashboard

**Files:**
- Modify: `JCH_Inbox/01_DASHBOARDS/hub.html`
- Test: manual browser verification against local dashboard server

- [ ] **Step 1: Add the kanban summary section markup**

Insert this block under the existing command panel in `JCH_Inbox/01_DASHBOARDS/hub.html`:

```html
<section class="section" id="kanban-overview">
  <div class="section-title">
    <span>Kanban PKA</span>
  </div>
  <div class="metrics-grid" id="kanban-metrics">
    <article class="metric ocre">
      <div class="metric-value" id="kanban-blocked">0</div>
      <div class="metric-label">Cartes bloquees</div>
    </article>
    <article class="metric vert">
      <div class="metric-value" id="kanban-validation">0</div>
      <div class="metric-label">En validation JCH</div>
    </article>
    <article class="metric ardoise">
      <div class="metric-value" id="kanban-in-progress">0</div>
      <div class="metric-label">En cours</div>
    </article>
    <article class="metric rouge">
      <div class="metric-value" id="kanban-ready">0</div>
      <div class="metric-label">Pret</div>
    </article>
  </div>
</section>
```

- [ ] **Step 2: Add the fetch logic**

Append this script near the existing dashboard data-loading script:

```html
<script>
async function loadKanbanSummary() {
  const response = await fetch("/api/kanban/summary");
  const summary = await response.json();
  document.getElementById("kanban-blocked").textContent = String(summary.blocked || 0);
  document.getElementById("kanban-validation").textContent = String(summary.awaiting_jch || 0);
  document.getElementById("kanban-in-progress").textContent = String((summary.totals || {})["En cours"] || 0);
  document.getElementById("kanban-ready").textContent = String((summary.totals || {})["Pret"] || 0);
}
</script>
```

- [ ] **Step 3: Run the local dashboard and verify manually**

Run: `python3 scripts/dashboard_server.py --host 127.0.0.1 --port 8787`
Expected: server starts and prints `PKA dashboards: http://127.0.0.1:8787`

Open `http://127.0.0.1:8787/01_DASHBOARDS/hub.html` in the Browser tool and verify:
- the new Kanban section appears
- counts render as `0` before live Plane data is wired in
- the page layout still works on desktop width and mobile width

- [ ] **Step 4: Stop the server after verification**

Expected: clean process termination with `Ctrl+C`

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add JCH_Inbox/01_DASHBOARDS/hub.html
  git commit -m "feat: add kanban overview to pka hub"
else
  echo "skip commit: repository not initialized"
fi
```

### Task 7: Add the governance SOP and rollout checklist

**Files:**
- Create: `wiki/SOPs/pka-kanban-governance.md`
- Create: `JCH_Inbox/90_TEMPLATES/pka-kanban-card-template.md`
- Create: `docs/system/pka-kanban-rollout-checklist.md`

- [ ] **Step 1: Write the governance SOP**

Create `wiki/SOPs/pka-kanban-governance.md` with these sections:

```markdown
# PKA Kanban Governance

## Canonical workflow
- A qualifier
- Pret
- En cours
- En attente
- En validation
- Termine
- Archive

## Label governance
- Only Dobby and Forge may create, rename, or delete transverse labels.
- Labels describing workflow state are forbidden.
- New labels require proof that status, type, field, or checklist cannot express the need.
- Monthly audit: duplicates, dead labels, synonyms, project-only drift.

## Required card fields
- title
- project
- type
- owner
- priority
- status
- description
```

- [ ] **Step 2: Write the reusable card template**

Create `JCH_Inbox/90_TEMPLATES/pka-kanban-card-template.md` with:

```markdown
# {{ title }}

- Project:
- Type:
- Owner:
- Priority:
- Lead specialist:
- Model used:
- Decision owner:
- Blocking reason:
- Expected outcome:
- Source link:

## Description

## Checklist
- [ ]

## Validation
- Reviewer:
- Decision:
```

- [ ] **Step 3: Write the rollout checklist**

Create `docs/system/pka-kanban-rollout-checklist.md` with:

```markdown
# PKA Kanban Rollout Checklist

- [ ] Confirm Plane workspace slug and API base
- [ ] Create one Plane project per folder in `JCH_Inbox/03_PROJECTS/`
- [ ] Fill every `plane_project_id` in `JCH_Inbox/99_SYSTEM/pka_plane_config.json`
- [ ] Create canonical statuses in Plane
- [ ] Create canonical labels from `JCH_Inbox/99_SYSTEM/pka_kanban_governance.json`
- [ ] Validate dashboard `/api/kanban/summary`
- [ ] Validate hub kanban section
- [ ] Run first monthly label audit
```

- [ ] **Step 4: Verify the new docs exist and are readable**

Run: `sed -n '1,220p' wiki/SOPs/pka-kanban-governance.md JCH_Inbox/90_TEMPLATES/pka-kanban-card-template.md docs/system/pka-kanban-rollout-checklist.md`
Expected: all three files print with the expected sections.

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add wiki/SOPs/pka-kanban-governance.md JCH_Inbox/90_TEMPLATES/pka-kanban-card-template.md docs/system/pka-kanban-rollout-checklist.md
  git commit -m "docs: add pka kanban governance and rollout guides"
else
  echo "skip commit: repository not initialized"
fi
```

### Task 8: Run the full local verification suite

**Files:**
- Modify: none
- Test: `tests/test_pka_kanban_schema.py`
- Test: `tests/test_pka_plane_adapter.py`
- Test: `tests/test_pka_kanban_service.py`
- Test: `tests/test_pka_kanban_bootstrap.py`
- Test: `tests/test_dashboard_kanban_endpoints.py`

- [ ] **Step 1: Run the targeted automated suite**

Run:

```bash
python3 -m unittest \
  tests.test_pka_kanban_schema \
  tests.test_pka_plane_adapter \
  tests.test_pka_kanban_service \
  tests.test_pka_kanban_bootstrap \
  tests.test_dashboard_kanban_endpoints \
  -v
```

Expected: all tests PASS

- [ ] **Step 2: Run the existing regression suite likely to be affected**

Run:

```bash
python3 -m unittest \
  tests.test_pka_system_check \
  tests.test_pka_system_improvement_audit \
  -v
```

Expected: PASS, proving the dashboard/system surface still behaves.

- [ ] **Step 3: Verify the config files are parseable**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path
for rel in [
    "JCH_Inbox/99_SYSTEM/pka_kanban_schema.json",
    "JCH_Inbox/99_SYSTEM/pka_kanban_governance.json",
    "JCH_Inbox/99_SYSTEM/pka_plane_config.json",
]:
    json.loads(Path(rel).read_text(encoding="utf-8"))
    print("OK", rel)
PY
```

Expected:

```text
OK JCH_Inbox/99_SYSTEM/pka_kanban_schema.json
OK JCH_Inbox/99_SYSTEM/pka_kanban_governance.json
OK JCH_Inbox/99_SYSTEM/pka_plane_config.json
```

- [ ] **Step 4: Record the implementation outcome**

Create or update the relevant project note with:

```markdown
## PKA Kanban rollout
- Plane-backed kanban layer scaffolded locally
- canonical statuses locked
- governance files committed locally
- dashboard summary endpoint available
```

- [ ] **Step 5: Commit**

```bash
if [ -d .git ]; then
  git add .
  git commit -m "feat: scaffold pka plane-backed kanban layer"
else
  echo "skip commit: repository not initialized"
fi
```

## Self-Review

Spec coverage checked:
- canonical workflow: Tasks 1, 3, 5, 7
- governed labels: Tasks 1 and 7
- standard card schema: Tasks 1 and 3
- Plane project mapping: Tasks 2 and 4
- dashboard integration: Tasks 5 and 6
- governance and rollout SOP: Task 7
- phased rollout and verification: Task 8

Placeholder scan checked:
- no `TBD`, `TODO`, or unresolved placeholder markers remain in the plan body
- every file path is concrete
- every verification step includes an exact command

Type consistency checked:
- canonical status spelling is consistent across schema, adapter, service, dashboard, and SOP tasks
- the config filenames are consistent across all tasks
- the dashboard route name `/api/kanban/summary` is reused consistently
