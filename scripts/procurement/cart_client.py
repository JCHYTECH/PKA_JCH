# scripts/procurement/cart_client.py
"""
Invoqué UNIQUEMENT après validation explicite JCH.
Pousse les composants validés dans un panier Mouser via l'API Cart.
JCH finalise la commande manuellement sur mouser.be.

⚠️  L'API Cart Mouser exige que l'IP de la machine soit whitelistée
    dans le compte Mouser (séparément de la Search API).
    Exécuter depuis le RPi (IP fixe, déjà connue de Mouser).
"""
import requests
from .models import ProcurementResult
from . import config as cfg


def push_cart(result: ProcurementResult, cart_name: str = "PKA_Procurement") -> str:
    """
    Crée ou met à jour un panier Mouser avec les composants du résultat.
    Retourne une string décrivant le résultat (URL panier ou message d'erreur).
    Jamais de commande automatique.
    """
    cart_key_to_use = cfg.MOUSER_CART_API_KEY or cfg.MOUSER_API_KEY
    if not cart_key_to_use:
        return (
            "⚠️ Mode simulation — panier non créé. "
            "Ajouter MOUSER_CART_API_KEY dans .procurement.env pour activer."
        )

    items = []
    for e in result.enriched:
        # Utilise found_mpn (retourné par Mouser) ou le mpn BOM
        mpn = e.found_mpn or e.component.mpn
        if not mpn or e.flag == "⚠️ MANUEL":
            continue
        items.append({
            "MouserPartNumber": mpn,
            "Quantity": str(e.component.qty),
            "CustomerPartNumber": e.component.ref,
        })

    if not items:
        return "⚠️ Aucun composant éligible au panier (MPN manquants ou tous marqués MANUEL)."

    payload = {
        "CartKey": "",  # vide = nouveau panier
        "CartItems": items,
    }
    url = f"{cfg.MOUSER_CART_URL}?apiKey={cart_key_to_use}"

    try:
        resp = requests.post(url, json=payload, timeout=15, allow_redirects=False)

        # Mouser renvoie 302 → Error.aspx quand l'IP n'est pas autorisée pour le Cart API
        if resp.status_code == 302:
            location = resp.headers.get("Location", "")
            if "Error.aspx" in location or "error" in location.lower():
                return (
                    "❌ Panier refusé par Mouser (302 → Error.aspx).\n"
                    "   Cause probable : IP non whitelistée pour la Cart API.\n"
                    "   Solution : lancer depuis le RPi (tkajch.local) dont l'IP\n"
                    "   est autorisée dans le compte Mouser.\n"
                    f"   URL tentée : {url.split('?')[0]}"
                )
            return f"❌ Redirection inattendue vers : {location}"

        resp.raise_for_status()
        data = resp.json()
        cart_key = data.get("CartKey", "")
        cart_url = f"https://www.mouser.be/Cart/?cartKey={cart_key}" if cart_key else "N/A"
        return f"✅ Panier Mouser créé : {cart_url}"

    except requests.exceptions.Timeout:
        return (
            "❌ Timeout Cart API — la requête a été redirigée vers www.mouser.com.\n"
            "   Cause probable : IP non whitelistée pour la Cart API.\n"
            "   Solution : lancer depuis le RPi (tkajch.local)."
        )
    except Exception as exc:
        return f"❌ Erreur création panier : {exc}"
