import pandas as pd

# Load datasets
inventory = pd.read_csv("fmcg_inventory_stockout_monthly.csv")
lost_sales = pd.read_csv("fmcg_lost_sales_monthly.csv")
products = pd.read_csv("fmcg_product_master.csv")
stores = pd.read_csv("fmcg_stores.csv")

# Merge inventory + lost sales
df = inventory.merge(
    lost_sales[["month", "store_id", "product_id", "lost_sales_qty"]],
    on=["month", "store_id", "product_id"],
    how="left"
)

df["lost_sales_qty"] = df["lost_sales_qty"].fillna(0)

# Corrected demand
df["corrected_demand"] = df["sold_qty"] + df["lost_sales_qty"]

# Enrich with product & store info
df = df.merge(products[["product_id", "category", "brand"]], on="product_id")
df = df.merge(stores[["store_id", "cluster"]], on="store_id")

# Time features
df["month_num"] = pd.to_datetime(df["month"]).dt.month

# Save training data
df.to_csv("training_table.csv", index=False)

print("✅ Training table created:", df.shape)
