import pytest
from chromadb_client import get_chroma_client, get_or_create_collection

def test_chroma_client_and_collection():
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    assert collection is not None
