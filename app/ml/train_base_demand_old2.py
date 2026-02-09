import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from app.ml.encoding_pipeline import encode_training_data


# -----------------------------
# Load training data
# -----------------------------
df = pd.read_csv(r"D:/agentic_fmcg_app/app/data/training_table.csv")

# -----------------------------
# Target variable
# -----------------------------
TARGET = "corrected_demand"

# -----------------------------
# Encode categorical features
# -----------------------------
df = encode_training_data(df)

# -----------------------------
# Feature selection
# -----------------------------
FEATURES = [
    # Time
    "month_num",

    # Behavior
    "cluster",

    # History (from feature_store)
    "lag_1",
    "lag_2",
    "rolling_mean_3",
    "rolling_std_3"
]

# Add encoded columns dynamically
FEATURES += [c for c in df.columns if c.startswith("product_id_hash_")]
FEATURES += [c for c in df.columns if c.startswith("store_id_hash_")]
FEATURES += ["brand_te"]
FEATURES += [c for c in df.columns if c.startswith("category_")]
FEATURES += [c for c in df.columns if c.startswith("store_type_")]

# -----------------------------
# Drop rows with missing features
# -----------------------------
df = df.dropna(subset=FEATURES + [TARGET])

X = df[FEATURES]
y = df[TARGET]

# -----------------------------
# Model definition
# -----------------------------
model = GradientBoostingRegressor(
    n_estimators=350,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.9,
    random_state=42
)

# -----------------------------
# Train
# -----------------------------
model.fit(X, y)

# -----------------------------
# Save model
# -----------------------------
joblib.dump(model, r"D:/agentic_fmcg_app/app/ml/base_demand_model.pkl")

print("Base demand model trained successfully")
print(f"Features used: {len(FEATURES)}")
