# FAQ Bot

A simple FAQ bot built with FastAPI, LangChain, and ChromaDB.  
It can answer user questions by retrieving relevant FAQ entries and can refresh its knowledge base from a CSV file using a single MCP‑tool.

## Features

- **Vector search** with ChromaDB and OpenAI embeddings.
- **LLM powered answers** using LangChain and OpenAI.
- **Single MCP‑tool** to refresh the FAQ database from a CSV file.
- **FastAPI** REST API with health checks.
- **Docker** and Docker‑Compose for easy deployment.
- **Unit & integration tests** with pytest.

## Prerequisites

- Docker & Docker‑Compose
- Python 3.11+ (for local development)
- An OpenAI API key

## Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/faq-bot.git
cd faq-bot

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
poetry install

# Copy the example env file
cp .env.example .env
# Edit .env with your OpenAI key
```

## Running locally

```bash
# Start the API
uvicorn src.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Docker

```bash
docker compose up --build
```

This will start:

- `chroma` – ChromaDB container.
- `api` – FastAPI container.

The API will be available at `http://localhost:8000`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/query` | Submit a question. Body: `{ "question": "..." }`. |
| `POST` | `/refresh` | Refresh FAQ database from a CSV file. Body: `{ "file_path": "/path/to/file.csv" }`. |
| `GET` | `/health` | Health check. |

## Testing

```bash
pytest
```

## FAQ

**Q: How does the bot decide when to refresh the FAQ?**  
A: The bot can be refreshed manually via the `/refresh` endpoint or by invoking the `RefreshFAQ` tool from within a conversation.

**Q: Where is the vector store persisted?**  
A: By default it is persisted in the `/data` directory inside the Chroma container. Adjust `CHROMA_PERSIST_DIRECTORY` in `.env` to change.

**Q: Can I use a different embedding model?**  
A: Yes, modify `src.ingestion.py` to use a different embedding provider.

## License

MIT License
