import streamlit as st
import requests
import json

API_URL = "http://192.168.0.106:8000/agentic/prompt"

st.set_page_config(page_title="FMCG Agentic Forecast", layout="centered")

st.title("📦 FMCG Agentic Demand Forecast & Inventory Planning")
st.caption("Natural language → Forecast → Business explanation")

# -------------------------------------------------
# Prompt Input
# -------------------------------------------------
st.subheader("🧠 Ask in Natural Language")

prompt = st.text_area(
    "Enter your question",
    height=200,
    value=(
       """ Please forecast the demand for Pepsi (product ID 105) at Store 15 for the month of November 2022.
        This is a Modern Trade (MT) store in cluster 4.
        The product belongs to the Beverages category.
        A promotion is active during this period.
        Please calculate base demand, promotional uplift, total demand, recommended safety stock,
        and explain the impact of the promotion on inventory planning.
        """    )
)

# -------------------------------------------------
# Run
# -------------------------------------------------
if st.button("🚀 Run Forecast"):
    with st.spinner("Running agentic pipeline..."):
        try:
            response = requests.post(
                API_URL,
                json={"prompt": prompt},
                timeout=60
            )
           
            # -----------------------------
            # HTTP-level check
            # -----------------------------
            if response.status_code != 200:
                st.error(f"API Error {response.status_code}")
                st.text(response.text)
                st.stop()

            # -----------------------------
            # JSON-level check
            # -----------------------------
            try:
                result = response.json()
            except json.JSONDecodeError:
                st.error("Invalid JSON returned from API")
                st.text(response.text)
                st.stop()

            # -----------------------------
            # Application-level error
            # -----------------------------
            if "error" in result:
                st.error("Unable to generate forecast")
                st.json(result)
                st.stop()

            # -------------------------------------------------
            # Metrics
            # -------------------------------------------------
            st.success("Forecast generated successfully")

            col1, col2, col3 = st.columns(3)
            col1.metric("Base Demand", result["base_demand"])
            col2.metric("Promo Uplift", result["promo_uplift"])
            col3.metric("Total Demand", result["total_demand"])

            if "recommended_safety_stock" in result:
                st.metric(
                    "📦 Recommended Safety Stock",
                    result["recommended_safety_stock"]
                )

            # -------------------------------------------------
            # Explanation
            # -------------------------------------------------
            if "explanation" in result:
                st.subheader("📖 Explanation")
                st.write(result["explanation"])

            # -------------------------------------------------
            # Debug
            # -------------------------------------------------
            with st.expander("🔍 Full API Response"):
                st.json(result)

        except requests.exceptions.RequestException as e:
            st.error("Connection error")
            st.write(str(e))
