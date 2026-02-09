import pandas as pd
import joblib
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction import FeatureHasher
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, make_scorer

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

HASH_FEATURES = ["product_id", "store_id"]
ONEHOT_FEATURES = ["category", "store_type"]
NUMERIC_FEATURES = ["month_num", "cluster"]

ALL_FEATURES = HASH_FEATURES + ONEHOT_FEATURES + NUMERIC_FEATURES

df = df.dropna(subset=ALL_FEATURES + [TARGET])

X = df[ALL_FEATURES]
y = df[TARGET]


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
    "model__n_estimators": [200, 300, 400, 500],
    "model__learning_rate": [0.03, 0.05, 0.08, 0.1],
    "model__max_depth": [3, 4, 5],
    "model__subsample": [0.7, 0.85, 1.0],
    "model__min_samples_leaf": [5, 10, 20],
}


# -------------------------------------------------
# Scorer (MAE is best for demand)
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
    verbose=2,
    n_jobs=-1,
    random_state=42,
)

print("🔍 Starting hyperparameter tuning...")
search.fit(X, y)


# -------------------------------------------------
# Best model
# -------------------------------------------------
best_pipeline = search.best_estimator_

print("\n🏆 Best parameters:")
for k, v in search.best_params_.items():
    print(f"  {k}: {v}")

print(f"\n📉 Best CV MAE: {-search.best_score_:.2f}")


# -------------------------------------------------
# Save SINGLE object (IMPORTANT)
# -------------------------------------------------
joblib.dump(best_pipeline, MODEL_PATH)

print("\n✅ Base demand pipeline trained successfully")
print(f"Saved to: {MODEL_PATH}")
