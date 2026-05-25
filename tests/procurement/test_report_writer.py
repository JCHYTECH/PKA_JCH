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
