# FAQ Bot

This project implements a FAQ chatbot that uses **ChromaDB** for vector storage and **LangChain** for conversational AI. It also demonstrates how to integrate a custom tool (MCP-tool) into the conversation flow.

## Features

- Store FAQ data in ChromaDB with embeddings.
- Retrieve relevant answers using similarity search.
- Generate responses with OpenAI LLM.
- Custom MCP-tool that transforms user queries.
- Command-line interface for quick interaction.
- Unit tests covering core functionality.

## Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)
- An OpenAI API key

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/faq-bot.git
cd faq-bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (or export the variables manually):

```dotenv
OPENAI_API_KEY=your_openai_api_key
CHROMA_PERSIST_DIR=./chromadb
FAQ_DATA_PATH=./data/faq.csv
TOP_K=5
CHUNK_SIZE=512
CHUNK_OVERLAP=64
LLM_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-ada-002
```

### 5. Prepare FAQ data

Place a CSV file at `./data/faq.csv` with two columns: `question` and `answer`. Example:

```csv
question,answer
What is your name?,I am a chatbot.
How can I help you?,Ask me anything about our services.
```

### 6. Ingest data into ChromaDB

```bash
python -c "from ingestion import ingest_faq_data; ingest_faq_data()"
```

## Running the Bot

```bash
python src/main.py
```

Type your question and press Enter. Type `exit` to quit.

## Testing

Run unit tests with:

```bash
pytest
```

## Docker

Build the Docker image:

```bash
docker build -t faq-bot .
```

Run the container (replace environment variables accordingly):

```bash
docker run -e OPENAI_API_KEY=... \
           -e CHROMA_PERSIST_DIR=/data/chromadb \
           -v $(pwd)/data:/data \
           faq-bot
```

## License

MIT License
