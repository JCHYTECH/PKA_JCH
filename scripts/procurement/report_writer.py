from datetime import date
from pathlib import Path
from collections import defaultdict
from .models import ProcurementResult, EnrichedComponent

_TEMPLATE = """\
# Rapport Procurement — {project} — {today}
{simulation_banner}
**Généré par :** Forge 🦦 (PKA Procurement Agent)
**Source BOM :** `{source_file}`
**Coût total estimé :** {total_cost:.2f} €
**Mode simulation :** {simulation_flag}

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
    for e in result.enriched:
        if e.obsolete:
            msg = f"🔴 **{e.component.ref}** (`{e.component.mpn}`) — Obsolète"
            if msg not in alerts:
                alerts.append(msg)
        if e.stock_qty == 0:
            msg = f"⚠️ **{e.component.ref}** (`{e.component.mpn}`) — Rupture de stock"
            if msg not in alerts:
                alerts.append(msg)
    alerts_section = "\n".join(f"- {a}" for a in alerts) if alerts else "_Aucune alerte._"

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
        cart_section=_cart_by_supplier(result),
        alternatives_section=alternatives_section,
        decisions_section=decisions_section,
    )
    out.write_text(content, encoding="utf-8")
    return out
