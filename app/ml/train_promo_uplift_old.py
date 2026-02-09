import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor

df = pd.read_csv("app/data/training_table.csv")

# Only promo months inferred by lost sales presence
promo_df = df[df["lost_sales_qty"] > 0].copy()

promo_df["promo_uplift"] = promo_df["lost_sales_qty"]

features = [
    "month_num",
    "cluster"
]

X = promo_df[features]
y = promo_df["promo_uplift"]

model = GradientBoostingRegressor(
    n_estimators=150,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "app/ml/promo_uplift_model.pkl")
print("✅ Promo uplift model trained")
