def build_features(df):
    df = df.sort_values(["store_id", "product_id", "month"])

    group_cols = ["store_id", "product_id"]

    df["lag_1"] = df.groupby(group_cols)["corrected_demand"].shift(1)
    df["lag_2"] = df.groupby(group_cols)["corrected_demand"].shift(2)

    df["rolling_mean_3"] = (
        df.groupby(group_cols)["corrected_demand"]
        .rolling(3)
        .mean()
        .reset_index(level=group_cols, drop=True)
    )

    df["rolling_std_3"] = (
        df.groupby(group_cols)["corrected_demand"]
        .rolling(3)
        .std()
        .reset_index(level=group_cols, drop=True)
    )

    df = df.dropna()
    return df
