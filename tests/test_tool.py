import pytest
from src.tool import RefreshFAQTool
from src.ingestion import ingest_faq_csv

@pytest.fixture
def mock_ingest(monkeypatch):
    def fake_ingest(file_path):
        return 42
    monkeypatch.setattr("src.ingestion.ingest_faq_csv", fake_ingest)

def test_refresh_tool_success(mock_ingest):
    tool = RefreshFAQTool()
    result = tool.run("/path/to/file.csv")
    assert "Successfully ingested 42" in result

def test_refresh_tool_failure(monkeypatch):
    def fake_ingest(file_path):
        raise RuntimeError("oops")
    monkeypatch.setattr("src.ingestion.ingest_faq_csv", fake_ingest)
    tool = RefreshFAQTool()
    result = tool.run("/path/to/file.csv")
    assert "Failed to refresh FAQ" in result
