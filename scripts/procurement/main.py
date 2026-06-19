# scripts/procurement/main.py
"""
Usage:
    python3 -m scripts.procurement.main --project WILDNEXUS --bom path/to/bom.xlsx
    python3 -m scripts.procurement.main --project DIM3 --bom path/to/bom.csv
    python3 -m scripts.procurement.main --project TEST --bom tests/procurement/fixtures/sample_bom.csv --output /tmp/test
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

from .bom_parser import parse
from .api_client import MouserClient
from .digikey_search import DigiKeySearchClient
from .llm_reasoner import LLMReasoner
from .bom_writer import enrich_bom
from .report_writer import write_report
from .basket_optimizer import optimize as optimize_baskets
from .validation import validate_component
from .supply_cache import get_cached, set_cache_both, cache_stats
from .models import ProcurementResult, EnrichedComponent, SupplierResult
from . import config as cfg


def _pick_best(enriched: EnrichedComponent) -> EnrichedComponent:
    """Choisit le meilleur fournisseur : priorité stock >0, puis prix le plus bas."""
    mouser_ok = enriched.mouser_stock is not None and enriched.mouser_stock > 0 and not enriched.obsolete
    digikey_ok = enriched.digikey_stock is not None and enriched.digikey_stock > 0

    if mouser_ok and digikey_ok:
        # Les deux OK → prix le plus bas
        mp = enriched.mouser_price or float('inf')
        dp = enriched.digikey_price or float('inf')
        enriched.best_supplier = "Mouser" if mp <= dp else "DigiKey"
    elif mouser_ok:
        enriched.best_supplier = "Mouser"
    elif digikey_ok:
        enriched.best_supplier = "DigiKey"
    else:
        enriched.best_supplier = "Aucun"

    # Appliquer le meilleur choix
    if enriched.best_supplier == "DigiKey":
        enriched.price_unit = enriched.digikey_price
        enriched.stock_qty = enriched.digikey_stock
        enriched.supplier_url = enriched.digikey_url
    return enriched


def compute_total(enriched: list) -> float:
    total = 0.0
    for e in enriched:
        if e.price_unit is not None:
            total += e.price_unit * e.component.qty
    return total


def run(project: str, bom_path: Path, output_dir: Path, push_cart_flag: bool = False, push_digikey_flag: bool = False, no_digikey_search: bool = False) -> None:
    print(f"\n🦦 Forge — Procurement Agent — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Projet : {project}")
    print(f"   BOM    : {bom_path}")
    print(f"   Mode   : {'⚠️  SIMULATION' if cfg.SIMULATION_MODE else '✅ API réelle'}  |  DigiKey: {'⏭️ skip' if no_digikey_search else '✅ actif'}\n")

    # 1. Parser la BOM
    print("📋 Parsing BOM...")
    bom = parse(bom_path, project)
    print(f"   {len(bom.components)} composants chargés\n")

    # 2. Interroger Mouser (avec cache H3)
    cache_hits = 0
    api_calls = 0
    print("🔍 Recherche Mouser...")
    client = MouserClient(api_key=cfg.MOUSER_API_KEY, simulation=cfg.SIMULATION_MODE)
    enriched = []
    for comp in bom.components:
        cached = get_cached(comp.mpn, "Mouser") if comp.mpn else None
        if cached and not cfg.SIMULATION_MODE:
            e = EnrichedComponent(
                component=comp,
                price_unit=cached["price_unit"],
                stock_qty=cached["stock_qty"],
                supplier_url=cached["supplier_url"] or "",
                found_mpn=cached["found_mpn"] or "",
                obsolete=bool(cached["obsolete"]),
                mouser_price=cached["price_unit"],
                mouser_stock=cached["stock_qty"],
                mouser_url=cached["supplier_url"] or "",
            )
            cache_hits += 1
            src = "📦"
        else:
            e = client.search_component(comp)
            api_calls += 1
            src = " "
        flag_str = f" {e.flag}" if e.flag else ""
        sim_str = " [SIM]" if e.simulation else ""
        price_display = f"{e.price_unit:.2f}€" if e.price_unit is not None else "N/A"
        print(f"  {src} {comp.ref:5s} {(comp.mpn or comp.description)[:35]:35s} "
              f"→ Mouser: {price_display:>8}  stock={e.stock_qty}{flag_str}{sim_str}")
        enriched.append(e)

    # 3. Interroger DigiKey (si activé, avec cache H3)
    if not no_digikey_search:
        print("\n🔍 Recherche DigiKey...")
        dk_client = DigiKeySearchClient(simulation=cfg.SIMULATION_MODE)
        for e in enriched:
            comp = e.component
            cached_dk = get_cached(comp.mpn, "DigiKey") if comp.mpn else None
            if cached_dk and not cfg.SIMULATION_MODE:
                dk_result = EnrichedComponent(
                    component=comp,
                    price_unit=cached_dk["price_unit"],
                    stock_qty=cached_dk["stock_qty"],
                    supplier_url=cached_dk["supplier_url"] or "",
                    found_mpn=cached_dk["found_mpn"] or "",
                    obsolete=bool(cached_dk["obsolete"]),
                )
                cache_hits += 1
                src = "📦"
            else:
                dk_result = dk_client.search_component(comp)
                api_calls += 1
                src = " "
            e.digikey_price = dk_result.price_unit
            e.digikey_stock = dk_result.stock_qty
            e.digikey_url = dk_result.supplier_url
            e.supplier_results.append(SupplierResult(
                supplier="DigiKey",
                price_unit=dk_result.price_unit,
                stock_qty=dk_result.stock_qty,
                obsolete=dk_result.obsolete,
                supplier_url=dk_result.supplier_url,
                found_mpn=dk_result.found_mpn,
                error=dk_result.error,
            ))

            dk_price = f"{e.digikey_price:.2f}€" if e.digikey_price is not None else "N/A"
            dk_flag = f" {dk_result.flag}" if dk_result.flag else ""
            print(f"  {src} {comp.ref:5s} {(comp.mpn or comp.description)[:35]:35s} "
                  f"→ DigiKey: {dk_price:>8}  stock={e.digikey_stock}{dk_flag}")

            # Stocker aussi le résultat Mouser
            e.mouser_price = e.price_unit
            e.mouser_stock = e.stock_qty
            e.mouser_url = e.supplier_url

        # Choisir le meilleur fournisseur pour chaque composant
        print("\n⚖️  Arbitrage Mouser vs DigiKey...")
        for e in enriched:
            e = _pick_best(e)
            best_price = f"{e.price_unit:.2f}€" if e.price_unit is not None else "N/A"
            print(f"   {e.component.ref:5s} → {e.best_supplier:7s}  {best_price:>8}  stock={e.stock_qty}")
    else:
        print("\n⏭️  DigiKey search désactivé (--no-digikey)")

    # Sauvegarder dans le cache
    if not cfg.SIMULATION_MODE:
        for e in enriched:
            if e.component.mpn:
                set_cache_both(e.component, e, e)

    stats = cache_stats()
    print(f"\n📦 Cache H3 : {cache_hits} hits, {api_calls} appels API  |  total cache: {stats['total']} entrées")

    result = ProcurementResult(
        bom=bom,
        enriched=enriched,
        total_cost_eur=compute_total(enriched),
        simulation=cfg.SIMULATION_MODE,
    )

    # 4. Validation MPN (H2)
    print("\n🔬 Validation MPN (H2 — Arbor Cycle 2)...")
    validations = {}
    for e in enriched:
        v = validate_component(e)
        validations[e.component.ref or e.component.description[:20]] = v
        icon = v.confidence
        warnings_str = f" — {len(v.warnings)} alerte(s)" if v.warnings else ""
        print(f"   {icon} {v.component_ref:20s} score={v.score:.0%}{warnings_str}")
        for w in v.warnings[:2]:
            print(f"      ⤷ {w}")
    result.validations = validations

    # 5. LLM : alternatives + narratif
    print("\n🧠 Raisonnement LLM (Forge)...")
    reasoner = LLMReasoner()
    result = reasoner.generate_alternatives(result)
    narrative = reasoner.generate_narrative(result, project)

    # 4. Optimisation panier
    if not no_digikey_search:
        print("\n🛒 Optimisation paniers Mouser/DigiKey...")
        opt_result = optimize_baskets(enriched)
        for basket in opt_result["baskets"]:
            comps_str = f"{len(basket.components)} composants"
            free_str = "✅ GRATUIT" if basket.free_shipping else f"{basket.shipping:.2f}€"
            print(f"   {basket.supplier:7s} : {comps_str:15s}  sous-total={basket.subtotal:.2f}€  port={free_str}  total={basket.total:.2f}€")
        if opt_result["unavailable"]:
            print(f"   ⚠️  {len(opt_result['unavailable'])} composant(s) indisponible(s)")
        for rec in opt_result["recommendations"]:
            print(f"   {rec}")
        result.optimization = opt_result
    else:
        result.optimization = None

    # 5. Enrichir le BOM source
    print("\n📊 Enrichissement BOM...")
    enriched_bom_path = enrich_bom(result, output_dir=output_dir)
    print(f"   → {enriched_bom_path}")

    # 5. Générer le rapport Markdown
    print("\n📝 Génération rapport...")
    report_path = write_report(result, output_dir=output_dir, narrative=narrative)
    print(f"   → {report_path}")

    # 6. Résumé final
    print(f"\n{'='*60}")
    print(f"  Coût total estimé : {result.total_cost_eur:.2f} €")
    alerts = [e for e in enriched if e.flag]
    if alerts:
        print(f"  ⚠️  Alertes : {len(alerts)} composant(s) à vérifier")
        for e in alerts:
            print(f"     - {e.component.ref} : {e.flag}")
    else:
        print("  ✅ Aucune alerte")
    print(f"{'='*60}")

    if push_cart_flag:
        try:
            from .cart_client import push_cart
            print("\n🛒 Création panier Mouser...")
            cart_result = push_cart(result)
            print(f"   {cart_result}")
        except ImportError:
            print("\n⚠️  Cart API non encore disponible (cart_client.py manquant).")
            print("   Lance Task 8 pour activer cette fonctionnalité.")
    else:
        print("\n⏳ En attente de validation JCH avant préparation panier.")
        print("   Relancer avec --push-cart pour créer le panier Mouser.")
        print("   Relancer avec --push-digikey pour créer la MyList DigiKey.")

    if push_digikey_flag:
        from .digikey_client import push_digikey_list
        print("\n🛒 Création MyList DigiKey...")
        dk_result = push_digikey_list(result)
        print(f"   {dk_result}")


def main():
    parser = argparse.ArgumentParser(description="PKA Procurement Agent")
    parser.add_argument("--project", required=True, help="Nom du projet (ex: WILDNEXUS)")
    parser.add_argument("--bom", required=True, type=Path, help="Chemin vers le fichier BOM")
    parser.add_argument(
        "--output",
        type=Path,
        default=cfg.TEAM_INBOX_PATH,
        help="Dossier de sortie (défaut: TEAM_Inbox/)",
    )
    parser.add_argument(
        "--push-cart",
        action="store_true",
        help="Pousse le panier Mouser après validation JCH (requiert MOUSER_API_KEY)",
    )
    parser.add_argument(
        "--push-digikey",
        action="store_true",
        help="Crée une MyList DigiKey après validation JCH (requiert DIGIKEY_CLIENT_ID/SECRET)",
    )
    parser.add_argument(
        "--no-digikey",
        action="store_true",
        help="Désactive la recherche DigiKey (Mouser uniquement)",
    )
    args = parser.parse_args()

    if not args.bom.exists():
        print(f"❌ Fichier BOM introuvable : {args.bom}", file=sys.stderr)
        sys.exit(1)

    run(
        project=args.project,
        bom_path=args.bom,
        output_dir=args.output,
        push_cart_flag=args.push_cart,
        push_digikey_flag=args.push_digikey,
        no_digikey_search=args.no_digikey,
    )


if __name__ == "__main__":
    main()