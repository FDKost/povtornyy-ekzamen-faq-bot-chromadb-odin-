import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chromadb")
    FAQ_DATA_PATH = os.getenv("FAQ_DATA_PATH", "./data/faq.csv")
    TOP_K = int(os.getenv("TOP_K", "5"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "64"))
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
