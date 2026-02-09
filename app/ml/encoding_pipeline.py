from app.ml.hash_encoding import hash_encode
from app.ml.onehot_encoding import onehot_encode
from app.ml.target_encoding import target_encode
import joblib

ENCODER_PATH = r"D:/agentic_fmcg_app/app/ml/encoders"


def encode_training_data(df):

    # 1. Hash encoding
    df = hash_encode(df, "product_id", 32)
    df = hash_encode(df, "store_id", 16)

    # 2. Target encoding
    df, brand_map, brand_mean = target_encode(
        df, "brand", "corrected_demand"
    )

    # 3. One-hot encoding
    df = onehot_encode(df, ["category", "store_type"])

    # Save target encoders
    joblib.dump(
        {
            "brand_map": brand_map,
            "brand_mean": brand_mean
        },
        f"{ENCODER_PATH}/target_encoders.pkl"
    )

    return df

def encode_inference_data(df):
    import joblib

    enc = joblib.load(f"{ENCODER_PATH}/target_encoders.pkl")

    # Hash encoding
    df = hash_encode(df, "product_id", 32)
    df = hash_encode(df, "store_id", 16)

    # Target encoding (brand)
    df["brand_te"] = df["brand"].map(enc["brand_map"]).fillna(enc["brand_mean"])
    df = df.drop(columns=["brand"])

    # One-hot (must match training columns)
    df = onehot_encode(df, ["category", "store_type"])

    return df
