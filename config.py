import os
from dotenv import load_dotenv

load_dotenv()

# MCP configuration
MCP_API_KEY = os.getenv("MCP_API_KEY")
MCP_CHAT_MODEL = os.getenv("MCP_CHAT_MODEL", "anthropic/claude-3-5-sonnet-20240620")
MCP_EMBEDDINGS_MODEL = os.getenv("MCP_EMBEDDINGS_MODEL", "cohere/embed-english-v3")

# ChromaDB configuration
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chromadb")
MAX_RETRIEVAL_DOCS = int(os.getenv("MAX_RETRIEVAL_DOCS", "5"))
