# scripts/procurement/llm_reasoner.py
import json
import anthropic
from .models import ProcurementResult, EnrichedComponent
from . import config as cfg


class LLMReasoner:
    """Utilise Claude pour générer des alternatives et le narratif du rapport."""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key or cfg.ANTHROPIC_API_KEY
        self._client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None

    def _call(self, system: str, user: str) -> str:
        if not self._client:
            return ""
        msg = self._client.messages.create(
            model=cfg.ANTHROPIC_MODEL,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return msg.content[0].text

    def generate_alternatives(self, result: ProcurementResult) -> ProcurementResult:
        """Pour chaque composant obsolète ou en rupture, demande 2 alternatives à Claude."""
        if not self._client:
            return result

        needs_alt = [
            e for e in result.enriched
            if e.obsolete or (e.stock_qty is not None and e.stock_qty == 0)
        ]
        for enriched in needs_alt:
            comp = enriched.component
            prompt = (
                f"Composant: {comp.description} (MPN: {comp.mpn})\n"
                f"Catégorie: {comp.category}\n"
                f"Raison: {'Obsolète' if enriched.obsolete else 'Rupture de stock'}\n\n"
                "Propose exactement 2 alternatives avec le même footprint/interface si possible. "
                "Retourne uniquement un JSON array de MPNs: [\"MPN1\", \"MPN2\"]"
            )
            try:
                raw = self._call(
                    system="Tu es un expert en composants électroniques. Réponds UNIQUEMENT en JSON.",
                    user=prompt,
                )
                alternatives = json.loads(raw)
                if isinstance(alternatives, list):
                    enriched.alternatives = [str(a) for a in alternatives[:2]]
            except (json.JSONDecodeError, Exception):
                enriched.alternatives = []

        return result

    def generate_narrative(self, result: ProcurementResult, project: str) -> str:
        """Génère la section narrative du rapport (résumé + alertes + recommandations)."""
        if not self._client:
            return "_LLM non disponible — narratif automatique désactivé._"

        summary_lines = []
        for e in result.enriched:
            line = (
                f"- {e.component.ref} ({e.component.mpn or e.component.description}): "
                f"prix={e.price_unit}€, stock={e.stock_qty}, "
                f"obsolète={e.obsolete}, flag={e.flag or 'OK'}"
            )
            summary_lines.append(line)

        prompt = (
            f"Projet: {project}\n"
            f"Mode simulation: {result.simulation}\n"
            f"Coût total estimé: {result.total_cost_eur:.2f}€\n\n"
            "Données composants:\n" + "\n".join(summary_lines) + "\n\n"
            "Rédige en français un résumé procurement (3-5 phrases max) couvrant: "
            "état global, alertes prioritaires, recommandations fournisseur."
        )
        return self._call(
            system="Tu es Forge, ingénieur systèmes PKA. Sois concis et factuel.",
            user=prompt,
        )
