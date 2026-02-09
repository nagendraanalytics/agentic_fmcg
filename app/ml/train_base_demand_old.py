# import pandas as pd
# import joblib
# from sklearn.ensemble import GradientBoostingRegressor

# # Load training data
# df = pd.read_csv("app/data/training_table.csv")

# features = [
#     "month_num",
#     "cluster"
# ]

# X = df[features]
# y = df["corrected_demand"]

# model = GradientBoostingRegressor(
#     n_estimators=250,
#     learning_rate=0.05,
#     max_depth=4,
#     random_state=42
# )

# model.fit(X, y)

# joblib.dump(model, "app/ml/base_demand_model.pkl")
# print("✅ Base demand model trained")

import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor

# Load training data
df = pd.read_csv("app/data/training_table.csv")

# -----------------------------
# Feature selection
# -----------------------------
features = [
    # Time
    "month_num",

    # Product
    "product_id",
    "brand",
    "category",

    # Store
    "store_id",
    "store_type",
    "cluster",

    # Behavior / history (from feature_store)
    "lag_1",
    "lag_2",
    "rolling_mean_3",
    "rolling_std_3"
]

# Drop rows where lag features are missing
df = df.dropna(subset=features)

X = df[features]
y = df["corrected_demand"]

# -----------------------------
# Model
# -----------------------------
model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "app/ml/base_demand_model.pkl")
print("Base demand model trained with product + store + history features")
