from openai import OpenAI
from app.mcp.context_builder import build_mcp_context

client = OpenAI()

def llm_agent(state):
    mcp = build_mcp_context(state)

    prompt = f"""
You are an FMCG supply chain expert.

Use ONLY the context below.
Do NOT invent rules.

CONTEXT:
{mcp}

Explain:
1. Why the stockout occurred
2. What evidence supports this
3. What action is recommended
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    state["explanation"] = response.choices[0].message.content

    return state
