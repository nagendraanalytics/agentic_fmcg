from app.langgraph.state import FMCGState

def monitoring_agent(state: FMCGState):
    risks = []

    if state["recommended_safety_stock"] < 100:
        risks.append("Low safety stock")

    if state["promo_flag"] and state["promo_uplift"] > 0:
        risks.append("Promo-driven risk")

    state["risk_flags"] = risks
    return state
