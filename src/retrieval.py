from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from chromadb import Client

from .config import settings
from .logger import logger

CHROMA_COLLECTION = "faq"

def get_chroma_client() -> Client:
    return Client(
        host=settings.chroma_host,
        port=settings.chroma_port,
        persist_directory=str(settings.chroma_persist_directory),
    )

def build_retrieval_chain():
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION)
    retriever = collection.as_retriever()
    llm = ChatOpenAI(
        openai_api_key=settings.openai_api_key,
        temperature=0.0,
        model_name="gpt-4o-mini",
    )
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    logger.info("Retrieval chain built.")
    return chain, collection
