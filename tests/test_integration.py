import os
import tempfile
import csv
import pytest
from fastapi.testclient import TestClient
from src.main import app
from chromadb import Client
from src.config import settings

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
def chroma_client():
    # Use a temporary directory for persistence
    tmp_dir = tempfile.mkdtemp()
    settings.chroma_persist_directory = tmp_dir
    client = Client(
        host=settings.chroma_host,
        port=settings.chroma_port,
        persist_directory=str(tmp_dir),
    )
    yield client
    # Cleanup
    client.close()

def test_end_to_end(client, chroma_client):
    # Create a small FAQ CSV
    tmp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(tmp_dir, "faq.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["question", "answer", "tags", "source"])
        writer.writerow(["What is Python?", "Python is a programming language.", "Python", "test"])
    # Refresh via API
    response = client.post("/refresh", json={"file_path": csv_path})
    assert response.status_code == 200
    # Query
    response = client.post("/query", json={"question": "Python"})
    assert response.status_code == 200
    assert "Python is a programming language." in response.json()["answer"]
