import pandas as pd

def target_encode(df, col, target):
    means = df.groupby(col)[target].mean()
    global_mean = df[target].mean()

    df[col + "_te"] = df[col].map(means).fillna(global_mean)
    df = df.drop(columns=[col])
    return df, means, global_mean
