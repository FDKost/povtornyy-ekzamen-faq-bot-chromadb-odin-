import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from config import Config
from chromadb_client import get_chroma_client, get_or_create_collection

def ingest_faq_data():
    df = pd.read_csv(Config.FAQ_DATA_PATH)
    if "question" not in df.columns or "answer" not in df.columns:
        raise ValueError("CSV must contain 'question' and 'answer' columns.")
    questions = df["question"].tolist()
    answers = df["answer"].tolist()
    documents = [f"Q: {q}\nA: {a}" for q, a in zip(questions, answers)]
    metadatas = [{"question": q, "answer": a} for q, a in zip(questions, answers)]
    embeddings = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    collection.add(
        documents=documents,
        embeddings=embeddings.embed_documents(documents),
        metadatas=metadatas,
    )
