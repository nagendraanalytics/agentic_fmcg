# from app.ml.predict import predict_promo_uplift

# def promo_uplift_agent(state):
    
#     state["promo_uplift"] = predict_promo_uplift(
#         month_num=state["month_num"],
#         cluster=state["cluster"]
#     )
#     state["promo_uplift"] = min(state["promo_uplift"], state["base_demand"] * 2)

#     return state

from app.ml.predict import predict_promo_uplift


def promo_uplift_agent(state: dict) -> dict:
    """
    Compute promo uplift and update LangGraph state.
    Assumes base_demand is already computed.
    """

    promo_uplift = predict_promo_uplift(
        store_id=int(state["store_id"]),
        product_id=int(state["product_id"]),
        category=state["category"],
        store_type=state["store_type"],
        month_num=int(state["month_num"]),
        cluster=int(state["cluster"])
    )

    # Safety cap: promo uplift should not explode
    promo_uplift = min(promo_uplift, int(state["base_demand"] * 2))

    state["promo_uplift"] = int(promo_uplift)

    return state
