# scripts/procurement/models.py
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Component:
    ref: str
    description: str
    qty: int
    mpn: str = ""
    preferred_supplier: str = ""
    category: str = ""
    notes: str = ""


@dataclass
class SupplierResult:
    """Résultat d'un fournisseur pour un composant."""
    supplier: str = ""  # "Mouser", "DigiKey", etc.
    price_unit: Optional[float] = None
    currency: str = "EUR"
    stock_qty: Optional[int] = None
    lead_time_days: Optional[int] = None
    obsolete: bool = False
    supplier_url: str = ""
    found_mpn: str = ""
    error: str = ""
    is_best: bool = False  # Meilleur choix pour ce composant


@dataclass
class EnrichedComponent:
    component: Component
    price_unit: Optional[float] = None  # Prix du meilleur fournisseur
    currency: str = "EUR"
    stock_qty: Optional[int] = None
    lead_time_days: Optional[int] = None
    obsolete: bool = False
    alternatives: List[str] = field(default_factory=list)
    supplier_url: str = ""
    found_mpn: str = ""  # MPN retourné par Mouser (peut différer du MPN BOM)
    simulation: bool = False
    error: str = ""
    flag: str = ""  # "", "⚠️ MANUEL", "🔴 OBSOLETE"
    # Multi-fournisseur
    supplier_results: List[SupplierResult] = field(default_factory=list)
    best_supplier: str = ""  # "Mouser", "DigiKey", "Aucun"
    mouser_price: Optional[float] = None
    mouser_stock: Optional[int] = None
    mouser_url: str = ""
    digikey_price: Optional[float] = None
    digikey_stock: Optional[int] = None
    digikey_url: str = ""


@dataclass
class BOMData:
    project: str
    source_file: str
    components: List[Component] = field(default_factory=list)


@dataclass
class ProcurementResult:
    bom: BOMData
    enriched: List[EnrichedComponent] = field(default_factory=list)
    total_cost_eur: float = 0.0
    simulation: bool = False
    alerts: List[str] = field(default_factory=list)
    optimization: Optional[dict] = None  # Résultat de basket_optimizer.optimize()
    validations: Optional[dict] = None  # Résultat de validation.validate_component()
