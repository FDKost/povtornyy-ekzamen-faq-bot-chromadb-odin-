import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Settings:
    openai_api_key: str
    chroma_host: str
    chroma_port: int
    chroma_persist_directory: Path

    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            chroma_host=os.getenv("CHROMA_HOST", "localhost"),
            chroma_port=int(os.getenv("CHROMA_PORT", "8000")),
            chroma_persist_directory=Path(os.getenv("CHROMA_PERSIST_DIRECTORY", "./chromadb")),
        )

settings = Settings.from_env()
