import joblib
import pandas as pd
from pathlib import Path

BASE_MODEL_PATH = Path("app/ml/base_demand_model.pkl")
PROMO_MODEL_PATH = Path("app/ml/promo_uplift_model.pkl")

_base_model = None
_promo_model = None


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


def predict_base_demand(month_num: int, cluster: int) -> int:
    if month_num is None or cluster is None:
        raise ValueError("month_num and cluster must not be None")

    model = _load_base_model()

    X = pd.DataFrame([{
        "month_num": int(month_num),
        "cluster": int(cluster)
    }])

    return int(model.predict(X)[0])


def predict_promo_uplift(month_num: int, cluster: int) -> int:
    if month_num is None or cluster is None:
        raise ValueError("month_num and cluster must not be None")

    model = _load_promo_model()

    X = pd.DataFrame([{
        "month_num": int(month_num),
        "cluster": int(cluster)
    }])

    return max(int(model.predict(X)[0]), 0)
