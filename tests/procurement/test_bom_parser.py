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
