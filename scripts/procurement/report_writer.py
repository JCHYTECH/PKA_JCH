from datetime import date
from pathlib import Path
from collections import defaultdict
from typing import List
from .models import ProcurementResult, EnrichedComponent

_TEMPLATE = """\
# Rapport Procurement — {project} — {today}
{simulation_banner}
**Généré par :** Forge 🦦 (PKA Procurement Agent)
**Source BOM :** `{source_file}`
**Coût total estimé :** {total_cost:.2f} €
**Mode simulation :** {simulation_flag}

---

## Comparaison Mouser vs DigiKey

{comparison_table}

---

## Paniers optimisés

{basket_section}

---

## Validation MPN (H2 — Arbor)

{validation_section}

---

## Checklist terrain Chouette 🦉

{chouette_checklist}

---

## Résumé

{narrative}

---

## Composants analysés

| Ref | Description | Qté | MPN | Prix unit. | Stock | Délai (j) | Statut | Fournisseur |
|-----|-------------|-----|-----|-----------|-------|-----------|--------|-------------|
{components_table}

---

## Alertes

{alerts_section}

---

## Paniers recommandés

{cart_section}

---

## Alternatives proposées

{alternatives_section}

---

## Décisions en attente JCH

{decisions_section}

---

*Aucune commande ne sera passée sans validation explicite JCH.*
"""


def _component_row(e: EnrichedComponent) -> str:
    comp = e.component
    price = f"{e.price_unit:.2f} €" if e.price_unit is not None else "N/A"
    stock = str(e.stock_qty) if e.stock_qty is not None else "N/A"
    lead = str(e.lead_time_days) if e.lead_time_days is not None else "N/A"
    status = e.flag if e.flag else ("⚠️ SIM" if e.simulation else "✅ OK")
    supplier_link = f"[Mouser]({e.supplier_url})" if e.supplier_url else "—"
    return (
        f"| {comp.ref} | {comp.description} | {comp.qty} | "
        f"`{comp.mpn or '—'}` | {price} | {stock} | {lead} | {status} | {supplier_link} |"
    )


def _comparison_row(e: EnrichedComponent) -> str:
    comp = e.component
    mp = f"{e.mouser_price:.2f}€" if e.mouser_price is not None else "N/A"
    ms = str(e.mouser_stock) if e.mouser_stock is not None else "N/A"
    dp = f"{e.digikey_price:.2f}€" if e.digikey_price is not None else "N/A"
    ds = str(e.digikey_stock) if e.digikey_stock is not None else "N/A"
    best = e.best_supplier or "—"
    return (
        f"| {comp.ref or '—':6s} | {comp.description[:35]:35s} | {comp.qty} | "
        f"`{comp.mpn or '—':25s}` | {mp:>8} | {ms:>6} | {dp:>8} | {ds:>6} | **{best}** |"
    )


def _chouette_checklist(enriched: List[EnrichedComponent]) -> str:
    """Génère la checklist terrain basée sur l'expérience WildNexus (Chouette)."""
    items = []
    for e in enriched:
        warnings = []
        desc = e.component.description.lower()
        mpn = (e.component.mpn or "").lower()

        # Vérifications automatiques
        if "868" in mpn or "lora" in desc:
            if "eu868" not in mpn and "863" not in mpn:
                warnings.append("📻 Vérifier bande EU868 (pas US915/AS923)")
        if "ov5640" in desc or "caméra" in desc:
            warnings.append("📸 Vérifier monture M12 + variante NoIR (pas IR-cut visible)")
            warnings.append("📸 Vérifier MOQ — commandes proto souvent refusées")
        if "led ir" in desc or "vslb" in mpn or "vslb" in desc:
            warnings.append("🔦 Confirmer longueur d'onde compatible faune (940nm préféré)")
        if "antenne" in desc or "antenna" in desc or "molex" in desc:
            warnings.append("📡 Vérifier connecteur IPEX/U.FL (pas SMA seul)")
        if "boîtier" in desc or "hammond" in desc or "boitier" in desc:
            warnings.append("📦 Vérifier place pour presse-étoupe + câble antenne")
        if "holder" in desc or "pile" in desc or "aa" in desc:
            warnings.append("🔋 Vérifier orientation contacts (ressort = −)")
        if "connecteur" in desc or "câble" in desc:
            warnings.append("🔌 Vérifier longueur câble suffisante pour boîtier")
        if warnings:
            items.append(f"**{e.component.ref}** — {e.component.description[:40]}\n" + "\n".join(f"  - {w}" for w in warnings))
    return "\n\n".join(items) if items else "_Aucune alerte terrain détectée automatiquement._"


def _cart_by_supplier(result: ProcurementResult) -> str:
    carts: dict = defaultdict(list)
    for e in result.enriched:
        supplier = e.component.preferred_supplier or "Non spécifié"
        if e.price_unit is not None:
            subtotal = e.price_unit * e.component.qty
            carts[supplier].append(
                f"- `{e.component.mpn or e.component.description}` "
                f"× {e.component.qty} = {subtotal:.2f} €  \n"
                f"  {e.supplier_url}"
            )
    if not carts:
        return "_Aucun panier disponible (mode simulation ou composants non trouvés)._"
    lines = []
    for supplier, items in carts.items():
        lines.append(f"### {supplier}\n" + "\n".join(items))
    return "\n\n".join(lines)


