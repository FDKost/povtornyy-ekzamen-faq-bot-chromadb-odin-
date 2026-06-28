import os
import pytest
from ingestion import ingest_faq_data
from chromadb_client import get_chroma_client, get_or_create_collection
from config import Config

@pytest.fixture
def clear_collection():
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    collection.delete(where={})
    return collection

def test_ingestion_creates_documents(clear_collection):
    ingest_faq_data()
    docs = clear_collection.get()
    assert len(docs["documents"]) > 0
