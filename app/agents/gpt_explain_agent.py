from app.langgraph.state import FMCGState

def gpt_explain_agent(state: FMCGState):
    state["explanation"] = (
        f"Base demand {state.get('base_demand')} units, "
        f"promo uplift {state.get('promo_uplift', 0)} units. "
        f"Recommended safety stock {state.get('recommended_safety_stock')} "
        f"is based on historical promo behavior."
    )
    return state
