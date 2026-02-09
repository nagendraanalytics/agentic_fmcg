from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(temperature=0.3)

EXPLANATION_PROMPT = PromptTemplate(
    input_variables=["prompt", "result"],
    template="""
User asked:
{prompt}

System computed:
- Base demand: {base_demand}
- Promo uplift: {promo_uplift}
- Total demand: {total_demand}
- Safety stock: {recommended_safety_stock}
- Service level: {service_level}

Rules applied:
{rules_applied}

Explain the result in simple business language.
Focus on:
- Why demand changed
- Promo impact
- Inventory implications
"""
)

def generate_explanation(prompt: str, result: dict) -> str:
    return llm.predict(
        EXPLANATION_PROMPT.format(
            prompt=prompt,
            base_demand=result["base_demand"],
            promo_uplift=result["promo_uplift"],
            total_demand=result["total_demand"],
            recommended_safety_stock=result["recommended_safety_stock"],
            service_level=result.get("service_level"),
            rules_applied=result.get("rules_applied"),
        )
    )
