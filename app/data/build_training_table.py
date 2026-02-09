import pandas as pd
from feature_store import build_features

# Load datasets
inventory = pd.read_csv("fmcg_inventory_stockout_monthly.csv")
# lost_sales = pd.read_csv("fmcg_lost_sales_monthly.csv")
products = pd.read_csv("fmcg_product_master.csv")
stores = pd.read_csv("fmcg_stores.csv")
promo_calendar_df=pd.DataFrame()
daily_df = pd.read_csv("fmcg_sales_5yrs_large.csv")

daily_df["date"] = pd.to_datetime(daily_df["date"])
daily_df["month"] = daily_df["date"].dt.to_period("M").dt.to_timestamp()
inventory["month"] = pd.to_datetime(inventory["month"], format="%Y-%m")
inventory["month_num"] = inventory["month"].dt.month



daily_df["lost_sales_qty"] = 0
agg = (
    daily_df.groupby(["store_id", "product_id", "month"])
    .agg(
        sales_qty=("sales_qty", "sum"),
        lost_sales_qty=("lost_sales_qty", "sum"),
        promo_flag=("onpromotion", "max"),
    )
    .reset_index()
)
agg["promo_flag"] = agg["promo_flag"].fillna(0).astype(int)
lost_sales=agg



# Merge inventory + lost sales
df = inventory.merge(
    lost_sales[["month", "store_id", "product_id", "sales_qty"]],
    on=["month", "store_id", "product_id"],
    how="left"
)

df["lost_sales_qty"] = df["sales_qty"].fillna(0)
df["promo_flag"] = df["stockout_flag"]

# Corrected demand
df["corrected_demand"] = df["sold_qty"] + df["sales_qty"]

# Enrich with product & store info
df = df.merge(products[["product_id", "category", "brand"]], on="product_id")
# df = df.merge(stores[["store_id", "cluster"]], on="store_id")
df = df.merge(
    stores[["store_id", "cluster", "store_type"]],
    on="store_id"
)


# Time features
df["month_num"] = pd.to_datetime(df["month"]).dt.month
df = build_features(df)

# Save training data
df.to_csv("training_table.csv", index=False)

print("✅ Training table created:", df.shape)
