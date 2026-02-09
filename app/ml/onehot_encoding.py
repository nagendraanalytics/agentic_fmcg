import pandas as pd

def onehot_encode(df, columns):
    return pd.get_dummies(
        df,
        columns=columns,
        drop_first=True
    )
