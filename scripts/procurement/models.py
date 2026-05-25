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
class EnrichedComponent:
    component: Component
    price_unit: Optional[float] = None
    currency: str = "EUR"
    stock_qty: Optional[int] = None
    lead_time_days: Optional[int] = None
    obsolete: bool = False
    alternatives: List[str] = field(default_factory=list)
    supplier_url: str = ""
    simulation: bool = False
    error: str = ""
    flag: str = ""  # "", "⚠️ MANUEL", "🔴 OBSOLETE"


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
