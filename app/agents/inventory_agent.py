# def inventory_agent(state):
#     demand = state["forecast"]
#     uplift = state.get("promo_uplift", 0)

#     safety_stock = int(demand * 0.30 + uplift)

#     state["recommended_safety_stock"] = safety_stock
#     state["total_demand"] = demand + uplift

#     return state

def inventory_agent(state: dict) -> dict:
    """
    Inventory & safety stock calculation agent.
    Assumes forecasting agents have already populated:
    - base_demand
    - promo_uplift (optional)
    - total_demand
    """

    # -----------------------------
    # Required inputs
    # -----------------------------
    base_demand = int(state.get("base_demand", 0))
    promo_uplift = int(state.get("promo_uplift", 0))

    # Ensure total_demand is correct and consistent
    total_demand = base_demand + promo_uplift
    state["total_demand"] = total_demand

    # -----------------------------
    # Service level (from rules or default)
    # -----------------------------
    service_level = float(state.get("service_level", 0.95))

    # -----------------------------
    # Base safety stock logic
    # (simple, interpretable, extensible)
    # -----------------------------
    # Example mapping:
    # 0.90 → 20%
    # 0.95 → 30%
    # 0.98 → 40%
    safety_factor_map = {
        0.90: 0.20,
        0.95: 0.30,
        0.98: 0.40,
    }

    safety_factor = safety_factor_map.get(service_level, 0.30)

    safety_stock = int(round(base_demand * safety_factor))

    # -----------------------------
    # Promo buffer (if applicable)
    # -----------------------------
    if promo_uplift > 0:
        # Keep buffer conservative — uplift is already incremental
        safety_stock += int(round(promo_uplift * 0.5))

    # -----------------------------
    # Final assignment
    # -----------------------------
    state["recommended_safety_stock"] = max(safety_stock, 0)

    return state
