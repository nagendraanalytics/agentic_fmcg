import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor

from encoding_pipeline import encode_training_data

# -----------------------------
# Load training data
# -----------------------------
df = pd.read_csv(r"D:/agentic_fmcg_app/app/data/training_table.csv")

# -----------------------------
# Filter PROMO periods only
# -----------------------------
promo_df = df[df["promo_flag"] == True].copy()

# -----------------------------
# Target variable
# Promo uplift = extra demand during promotion
# -----------------------------
TARGET = "promo_uplift"

# If promo_uplift is not precomputed, derive it safely
if TARGET not in promo_df.columns:
    promo_df[TARGET] = promo_df["lost_sales_qty"].fillna(0)

# -----------------------------
# Encode categorical features
# (same pipeline as base model)
# -----------------------------
promo_df = encode_training_data(promo_df)

# -----------------------------
# Feature selection
# -----------------------------
FEATURES = [
    # Time
    "month_num",

    # Store / behavior
    "cluster",

    # History (promo sensitivity depends on recent trend)
    "lag_1",
    "rolling_mean_3",
    "rolling_std_3"
]

# Add encoded columns dynamically
FEATURES += [c for c in promo_df.columns if c.startswith("product_id_hash_")]
FEATURES += [c for c in promo_df.columns if c.startswith("store_id_hash_")]
FEATURES += ["brand_te"]
FEATURES += [c for c in promo_df.columns if c.startswith("category_")]
FEATURES += [c for c in promo_df.columns if c.startswith("store_type_")]

# -----------------------------
# Drop rows with missing values
# -----------------------------
promo_df = promo_df.dropna(subset=FEATURES + [TARGET])

X = promo_df[FEATURES]
y = promo_df[TARGET]

# -----------------------------
# Model definition
# -----------------------------
model = GradientBoostingRegressor(
    n_estimators=250,
    learning_rate=0.05,
    max_depth=3,
    subsample=0.85,
    random_state=42
)

# -----------------------------
# Train model
# -----------------------------
model.fit(X, y)

# -----------------------------
# Save model
# -----------------------------
joblib.dump(model, "D:/agentic_fmcg_app/app/ml/promo_uplift_model.pkl")

print("✅ Promo uplift model trained successfully")
print(f"📊 Promo rows used: {len(promo_df)}")
print(f"📊 Features used: {len(FEATURES)}")
