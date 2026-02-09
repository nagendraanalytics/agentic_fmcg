import yaml
from app.langgraph.state import FMCGState

with open("app/rules/inventory_rules.yaml") as f:
    RULES = yaml.safe_load(f)

def rule_agent(state: FMCGState):
    print("RULES AGENT: START", state)
    state["rules_applied"] = RULES
    state["service_level"] = RULES.get("service_level", 0.95)
    print("RULES AGENT: END", state)
    return state
