from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
import os

VECTOR_PATH = "app/rag/faiss_index"

def build_vector_store():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large"
    )

    docs = []
    docs_path = "app/rag/documents"

    for file in os.listdir(docs_path):
        loader = TextLoader(os.path.join(docs_path, file))
        docs.extend(loader.load())

    vectorstore = FAISS.from_documents(docs, embeddings)
    
    vectorstore.save_local(VECTOR_PATH)

    return vectorstore
