# scripts/procurement/api_client.py
import time
import requests
from typing import Optional
from .models import Component, EnrichedComponent
from . import config as cfg


_SIMULATION_STOCK = {
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
                    found_mpn=part.get("ManufacturerPartNumber", ""),
                    simulation=False,
                )
            except Exception as exc:
                if attempt == 2:
                    sim = _simulate(comp)
                    sim.error = str(exc)
                    return sim
                time.sleep(1.5 * (attempt + 1))

        # fallback (unreachable mais requis)
        return _simulate(comp)
