import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

from .config import settings
from .logger import logger
from .retrieval import build_retrieval_chain
from .tool import RefreshFAQTool, RetrieveFAQTool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.chat_models import ChatOpenAI

app = FastAPI(
    title="FAQ Bot",
    description="Answer FAQs using ChromaDB and OpenAI",
    version="0.1.0",
)

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build components
retrieval_chain, collection = build_retrieval_chain()
refresh_tool = RefreshFAQTool()
retrieve_tool = RetrieveFAQTool(collection=collection)

llm = ChatOpenAI(
    openai_api_key=settings.openai_api_key,
    temperature=0.0,
    model_name="gpt-4o-mini",
)

tools = [refresh_tool, retrieve_tool]
agent = create_openai_tools_agent(llm=llm, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

class QueryRequest(BaseModel):
    question: str

class RefreshRequest(BaseModel):
    file_path: str

@app.post("/query")
async def query_endpoint(req: QueryRequest):
    try:
        result = agent_executor.invoke({"input": req.question})
        answer = result.get("output", "")
        return {"answer": answer}
    except Exception as e:
        logger.exception("Error processing query")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refresh")
async def refresh_endpoint(req: RefreshRequest):
    try:
        result = refresh_tool.run(req.file_path)
        return {"message": result}
    except Exception as e:
        logger.exception("Error refreshing FAQ")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
