from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from pathlib import Path

# Where to save the index
VECTOR_PATH = Path("app/rag/faiss_index")

VECTOR_PATH.mkdir(parents=True, exist_ok=True)

# Example FMCG knowledge (replace with your real docs)
from langchain.docstore.document import Document

docs = [

    # Promotion & Demand Behavior
    Document(
        page_content=(
            "Promotion in Oct-2022 led to increased demand volatility and elevated stockout risk. "
            "Products under promotion experienced higher variability in daily sales."
        )
    ),

    Document(
        page_content=(
            "High promotion intensity is strongly correlated with temporary spikes in demand, "
            "often exceeding baseline forecasts."
        )
    ),

    # Safety Stock & Replenishment
    Document(
        page_content=(
            "Increasing safety stock by 1.5x during promotional periods reduced lost sales "
            "by buffering against sudden demand surges."
        )
    ),

    Document(
        page_content=(
            "Higher service levels during promotion windows improve on-shelf availability "
            "for high-frequency products."
        )
    ),

    # Stockout Risk
    Document(
        page_content=(
            "High stockout rates are associated with rapid demand acceleration and insufficient "
            "inventory coverage during peak periods."
        )
    ),

    Document(
        page_content=(
            "Products with high sales velocity require faster replenishment cycles "
            "to prevent availability gaps."
        )
    ),

    # Forecast & Planning
    Document(
        page_content=(
            "Forecast error typically increases during promotions due to nonlinear demand uplift "
            "and customer substitution effects."
        )
    ),

    Document(
        page_content=(
            "Smoothing forecast adjustments can reduce planning volatility when historical "
            "promo performance shows consistent uplift patterns."
        )
    ),

    # Inventory Coverage
    Document(
        page_content=(
            "Low days of inventory coverage is a leading indicator of near-term stockout risk, "
            "especially during demand peaks."
        )
    ),

    Document(
        page_content=(
            "Expedited replenishment is recommended when inventory coverage drops below "
            "critical thresholds."
        )
    )
]


embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Build FAISS index
vectorstore = FAISS.from_documents(docs, embeddings)

# Save locally
vectorstore.save_local(VECTOR_PATH)

print("✅ FAISS index created at:", VECTOR_PATH)

