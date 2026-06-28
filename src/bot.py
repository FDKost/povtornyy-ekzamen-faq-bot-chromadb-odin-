from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from chromadb_client import get_chroma_client, get_or_create_collection
from config import Config
from mcp_tool import UppercaseTool

class FAQBot:
    def __init__(self):
        self.llm = OpenAI(model=Config.LLM_MODEL, temperature=0)
        self.embeddings = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)
        self.client = get_chroma_client()
        self.collection = get_or_create_collection(self.client)
        self.vectorstore = Chroma(
            client=self.client,
            collection_name="faq",
            embedding_function=self.embeddings,
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": Config.TOP_K})
        self.tool = UppercaseTool()
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
        )

    def answer(self, question: str) -> str:
        preprocessed = self.tool.run(question)
        result = self.chain.run(preprocessed)
        return result
