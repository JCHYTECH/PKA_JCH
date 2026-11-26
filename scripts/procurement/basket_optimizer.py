# scripts/procurement/basket_optimizer.py
"""
Optimise la répartition des composants entre Mouser et DigiKey
en fonction des prix, stocks, et seuils de livraison gratuite.

Règles :
- Mouser BE : livraison gratuite ≥ 50 €, sinon ~18 €
- DigiKey BE : livraison gratuite ≥ 50 €, sinon ~18 €
- Priorité : disponibilité > coût total livré > centralisation
"""
from dataclasses import dataclass, field
from typing import List, Optional
from .models import EnrichedComponent

# Seuils de livraison gratuite (source: sites officiels, vérifiés 2026-05-18)
SHIPPING_THRESHOLDS = {
    "Mouser": {"free_at": 50.0, "cost_below": 18.0, "currency": "EUR"},
    "DigiKey": {"free_at": 50.0, "cost_below": 18.0, "currency": "EUR"},
}


@dataclass
class Basket:
    supplier: str
    components: List[EnrichedComponent] = field(default_factory=list)
    subtotal: float = 0.0
    shipping: float = 0.0
    total: float = 0.0
    free_shipping: bool = False


def _component_cost(e: EnrichedComponent, supplier: str) -> float:
    """Coût total pour ce composant chez ce fournisseur."""
    price = e.mouser_price if supplier == "Mouser" else e.digikey_price
    if price is None:
        return 0.0
    return price * e.component.qty


def _price_for(e: EnrichedComponent, supplier: str) -> Optional[float]:
    return e.mouser_price if supplier == "Mouser" else e.digikey_price


def _stock_for(e: EnrichedComponent, supplier: str) -> Optional[int]:
    return e.mouser_stock if supplier == "Mouser" else e.digikey_stock


def calculate_shipping(supplier: str, subtotal: float) -> tuple:
    """Retourne (frais_port, gratuit)."""
    threshold = SHIPPING_THRESHOLDS.get(supplier, {})
    free_at = threshold.get("free_at", 50.0)
    cost = threshold.get("cost_below", 18.0)
    if subtotal >= free_at:
        return (0.0, True)
    return (cost, False)


def optimize(enriched: List[EnrichedComponent]) -> dict:
    """
    Optimise la répartition Mouser/DigiKey.

    Stratégie :
    1. Assigner chaque composant au meilleur fournisseur (best_supplier)
    2. Calculer les paniers et frais de port
    3. Si un panier est juste sous le seuil de gratuité, proposer
       de déplacer un composant de l'autre panier pour l'atteindre.
    4. Si un composant est dispo que chez l'un, forcer ce fournisseur.

    Retourne un dict avec :
    - baskets: liste de Basket
    - total_cost: coût total avec frais de port
    - savings_vs_manual: économie estimée vs 8 paniers manuels
    - recommendations: liste de strings
    """
    mouser_basket = Basket(supplier="Mouser")
    digikey_basket = Basket(supplier="DigiKey")
    unavailable = []

    for e in enriched:
        # Si le composant n'est dispo que chez l'un, forcer
        m_ok = _stock_for(e, "Mouser") is not None and (_stock_for(e, "Mouser") or 0) > 0
        d_ok = _stock_for(e, "DigiKey") is not None and (_stock_for(e, "DigiKey") or 0) > 0

        if m_ok and not d_ok:
            mouser_basket.components.append(e)
            mouser_basket.subtotal += _component_cost(e, "Mouser")
        elif d_ok and not m_ok:
            digikey_basket.components.append(e)
            digikey_basket.subtotal += _component_cost(e, "DigiKey")
        elif not m_ok and not d_ok:
            unavailable.append(e)
        else:
            # Les deux dispos → suivre best_supplier
            if e.best_supplier == "DigiKey":
                digikey_basket.components.append(e)
                digikey_basket.subtotal += _component_cost(e, "DigiKey")
            else:
                mouser_basket.components.append(e)
                mouser_basket.subtotal += _component_cost(e, "Mouser")

    # Calculer frais de port
    for basket in [mouser_basket, digikey_basket]:
        basket.shipping, basket.free_shipping = calculate_shipping(
            basket.supplier, basket.subtotal
        )
        basket.total = basket.subtotal + basket.shipping

    # Optimisation de rattrapage : si un panier est à <5€ du seuil gratuit
    recommendations = []
    for below_basket, above_basket in [
        (mouser_basket, digikey_basket),
        (digikey_basket, mouser_basket),
    ]:
        threshold = SHIPPING_THRESHOLDS[below_basket.supplier]["free_at"]
        gap = threshold - below_basket.subtotal
        if 0 < gap < 10.0 and below_basket.shipping > 0:
            # Chercher un composant dans above_basket qui pourrait combler le gap
            for e in above_basket.components[:]:
                cost_if_moved = _component_cost(e, below_basket.supplier)
                if cost_if_moved <= 0:
                    continue
                savings = below_basket.shipping - cost_if_moved
                if savings > 0:
                    recommendations.append(
                        f"💡 Déplacer {e.component.ref} ({e.component.description[:30]}) "
                        f"de {above_basket.supplier} → {below_basket.supplier} "
                        f"(+{cost_if_moved:.2f}€, économie port: {below_basket.shipping:.2f}€, "
                        f"net: {savings:.2f}€)"
                    )

    total = mouser_basket.total + digikey_basket.total
    manual_shipping_estimate = 55.0  # 8 paniers manuels ≈ 55€ de port (source: Bruno)

    return {
        "baskets": [mouser_basket, digikey_basket],
        "total_cost": total,
        "shipping_total": mouser_basket.shipping + digikey_basket.shipping,
        "savings_vs_manual": manual_shipping_estimate - (mouser_basket.shipping + digikey_basket.shipping),
        "unavailable": unavailable,
        "recommendations": recommendations,
    }
