# scripts/procurement/validation.py
"""
Double-validation MPN : extraction des specs attendues depuis la description BOM
et contre-vérification contre les paramètres retournés par l'API (Mouser/DigiKey).

Cycle Arbor H2 — Réduit le risque d'erreur de variante (suffixe packaging,
fréquence radio, cutoff tape/reel, etc.).
"""
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from .models import EnrichedComponent


@dataclass
class SpecCheck:
    """Un contrôle de spec extrait de la description BOM."""
    param: str          # Nom du paramètre (ex: "Tension sortie", "Fréquence")
    expected: str       # Valeur attendue (ex: "3.3V", "868MHz")
    found: str = ""     # Valeur trouvée dans l'API
    match: bool = False
    warning: str = ""


@dataclass
class ValidationResult:
    component_ref: str
    confidence: str = "✅"  # ✅ Haute, ⚠️ Moyenne, 🔴 Basse
    score: float = 1.0     # 0.0–1.0
    checks: List[SpecCheck] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


# ── Extracteurs de specs depuis la description BOM ──────────────────────────

_VOLTAGE_PATTERNS = [
    (r'(\d+\.?\d*)\s*V\b', "V"),          # "3.3V", "5V", "1.8V"
    (r'(\d+\.?\d*)\s*volt', "V"),
]
_CURRENT_PATTERNS = [
    (r'(\d+\.?\d*)\s*mA\b', "mA"),
    (r'(\d+\.?\d*)\s*A\b', "A"),
    (r'(\d+\.?\d*)\s*µA\b', "µA"),
    (r'(\d+\.?\d*)\s*nA\b', "nA"),
]
_FREQ_PATTERNS = [
    (r'(\d+\.?\d*)\s*MHz\b', "MHz"),
    (r'(\d+\.?\d*)\s*GHz\b', "GHz"),
    (r'(\d+\.?\d*)\s*kHz\b', "kHz"),
    (r'(\d+)\s*MHz', "MHz"),  # "868MHz" sans espace
]
_PACKAGE_PATTERNS = [
    (r'\b(SOT-?23\b)', ""),
    (r'\b(SOT-?583\b)', ""),
    (r'\b(QFN\d*)\b', ""),
    (r'\b(0603|0805|1206|0402)\b', ""),
    (r'\b(TSOT\d*)\b', ""),
    (r'\b(DFN\d*)\b', ""),
    (r'\b(SOIC-?\d*)\b', ""),
    (r'\b(TO-?\d+)\b', ""),
]
_TYPE_HINTS = {
    "buck": "buck_converter",
    "ldo": "ldo_regulator",
    "mosfet": "mosfet",
    "led": "led",
    "pir": "pir_sensor",
    "mems": "mems_microphone",
    "micro": "mems_microphone",
    "inductance": "inductor",
    "inductor": "inductor",
    "antenne": "antenna",
    "antenna": "antenna",
    "capteur": "sensor",
    "sensor": "sensor",
    "dissipateur": "heatsink",
    "heatsink": "heatsink",
    "passifs": "passive_kit",
    "lora": "lora_radio",
    "lora": "lora_radio",
    "868": "eu868",
    "915": "us915",
}


def _extract_value(pattern_list: list, text: str) -> Optional[str]:
    for pat, unit in pattern_list:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = m.group(1)
            return f"{val}{unit}" if unit else val
    return None


def _extract_voltage(text: str) -> Optional[str]:
    return _extract_value(_VOLTAGE_PATTERNS, text)


def _extract_current(text: str) -> Optional[str]:
    return _extract_value(_CURRENT_PATTERNS, text)


def _extract_frequency(text: str) -> Optional[str]:
    return _extract_value(_FREQ_PATTERNS, text)


def _extract_package(text: str) -> Optional[str]:
    return _extract_value(_PACKAGE_PATTERNS, text)


def _extract_type(text: str) -> Optional[str]:
    text_lower = text.lower()
    for keyword, hint in _TYPE_HINTS.items():
        if keyword in text_lower:
            return hint
    return None


def _normalize(value: str) -> str:
    """Normalise une valeur pour comparaison."""
    v = value.strip().lower().replace(" ", "").replace(",", ".")
    # Enlever les unités redondantes dans les paramètres API
    v = v.replace("volt", "v").replace("amp", "a").replace("hertz", "hz")
    return v


def _fuzzy_match(expected: str, found: str) -> bool:
    """Vérifie si la valeur trouvée correspond à l'attendue."""
    e = _normalize(expected)
    f = _normalize(found)
    if e == f:
        return True
    # Tolérance numérique (ex: "3.3v" vs "3.3 v")
    e_num = re.sub(r'[^0-9.]', '', e)
    f_num = re.sub(r'[^0-9.]', '', f)
    if e_num and f_num:
        try:
            if abs(float(e_num) - float(f_num)) < 0.01:
                return True
        except ValueError:
            pass
    # L'un contient l'autre
    return e in f or f in e


# ── Recherche dans les paramètres API ────────────────────────────────────────

def _search_in_params(params: list, keywords: List[str]) -> Optional[str]:
    """Cherche une valeur dans les paramètres API (DigiKey/Mouser)."""
    if not params:
        return None
    for param in params:
        if isinstance(param, dict):
            name = str(param.get("Parameter", param.get("ParameterText", ""))).lower()
            value = str(param.get("Value", param.get("ValueText", "")))
        elif isinstance(param, str):
            name = param.lower()
            value = ""
        else:
            continue
        for kw in keywords:
            if kw in name:
                return value
    return None


