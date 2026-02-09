# from sklearn.feature_extraction import FeatureHasher
# import pandas as pd

# def hash_encode(df, column, n_features=16):
#     hasher = FeatureHasher(
#         n_features=n_features,
#         input_type="string"
#     )
#     hashed = hasher.transform(df[column].astype(str))
#     hashed_df = pd.DataFrame(
#         hashed.toarray(),
#         columns=[f"{column}_hash_{i}" for i in range(n_features)],
#         index=df.index
#     )
#     df = df.drop(columns=[column])
#     return pd.concat([df, hashed_df], axis=1)

from sklearn.feature_extraction import FeatureHasher
import pandas as pd

def hash_encode(df, column, n_features=32):
    hasher = FeatureHasher(n_features=n_features, input_type="string")

    hashed = hasher.transform(
        df[column].astype(str).apply(lambda x: [x])
    )

    hashed_df = pd.DataFrame(
        hashed.toarray(),
        columns=[f"{column}_hash_{i}" for i in range(n_features)],
        index=df.index
    )

    df = df.drop(columns=[column])
    df = pd.concat([df, hashed_df], axis=1)

    return df
