# tests/procurement/test_api_client.py
import pytest
import responses as resp_lib
from unittest.mock import patch
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
@patch('scripts.procurement.api_client.time.sleep')
def test_search_api_timeout_fallback_simulation(mock_sleep):
    from scripts.procurement.config import MOUSER_SEARCH_URL
    resp_lib.add(
        resp_lib.POST,
        MOUSER_SEARCH_URL,
        body=Exception("timeout"),
    )
    resp_lib.add(
        resp_lib.POST,
        MOUSER_SEARCH_URL,
        body=Exception("timeout"),
    )
    resp_lib.add(
        resp_lib.POST,
        MOUSER_SEARCH_URL,
        body=Exception("timeout"),
    )
    client = MouserClient(api_key="TEST_KEY", simulation=False)
    comp = Component(ref="U1", description="ESP32", qty=1, mpn="ESP32-S3-WROOM-1U-N8R8")
    result = client.search_component(comp)
    assert result.simulation is True
    assert result.error != ""
