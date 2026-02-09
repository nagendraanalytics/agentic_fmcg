
from typing import TypedDict, Optional, List, Literal


class FMCGState(TypedDict, total=False):
    # -------------------------------------------------
    # INPUT (from API / Postman)
    # -------------------------------------------------
    store_id: int
    product_id: int
    month: str                 # e.g. "2022-10"
    promo_flag: bool

    # -------------------------------------------------
    # MASTER DATA (looked up, NOT predicted)
    # -------------------------------------------------
    brand: str
    category: str
    store_type: str

    # -------------------------------------------------
    # DERIVED (Planner / Pre-processing)
    # -------------------------------------------------
    month_num: int
    cluster: int
    route: Literal["promo", "no_promo"]

    # -------------------------------------------------
    # FEATURE STORE (historical behavior)
    # -------------------------------------------------
    # lag_1: Optional[float]
    # lag_2: Optional[float]
    # rolling_mean_3: Optional[float]
    # rolling_std_3: Optional[float]

    # -------------------------------------------------
    # FORECAST / ML OUTPUTS
    # -------------------------------------------------
    base_demand: int
    promo_uplift: int
    forecast: int              # usually same as base_demand
    total_demand: int

    # -------------------------------------------------
    # RULES / INVENTORY DECISIONS
    # -------------------------------------------------
    rules_applied: dict
    service_level: float
    recommended_safety_stock: int

    # -------------------------------------------------
    # MONITORING / RISK
    # -------------------------------------------------
    risk_flags: List[str]

    # -------------------------------------------------
    # RAG / EXPLANATION
    # -------------------------------------------------
    retrieved_knowledge: str
    explanation: str
