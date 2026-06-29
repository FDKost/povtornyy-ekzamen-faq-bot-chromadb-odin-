"""
Script to ingest FAQ documents into ChromaDB.
Place your FAQ text files in the 'data/faq' directory.
"""
import os
from pathlib import Path
from utils.chroma_utils import ingest_documents
from config import MCP_API_KEY, MCP_EMBEDDINGS_MODEL

def load_documents(folder: str) -> list:
    docs = []
    for file_path in Path(folder).glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            docs.append(f.read())
    return docs

if __name__ == "__main__":
    folder = "data/faq"
    if not os.path.isdir(folder):
        print(f"Folder '{folder}' does not exist. Create it and add .txt files.")
        exit(1)
    documents = load_documents(folder)
    if not documents:
        print("No documents found.")
        exit(1)
    print(f"Found {len(documents)} documents. Ingesting into ChromaDB...")
    ingest_documents(
        embeddings=None,  # embeddings will be initialized in main.py
        documents=documents,
    )
    print("Ingestion complete.")
