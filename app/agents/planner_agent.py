import pandas as pd
from app.langgraph.state import FMCGState

def planner_agent(state: FMCGState):
    print("PLANNER AGENT: START", state)
    state["month_num"] = pd.to_datetime(state["month"]).month
    state["cluster"] = state.get("cluster", 0)
    state["route"] = "promo" if state.get("promo_flag") else "no_promo"
    print("PLANNER AGENT: END",state)
    return state
