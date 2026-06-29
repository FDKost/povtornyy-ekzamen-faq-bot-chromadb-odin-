import os
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ask_endpoint():
    response = client.post("/ask", json={"question": "What is your name?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0
