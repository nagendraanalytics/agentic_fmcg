from pydantic import BaseModel, ValidationError

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
    try:
        return ParsedPrompt(**parsed).dict()
    except ValidationError as e:
        raise ValueError(f"Invalid or missing fields: {e}")
