import joblib
import pandas as pd
from pathlib import Path

# -------------------------------------------------
# Model paths
# -------------------------------------------------
BASE_MODEL_PATH = Path("app/ml/base_demand_model.pkl")
PROMO_MODEL_PATH = Path("app/ml/promo_uplift_model.pkl")

_base_pipeline = None
_promo_pipeline = None


# -------------------------------------------------
# Lazy loaders (singleton)
# -------------------------------------------------
def _load_base_pipeline():
    global _base_pipeline
    if _base_pipeline is None:
        if not BASE_MODEL_PATH.exists():
            raise FileNotFoundError(f"Base model not found: {BASE_MODEL_PATH}")
        _base_pipeline = joblib.load(BASE_MODEL_PATH)
    return _base_pipeline


def _load_promo_pipeline():
    global _promo_pipeline
    if _promo_pipeline is None:
        if not PROMO_MODEL_PATH.exists():
            raise FileNotFoundError(f"Promo model not found: {PROMO_MODEL_PATH}")
        _promo_pipeline = joblib.load(PROMO_MODEL_PATH)
    return _promo_pipeline


# -------------------------------------------------
# Build RAW feature row (NO encoding here)
# -------------------------------------------------
def _build_raw_row(
    *,
    store_id: int,
    product_id: int,
    category: str,
    store_type: str,
    month_num: int,
    cluster: int
) -> pd.DataFrame:
    """
    Build a single-row DataFrame using RAW features.
    Encoding is handled INSIDE the pipeline.
    """

    return pd.DataFrame([{
        "store_id": store_id,
        "product_id": product_id,
        "category": category,
        "store_type": store_type,
        "month_num": month_num,
        "cluster": cluster
    }])


# -------------------------------------------------
# Base demand prediction
# -------------------------------------------------
def predict_base_demand(
    *,
    store_id: int,
    product_id: int,
    category: str,
    store_type: str,
    month_num: int,
    cluster: int
) -> int:
    """
    Predict base (non-promo) demand.
    """

    pipeline = _load_base_pipeline()

    X = _build_raw_row(
        store_id=store_id,
        product_id=product_id,
        category=category,
        store_type=store_type,
        month_num=month_num,
        cluster=cluster
    )

    pred = pipeline.predict(X)[0]
    pred = float(pred)  # force Python type

    return max(int(round(pred)), 0)


# -------------------------------------------------
# Promo uplift prediction
# -------------------------------------------------
def predict_promo_uplift(
    *,
    store_id: int,
    product_id: int,
    category: str,
    store_type: str,
    month_num: int,
    cluster: int
) -> int:
    """
    Predict incremental demand due to promotion.
    """

    pipeline = _load_promo_pipeline()

    X = _build_raw_row(
        store_id=store_id,
        product_id=product_id,
        category=category,
        store_type=store_type,
        month_num=month_num,
        cluster=cluster
    )

    uplift = pipeline.predict(X)[0]
    uplift = float(uplift)  # force Python type

    return max(int(round(uplift)), 0)
