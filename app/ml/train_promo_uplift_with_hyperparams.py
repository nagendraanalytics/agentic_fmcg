import pandas as pd
import joblib
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.feature_extraction import FeatureHasher
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, make_scorer

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
# Feature groups (STRUCTURAL ONLY)
# -------------------------------------------------
HASH_FEATURES = ["product_id", "store_id"]
ONEHOT_FEATURES = ["category", "store_type"]
NUMERIC_FEATURES = ["month_num", "cluster"]

ALL_FEATURES = HASH_FEATURES + ONEHOT_FEATURES + NUMERIC_FEATURES

promo_df = promo_df.dropna(subset=ALL_FEATURES + [TARGET])

X = promo_df[ALL_FEATURES]
y = promo_df[TARGET]

print(f"📊 Promo rows used for training: {len(promo_df)}")


# -------------------------------------------------
# Preprocessing
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
# Base model
# -------------------------------------------------
gbr = GradientBoostingRegressor(random_state=42)


# -------------------------------------------------
# Full pipeline
# -------------------------------------------------
pipeline = Pipeline(
    steps=[
        ("preprocess", preprocessor),
        ("model", gbr),
    ]
)


# -------------------------------------------------
# Hyperparameter search space
# -------------------------------------------------
param_dist = {
    "model__n_estimators": [150, 250, 350, 450],
    "model__learning_rate": [0.03, 0.05, 0.08, 0.1],
    "model__max_depth": [2, 3, 4],
    "model__subsample": [0.7, 0.85, 1.0],
    "model__min_samples_leaf": [5, 10, 20],
}


# -------------------------------------------------
# Scoring (MAE is best for uplift)
# -------------------------------------------------
mae_scorer = make_scorer(mean_absolute_error, greater_is_better=False)


# -------------------------------------------------
# Hyperparameter tuning
# -------------------------------------------------
search = RandomizedSearchCV(
    pipeline,
    param_distributions=param_dist,
    n_iter=20,
    scoring=mae_scorer,
    cv=3,
    n_jobs=-1,
    verbose=2,
    random_state=42,
)

print("🔍 Starting promo uplift hyperparameter tuning...")
search.fit(X, y)


# -------------------------------------------------
# Best estimator
# -------------------------------------------------
best_pipeline = search.best_estimator_

print("\n🏆 Best promo uplift parameters:")
for k, v in search.best_params_.items():
    print(f"  {k}: {v}")

print(f"\n📉 Best CV MAE: {-search.best_score_:.2f}")


# -------------------------------------------------
# Save SINGLE object
# -------------------------------------------------
joblib.dump(best_pipeline, MODEL_PATH)

print("\n✅ Promo uplift pipeline trained successfully")
print(f"💾 Model saved to: {MODEL_PATH}")