def _basket_section(result: ProcurementResult) -> str:
    opt = result.optimization
    if not opt:
        return "_Optimisation panier non disponible (mode Mouser seul)._"
    lines = []
    for basket in opt["baskets"]:
        free_icon = "✅" if basket.free_shipping else "❌"
        lines.append(
            f"### {basket.supplier} — {len(basket.components)} composants\n"
            f"- Sous-total : {basket.subtotal:.2f} €\n"
            f"- Livraison : {basket.shipping:.2f} € {free_icon} gratuit\n"
            f"- **Total : {basket.total:.2f} €**"
        )
    lines.append(f"\n💰 Économie estimée vs 8 paniers manuels : **{opt['savings_vs_manual']:.2f} €** de frais de port")
    if opt["recommendations"]:
        lines.append("\n### Suggestions d'optimisation\n" + "\n".join(opt["recommendations"]))
    return "\n\n".join(lines)


def _validation_section(result: ProcurementResult) -> str:
    """Génère la section validation MPN du rapport."""
    if not result.validations:
        return "_Validation MPN non disponible._"
    lines = [
        "| Ref | Confiance | Score | Vérifications |",
        "|-----|-----------|------:|--------------|",
    ]
    for ref, v in result.validations.items():
        checks_str = "; ".join(
            f"{'✅' if c.match else '❌'} {c.param}" for c in v.checks
        ) if v.checks else "—"
        warnings_str = "<br>".join(v.warnings) if v.warnings else ""
        detail = f"{checks_str}"
        if warnings_str:
            detail += f"<br>⚠️ {warnings_str}"
        lines.append(f"| {ref:20s} | {v.confidence} | {v.score:.0%} | {detail} |")
    return "\n".join(lines)


def write_report(
    result: ProcurementResult,
    output_dir: Path,
    narrative: str = "",
) -> Path:
    today = date.today().isoformat()
    project = result.bom.project
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{today}_Forge_procurement_{project}.md"
    out = output_dir / filename

    simulation_banner = (
        "> ⚠️ **[SIMULATION]** — Les données prix/stock sont simulées. "
        "Aucune clé API active.\n"
        if result.simulation else ""
    )

    components_table = "\n".join(_component_row(e) for e in result.enriched)

    alerts = list(result.alerts or [])
    comparison_table = (
        "| Ref | Description | Qté | MPN | Prix Mouser | Stock M | Prix DK | Stock DK | Best |\n"
        "|-----|-------------|-----|-----|------------:|--------:|--------:|--------:|------|\n"
        + "\n".join(_comparison_row(e) for e in result.enriched)
    )
    for e in result.enriched:
        if e.obsolete:
            msg = f"🔴 **{e.component.ref}** (`{e.component.mpn}`) — Obsolète"
            if msg not in alerts:
                alerts.append(msg)
        if e.stock_qty == 0:
            msg = f"⚠️ **{e.component.ref}** (`{e.component.mpn}`) — Rupture de stock"
            if msg not in alerts:
                alerts.append(msg)
    alerts_section = "\n".join(f"- {a}" for a in alerts) if alerts else "✅ _Aucune alerte._"

    alt_lines = []
    for e in result.enriched:
        if e.alternatives:
            alt_lines.append(
                f"- **{e.component.ref}** (`{e.component.mpn}`): "
                + ", ".join(f"`{a}`" for a in e.alternatives)
            )
    alternatives_section = "\n".join(alt_lines) if alt_lines else "_Aucune alternative proposée._"

    manual = [e for e in result.enriched if e.flag == "⚠️ MANUEL"]
    decisions = []
    if manual:
        decisions.append("**Composants à localiser manuellement :**")
        for e in manual:
            decisions.append(
                f"- {e.component.ref} — {e.component.description} (`{e.component.mpn}`)"
            )
    if result.simulation:
        decisions.append("\n**Activer les clés API** pour obtenir des données réelles.")
    decisions_section = "\n".join(decisions) if decisions else "_Aucune décision bloquante._"

    content = _TEMPLATE.format(
        project=project,
        today=today,
        simulation_banner=simulation_banner,
        source_file=result.bom.source_file,
        total_cost=result.total_cost_eur,
        simulation_flag="OUI ⚠️" if result.simulation else "NON",
        narrative=narrative or "_Narratif LLM non disponible._",
        components_table=components_table,
        alerts_section=alerts_section,
        comparison_table=comparison_table,
        basket_section=_basket_section(result),
        validation_section=_validation_section(result),
        chouette_checklist=_chouette_checklist(result.enriched),
        cart_section=_cart_by_supplier(result),
        alternatives_section=alternatives_section,
        decisions_section=decisions_section,
    )
    out.write_text(content, encoding="utf-8")
    return out