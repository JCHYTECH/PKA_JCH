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
