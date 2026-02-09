from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

VECTOR_PATH = "app/rag/faiss_index"

def retrieve_context(query: str, k: int = 3):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large"
    )

    # vectorstore = FAISS.load_local(VECTOR_PATH, embeddings)
    vectorstore = FAISS.load_local(
    VECTOR_PATH,
    embeddings,
    allow_dangerous_deserialization=True
    )

    docs = vectorstore.similarity_search(query, k=k)

    return "\n".join([doc.page_content for doc in docs])
