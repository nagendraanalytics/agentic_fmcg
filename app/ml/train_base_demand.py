import pandas as pd
import joblib
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction import FeatureHasher
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import FunctionTransformer
from app.ml.transformers import to_list_of_strings


# -------------------------------------------------
# Paths
# -------------------------------------------------
DATA_PATH = Path(r"D:/agentic_fmcg_app/app/data/training_table.csv")
MODEL_PATH = Path(r"D:/agentic_fmcg_app/app/ml/base_demand_model.pkl")


# -------------------------------------------------
# Load data
# -------------------------------------------------
df = pd.read_csv(DATA_PATH)

TARGET = "corrected_demand"

# -------------------------------------------------
# Feature groups (RAW, NOT ENCODED)
# -------------------------------------------------
HASH_FEATURES = ["product_id", "store_id"]

ONEHOT_FEATURES = ["category", "store_type"]

NUMERIC_FEATURES = [
    "month_num",
    "cluster"
    
]

ALL_FEATURES = HASH_FEATURES + ONEHOT_FEATURES + NUMERIC_FEATURES

df = df.dropna(subset=ALL_FEATURES + [TARGET])

X = df[ALL_FEATURES]
y = df[TARGET]

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
    n_estimators=350,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.9,
    random_state=42,
)

# -------------------------------------------------
# Full pipeline (🔥 THIS IS THE KEY 🔥)
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

print("✅ Base demand pipeline trained successfully")
print(f"Saved to: {MODEL_PATH}")
