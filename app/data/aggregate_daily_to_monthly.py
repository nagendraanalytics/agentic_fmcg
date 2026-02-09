import pandas as pd

def aggregate_daily_to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    agg = (
        df.groupby(["store_id", "product_id", "month"])
        .agg(
            sold_qty=("sold_qty", "sum"),
            lost_sales_qty=("lost_sales_qty", "sum"),
            promo_flag=("promo_flag", "max"),
        )
        .reset_index()
    )

    agg["promo_flag"] = agg["promo_flag"].fillna(0).astype(int)

    return agg
