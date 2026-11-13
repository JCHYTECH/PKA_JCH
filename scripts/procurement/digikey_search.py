# scripts/procurement/digikey_search.py
"""
DigiKey Product Search v4 — KeywordSearch endpoint.
Réutilise l'authentification OAuth2 de digikey_client.py.

Endpoint: POST https://api.digikey.com/products/v4/search/keyword
Docs: https://developer.digikey.com/products/product-information-v4/productsearch/keywordsearch
"""
import time
import requests
from typing import Optional
from .models import Component, EnrichedComponent
from . import config as cfg
from .digikey_client import _get_access_token

_SEARCH_URL = f"{'https://sandbox-api.digikey.com' if cfg.DIGIKEY_SANDBOX else 'https://api.digikey.com'}/products/v4/search/keyword"


def _digikey_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "X-DIGIKEY-Client-Id": cfg.DIGIKEY_CLIENT_ID,
        "X-DIGIKEY-Locale-Site": "BE",
        "X-DIGIKEY-Locale-Language": "en",
        "X-DIGIKEY-Locale-Currency": "EUR",
        "Content-Type": "application/json",
    }


def _parse_price(standard_pricing: list) -> Optional[float]:
    """Extrait le prix unitaire du premier break point."""
    if not standard_pricing:
        return None
    try:
        return float(standard_pricing[0].get("UnitPrice", 0))
    except (ValueError, TypeError, IndexError, AttributeError):
        return None


def _parse_stock(quantity_available: int) -> Optional[int]:
    try:
        return int(quantity_available)
    except (ValueError, TypeError):
        return None


class DigiKeySearchClient:
    """Client de recherche produit DigiKey v4 avec OAuth2."""

    def __init__(self, simulation: bool = False):
        self.simulation = simulation or not cfg.DIGIKEY_CLIENT_ID

    def search_component(self, comp: Component) -> EnrichedComponent:
        if self.simulation:
            return EnrichedComponent(
                component=comp,
                flag="⚠️ SIM",
                simulation=True,
                supplier_url=f"https://www.digikey.be/en/products/result?keywords={comp.mpn}",
            )

        query = comp.mpn if comp.mpn else comp.description
        body = {
            "Keywords": query,
            "Limit": 3,
            "Offset": 0,
        }

        for attempt in range(3):
            try:
                token = _get_access_token()
                resp = requests.post(
                    _SEARCH_URL,
                    json=body,
                    headers=_digikey_headers(token),
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()
                products = data.get("Products", [])
                if not products:
                    return EnrichedComponent(
                        component=comp,
                        flag="⚠️ MANUEL",
                        error="Composant non trouvé dans DigiKey",
                        supplier_url=f"https://www.digikey.be/en/products/result?keywords={query}",
                    )

                product = products[0]
                # DigiKey v4 retourne UnitPrice directement (pas dans StandardPricing pour KeywordSearch)
                price = product.get("UnitPrice")
                if price is not None:
                    try:
                        price = float(price)
                    except (ValueError, TypeError):
                        price = None
                stock = _parse_stock(product.get("QuantityAvailable", 0))
                dk_part = product.get("DigiKeyPartNumber", "")
                mpn = product.get("ManufacturerProductNumber", "")
                product_status = product.get("ProductStatus", {})
                if isinstance(product_status, dict):
                    lifecycle = str(product_status.get("Status", "")).lower()
                else:
                    lifecycle = str(product_status).lower()
                obsolete = any(kw in lifecycle for kw in ["obsolete", "eol", "discontinued"])

                supplier_url = (
                    f"https://www.digikey.be/en/products/detail/{dk_part}"
                    if dk_part
                    else f"https://www.digikey.be/en/products/result?keywords={query}"
                )

                return EnrichedComponent(
                    component=comp,
                    price_unit=price,
                    currency="EUR",
                    stock_qty=stock,
                    lead_time_days=None,
                    obsolete=obsolete,
                    flag="🔴 OBSOLETE" if obsolete else "",
                    supplier_url=supplier_url,
                    found_mpn=mpn,
                    simulation=False,
                )

            except Exception as exc:
                if attempt == 2:
                    return EnrichedComponent(
                        component=comp,
                        flag="⚠️ ERREUR",
                        error=str(exc)[:200],
                        simulation=False,
                    )
                time.sleep(1.5 * (attempt + 1))

        return EnrichedComponent(component=comp, flag="⚠️ ERREUR", simulation=False)
