import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_mcp import MCPChatModel, MCPEmbeddings
from langchain.vectorstores import Chroma
from langchain.agents import initialize_agent, AgentType
from langchain.tools.retriever import VectorStoreRetrieverTool
from tools.http_tool import http_get_tool
from utils.chroma_utils import get_chroma_collection
from config import (
    MCP_API_KEY,
    MCP_CHAT_MODEL,
    MCP_EMBEDDINGS_MODEL,
    CHROMA_DB_PATH,
    MAX_RETRIEVAL_DOCS,
)

app = FastAPI(title="FAQ Bot")

class QuestionRequest(BaseModel):
    question: str

# Initialize embeddings
embeddings = MCPEmbeddings(
    model_name=MCP_EMBEDDINGS_MODEL,
    api_key=MCP_API_KEY,
)

# Initialize Chroma collection
chroma = get_chroma_collection(embeddings)

# Create a retriever tool for the vector store
retriever_tool = VectorStoreRetrieverTool(
    vectorstore=chroma,
    name="vector_retrieval",
    description="Useful for retrieving FAQ answers from the vector store.",
)

# Initialize LLM
llm = MCPChatModel(
    model_name=MCP_CHAT_MODEL,
    api_key=MCP_API_KEY,
    temperature=0.2,
)

# Initialize agent with tools
agent = initialize_agent(
    tools=[retriever_tool, http_get_tool],
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
)

@app.post("/ask")
async def ask(request: QuestionRequest):
    """
    Endpoint to ask a question to the FAQ bot.
    """
    try:
        answer = agent.run(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
