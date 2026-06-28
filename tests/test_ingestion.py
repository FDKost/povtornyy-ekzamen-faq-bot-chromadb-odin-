import os
import tempfile
import csv
from pathlib import Path

import pytest
from chromadb import Client

from src.ingestion import ingest_faq_csv, get_chroma_client, CHROMA_COLLECTION
from src.config import settings

@pytest.fixture
def temp_csv(tmp_path):
    file_path = tmp_path / "faq.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["question", "answer", "tags", "source"])
        writer.writerow(["What is AI?", "Artificial Intelligence.", "AI,ML", "test"])
        writer.writerow(["What is ML?", "Machine Learning.", "ML", "test"])
    return file_path

def test_ingest_faq_csv(temp_csv):
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION)
    # Ensure collection is empty
    collection.delete(where={})
    count = ingest_faq_csv(str(temp_csv))
    assert count > 0
    docs = collection.get()
    assert len(docs["ids"]) == count
    assert len(docs["documents"]) == count
