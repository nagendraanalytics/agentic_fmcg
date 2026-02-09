import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import joblib

MODEL_PATH = "app/ml/demand_model.pkl"

def train_model(df: pd.DataFrame):
    """
    df must contain:
    corrected_demand, promo_flag, month, store_cluster
    """
    X = df.drop(columns=["corrected_demand"])
    y = df["corrected_demand"]

    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    )

    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)

    return model
