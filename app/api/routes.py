# import pandas as pd
# from fastapi import APIRouter, HTTPException
# from app.langgraph.graph import graph_app
# from app.api.schemas import InventoryRequest
# from app.utils.json_safe import make_json_safe

# stores = pd.read_csv("app/data/fmcg_stores.csv")

# router = APIRouter()

# @router.post("/agentic/inventory")
# def run_agentic_pipeline(payload: InventoryRequest):
#     store_row = stores[stores["store_id"] == payload.store_id]

#     if store_row.empty:
#         raise HTTPException(status_code=404, detail="Store not found")

#     store = store_row.iloc[0]

#     state = payload.dict()
#     state["cluster"] = store["cluster"]
#     state["month_num"] = int(payload.month.split("-")[1])

#     return graph_app.invoke(state)

import pandas as pd
from fastapi import APIRouter, HTTPException
from app.langgraph.graph import graph_app
from app.api.schemas import InventoryRequest
from app.utils.json_safe import make_json_safe
from app.api.schemas import PromptRequest
from app.llm.prompt_parser import parse_prompt
from app.llm.explanation_agent import generate_explanation
from pydantic import BaseModel, ValidationError

router = APIRouter()

class ParsedPrompt(BaseModel):
    store_id: int
    product_id: int
    brand: str
    category: str
    store_type: str
    month: str
    cluster: int
    promo_flag: bool

def validate_prompt(parsed: dict) -> dict:
    if "error" in parsed:
        raise ValueError(parsed["error"])

    return ParsedPrompt(**parsed).dict()

@router.post("/agentic/prompt")
def run_agentic_from_prompt(payload: PromptRequest):
    try:
        parsed = parse_prompt(payload.prompt)
        print("PARSED PROMPT:", parsed)

        if "error" in parsed:
            return {
                "error": "Prompt parsing failed",
                "details": parsed["error"]
            }
        
        state = validate_prompt(parsed)
        print("VALIDATED STATE:", state)

        result = graph_app.invoke(state)
        print("GRAPH RESULT:", result)

        explanation = generate_explanation(
            prompt=payload.prompt,
            result=result
        )

        result["explanation"] = explanation
        return make_json_safe(result)
        
        

    except Exception as e:
        import traceback
        traceback.print_exc()   # 👈 THIS IS KEY
        return {
            "error": "Failed to process prompt",
            "details": str(e)
        }




@router.post("/agentic/inventory")
def run_agentic_pipeline(payload: InventoryRequest):
    """
    Entry point for Agentic FMCG pipeline.
    Do NOT enrich master data here.
    Planner agent handles enrichment.
    """
    

    # Minimal, clean state
    state = payload.dict()
    # print("STATE:",state)
    # result = graph_app.invoke({
    #   "store_id": 18,
    #   "product_id": 105,
    #   "brand": "Pepsi",
    #   "category": "Beverages",
    #   "store_type": "Supermarket",
    #   "month": "2022-10",
    #   "cluster": 4,
    #   "promo_flag": True
    # })
    
    
    try:
        result = graph_app.invoke(state)
        return make_json_safe(result)

    except ValueError as e:
        # Agent-level validation errors
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Unexpected failures
        raise HTTPException(status_code=500, detail=str(e))
