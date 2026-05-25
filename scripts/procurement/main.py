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
from .llm_reasoner import LLMReasoner
from .bom_writer import enrich_bom
from .report_writer import write_report
from .models import ProcurementResult, EnrichedComponent
from . import config as cfg


def compute_total(enriched: list) -> float:
    total = 0.0
    for e in enriched:
        if e.price_unit is not None:
            total += e.price_unit * e.component.qty
    return total


def run(project: str, bom_path: Path, output_dir: Path, push_cart_flag: bool = False) -> None:
    print(f"\n🦦 Forge — Procurement Agent — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Projet : {project}")
    print(f"   BOM    : {bom_path}")
    print(f"   Mode   : {'⚠️  SIMULATION' if cfg.SIMULATION_MODE else '✅ API réelle'}\n")

    # 1. Parser la BOM
    print("📋 Parsing BOM...")
    bom = parse(bom_path, project)
    print(f"   {len(bom.components)} composants chargés\n")

    # 2. Interroger l'API Mouser
    print("🔍 Recherche Mouser...")
    client = MouserClient(api_key=cfg.MOUSER_API_KEY, simulation=cfg.SIMULATION_MODE)
    enriched = []
    for comp in bom.components:
        e = client.search_component(comp)
        flag_str = f" {e.flag}" if e.flag else ""
        sim_str = " [SIM]" if e.simulation else ""
        price_display = f"{e.price_unit:.2f}" if e.price_unit is not None else "N/A"
        print(f"   {comp.ref:5s} {(comp.mpn or comp.description)[:35]:35s} "
              f"→ {price_display:>6} €  stock={e.stock_qty}{flag_str}{sim_str}")
        enriched.append(e)

    result = ProcurementResult(
        bom=bom,
        enriched=enriched,
        total_cost_eur=compute_total(enriched),
        simulation=cfg.SIMULATION_MODE,
    )

    # 3. LLM : alternatives + narratif
    print("\n🧠 Raisonnement LLM (Forge)...")
    reasoner = LLMReasoner()
    result = reasoner.generate_alternatives(result)
    narrative = reasoner.generate_narrative(result, project)

    # 4. Enrichir le BOM source
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
        from .cart_client import push_cart
        print("\n🛒 Création panier Mouser...")
        cart_result = push_cart(result)
        print(f"   {cart_result}")
    else:
        print("\n⏳ En attente de validation JCH avant préparation panier.")
        print("   Relancer avec --push-cart pour créer le panier Mouser.")


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
    args = parser.parse_args()

    if not args.bom.exists():
        print(f"❌ Fichier BOM introuvable : {args.bom}", file=sys.stderr)
        sys.exit(1)

    run(
        project=args.project,
        bom_path=args.bom,
        output_dir=args.output,
        push_cart_flag=args.push_cart,
    )


if __name__ == "__main__":
    main()
