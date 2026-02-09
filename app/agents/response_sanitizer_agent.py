import numpy as np
from app.langgraph.state import FMCGState

def response_sanitizer_agent(state: FMCGState):
    clean_state = {}

    for k, v in state.items():
        if isinstance(v, np.integer):
            clean_state[k] = int(v)
        elif isinstance(v, np.floating):
            clean_state[k] = float(v)
        elif isinstance(v, list):
            clean_state[k] = [
                int(x) if isinstance(x, np.integer)
                else float(x) if isinstance(x, np.floating)
                else x
                for x in v
            ]
        else:
            clean_state[k] = v

    return clean_state
