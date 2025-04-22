# Github AI Repo Assistant
implementation Rag architecture, used embeddings, vector stores/db for efficient retrieval of necessary code chunk, to limit context window

command-line tool(for now) that helps in understanding, querying, summarizing, and even generateing tests/docs(not yet) for your code repositories using large language models like **Gemini** or **Ollama**.  
It uses FAISS vector stores for retrieval-augmented generation (RAG).

---

## Features

- Ask natural language questions about your codebase
- Context-aware responses via embedding search + LLMs
- `/summarize` — generate summaries of your entire repo
- `/history` — view or export previous Q&A
- FAISS-based semantic search

---

## 📦 Installation

```bash (python env recommended)
git clone https://github.com/your-username/repochat.git
cd repochat
pip install -r requirements.txt

1. Create a .env file with your Gemini API key (or configure Ollama):
GEMINI_API_KEY=your_api_key_here

2.Chunk & embed your repo:
python3 scripts/embed_repo.py

3. run
python main.py

```

# How It Works

- Embedding: Your repo is parsed and chunked into text + vector embeddings using your chosen model.

- Storage: Chunks are stored in a FAISS index + metadata in JSON.

- Querying: Queries are embedded, and top relevant chunks are retrieved.

- LLM Response: Chunks + user query are sent to Gemini/Ollama for a final answer.


embedding-> Gemini text-embedding-004 / ollama nomic-embed model
Text generation-> gemini-2-flash / ollama mistral or llama
