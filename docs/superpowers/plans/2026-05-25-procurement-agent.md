# Procurement Agent — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construire un agent procurement semi-autonome PKA qui lit une BOM (Excel/CSV/MD), interroge l'API Mouser (Search + Cart), enrichit la BOM, génère un rapport Markdown, et attend la validation JCH avant toute action.

**Architecture:** Scripts [[Python]] sur RPi (

**Tech Stack:** [[Python]] 3.11+, openpyxl, requests, anthropic SDK, python-dotenv, pytest, responses (mock HTTP)

**Spec:** `docs/superpowers/specs/2026-05-25-procurement-agent-design.md`

---

## Structure des fichiers

```
scripts/procurement/
├── __init__.py
├── models.py          # Dataclasses : Component, EnrichedComponent, BOMData
├── config.py          # Chargement .env, détection mode simulation
├── bom_parser.py      # Excel / CSV / MD → BOMData
├── api_client.py      # Mouser Search API + Cart API (+ simulation)
├── llm_reasoner.py    # Anthropic API : alternatives, scoring, narratif
├── bom_writer.py      # Enrichit BOM source (Excel ou CSV)
├── report_writer.py   # Génère rapport Markdown dans TEAM_Inbox/
└── main.py            # CLI entry point

tests/procurement/
├── __init__.py
├── fixtures/
│   ├── sample_bom.xlsx      # généré en Task 1
│   ├── sample_bom.csv
│   └── sample_bom.md
├── test_bom_parser.py
├── test_api_client.py
├── test_llm_reasoner.py
├── test_bom_writer.py
└── test_report_writer.py

.procurement.env               # à la racine home RPi — JAMAIS commité
```

---

## Task 1 : Setup — modèles, config, fixtures

**Files:**
- Create: `scripts/procurement/__init__.py`
- Create: `scripts/procurement/models.py`
- Create: `scripts/procurement/config.py`
- Create: `tests/procurement/__init__.py`
- Create: `tests/procurement/fixtures/sample_bom.csv`
- Create: `tests/procurement/fixtures/sample_bom.md`
- Create: `tests/procurement/fixtures/generate_fixture_xlsx.py`

---

- [ ] **Step 1 : Créer l'arborescence**

```bash
cd /Users/jchavauxm5/PKA_JCH
mkdir -p scripts/procurement tests/procurement/fixtures
touch scripts/procurement/__init__.py tests/procurement/__init__.py
```

- [ ] **Step 2 : Écrire `models.py`**

```python
# scripts/procurement/models.py
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Component:
    ref: str
    description: str
    qty: int
    mpn: str = ""
    preferred_supplier: str = ""
    category: str = ""
    notes: str = ""


@dataclass
class EnrichedComponent:
    component: Component
    price_unit: Optional[float] = None
    currency: str = "EUR"
    stock_qty: Optional[int] = None
    lead_time_days: Optional[int] = None
    obsolete: bool = False
    alternatives: List[str] = field(default_factory=list)
    supplier_url: str = ""
    simulation: bool = False
    error: str = ""
    flag: str = ""  # "", "⚠️ MANUEL", "🔴 OBSOLETE"


@dataclass
class BOMData:
    project: str
    source_file: str
    components: List[Component] = field(default_factory=list)


@dataclass
class ProcurementResult:
    bom: BOMData
    enriched: List[EnrichedComponent] = field(default_factory=list)
    total_cost_eur: float = 0.0
    simulation: bool = False
    alerts: List[str] = field(default_factory=list)
```

- [ ] **Step 3 : Écrire `config.py`**

```python
# scripts/procurement/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Cherche .procurement.env dans home dir (RPi) puis répertoire courant
_env_paths = [
    Path.home() / ".procurement.env",
    Path(".procurement.env"),
]
for _p in _env_paths:
    if _p.exists():
        load_dotenv(_p)
        break

MOUSER_API_KEY: str = os.getenv("MOUSER_API_KEY", "")
MOUSER_SEARCH_URL = "https://api.mouser.com/api/v2/search/keyword"
MOUSER_CART_URL = "https://api.mouser.com/api/v2/cart"

ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-sonnet-4-6"

# Mode simulation si aucune clé Mouser
SIMULATION_MODE: bool = not bool(MOUSER_API_KEY)

# Dossier TEAM_Inbox relatif à la racine PKA
TEAM_INBOX_PATH = Path(__file__).parent.parent.parent / "TEAM_Inbox"
```

- [ ] **Step 4 : Créer les fixtures CSV et MD**

```csv
# tests/procurement/fixtures/sample_bom.csv
ref,description,qty,mpn,preferred_supplier,category,notes
U1,ESP32-S3-WROOM-1U-N8R8,5,ESP32-S3-WROOM-1U-N8R8,Mouser,MCU,8MB PSRAM
C1,Condensateur 100nF 0402,20,,Mouser,Passif,
U2,SHT31-DIS-B,2,SHT31-DIS-B2.5kS,Mouser,Capteur,I2C
```

```markdown
# tests/procurement/fixtures/sample_bom.md
| Ref | Description | Qty | MPN | Preferred Supplier | Category | Notes |
|-----|-------------|-----|-----|--------------------|----------|-------|
| U1 | ESP32-S3-WROOM-1U-N8R8 | 5 | ESP32-S3-WROOM-1U-N8R8 | Mouser | MCU | 8MB PSRAM |
| C1 | Condensateur 100nF 0402 | 20 | | Mouser | Passif | |
| U2 | SHT31-DIS-B | 2 | SHT31-DIS-B2.5kS | Mouser | Capteur | I2C |
```

- [ ] **Step 5 : Générer la fixture XLSX**

```python
# tests/procurement/fixtures/generate_fixture_xlsx.py
import openpyxl
from pathlib import Path

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BOM"

# Ligne titre fusionnée (comme BOM WildNexus réelle)
ws.merge_cells("A1:G1")
ws["A1"] = "WildNexus P0 — Test BOM | Mis à jour : 2026-05-25"

headers = ["Ref", "Description", "Qty", "MPN", "Preferred Supplier", "Category", "Notes"]
ws.append(headers)

rows = [
    ("U1", "ESP32-S3-WROOM-1U-N8R8", 5, "ESP32-S3-WROOM-1U-N8R8", "Mouser", "MCU", "8MB PSRAM"),
    ("C1", "Condensateur 100nF 0402", 20, "", "Mouser", "Passif", ""),
    ("U2", "SHT31-DIS-B", 2, "SHT31-DIS-B2.5kS", "Mouser", "Capteur", "I2C"),
]
for row in rows:
    ws.append(row)

out = Path(__file__).parent / "sample_bom.xlsx"
wb.save(out)
print(f"Fixture créée : {out}")
```

```bash
python3 tests/procurement/fixtures/generate_fixture_xlsx.py
```
Résultat attendu : `Fixture créée : tests/procurement/fixtures/sample_bom.xlsx`

- [ ] **Step 6 : Commit**

```bash
git add scripts/procurement/ tests/procurement/
git commit -m "feat(procurement): scaffold — models, config, fixtures"
```

---

## Task 2 : BOM Parser (Excel / CSV / MD)

**Files:**
- Create: `scripts/procurement/bom_parser.py`
- Create: `tests/procurement/test_bom_parser.py`

---

- [ ] **Step 1 : Écrire les tests (TDD)**

```python
# tests/procurement/test_bom_parser.py
import pytest
from pathlib import Path
from scripts.procurement.bom_parser import parse
from scripts.procurement.models import BOMData, Component

FIXTURES = Path("tests/procurement/fixtures")


def _assert_wildnexus_components(bom: BOMData):
    assert isinstance(bom, BOMData)
    assert bom.project == "TEST"
    assert len(bom.components) == 3
    u1 = bom.components[0]
    assert u1.ref == "U1"
    assert u1.description == "ESP32-S3-WROOM-1U-N8R8"
    assert u1.qty == 5
    assert u1.mpn == "ESP32-S3-WROOM-1U-N8R8"
    assert u1.preferred_supplier == "Mouser"


def test_parse_csv():
    bom = parse(FIXTURES / "sample_bom.csv", "TEST")
    _assert_wildnexus_components(bom)


def test_parse_markdown():
    bom = parse(FIXTURES / "sample_bom.md", "TEST")
    _assert_wildnexus_components(bom)


def test_parse_excel():
    bom = parse(FIXTURES / "sample_bom.xlsx", "TEST")
    _assert_wildnexus_components(bom)


def test_parse_unsupported_format():
    with pytest.raises(ValueError, match="Format non supporté"):
        parse(FIXTURES / "sample_bom.json", "TEST")


def test_component_with_empty_mpn():
    bom = parse(FIXTURES / "sample_bom.csv", "TEST")
    c1 = bom.components[1]
    assert c1.ref == "C1"
    assert c1.mpn == ""
```

- [ ] **Step 2 : Vérifier que les tests échouent**

```bash
cd /Users/jchavauxm5/PKA_JCH
python3 -m pytest tests/procurement/test_bom_parser.py -v 2>&1 | head -20
```
Résultat attendu : `ModuleNotFoundError` ou `ImportError`

- [ ] **Step 3 : Écrire `bom_parser.py`**

```python
# scripts/procurement/bom_parser.py
import csv
import re
from pathlib import Path
from typing import Optional
import openpyxl
from .models import BOMData, Component

# Mapping noms de colonnes → champs Component
_COLUMN_MAP = {
    "ref": ["ref", "reference", "designator", "repère"],
    "description": ["description", "desc", "composant", "component", "désignation"],
    "qty": ["qty", "quantity", "quantité", "qte", "q", "nb"],
    "mpn": ["mpn", "part number", "manufacturer part number", "référence fabricant", "pn"],
    "preferred_supplier": ["preferred_supplier", "fournisseur", "supplier", "preferred supplier"],
    "category": ["category", "catégorie", "type", "famille"],
    "notes": ["notes", "note", "remarques", "commentaire"],
}


def _map_column(header: str) -> str:
    h = header.strip().lower()
    for field, aliases in _COLUMN_MAP.items():
        if h in aliases:
            return field
    return h


def _row_to_component(row: dict) -> Component:
    try:
        qty = int(float(str(row.get("qty", 1) or 1)))
    except (ValueError, TypeError):
        qty = 1
    return Component(
        ref=str(row.get("ref", "")).strip(),
        description=str(row.get("description", "")).strip(),
        qty=qty,
        mpn=str(row.get("mpn", "") or "").strip(),
        preferred_supplier=str(row.get("preferred_supplier", "") or "").strip(),
        category=str(row.get("category", "") or "").strip(),
        notes=str(row.get("notes", "") or "").strip(),
    )


def _is_title_row(row: tuple) -> bool:
    """Ignore les lignes de titre fusionnées (1 seule valeur non-None)."""
    non_null = [v for v in row if v is not None and str(v).strip()]
    return len(non_null) <= 1


def parse_excel(path: Path, project: str) -> BOMData:
    wb = openpyxl.load_workbook(path)
    # Cherche une feuille nommée BOM, sinon prend la première
    ws = next((wb[n] for n in wb.sheetnames if "bom" in n.lower()), wb.active)

    headers = None
    components = []
    for row in ws.iter_rows(values_only=True):
        if all(v is None for v in row):
            continue
        if headers is None:
            if _is_title_row(row):
                continue
            headers = [_map_column(str(v)) if v is not None else "" for v in row]
            continue
        row_dict = {h: v for h, v in zip(headers, row)}
        if not row_dict.get("ref") and not row_dict.get("description"):
            continue
        components.append(_row_to_component(row_dict))

    return BOMData(project=project, source_file=str(path), components=components)


def parse_csv(path: Path, project: str) -> BOMData:
    with open(path, encoding="utf-8") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        mapped_headers = {k: _map_column(k) for k in (reader.fieldnames or [])}
        components = []
        for row in reader:
            mapped = {mapped_headers[k]: v for k, v in row.items()}
            if not mapped.get("ref") and not mapped.get("description"):
                continue
            components.append(_row_to_component(mapped))

    return BOMData(project=project, source_file=str(path), components=components)


def parse_markdown(path: Path, project: str) -> BOMData:
    content = path.read_text(encoding="utf-8")
    headers = None
    components = []
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        # Ligne séparateur (---)
        if all(re.match(r"^:?-+:?$", c) or c == "" for c in cells):
            continue
        if headers is None:
            headers = [_map_column(c) for c in cells]
            continue
        row_dict = dict(zip(headers, cells))
        if not row_dict.get("ref") and not row_dict.get("description"):
            continue
        components.append(_row_to_component(row_dict))

    return BOMData(project=project, source_file=str(path), components=components)


def parse(path: Path, project: str) -> BOMData:
    ext = path.suffix.lower()
    if ext in (".xlsx", ".xls"):
        return parse_excel(path, project)
    elif ext == ".csv":
        return parse_csv(path, project)
    elif ext == ".md":
        return parse_markdown(path, project)
    else:
        raise ValueError(
            f"Format non supporté: {ext}. Formats acceptés: .xlsx, .csv, .md"
        )
```

- [ ] **Step 4 : Lancer les tests**

```bash
python3 -m pytest tests/procurement/test_bom_parser.py -v
```
Résultat attendu :
```
test_parse_csv PASSED
test_parse_markdown PASSED
test_parse_excel PASSED
test_parse_unsupported_format PASSED
test_component_with_empty_mpn PASSED
```

- [ ] **Step 5 : Commit**

```bash
git add scripts/procurement/bom_parser.py tests/procurement/test_bom_parser.py
git commit -m "feat(procurement): BOM parser — Excel, CSV, Markdown"
```

---

## Task 3 : Mouser API Client (simulation + Search API)

**Files:**
- Create: `scripts/procurement/api_client.py`
- Create: `tests/procurement/test_api_client.py`

---

- [ ] **Step 1 : Écrire les tests**

```python
# tests/procurement/test_api_client.py
import pytest
import responses as resp_lib
from scripts.procurement.api_client import MouserClient
from scripts.procurement.models import Component, EnrichedComponent
from scripts.procurement import config

# --- Simulation mode ---

def test_simulation_returns_enriched_component():
    client = MouserClient(api_key="", simulation=True)
    comp = Component(ref="U1", description="ESP32-S3-WROOM-1U-N8R8", qty=5,
                     mpn="ESP32-S3-WROOM-1U-N8R8", preferred_supplier="Mouser")
    result = client.search_component(comp)
    assert isinstance(result, EnrichedComponent)
    assert result.simulation is True
    assert result.price_unit is not None
    assert result.stock_qty is not None


def test_simulation_out_of_stock_triggers_flag():
    client = MouserClient(api_key="", simulation=True)
    comp = Component(ref="X1", description="Composant inexistant simulé", qty=1,
                     mpn="OBSOLETE-PART-999")
    result = client.search_component(comp)
    assert result.simulation is True


# --- Real API (mocked HTTP) ---

@resp_lib.activate
def test_search_real_api_returns_enriched():
    import json
    from scripts.procurement.config import MOUSER_SEARCH_URL

    mock_response = {
        "SearchResults": {
            "Parts": [{
                "ManufacturerPartNumber": "ESP32-S3-WROOM-1U-N8R8",
                "PriceBreaks": [{"Price": "5.36", "Quantity": 1}],
                "AvailabilityInStock": "1200",
                "LeadTime": "2 days",
                "ProductDetailUrl": "https://www.mouser.be/ProductDetail/test",
                "LifecycleStatus": "Active",
            }]
        }
    }
    resp_lib.add(
        resp_lib.POST,
        MOUSER_SEARCH_URL,
        json=mock_response,
        status=200,
    )
    client = MouserClient(api_key="TEST_KEY", simulation=False)
    comp = Component(ref="U1", description="ESP32-S3", qty=5,
                     mpn="ESP32-S3-WROOM-1U-N8R8", preferred_supplier="Mouser")
    result = client.search_component(comp)
    assert result.price_unit == pytest.approx(5.36)
    assert result.stock_qty == 1200
    assert result.simulation is False
    assert result.obsolete is False


@resp_lib.activate
def test_search_not_found_flags_manual():
    from scripts.procurement.config import MOUSER_SEARCH_URL
    resp_lib.add(
        resp_lib.POST,
        MOUSER_SEARCH_URL,
        json={"SearchResults": {"Parts": []}},
        status=200,
    )
    client = MouserClient(api_key="TEST_KEY", simulation=False)
    comp = Component(ref="Z1", description="Inconnu", qty=1, mpn="UNKNOWN-MPN")
    result = client.search_component(comp)
    assert result.flag == "⚠️ MANUEL"


@resp_lib.activate
def test_search_api_timeout_fallback_simulation():
    import responses as r
    from scripts.procurement.config import MOUSER_SEARCH_URL
    r.add(r.POST, MOUSER_SEARCH_URL, body=Exception("timeout"))
    client = MouserClient(api_key="TEST_KEY", simulation=False)
    comp = Component(ref="U1", description="ESP32", qty=1, mpn="ESP32-S3-WROOM-1U-N8R8")
    result = client.search_component(comp)
    assert result.simulation is True
    assert "timeout" in result.error.lower() or result.error != ""
```

- [ ] **Step 2 : Installer `responses` si absent**

```bash
pip3 install responses
```

- [ ] **Step 3 : Vérifier que les tests échouent**

```bash
python3 -m pytest tests/procurement/test_api_client.py -v 2>&1 | head -10
```
Résultat attendu : `ImportError: cannot import name 'MouserClient'`

- [ ] **Step 4 : Écrire `api_client.py`**

```python
# scripts/procurement/api_client.py
import time
import random
import requests
from typing import Optional
from .models import Component, EnrichedComponent
from . import config as cfg


_SIMULATION_STOCK = {
    # MPN connus → données simulées réalistes
    "ESP32-S3-WROOM-1U-N8R8": (5.36, 1200, 2, False),
    "SHT31-DIS-B2.5KS": (4.20, 850, 3, False),
    "EKMB1107111": (3.90, 200, 5, False),
}
_SIMULATION_DEFAULT = (9.99, 50, 7, False)
_SIMULATION_OBSOLETE_KEYWORDS = ["obsolete", "eol", "discontinued", "legacy"]


def _simulate(comp: Component) -> EnrichedComponent:
    mpn_upper = comp.mpn.upper()
    if any(kw in comp.description.lower() or kw in mpn_upper.lower()
           for kw in _SIMULATION_OBSOLETE_KEYWORDS):
        return EnrichedComponent(
            component=comp,
            obsolete=True,
            flag="🔴 OBSOLETE",
            simulation=True,
            error="",
        )
    price, stock, lead, obsolete = _SIMULATION_STOCK.get(comp.mpn, _SIMULATION_DEFAULT)
    return EnrichedComponent(
        component=comp,
        price_unit=price,
        currency="EUR",
        stock_qty=stock,
        lead_time_days=lead,
        obsolete=obsolete,
        supplier_url=f"https://www.mouser.be/Search/Refine?Keyword={comp.mpn}",
        simulation=True,
    )


def _parse_price(price_str: str) -> Optional[float]:
    try:
        return float(price_str.replace(",", ".").replace("€", "").strip())
    except (ValueError, AttributeError):
        return None


def _parse_stock(stock_str: str) -> Optional[int]:
    try:
        return int(str(stock_str).replace(",", "").strip())
    except (ValueError, AttributeError):
        return None


class MouserClient:
    def __init__(self, api_key: str, simulation: bool = False):
        self.api_key = api_key
        self.simulation = simulation or not api_key

    def search_component(self, comp: Component) -> EnrichedComponent:
        if self.simulation:
            return _simulate(comp)

        query = comp.mpn if comp.mpn else comp.description
        payload = {
            "SearchByKeywordRequest": {
                "keyword": query,
                "records": 3,
                "startingRecord": 0,
                "searchOptions": "string",
                "searchWithYourSignUpLanguage": "string",
            }
        }
        url = f"{cfg.MOUSER_SEARCH_URL}?apiKey={self.api_key}"

        for attempt in range(3):
            try:
                resp = requests.post(url, json=payload, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                parts = data.get("SearchResults", {}).get("Parts", [])
                if not parts:
                    return EnrichedComponent(
                        component=comp,
                        flag="⚠️ MANUEL",
                        simulation=False,
                        error="Composant non trouvé dans Mouser",
                    )
                part = parts[0]
                price_breaks = part.get("PriceBreaks", [])
                price = _parse_price(price_breaks[0]["Price"]) if price_breaks else None
                stock = _parse_stock(part.get("AvailabilityInStock", 0))
                lifecycle = str(part.get("LifecycleStatus", "")).lower()
                obsolete = any(kw in lifecycle for kw in ["obsolete", "eol", "discontinued"])
                return EnrichedComponent(
                    component=comp,
                    price_unit=price,
                    currency="EUR",
                    stock_qty=stock,
                    lead_time_days=None,
                    obsolete=obsolete,
                    flag="🔴 OBSOLETE" if obsolete else "",
                    supplier_url=part.get("ProductDetailUrl", ""),
                    simulation=False,
                )
            except Exception as exc:
                if attempt == 2:
                    sim = _simulate(comp)
                    sim.error = str(exc)
                    return sim
                time.sleep(1.5 * (attempt + 1))

        # unreachable mais garde mypy content
        return _simulate(comp)
```

- [ ] **Step 5 : Lancer les tests**

```bash
python3 -m pytest tests/procurement/test_api_client.py -v
```
Résultat attendu : 5 tests PASSED

- [ ] **Step 6 : Commit**

```bash
git add scripts/procurement/api_client.py tests/procurement/test_api_client.py
git commit -m "feat(procurement): Mouser Search API client + simulation mode"
```

---

## Task 4 : LLM Reasoner ([[Forge]] via Anthropic API)

**Files:**
- Create: `scripts/procurement/llm_reasoner.py`
- Create: `tests/procurement/test_llm_reasoner.py`

---

- [ ] **Step 1 : Écrire les tests**

```python
# tests/procurement/test_llm_reasoner.py
from unittest.mock import patch, MagicMock
from scripts.procurement.llm_reasoner import LLMReasoner
from scripts.procurement.models import Component, EnrichedComponent, BOMData, ProcurementResult


def _make_result() -> ProcurementResult:
    comp = Component(ref="U1", description="ESP32-S3-WROOM-1U-N8R8", qty=5,
                     mpn="ESP32-S3-WROOM-1U-N8R8", preferred_supplier="Mouser")
    enriched = EnrichedComponent(
        component=comp, price_unit=5.36, stock_qty=1200,
        lead_time_days=2, simulation=False
    )
    comp2 = Component(ref="X1", description="Composant obsolète", qty=1,
                      mpn="OLD-PART-001")
    enriched2 = EnrichedComponent(
        component=comp2, obsolete=True, flag="🔴 OBSOLETE", simulation=False
    )
    bom = BOMData(project="TEST", source_file="test.csv",
                  components=[comp, comp2])
    return ProcurementResult(bom=bom, enriched=[enriched, enriched2])


@patch("scripts.procurement.llm_reasoner.anthropic.Anthropic")
def test_generate_alternatives_for_obsolete(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text='["ESP32-S3-WROOM-1-N8R8", "ESP32-S3-MINI-1-N8"]')]
    )
    reasoner = LLMReasoner(api_key="TEST")
    result = _make_result()
    updated = reasoner.generate_alternatives(result)
    obsolete_items = [e for e in updated.enriched if e.obsolete]
    assert len(obsolete_items) == 1
    assert len(obsolete_items[0].alternatives) >= 1


@patch("scripts.procurement.llm_reasoner.anthropic.Anthropic")
def test_narrative_report_returns_string(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="## Résumé\nProcurement OK.")]
    )
    reasoner = LLMReasoner(api_key="TEST")
    result = _make_result()
    narrative = reasoner.generate_narrative(result, project="TEST")
    assert isinstance(narrative, str)
    assert len(narrative) > 10


@patch("scripts.procurement.llm_reasoner.anthropic.Anthropic")
def test_no_api_key_skips_llm(mock_anthropic_cls):
    reasoner = LLMReasoner(api_key="")
    result = _make_result()
    updated = reasoner.generate_alternatives(result)
    mock_anthropic_cls.assert_not_called()
    assert updated is result  # retourne tel quel sans LLM
```

- [ ] **Step 2 : Vérifier échec**

```bash
python3 -m pytest tests/procurement/test_llm_reasoner.py -v 2>&1 | head -10
```
Résultat attendu : `ImportError`

- [ ] **Step 3 : Écrire `llm_reasoner.py`**

```python
# scripts/procurement/llm_reasoner.py
import json
import anthropic
from .models import ProcurementResult, EnrichedComponent
from . import config as cfg


class LLMReasoner:
    """Utilise Claude pour générer des alternatives et le narratif du rapport."""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key or cfg.ANTHROPIC_API_KEY
        self._client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None

    def _call(self, system: str, user: str) -> str:
        if not self._client:
            return ""
        msg = self._client.messages.create(
            model=cfg.ANTHROPIC_MODEL,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return msg.content[0].text

    def generate_alternatives(self, result: ProcurementResult) -> ProcurementResult:
        """Pour chaque composant obsolète ou en rupture, demande 2 alternatives à Claude."""
        if not self._client:
            return result

        needs_alt = [
            e for e in result.enriched
            if e.obsolete or (e.stock_qty is not None and e.stock_qty == 0)
        ]
        for enriched in needs_alt:
            comp = enriched.component
            prompt = (
                f"Composant: {comp.description} (MPN: {comp.mpn})\n"
                f"Catégorie: {comp.category}\n"
                f"Raison: {'Obsolète' if enriched.obsolete else 'Rupture de stock'}\n\n"
                "Propose exactement 2 alternatives avec le même footprint/interface si possible. "
                "Retourne uniquement un JSON array de MPNs: [\"MPN1\", \"MPN2\"]"
            )
            try:
                raw = self._call(
                    system="Tu es un expert en composants électroniques. Réponds UNIQUEMENT en JSON.",
                    user=prompt,
                )
                alternatives = json.loads(raw)
                if isinstance(alternatives, list):
                    enriched.alternatives = [str(a) for a in alternatives[:2]]
            except (json.JSONDecodeError, Exception):
                enriched.alternatives = []

        return result

    def generate_narrative(self, result: ProcurementResult, project: str) -> str:
        """Génère la section narrative du rapport (résumé + alertes + recommandations)."""
        if not self._client:
            return "_LLM non disponible — narratif automatique désactivé._"

        summary_lines = []
        for e in result.enriched:
            line = (
                f"- {e.component.ref} ({e.component.mpn or e.component.description}): "
                f"prix={e.price_unit}€, stock={e.stock_qty}, "
                f"obsolète={e.obsolete}, flag={e.flag or 'OK'}"
            )
            summary_lines.append(line)

        prompt = (
            f"Projet: {project}\n"
            f"Mode simulation: {result.simulation}\n"
            f"Coût total estimé: {result.total_cost_eur:.2f}€\n\n"
            "Données composants:\n" + "\n".join(summary_lines) + "\n\n"
            "Rédige en français un résumé procurement (3-5 phrases max) couvrant: "
            "état global, alertes prioritaires, recommandations fournisseur."
        )
        return self._call(
            system="Tu es Forge, ingénieur systèmes PKA. Sois concis et factuel.",
            user=prompt,
        )
```

- [ ] **Step 4 : Lancer les tests**

```bash
python3 -m pytest tests/procurement/test_llm_reasoner.py -v
```
Résultat attendu : 3 tests PASSED

- [ ] **Step 5 : Commit**

```bash
git add scripts/procurement/llm_reasoner.py tests/procurement/test_llm_reasoner.py
git commit -m "feat(procurement): LLM reasoner — alternatives + narratif via Anthropic API"
```

---

## Task 5 : BOM Writer (enrichissement BOM source)

**Files:**
- Create: `scripts/procurement/bom_writer.py`
- Create: `tests/procurement/test_bom_writer.py`

---

- [ ] **Step 1 : Écrire les tests**

```python
# tests/procurement/test_bom_writer.py
import shutil
from pathlib import Path
import openpyxl
from scripts.procurement.bom_writer import enrich_bom
from scripts.procurement.models import Component, EnrichedComponent, BOMData, ProcurementResult

FIXTURES = Path("tests/procurement/fixtures")
TMP = Path("/tmp/procurement_test")


def _make_result(source: Path) -> ProcurementResult:
    comp = Component(ref="U1", description="ESP32-S3-WROOM-1U-N8R8", qty=5,
                     mpn="ESP32-S3-WROOM-1U-N8R8")
    enriched = EnrichedComponent(
        component=comp, price_unit=5.36, stock_qty=1200,
        lead_time_days=2, simulation=False,
        supplier_url="https://www.mouser.be/test"
    )
    bom = BOMData(project="TEST", source_file=str(source), components=[comp])
    return ProcurementResult(bom=bom, enriched=[enriched], total_cost_eur=26.80)


def setup_function():
    TMP.mkdir(exist_ok=True)


def teardown_function():
    shutil.rmtree(TMP, ignore_errors=True)


def test_enrich_xlsx_creates_output():
    src = TMP / "sample_bom.xlsx"
    shutil.copy(FIXTURES / "sample_bom.xlsx", src)
    result = _make_result(src)
    out = enrich_bom(result, output_dir=TMP)
    assert out.exists()
    wb = openpyxl.load_workbook(out)
    ws = wb.active
    headers = [cell.value for cell in ws[2]]  # ligne 2 = headers (ligne 1 = titre)
    assert any("Prix" in str(h) for h in headers if h)


def test_enrich_csv_creates_output():
    src = TMP / "sample_bom.csv"
    shutil.copy(FIXTURES / "sample_bom.csv", src)
    result = _make_result(src)
    out = enrich_bom(result, output_dir=TMP)
    assert out.exists()
    content = out.read_text()
    assert "Prix" in content or "prix" in content
```

- [ ] **Step 2 : Vérifier échec**

```bash
python3 -m pytest tests/procurement/test_bom_writer.py -v 2>&1 | head -10
```
Résultat attendu : `ImportError`

- [ ] **Step 3 : Écrire `bom_writer.py`**

```python
# scripts/procurement/bom_writer.py
import csv
import shutil
from datetime import date
from pathlib import Path
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from .models import ProcurementResult, EnrichedComponent

_ENRICH_HEADERS = [
    "Prix unit. (EUR)", "Stock", "Délai (j)", "Obsolète",
    "Alternative", "URL fournisseur", "Simulation",
]

_BLUE_DARK = "1F4E79"
_BLUE_LIGHT = "D6E4F0"
_YELLOW = "FFF2CC"
_GREEN = "E2EFDA"
_RED = "FFD7D7"


def _fill(color: str) -> PatternFill:
    return PatternFill("solid", fgColor=color)


def _enrich_row(e: EnrichedComponent) -> list:
    return [
        f"{e.price_unit:.2f}" if e.price_unit is not None else "N/A",
        str(e.stock_qty) if e.stock_qty is not None else "N/A",
        str(e.lead_time_days) if e.lead_time_days is not None else "N/A",
        "🔴 OUI" if e.obsolete else "NON",
        ", ".join(e.alternatives) if e.alternatives else "",
        e.supplier_url,
        "OUI" if e.simulation else "NON",
    ]


def _enrich_xlsx(src: Path, result: ProcurementResult, output_dir: Path) -> Path:
    out_name = src.stem + f"_enrichi_{date.today().isoformat()}.xlsx"
    out = output_dir / out_name
    shutil.copy(src, out)

    wb = openpyxl.load_workbook(out)
    ws = next((wb[n] for n in wb.sheetnames if "bom" in n.lower()), wb.active)

    # Trouver la ligne de headers (première ligne avec > 1 valeur non-None)
    header_row_idx = None
    for idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
        non_null = [v for v in row if v is not None and str(v).strip()]
        if len(non_null) > 1:
            header_row_idx = idx
            break

    if header_row_idx is None:
        wb.save(out)
        return out

    # Ajouter headers enrichissement
    last_col = ws.max_column
    for i, h in enumerate(_ENRICH_HEADERS):
        cell = ws.cell(row=header_row_idx, column=last_col + 1 + i, value=h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = _fill(_BLUE_DARK)
        cell.alignment = Alignment(wrap_text=True)

    # Map ref → EnrichedComponent
    enriched_map = {e.component.ref: e for e in result.enriched}

    # Parcourir les lignes de données
    headers_raw = [ws.cell(row=header_row_idx, column=c).value
                   for c in range(1, last_col + 1)]
    ref_col = next(
        (i + 1 for i, h in enumerate(headers_raw)
         if h and "ref" in str(h).lower()),
        1
    )
    for row_idx in range(header_row_idx + 1, ws.max_row + 1):
        ref_val = ws.cell(row=row_idx, column=ref_col).value
        if not ref_val:
            continue
        e = enriched_map.get(str(ref_val).strip())
        if not e:
            continue
        values = _enrich_row(e)
        row_fill = _fill(_RED if e.obsolete else (_YELLOW if e.simulation else _BLUE_LIGHT))
        for i, val in enumerate(values):
            cell = ws.cell(row=row_idx, column=last_col + 1 + i, value=val)
            cell.fill = row_fill

    wb.save(out)
    return out


def _enrich_csv(src: Path, result: ProcurementResult, output_dir: Path) -> Path:
    out_name = src.stem + f"_enrichi_{date.today().isoformat()}.csv"
    out = output_dir / out_name
    enriched_map = {e.component.ref: e for e in result.enriched}

    with open(src, encoding="utf-8") as fin, open(out, "w", newline="", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        fieldnames = list(reader.fieldnames or []) + _ENRICH_HEADERS
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            ref = row.get("ref", row.get("Ref", "")).strip()
            e = enriched_map.get(ref)
            if e:
                values = _enrich_row(e)
                row.update(dict(zip(_ENRICH_HEADERS, values)))
            writer.writerow(row)

    return out


def enrich_bom(result: ProcurementResult, output_dir: Path) -> Path:
    src = Path(result.bom.source_file)
    output_dir.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in (".xlsx", ".xls"):
        return _enrich_xlsx(src, result, output_dir)
    else:
        return _enrich_csv(src, result, output_dir)
```

- [ ] **Step 4 : Lancer les tests**

```bash
python3 -m pytest tests/procurement/test_bom_writer.py -v
```
Résultat attendu : 2 tests PASSED

- [ ] **Step 5 : Commit**

```bash
git add scripts/procurement/bom_writer.py tests/procurement/test_bom_writer.py
git commit -m "feat(procurement): BOM writer — enrichissement Excel et CSV"
```

---

## Task 6 : Report Writer (Markdown → TEAM_Inbox)

**Files:**
- Create: `scripts/procurement/report_writer.py`
- Create: `tests/procurement/test_report_writer.py`

---

- [ ] **Step 1 : Écrire les tests**

```python
# tests/procurement/test_report_writer.py
import shutil
from pathlib import Path
from datetime import date
from scripts.procurement.report_writer import write_report
from scripts.procurement.models import Component, EnrichedComponent, BOMData, ProcurementResult

TMP = Path("/tmp/procurement_report_test")


def _make_result() -> ProcurementResult:
    comp = Component(ref="U1", description="ESP32-S3-WROOM-1U-N8R8", qty=5,
                     mpn="ESP32-S3-WROOM-1U-N8R8", preferred_supplier="Mouser")
    enriched = EnrichedComponent(
        component=comp, price_unit=5.36, stock_qty=1200,
        lead_time_days=2, simulation=False, supplier_url="https://mouser.be/test"
    )
    comp2 = Component(ref="X1", description="Pièce obsolète", qty=1, mpn="OLD-001")
    enriched2 = EnrichedComponent(
        component=comp2, obsolete=True, flag="🔴 OBSOLETE",
        alternatives=["NEW-001A", "NEW-001B"], simulation=False
    )
    bom = BOMData(project="WILDNEXUS", source_file="bom.xlsx", components=[comp, comp2])
    return ProcurementResult(
        bom=bom, enriched=[enriched, enriched2],
        total_cost_eur=26.80, simulation=False,
        alerts=["X1 est obsolète"]
    )


def setup_function():
    TMP.mkdir(exist_ok=True)


def teardown_function():
    shutil.rmtree(TMP, ignore_errors=True)


def test_report_file_created():
    result = _make_result()
    out = write_report(result, output_dir=TMP, narrative="Procurement OK.")
    assert out.exists()
    assert out.suffix == ".md"
    assert date.today().isoformat() in out.name


def test_report_contains_required_sections():
    result = _make_result()
    out = write_report(result, output_dir=TMP, narrative="Procurement OK.")
    content = out.read_text()
    assert "# Rapport Procurement" in content
    assert "## Résumé" in content
    assert "## Composants analysés" in content
    assert "## Alertes" in content
    assert "## Paniers recommandés" in content
    assert "## Alternatives proposées" in content
    assert "## Décisions en attente JCH" in content


def test_report_simulation_flag():
    result = _make_result()
    result.simulation = True
    out = write_report(result, output_dir=TMP, narrative="")
    content = out.read_text()
    assert "SIMULATION" in content


def test_report_obsolete_item_listed():
    result = _make_result()
    out = write_report(result, output_dir=TMP, narrative="")
    content = out.read_text()
    assert "OLD-001" in content or "Pièce obsolète" in content
    assert "NEW-001A" in content
```

- [ ] **Step 2 : Vérifier échec**

```bash
python3 -m pytest tests/procurement/test_report_writer.py -v 2>&1 | head -10
```

- [ ] **Step 3 : Écrire `report_writer.py`**

```python
# scripts/procurement/report_writer.py
from datetime import date
from pathlib import Path
from .models import ProcurementResult

_TEMPLATE = """\
# Rapport Procurement — {project} — {today}
{simulation_banner}
**Généré par :** Forge 🦦 (PKA Procurement Agent)  
**Source BOM :** `{source_file}`  
**Coût total estimé :** {total_cost:.2f} €  
**Mode simulation :** {simulation_flag}

---

## Résumé

{narrative}

---

## Composants analysés

| Ref | Description | Qté | MPN | Prix unit. | Stock | Délai (j) | Statut | Fournisseur |
|-----|-------------|-----|-----|-----------|-------|-----------|--------|-------------|
{components_table}

---

## Alertes

{alerts_section}

---

## Paniers recommandés

{cart_section}

---

## Alternatives proposées

{alternatives_section}

---

## Décisions en attente JCH

{decisions_section}

---

*Aucune commande ne sera passée sans validation explicite JCH.*
"""


def _component_row(e) -> str:
    comp = e.component
    price = f"{e.price_unit:.2f} €" if e.price_unit is not None else "N/A"
    stock = str(e.stock_qty) if e.stock_qty is not None else "N/A"
    lead = str(e.lead_time_days) if e.lead_time_days is not None else "N/A"
    status = e.flag if e.flag else ("⚠️ SIM" if e.simulation else "✅ OK")
    supplier_link = f"[Mouser]({e.supplier_url})" if e.supplier_url else "—"
    return (
        f"| {comp.ref} | {comp.description} | {comp.qty} | "
        f"`{comp.mpn or '—'}` | {price} | {stock} | {lead} | {status} | {supplier_link} |"
    )


def _cart_by_supplier(result: ProcurementResult) -> str:
    from collections import defaultdict
    carts: dict[str, list] = defaultdict(list)
    for e in result.enriched:
        supplier = e.component.preferred_supplier or "Non spécifié"
        if e.price_unit is not None:
            subtotal = e.price_unit * e.component.qty
            carts[supplier].append(
                f"- `{e.component.mpn or e.component.description}` "
                f"× {e.component.qty} = {subtotal:.2f} €  \n"
                f"  {e.supplier_url}"
            )
    if not carts:
        return "_Aucun panier disponible (mode simulation ou composants non trouvés)._"
    lines = []
    for supplier, items in carts.items():
        lines.append(f"### {supplier}\n" + "\n".join(items))
    return "\n\n".join(lines)


def write_report(
    result: ProcurementResult,
    output_dir: Path,
    narrative: str = "",
) -> Path:
    today = date.today().isoformat()
    project = result.bom.project
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{today}_Forge_procurement_{project}.md"
    out = output_dir / filename

    simulation_banner = (
        "> ⚠️ **[SIMULATION]** — Les données prix/stock sont simulées. "
        "Aucune clé API active.\n"
        if result.simulation else ""
    )

    components_table = "\n".join(_component_row(e) for e in result.enriched)

    alerts = result.alerts or []
    obsolete = [e for e in result.enriched if e.obsolete]
    no_stock = [e for e in result.enriched if e.stock_qty == 0]
    for e in obsolete:
        msg = f"🔴 **{e.component.ref}** (`{e.component.mpn}`) — Obsolète"
        if msg not in alerts:
            alerts.append(msg)
    for e in no_stock:
        msg = f"⚠️ **{e.component.ref}** (`{e.component.mpn}`) — Rupture de stock"
        if msg not in alerts:
            alerts.append(msg)
    alerts_section = "\n".join(f"- {a}" for a in alerts) if alerts else "_Aucune alerte._"

    alt_lines = []
    for e in result.enriched:
        if e.alternatives:
            alt_lines.append(
                f"- **{e.component.ref}** (`{e.component.mpn}`): "
                + ", ".join(f"`{a}`" for a in e.alternatives)
            )
    alternatives_section = "\n".join(alt_lines) if alt_lines else "_Aucune alternative proposée._"

    manual = [e for e in result.enriched if e.flag == "⚠️ MANUEL"]
    decisions = []
    if manual:
        decisions.append("**Composants à localiser manuellement :**")
        for e in manual:
            decisions.append(f"- {e.component.ref} — {e.component.description} (`{e.component.mpn}`)")
    if result.simulation:
        decisions.append("\n**Activer les clés API** pour obtenir des données réelles.")
    decisions_section = "\n".join(decisions) if decisions else "_Aucune décision bloquante._"

    content = _TEMPLATE.format(
        project=project,
        today=today,
        simulation_banner=simulation_banner,
        source_file=result.bom.source_file,
        total_cost=result.total_cost_eur,
        simulation_flag="OUI ⚠️" if result.simulation else "NON",
        narrative=narrative or "_Narratif LLM non disponible._",
        components_table=components_table,
        alerts_section=alerts_section,
        cart_section=_cart_by_supplier(result),
        alternatives_section=alternatives_section,
        decisions_section=decisions_section,
    )
    out.write_text(content, encoding="utf-8")
    return out
```

- [ ] **Step 4 : Lancer les tests**

```bash
python3 -m pytest tests/procurement/test_report_writer.py -v
```
Résultat attendu : 4 tests PASSED

- [ ] **Step 5 : Commit**

```bash
git add scripts/procurement/report_writer.py tests/procurement/test_report_writer.py
git commit -m "feat(procurement): report writer — Markdown structuré vers TEAM_Inbox"
```

---

## Task 7 : CLI Orchestrateur (`main.py`)

**Files:**
- Create: `scripts/procurement/main.py`

---

- [ ] **Step 1 : Écrire `main.py`**

```python
# scripts/procurement/main.py
"""
Usage:
    python3 -m scripts.procurement.main --project WILDNEXUS --bom path/to/bom.xlsx
    python3 -m scripts.procurement.main --project DIM3 --bom path/to/bom.csv
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

from .bom_parser import parse
from .api_client import MouserClient
from .llm_reasoner import LLMReasoner
from .bom_writer import enrich_bom
from .report_writer import write_report
from .models import ProcurementResult, EnrichedComponent
from . import config as cfg


def compute_total(enriched: list[EnrichedComponent]) -> float:
    total = 0.0
    for e in enriched:
        if e.price_unit is not None:
            total += e.price_unit * e.component.qty
    return total


def run(project: str, bom_path: Path, output_dir: Path) -> None:
    print(f"\n🦦 Forge — Procurement Agent — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Projet : {project}")
    print(f"   BOM    : {bom_path}")
    print(f"   Mode   : {'⚠️  SIMULATION' if cfg.SIMULATION_MODE else '✅ API réelle'}\n")

    # 1. Parser la BOM
    print("📋 Parsing BOM...")
    bom = parse(bom_path, project)
    print(f"   {len(bom.components)} composants chargés\n")

    # 2. Interroger l'API Mouser
    print("🔍 Recherche Mouser...")
    client = MouserClient(api_key=cfg.MOUSER_API_KEY, simulation=cfg.SIMULATION_MODE)
    enriched = []
    for comp in bom.components:
        e = client.search_component(comp)
        flag_str = f" {e.flag}" if e.flag else ""
        sim_str = " [SIM]" if e.simulation else ""
        print(f"   {comp.ref:5s} {comp.mpn or comp.description[:30]:35s} "
              f"→ {e.price_unit or 'N/A':>6} €  stock={e.stock_qty}{flag_str}{sim_str}")
        enriched.append(e)

    result = ProcurementResult(
        bom=bom,
        enriched=enriched,
        total_cost_eur=compute_total(enriched),
        simulation=cfg.SIMULATION_MODE,
    )

    # 3. LLM : alternatives + narratif
    print("\n🧠 Raisonnement LLM (Forge)...")
    reasoner = LLMReasoner()
    result = reasoner.generate_alternatives(result)
    narrative = reasoner.generate_narrative(result, project)

    # 4. Enrichir le BOM source
    print("\n📊 Enrichissement BOM...")
    enriched_bom_path = enrich_bom(result, output_dir=output_dir)
    print(f"   → {enriched_bom_path}")

    # 5. Générer le rapport Markdown
    print("\n📝 Génération rapport...")
    report_path = write_report(result, output_dir=output_dir, narrative=narrative)
    print(f"   → {report_path}")

    # 6. Résumé final
    print(f"\n{'='*60}")
    print(f"  Coût total estimé : {result.total_cost_eur:.2f} €")
    alerts = [e for e in enriched if e.flag]
    if alerts:
        print(f"  ⚠️  Alertes : {len(alerts)} composant(s) à vérifier")
        for e in alerts:
            print(f"     - {e.component.ref} : {e.flag}")
    else:
        print("  ✅ Aucune alerte")
    print(f"{'='*60}")
    print("\n⏳ En attente de validation JCH avant préparation panier.")


def main():
    parser = argparse.ArgumentParser(description="PKA Procurement Agent")
    parser.add_argument("--project", required=True, help="Nom du projet (ex: WILDNEXUS)")
    parser.add_argument("--bom", required=True, type=Path, help="Chemin vers le fichier BOM")
    parser.add_argument(
        "--output",
        type=Path,
        default=cfg.TEAM_INBOX_PATH,
        help="Dossier de sortie (défaut: TEAM_Inbox/)",
    )
    args = parser.parse_args()

    if not args.bom.exists():
        print(f"❌ Fichier BOM introuvable : {args.bom}", file=sys.stderr)
        sys.exit(1)

    run(project=args.project, bom_path=args.bom, output_dir=args.output)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2 : Test end-to-end en mode simulation**

```bash
cd /Users/jchavauxm5/PKA_JCH
python3 -m scripts.procurement.main \
  --project TEST \
  --bom tests/procurement/fixtures/sample_bom.csv \
  --output /tmp/procurement_e2e_test
```

Résultat attendu :
```
🦦 Forge — Procurement Agent — ...
   Projet : TEST
   Mode   : ⚠️  SIMULATION
📋 Parsing BOM... 3 composants chargés
🔍 Recherche Mouser...
   U1    ESP32-S3-WROOM-1U-N8R8          →   9.99 €  stock=50 [SIM]
   ...
📊 Enrichissement BOM... → /tmp/...
📝 Génération rapport... → /tmp/...
  Coût total estimé : XX.XX €
⏳ En attente de validation JCH...
```

- [ ] **Step 3 : Vérifier les fichiers générés**

```bash
ls /tmp/procurement_e2e_test/
cat /tmp/procurement_e2e_test/*_Forge_procurement_TEST.md
```

- [ ] **Step 4 : Commit**

```bash
git add scripts/procurement/main.py
git commit -m "feat(procurement): CLI orchestrateur — pipeline complet end-to-end"
```

---

## Task 8 : Mouser Cart API (post-validation JCH)

**Files:**
- Create: `scripts/procurement/cart_client.py`

---

- [ ] **Step 1 : Écrire `cart_client.py`**

```python
# scripts/procurement/cart_client.py
"""
Invoqué UNIQUEMENT après validation explicite JCH.
Pousse les composants validés dans un panier Mouser via l'API Cart.
JCH finalise la commande manuellement sur mouser.be.
"""
import requests
from .models import ProcurementResult
from . import config as cfg


def push_cart(result: ProcurementResult, cart_name: str = "PKA_Procurement") -> str:
    """
    Crée ou met à jour un panier Mouser avec les composants du résultat.
    Retourne l'URL du panier ou un message d'erreur.
    """
    if cfg.SIMULATION_MODE:
        return (
            "⚠️ Mode simulation — panier non créé. "
            "Ajouter MOUSER_API_KEY dans .procurement.env pour activer."
        )

    items = []
    for e in result.enriched:
        if not e.component.mpn or e.flag == "⚠️ MANUEL":
            continue  # Ne pas ajouter les composants sans MPN ou non trouvés
        items.append({
            "MouserPartNumber": e.component.mpn,
            "Quantity": str(e.component.qty),
            "CustomerPartNumber": e.component.ref,
        })

    if not items:
        return "⚠️ Aucun composant éligible au panier (MPN manquants ou non trouvés)."

    payload = {
        "CartKey": "",  # vide = nouveau panier
        "CartItems": items,
    }
    url = f"{cfg.MOUSER_CART_URL}?apiKey={cfg.MOUSER_API_KEY}"

    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        cart_key = data.get("CartKey", "")
        cart_url = f"https://www.mouser.be/Cart/?cartKey={cart_key}" if cart_key else "N/A"
        return f"✅ Panier Mouser créé : {cart_url}"
    except Exception as exc:
        return f"❌ Erreur création panier : {exc}"
```

- [ ] **Step 2 : Ajouter la commande `--push-cart` à `main.py`**

Dans `scripts/procurement/main.py`, ajouter après la définition du parser :
```python
    parser.add_argument(
        "--push-cart",
        action="store_true",
        help="Pousse le panier Mouser après validation JCH (requiert MOUSER_API_KEY)"
    )
```

Et à la fin de `run()`, avant le message d'attente :
```python
    if push_cart_flag:
        from .cart_client import push_cart
        print("\n🛒 Création panier Mouser...")
        cart_result = push_cart(result)
        print(f"   {cart_result}")
    else:
        print("\n⏳ En attente de validation JCH avant préparation panier.")
        print("   Relancer avec --push-cart pour créer le panier Mouser.")
```

Mettre à jour la signature de `run()` :
```python
def run(project: str, bom_path: Path, output_dir: Path, push_cart_flag: bool = False) -> None:
```

Et dans `main()` :
```python
    run(project=args.project, bom_path=args.bom, output_dir=args.output,
        push_cart_flag=args.push_cart)
```

- [ ] **Step 3 : Test simulation Cart**

```bash
python3 -m scripts.procurement.main \
  --project TEST \
  --bom tests/procurement/fixtures/sample_bom.csv \
  --output /tmp/test_cart \
  --push-cart
```

Résultat attendu (sans clé) :
```
🛒 Création panier Mouser...
   ⚠️ Mode simulation — panier non créé. Ajouter MOUSER_API_KEY...
```

- [ ] **Step 4 : Commit**

```bash
git add scripts/procurement/cart_client.py scripts/procurement/main.py
git commit -m "feat(procurement): Mouser Cart API — push panier post-validation JCH"
```

---

## Task 9 : Déploiement RPi

**Files:**
- Create: `scripts/procurement/deploy_rpi.sh`

---

- [ ] **Step 1 : Trouver l'IP publique de ta box (à enregistrer chez Mouser)**

```bash
curl -s ifconfig.me
```
→ Note cette IP. Va sur [developer.mouser.com](https://developer.mouser.com), enregistre ton app, whitelist cette IP, copie la clé.

- [ ] **Step 2 : Créer le script de déploiement**

```bash
# scripts/procurement/deploy_rpi.sh
#!/bin/bash
# Déploie l'agent procurement sur le RPi
RPi_HOST="jchavaux@192.168.1.48"
RPi_DIR="/home/jchavaux/pka/procurement"

echo "📦 Création dossier RPi..."
ssh $RPi_HOST "mkdir -p $RPi_DIR"

echo "📤 Transfert scripts..."
scp -r scripts/procurement/*.py $RPi_HOST:$RPi_DIR/
scp -r tests/procurement/fixtures/*.xlsx $RPi_HOST:$RPi_DIR/fixtures/ 2>/dev/null || true

echo "📦 Installation dépendances RPi..."
ssh $RPi_HOST "pip3 install openpyxl requests anthropic python-dotenv --quiet"

echo ""
echo "✅ Déploiement OK"
echo ""
echo "👉 Sur le RPi, crée ~/.procurement.env avec :"
echo "   MOUSER_API_KEY=ta_cle_ici"
echo "   ANTHROPIC_API_KEY=ta_cle_ici"
echo ""
echo "👉 Test RPi :"
echo "   ssh $RPi_HOST"
echo "   cd $RPi_DIR"
echo "   python3 main.py --project TEST --bom fixtures/sample_bom.csv --output /tmp/test"
```

```bash
chmod +x scripts/procurement/deploy_rpi.sh
```

- [ ] **Step 3 : Configurer `.procurement.env` sur le RPi**

```bash
ssh jchavaux@192.168.1.48
```
```bash
# Sur le RPi :
cat > ~/.procurement.env << 'EOF'
MOUSER_API_KEY=REMPLACER_PAR_TA_CLE
ANTHROPIC_API_KEY=REMPLACER_PAR_TA_CLE
EOF
chmod 600 ~/.procurement.env
```

- [ ] **Step 4 : Déployer et tester**

```bash
# Depuis le Mac
./scripts/procurement/deploy_rpi.sh
```

```bash
# Depuis le RPi
ssh jchavaux@192.168.1.48
cd /home/jchavaux/pka/procurement
python3 main.py --project WILDNEXUS \
  --bom /chemin/vers/WILDNEXUS_BOM_P0_v0.2.xlsx \
  --output /home/jchavaux/pka/TEAM_Inbox
```

- [ ] **Step 5 : Commit final**

```bash
git add scripts/procurement/deploy_rpi.sh
git commit -m "feat(procurement): script déploiement RPi"
```

---

## Récapitulatif des dépendances

```
# requirements (scripts/procurement/requirements.txt)
openpyxl>=3.1.0
requests>=2.31.0
anthropic>=0.34.0
python-dotenv>=1.0.0

# dev / test
pytest>=8.0.0
responses>=0.25.0
```

```bash
pip3 install responses  # si absent en local
```

---

## Commande finale (Mac → WildNexus)

```bash
# Depuis le RPi (ou Mac en mode simulation)
python3 -m scripts.procurement.main \
  --project WILDNEXUS \
  --bom "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/07_PROCUREMENT_BOM/WILDNEXUS_BOM_P0_v0.2.xlsx"
```
