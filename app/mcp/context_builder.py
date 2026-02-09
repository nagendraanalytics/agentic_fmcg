def build_mcp_context(state):
    return {
        "business_context": {
            "store_id": state["store_id"],
            "product_id": state["product_id"],
            "promo_flag": state.get("promo_flag")
        },
        "rules_context": state.get("rules_applied"),
        "model_context": {
            "forecast": state.get("forecast"),
            "safety_stock": state.get("recommended_safety_stock")
        },
        "knowledge_context": state.get("retrieved_knowledge")
    }
