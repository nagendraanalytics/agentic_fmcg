from typing import Dict, Any

from app.ml.predict import (
    predict_base_demand,
    predict_promo_uplift,
)

# -------------------------------------------------
# Forecast Agent
# -------------------------------------------------
def forecast_agent(input_data: Dict[str, Any]) -> Dict[str, int]:
    """
    Forecast total demand using:
    - Base demand model
    - Promo uplift model (optional)

    Expected input_data keys:
    {
        store_id: int,
        product_id: int,
        category: str,
        store_type: str,
        month_num: int,
        cluster: int,
        promo_flag: bool (optional)
    }
    """

    # -------------------------------------------------
    # Required fields (STRICT but CORRECT)
    # -------------------------------------------------
    # required_fields = [
    #     "store_id",
    #     "product_id",
    #     "category",
    #     "store_type",
    #     "month_num",
    #     "cluster",
    # ]

    # missing = [f for f in required_fields if f not in input_data]
    # if missing:
    #     raise ValueError(f"Missing required fields: {missing}")

    # -------------------------------------------------
    # Defaults for optional features
    # -------------------------------------------------
    # lag_1 = float(input_data.get("lag_1", 0.0))
    # lag_2 = float(input_data.get("lag_2", 0.0))
    # rolling_mean_3 = float(input_data.get("rolling_mean_3", 0.0))
    # rolling_std_3 = float(input_data.get("rolling_std_3", 0.0))

    promo_flag = bool(input_data.get("promo_flag", False))

    # -------------------------------------------------
    # Base demand prediction
    # -------------------------------------------------
    base_demand = predict_base_demand(
        store_id=int(input_data["store_id"]),
        product_id=int(input_data["product_id"]),
        category=input_data["category"],
        store_type=input_data["store_type"],
        month_num=int(input_data["month_num"]),
        cluster=int(input_data["cluster"]),
        # lag_1=lag_1,
        # lag_2=lag_2,
        # rolling_mean_3=rolling_mean_3,
        # rolling_std_3=rolling_std_3,
    )

    # -------------------------------------------------
    # Promo uplift (ONLY if promo_flag = True)
    # -------------------------------------------------
    promo_uplift = 0
    if promo_flag:
        promo_uplift = predict_promo_uplift(
            store_id=int(input_data["store_id"]),
            product_id=int(input_data["product_id"]),
            category=input_data["category"],
            store_type=input_data["store_type"],
            month_num=int(input_data["month_num"]),
            cluster=int(input_data["cluster"]),
            # lag_1=lag_1,
            # rolling_mean_3=rolling_mean_3,
            # rolling_std_3=rolling_std_3,
        )

    # -------------------------------------------------
    # Final response (JSON-safe)
    # -------------------------------------------------
    return {
        "base_demand": int(base_demand),
        "promo_uplift": int(promo_uplift),
        "total_demand": int(base_demand + promo_uplift),
    }
