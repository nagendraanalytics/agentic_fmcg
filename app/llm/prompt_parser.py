from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import json

llm = ChatOpenAI(temperature=0)

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["prompt"],
    template="""
You are an FMCG demand planning system.

From the user message below, extract the following fields.
The user may describe them in natural language.

Required fields (MUST be present in the prompt):
- store_id (integer)
- product_id (integer OR infer from brand if explicitly mentioned)
- month (YYYY-MM)
- promo_flag (true or false)
- brand (string)
- category (string)
- store_type (string)
- cluster (integer)

Rules:
- Do NOT guess values that are not mentioned
- If a required field is missing, return:
  {{ "error": "missing_<field_name>" }}
- Return ONLY valid JSON
- No markdown, no explanations, no extra text

User message:
{prompt}
"""
)
def parse_prompt(prompt: str) -> dict:
    response = llm.predict(PROMPT_TEMPLATE.format(prompt=prompt)).strip()

    if not response:
        return {"error": "empty_llm_response"}

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"error": f"invalid_json_from_llm: {response}"}


# def parse_prompt(prompt: str) -> dict:
#     response = llm.predict(PROMPT_TEMPLATE.format(prompt=prompt)).strip()

#     # if not response:
#     #     return {"error": "empty_llm_response"}

#     # try:
#     #     parsed = json.loads(response)
#     # except json.JSONDecodeError:
#     #     return {"error": f"invalid_json_from_llm: {response}"}

#     # return parsed
#     return response

# print(parse_prompt( """ Please forecast the demand for Pepsi (product ID 105) at Store 15 for the month of November 2022.
#   This is a Modern Trade (MT) store in cluster 4.
#   The product belongs to the Beverages category.
#   A promotion is active during this period.
#   Please calculate base demand, promotional uplift, total demand, recommended safety stock,
#   and explain the impact of the promotion on inventory planning.
#   """))