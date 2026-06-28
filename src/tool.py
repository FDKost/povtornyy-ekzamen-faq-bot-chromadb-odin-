from typing import Dict

from langchain.tools import BaseTool
from langchain.schema import AgentAction, AgentFinish

from .ingestion import ingest_faq_csv
from .logger import logger

class RefreshFAQTool(BaseTool):
    name = "RefreshFAQ"
    description = (
        "Refreshes the FAQ database from a CSV file. "
        "Provide the full path to the CSV file."
    )

    def _run(self, file_path: str) -> str:
        try:
            count = ingest_faq_csv(file_path)
            return f"Successfully ingested {count} FAQ entries from {file_path}."
        except Exception as e:
            logger.exception("Error during FAQ refresh")
            return f"Failed to refresh FAQ: {str(e)}"

    def _arun(self, file_path: str) -> str:
        return self._run(file_path)

class RetrieveFAQTool(BaseTool):
    name = "RetrieveFAQ"
    description = (
        "Retrieves relevant FAQ entries for a given query. "
        "Use this tool to fetch context before answering."
    )

    def __init__(self, collection):
        super().__init__()
        self.collection = collection

    def _run(self, query: str) -> str:
        try:
            results = self.collection.as_retriever().get_relevant_documents(query)
            context = "\n\n".join([doc.page_content for doc in results])
            return context if context else "No relevant FAQ entries found."
        except Exception as e:
            logger.exception("Error during FAQ retrieval")
            return f"Failed to retrieve FAQ: {str(e)}"

    def _arun(self, query: str) -> str:
        return self._run(query)
