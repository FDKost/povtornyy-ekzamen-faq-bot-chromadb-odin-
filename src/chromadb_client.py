from chromadb import Client
from chromadb.config import Settings
from config import Config

def get_chroma_client() -> Client:
    client = Client(Settings(persist_directory=Config.CHROMA_PERSIST_DIR))
    return client

def get_or_create_collection(client: Client, name: str = "faq"):
    collection = client.get_or_create_collection(name=name)
    return collection
