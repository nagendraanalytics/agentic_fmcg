# from app.langgraph.state import FMCGState
# from app.ml.predict import predict_base_demand

# def forecast_agent(state: FMCGState):
#     required = ["store_id", "product_id", "brand", "category", "store_type", "cluster"]
#     missing = [k for k in required if k not in state]
#     if missing:
#         raise ValueError(f"Missing required fields in state: {missing}")
#     if "month_num" not in state:
#         raise RuntimeError("month_num missing. PlannerAgent must run first.")
    
    
#     state["base_demand"] = predict_base_demand(
#         month_num=state["month_num"],
#         cluster=state["cluster"]
#     )

#     # Keep compatibility
#     state["forecast"] = state["base_demand"]
#     return state

from app.langgraph.state import FMCGState
from app.ml.predict import predict_base_demand
import pandas as pd

def forecast_agent(state: FMCGState):
    print("FORECAST AGENT: START", state)
    required = [
        "store_id", "product_id", "brand",
        "category", "store_type", "cluster", "month"
    ]
    missing = [k for k in required if k not in state]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    month_num = pd.to_datetime(state["month"]).month
    state["month_num"] = month_num

    # state["base_demand"] = predict_base_demand(
    #     store_id=state["store_id"],
    #     product_id=state["product_id"],
    #     brand=state["brand"],
    #     category=state["category"],
    #     store_type=state["store_type"],
    #     month_num=month_num,
    #     cluster=state["cluster"],
    #     lag_1=state.get("lag_1", 0.0),
    #     lag_2=state.get("lag_2", 0.0),
    #     rolling_mean_3=state.get("rolling_mean_3", 0.0),
    #     rolling_std_3=state.get("rolling_std_3", 0.0),
    # )

    # state["forecast"] = state["base_demand"]
    print("FORECAST AGENT: END", state)
    return state
