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
    # Trouver la ligne de headers (première ligne avec > 1 valeur non-None)
    header_row = None
    for row in ws.iter_rows(values_only=True):
        non_null = [v for v in row if v is not None and str(v).strip()]
        if len(non_null) > 1:
            header_row = row
            break
    assert header_row is not None
    header_strs = [str(h) for h in header_row if h is not None]
    assert any("Prix" in h for h in header_strs)


def test_enrich_csv_creates_output():
    src = TMP / "sample_bom.csv"
    shutil.copy(FIXTURES / "sample_bom.csv", src)
    result = _make_result(src)
    out = enrich_bom(result, output_dir=TMP)
    assert out.exists()
    content = out.read_text()
    assert "Prix" in content or "prix" in content