def _extract_parameters_from_response(e: EnrichedComponent, supplier: str) -> list:
    """Récupère les paramètres depuis la réponse API stockée."""
    for sr in e.supplier_results:
        if sr.supplier == supplier:
            return getattr(sr, '_raw_params', [])
    return []


# ── Validation principale ────────────────────────────────────────────────────

def validate_component(e: EnrichedComponent) -> ValidationResult:
    """
    Valide le composant trouvé contre la description BOM.
    
    Stratégie :
    1. Extraire les specs de la description BOM
    2. Chercher ces specs dans les paramètres API (Mouser ou DigiKey selon best_supplier)
    3. Signaler les discordances
    
    Retourne un ValidationResult avec score de confiance et avertissements.
    """
    desc = f"{e.component.description} {e.component.mpn} {e.component.notes}"
    checks = []
    warnings = []

    # Extraire les specs attendues
    expected_voltage = _extract_voltage(desc)
    expected_current = _extract_current(desc)
    expected_freq = _extract_frequency(desc)
    expected_package = _extract_package(desc)
    expected_type = _extract_type(desc)

    # Récupérer les paramètres du meilleur fournisseur
    supplier = e.best_supplier or "Mouser"
    params = _extract_parameters_from_response(e, supplier)

    # Vérifier la tension
    if expected_voltage:
        found_v = _search_in_params(params, ["voltage", "output voltage", "tension", "vout"])
        match = _fuzzy_match(expected_voltage, found_v) if found_v else False
        checks.append(SpecCheck(
            param="Tension",
            expected=expected_voltage,
            found=found_v or "non trouvé",
            match=match,
            warning="" if match else f"Tension attendue {expected_voltage}, trouvé {found_v or 'rien'}"
        ))
        if not match:
            warnings.append(checks[-1].warning)

    # Vérifier le courant
    if expected_current:
        found_c = _search_in_params(params, ["current", "output current", "courant", "iout", "rated current"])
        match = _fuzzy_match(expected_current, found_c) if found_c else False
        checks.append(SpecCheck(
            param="Courant",
            expected=expected_current,
            found=found_c or "non trouvé",
            match=match,
            warning="" if match else f"Courant attendu {expected_current}, trouvé {found_c or 'rien'}"
        ))
        if not match:
            warnings.append(checks[-1].warning)

    # Vérifier la fréquence (critique pour LoRa/radio)
    if expected_freq:
        found_f = _search_in_params(params, ["frequency", "fréquence", "band", "freq"])
        match = _fuzzy_match(expected_freq, found_f) if found_f else False
        checks.append(SpecCheck(
            param="Fréquence",
            expected=expected_freq,
            found=found_f or "non trouvé",
            match=match,
            warning="" if match else f"FRÉQUENCE CRITIQUE: attendu {expected_freq}, trouvé {found_f or 'rien'}"
        ))
        if not match:
            warnings.append(checks[-1].warning)

    # Vérifier le package
    if expected_package:
        found_p = _search_in_params(params, ["package", "case", "boîtier", "supplier device package"])
        match = _fuzzy_match(expected_package, found_p) if found_p else False
        checks.append(SpecCheck(
            param="Package",
            expected=expected_package,
            found=found_p or "non trouvé",
            match=match,
            warning="" if match else f"Package attendu {expected_package}, trouvé {found_p or 'rien'}"
        ))
        if not match:
            warnings.append(checks[-1].warning)

    # Vérifier le type de composant
    if expected_type:
        type_hint_ok = True  # Le type hint est informatif, pas bloquant
        # Vérifications spécifiques par type
        if "eu868" in desc.lower() or "868" in desc.lower():
            found_band = _search_in_params(params, ["frequency", "band", "freq"])
            if found_band and "868" not in found_band and "863" not in found_band:
                type_hint_ok = False
                warnings.append(f"Bande fréquence: attendu 868MHz, trouvé {found_band}")

    # Calculer le score de confiance
    total_checks = len(checks)
    passed = sum(1 for c in checks if c.match)
    no_data = sum(1 for c in checks if c.found == "non trouvé")
    # Si toutes les vérifications n'ont pas de données API, ne pas pénaliser
    if total_checks > 0 and no_data == total_checks:
        score = 0.8  # Confiance modérée : specs extraites mais pas vérifiables
    else:
        score = passed / total_checks if total_checks > 0 else 1.0

    if score >= 0.9:
        confidence = "✅"
    elif score >= 0.6:
        confidence = "⚠️"
    else:
        confidence = "🔴"

    # Ajouter les avertissements génériques
    if e.obsolete:
        warnings.append("Composant obsolète")
        confidence = "🔴"
        score = min(score, 0.3)
    if e.stock_qty is not None and e.stock_qty == 0:
        warnings.append("Rupture de stock")
        confidence = "🔴"
        score = min(score, 0.4)

    return ValidationResult(
        component_ref=e.component.ref or e.component.description[:20],
        confidence=confidence,
        score=score,
        checks=checks,
        warnings=warnings,
    )
