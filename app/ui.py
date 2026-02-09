import streamlit as st
import requests

st.title("FMCG Inventory Forecast")

payload = {
    "store_id": st.number_input("Store ID", value=18),
    "product_id": st.number_input("Product ID", value=105),
    "month": st.text_input("Month", "2022-10"),
    "promo_flag": st.checkbox("Promo Active", True),
}

if st.button("Run Forecast"):
    r = requests.post(
        "http://192.168.0.106:8000/agentic/inventory",
        json=payload
    )
    st.json(r.json())
