# FAQ Bot – ChromaDB + MCP Tool

This project implements a FAQ chatbot that uses **ChromaDB** for vector storage and **MCP-compatible** LLMs and embeddings (e.g., Anthropic Claude, Cohere).  
It also provides an **MCP-style HTTP tool** that the LLM can call to fetch external data.

## Features

- **LLM**: Uses MCP-compatible chat models via `langchain-mcp`.
- **Embeddings**: Uses MCP-compatible embeddings via `langchain-mcp`.
- **Vector Store**: Persistent ChromaDB collection for FAQ documents.
- **HTTP Tool**: A reusable tool that performs HTTP GET requests and returns JSON.
- **FastAPI**: Exposes a simple `/ask` endpoint for querying the bot.

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourorg/faq-bot.git
   cd faq-bot
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy `.env.example` to `.env` and fill in your MCP API key and model names.

   ```bash
   cp .env.example .env
   ```

5. **Add FAQ documents**

   Place your FAQ text files in a folder (e.g., `data/faq`).  
   Run the following script to ingest them into ChromaDB:

   ```bash
   python ingest.py
   ```

6. **Run the server**

   ```bash
   uvicorn main:app --reload
   ```

   The bot will be available at `http://127.0.0.1:8000`.

## API

### POST /ask

```json
{
  "question": "What is the return policy?"
}
```

**Response**

```json
{
  "answer": "Our return policy allows returns within 30 days..."
}
```

## Development

- **Testing**: Run `pytest` to execute unit tests.
- **Linting**: Use `flake8` or `black` for code formatting.
- **CI/CD**: The repository includes a GitHub Actions workflow that installs dependencies, runs tests, and builds a Docker image.

## License

MIT License
