# app/data/master_data.py
import pandas as pd

PRODUCT_MASTER = pd.read_csv(r"D:/agentic_fmcg_app/app/data/fmcg_product_master.csv").set_index("product_id")
STORE_MASTER = pd.read_csv(r"D:/agentic_fmcg_app/app/data/fmcg_stores.csv").set_index("store_id")
