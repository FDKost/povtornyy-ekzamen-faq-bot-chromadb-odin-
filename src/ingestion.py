import csv
import os
from pathlib import Path
from typing import List, Dict

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb import Client
from chromadb.utils import embedding_functions

from .config import settings
from .logger import logger

CHROMA_COLLECTION = "faq"

def get_chroma_client() -> Client:
    return Client(
        host=settings.chroma_host,
        port=settings.chroma_port,
        persist_directory=str(settings.chroma_persist_directory),
    )

def ingest_faq_csv(file_path: str) -> int:
    """
    Ingests a CSV file containing FAQ data into ChromaDB.
    CSV columns: question, answer, tags (comma separated), source
    Returns the number of documents ingested.
    """
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION)

    documents = []
    metadatas = []

    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            content = f"{row.get('question', '')}\n{row.get('answer', '')}"
            documents.append(content)
            metadatas.append(
                {
                    "source": row.get("source", ""),
                    "tags": row.get("tags", "").split(","),
                }
            )

    if not documents:
        logger.warning(f"No documents found in {file_path}")
        return 0

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(
        [
            {"page_content": doc, "metadata": meta}
            for doc, meta in zip(documents, metadatas)
        ]
    )

    # Prepare embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

    # Upsert into Chroma
    ids = [f"doc_{i}" for i in range(len(split_docs))]
    texts = [doc["page_content"] for doc in split_docs]
    metadatas = [doc["metadata"] for doc in split_docs]

    collection.upsert(
        ids=ids,
        embeddings=embeddings.embed_documents(texts),
        documents=texts,
        metadatas=metadatas,
    )

    logger.info(f"Ingested {len(split_docs)} chunks from {file_path}")
    return len(split_docs)

def cleanup_stale_documents(days: int = 30) -> int:
    """
    Deletes documents older than the specified number of days.
    Assumes metadata contains a 'timestamp' field in ISO format.
    """
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION)
    # This is a placeholder; actual implementation would require metadata tracking.
    # For simplicity, we skip deletion logic.
    logger.info("Cleanup routine executed (no-op).")
    return 0
