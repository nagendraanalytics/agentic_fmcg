import joblib
import pandas as pd
from pathlib import Path

from app.ml.encoding_pipeline import encode_inference_data


BASE_MODEL_PATH = Path("app/ml/base_demand_model.pkl")
PROMO_MODEL_PATH = Path("app/ml/promo_uplift_model.pkl")

_base_model = None
_promo_model = None


# -------------------------------------------------
# Model loaders (singleton)
# -------------------------------------------------
def _load_base_model():
    global _base_model
    if _base_model is None:
        if not BASE_MODEL_PATH.exists():
            raise FileNotFoundError(f"Base model not found: {BASE_MODEL_PATH}")
        _base_model = joblib.load(BASE_MODEL_PATH)
    return _base_model


def _load_promo_model():
    global _promo_model
    if _promo_model is None:
        if not PROMO_MODEL_PATH.exists():
            raise FileNotFoundError(f"Promo model not found: {PROMO_MODEL_PATH}")
        _promo_model = joblib.load(PROMO_MODEL_PATH)
    return _promo_model


# -------------------------------------------------
# Feature builder (CRITICAL)
# -------------------------------------------------
def _build_feature_row(
    *,
    store_id: int,
    product_id: int,
    brand: str,
    category: str,
    store_type: str,
    month_num: int,
    cluster: int,
    promo_flag: int = 0,
    lag_1: float = 0.0,
    lag_2: float = 0.0,
    rolling_mean_3: float = 0.0,
    rolling_std_3: float = 0.0
) -> pd.DataFrame:
    """
    Build a single-row DataFrame matching training features.
    """

    row = pd.DataFrame([{
        "store_id": store_id,
        "product_id": product_id,
        "brand": brand,
        "category": category,
        "store_type": store_type,
        "month_num": month_num,
        "cluster": cluster,
        "promo_flag": promo_flag,
        "lag_1": lag_1,
        "lag_2": lag_2,
        "rolling_mean_3": rolling_mean_3,
        "rolling_std_3": rolling_std_3
    }])

    # Apply SAME encoding pipeline as training
    row = encode_inference_data(row)

    return row


# -------------------------------------------------
# Base demand prediction
# -------------------------------------------------
def predict_base_demand(
    *,
    store_id: int,
    product_id: int,
    brand: str,
    category: str,
    store_type: str,
    month_num: int,
    cluster: int,
    lag_1: float = 0.0,
    lag_2: float = 0.0,
    rolling_mean_3: float = 0.0,
    rolling_std_3: float = 0.0
) -> int:
    """
    Predict normal (non-promo) demand.
    """

    model = _load_base_model()

    X = _build_feature_row(
        store_id=store_id,
        product_id=product_id,
        brand=brand,
        category=category,
        store_type=store_type,
        month_num=month_num,
        cluster=cluster,
        promo_flag=0,
        lag_1=lag_1,
        lag_2=lag_2,
        rolling_mean_3=rolling_mean_3,
        rolling_std_3=rolling_std_3
    )

    prediction = model.predict(X)[0]
    return max(int(round(prediction)), 0)


# -------------------------------------------------
# Promo uplift prediction
# -------------------------------------------------
def predict_promo_uplift(
    *,
    store_id: int,
    product_id: int,
    brand: str,
    category: str,
    store_type: str,
    month_num: int,
    cluster: int,
    lag_1: float = 0.0,
    rolling_mean_3: float = 0.0,
    rolling_std_3: float = 0.0
) -> int:
    """
    Predict additional demand due to promotion.
    """

    model = _load_promo_model()

    X = _build_feature_row(
        store_id=store_id,
        product_id=product_id,
        brand=brand,
        category=category,
        store_type=store_type,
        month_num=month_num,
        cluster=cluster,
        promo_flag=1,
        lag_1=lag_1,
        rolling_mean_3=rolling_mean_3,
        rolling_std_3=rolling_std_3
    )

    uplift = model.predict(X)[0]
    return max(int(round(uplift)), 0)
