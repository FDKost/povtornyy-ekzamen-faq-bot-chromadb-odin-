from chromadb import PersistentClient
from langchain.embeddings import Embeddings
from langchain.vectorstores import Chroma
from config import CHROMA_DB_PATH, MAX_RETRIEVAL_DOCS
from typing import List

def get_chroma_collection(embeddings: Embeddings, collection_name: str = "faq") -> Chroma:
    """
    Returns a Chroma collection. Creates it if it does not exist.
    """
    client = PersistentClient(CHROMA_DB_PATH)
    if collection_name in client.list_collections():
        collection = client.get_collection(name=collection_name)
    else:
        collection = client.create_collection(name=collection_name)
    return Chroma(
        collection=collection,
        embedding_function=embeddings,
    )

def ingest_documents(embeddings, documents: List[str], collection_name: str = "faq"):
    """
    Ingests a list of documents into the Chroma collection.
    """
    chroma = get_chroma_collection(embeddings, collection_name)
    chroma.add_texts(documents)
