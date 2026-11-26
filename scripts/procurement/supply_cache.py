# scripts/procurement/supply_cache.py
"""
Cache de recherche procurement — table supply_cache dans team.db.

Cycle Arbor H3 — Réduit les appels API redondants.
Un MPN déjà recherché est servi depuis le cache si le TTL n'est pas expiré.

TTL par défaut :
- Composants avec stock : 7 jours (le stock change vite)
- Composants sans stock / obsolètes : 1 jour
- Prix seuls (hors stock) : 30 jours
"""
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .models import EnrichedComponent, Component

_DB_PATH = Path(__file__).parent.parent.parent / "TEAM" / "team.db"


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def get_cached(mpn: str, supplier: str) -> Optional[dict]:
    """Récupère une entrée du cache si elle existe et n'est pas expirée."""
    if not mpn:
        return None
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM supply_cache WHERE mpn = ? AND supplier = ?",
            (mpn, supplier)
        ).fetchone()
        if not row:
            return None
        row = dict(row)
        last = datetime.fromisoformat(row["last_checked"])
        ttl = row["ttl_days"]
        if datetime.now() - last > timedelta(days=ttl):
            return None  # Expiré
        return row
    except Exception:
        return None
    finally:
        conn.close()


def set_cache(mpn: str, supplier: str, enriched: EnrichedComponent) -> None:
    """Enregistre ou met à jour une entrée dans le cache."""
    if not mpn:
        return
    # Ne pas cacher des données vides (protège contre les runs partiels)
    price = enriched.price_unit
    stock = enriched.stock_qty
    if supplier == "DigiKey":
        price = enriched.digikey_price
        stock = enriched.digikey_stock
    if price is None and stock is None:
        return  # Rien à cacher

    # Déterminer le TTL
    if enriched.obsolete or enriched.flag == "🔴 OBSOLETE":
        ttl = 365  # Obsolète → garder longtemps
    elif enriched.stock_qty is not None and enriched.stock_qty == 0:
        ttl = 1    # Rupture → revérifier demain
    elif enriched.stock_qty is not None and enriched.stock_qty > 0:
        ttl = 7    # En stock → 1 semaine
    else:
        ttl = 30   # Prix seul → 1 mois

    conn = _get_conn()
    try:
        conn.execute(
            """INSERT OR REPLACE INTO supply_cache
               (mpn, supplier, price_unit, stock_qty, currency, supplier_url,
                found_mpn, obsolete, last_checked, ttl_days)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                mpn,
                supplier,
                enriched.price_unit if supplier == enriched.best_supplier or supplier == "Mouser"
                    else (enriched.digikey_price if supplier == "DigiKey" else enriched.mouser_price),
                enriched.stock_qty if supplier == enriched.best_supplier or supplier == "Mouser"
                    else (enriched.digikey_stock if supplier == "DigiKey" else enriched.mouser_stock),
                enriched.currency,
                enriched.supplier_url if supplier == enriched.best_supplier else
                    (enriched.digikey_url if supplier == "DigiKey" else enriched.mouser_url),
                enriched.found_mpn,
                1 if enriched.obsolete else 0,
                datetime.now().isoformat(),
                ttl,
            )
        )
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


def set_cache_both(comp: Component, mouser_result: EnrichedComponent, digikey_result: EnrichedComponent) -> None:
    """Enregistre les résultats Mouser ET DigiKey dans le cache."""
    mpn = comp.mpn
    if not mpn:
        return

    # Mouser
    m = EnrichedComponent(component=comp)
    m.price_unit = mouser_result.price_unit
    m.stock_qty = mouser_result.stock_qty
    m.supplier_url = mouser_result.supplier_url
    m.found_mpn = mouser_result.found_mpn
    m.obsolete = mouser_result.obsolete
    m.flag = mouser_result.flag
    m.best_supplier = "Mouser"
    m.mouser_price = mouser_result.price_unit
    m.mouser_stock = mouser_result.stock_qty
    m.mouser_url = mouser_result.supplier_url
    set_cache(mpn, "Mouser", m)

    # DigiKey
    d = EnrichedComponent(component=comp)
    d.best_supplier = "DigiKey"
    d.digikey_price = digikey_result.price_unit
    d.digikey_stock = digikey_result.stock_qty
    d.digikey_url = digikey_result.supplier_url
    d.obsolete = digikey_result.obsolete
    d.flag = digikey_result.flag
    set_cache(mpn, "DigiKey", d)


def cache_stats() -> dict:
    """Retourne les statistiques du cache."""
    conn = _get_conn()
    try:
        total = conn.execute("SELECT COUNT(*) as n FROM supply_cache").fetchone()["n"]
        fresh = conn.execute(
            "SELECT COUNT(*) as n FROM supply_cache WHERE last_checked > ?",
            (datetime.now().isoformat(),)
        ).fetchone()["n"]  # Approximation
        return {"total": total, "fresh": fresh}
    except Exception:
        return {"total": 0, "fresh": 0}
    finally:
        conn.close()
