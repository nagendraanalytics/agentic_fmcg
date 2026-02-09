from langgraph.graph import StateGraph
from app.langgraph.state import FMCGState

from app.agents.planner_agent import planner_agent
from app.agents.rule_agent import rule_agent
from app.agents.forecast_agent import forecast_agent
from app.agents.promo_uplift_agent import promo_uplift_agent
from app.agents.inventory_agent import inventory_agent
from app.agents.monitoring_agent import monitoring_agent
from app.agents.rag_agent import rag_agent
from app.agents.gpt_explain_agent import gpt_explain_agent
from app.agents.response_sanitizer_agent import response_sanitizer_agent


graph = StateGraph(FMCGState)

# Nodes
graph.add_node("planner", planner_agent)
graph.add_node("rules", rule_agent)
graph.add_node("forecast", forecast_agent)
graph.add_node("promo_uplift", promo_uplift_agent)
graph.add_node("inventory", inventory_agent)
graph.add_node("monitoring", monitoring_agent)
graph.add_node("rag", rag_agent)
graph.add_node("explain", gpt_explain_agent)
graph.add_node("sanitize", response_sanitizer_agent)


# Entry
graph.set_entry_point("planner")

# Base flow
graph.add_edge("planner", "rules")
graph.add_edge("rules", "forecast")

# Conditional routing (CRITICAL)
def promo_router(state: FMCGState):
    return "promo" if state["promo_flag"] else "no_promo"

graph.add_conditional_edges(
    "forecast",
    promo_router,
    {
        "promo": "promo_uplift",
        "no_promo": "inventory"
    }
)

graph.add_edge("promo_uplift", "inventory")
graph.add_edge("inventory", "monitoring")
graph.add_edge("monitoring", "rag")
graph.add_edge("rag", "explain")
graph.add_edge("explain", "sanitize")

graph_app = graph.compile()
