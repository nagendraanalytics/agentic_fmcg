from app.rag.retriever import retrieve_context

def rag_agent(state):
    query = f"""
    Store {state['store_id']}, Product {state['product_id']},
    Promo={state.get('promo_flag')}
    Inventory issue explanation
    """
    context = retrieve_context(query)
    state["retrieved_knowledge"] = context
    if not context:
        state["retrieved_knowledge"] = "No similar historical cases found."
    
    return state
