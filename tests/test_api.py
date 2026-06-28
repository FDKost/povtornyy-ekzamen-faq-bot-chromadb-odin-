import json
import os
import tempfile
import csv
import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_query_endpoint(client, monkeypatch):
    # Mock the agent_executor.invoke to return a dummy answer
    def fake_invoke(input_dict):
        return {"output": "This is a test answer."}
    monkeypatch.setattr("src.main.agent_executor", fake_invoke)
    response = client.post("/query", json={"question": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"answer": "This is a test answer."}

def test_refresh_endpoint(client, monkeypatch):
    def fake_run(file_path):
        return f"Mocked refresh from {file_path}"
    monkeypatch.setattr("src.main.refresh_tool", fake_run)
    response = client.post("/refresh", json={"file_path": "/tmp/file.csv"})
    assert response.status_code == 200
    assert response.json() == {"message": "Mocked refresh from /tmp/file.csv"}
