from pydantic import BaseModel
from typing import Optional, List

class InventoryRequest(BaseModel):
    store_id: int
    product_id: int
    brand: str
    category: str
    store_type: str
    month: str
    cluster: int
    promo_flag: bool    

class InventoryResponse(BaseModel):
    base_demand: int
    promo_uplift: Optional[int]
    total_demand: int
    recommended_safety_stock: int
    risk_flags: Optional[List[str]]
    explanation: str


class PromptRequest(BaseModel):
    prompt: str



class ForecastRequest(BaseModel):
    promo_flag: int
    month: int

class ForecastResponse(BaseModel):
    forecast_demand: int




