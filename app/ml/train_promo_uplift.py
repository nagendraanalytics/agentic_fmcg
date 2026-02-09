import pandas as pd
import joblib
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.feature_extraction import FeatureHasher
from sklearn.ensemble import GradientBoostingRegressor
from app.ml.transformers import to_list_of_strings

# -------------------------------------------------
# Paths
# -------------------------------------------------
DATA_PATH = Path("D:/agentic_fmcg_app/app/data/training_table.csv")
MODEL_PATH = Path("D:/agentic_fmcg_app/app/ml/promo_uplift_model.pkl")

# -------------------------------------------------
# Load data
# -------------------------------------------------
df = pd.read_csv(DATA_PATH)

# -------------------------------------------------
# Filter PROMO rows only
# -------------------------------------------------
promo_df = df[df["promo_flag"] == True].copy()

# -------------------------------------------------
# Target variable
# -------------------------------------------------
TARGET = "promo_uplift"

# Safe derivation if not present
if TARGET not in promo_df.columns:
    promo_df[TARGET] = promo_df["lost_sales_qty"].fillna(0)

# -------------------------------------------------
# RAW feature groups (no encoding here)
# -------------------------------------------------
HASH_FEATURES = ["product_id", "store_id"]

ONEHOT_FEATURES = ["category", "store_type"]

NUMERIC_FEATURES = [
    "month_num",
    "cluster"
]

ALL_FEATURES = HASH_FEATURES + ONEHOT_FEATURES + NUMERIC_FEATURES

promo_df = promo_df.dropna(subset=ALL_FEATURES + [TARGET])

X = promo_df[ALL_FEATURES]
y = promo_df[TARGET]

# -------------------------------------------------
# Preprocessing pipeline
# -------------------------------------------------
preprocessor = ColumnTransformer(
    transformers=[
        (
            "product_hash",
            Pipeline([
                ("to_list", FunctionTransformer(to_list_of_strings, validate=False)),
                ("hash", FeatureHasher(n_features=32, input_type="string")),
            ]),
            ["product_id"],
        ),
        (
            "store_hash",
            Pipeline([
                ("to_list", FunctionTransformer(to_list_of_strings, validate=False)),
                ("hash", FeatureHasher(n_features=16, input_type="string")),
            ]),
            ["store_id"],
        ),
        (
            "category_ohe",
            OneHotEncoder(handle_unknown="ignore"),
            ["category"],
        ),
        (
            "store_type_ohe",
            OneHotEncoder(handle_unknown="ignore"),
            ["store_type"],
        ),
    ],
    remainder="passthrough",
)

# -------------------------------------------------
# Model
# -------------------------------------------------
model = GradientBoostingRegressor(
    n_estimators=250,
    learning_rate=0.05,
    max_depth=3,
    subsample=0.85,
    random_state=42,
)

# -------------------------------------------------
# Full pipeline
# -------------------------------------------------
pipeline = Pipeline(
    steps=[
        ("preprocess", preprocessor),
        ("model", model),
    ]
)

# -------------------------------------------------
# Train
# -------------------------------------------------
pipeline.fit(X, y)

# -------------------------------------------------
# Save SINGLE object
# -------------------------------------------------
joblib.dump(pipeline, MODEL_PATH)

print("✅ Promo uplift pipeline trained successfully")
print(f"📊 Promo rows used: {len(promo_df)}")
print(f"💾 Model saved to: {MODEL_PATH}")
