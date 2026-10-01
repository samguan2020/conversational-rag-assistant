# Conversational RAG Assistant

A multi-tenant retrieval-augmented generation (RAG) backend: upload documents
into isolated "channels," then ask questions and get answers grounded in the
retrieved context, with conversation memory across turns.

> Implements the retrieval-augmented generation pattern from
> [Lewis et al. (2020)](#reference) — answer generation grounded in
> documents retrieved at query time, instead of relying only on what's
> baked into the model's weights.

## Showcase

Read the case study: **[samguan2020.github.io/conversational-rag-assistant](https://samguan2020.github.io/conversational-rag-assistant/)**

The page source is [`docs/index.html`](docs/index.html), served by GitHub Pages.

## How it works

1. **Ingest** (`POST /rags/docs`) — upload a PDF or TXT file for a channel.
   The document is split into ~200-character chunks (20-character overlap),
   embedded, and written into that channel's vector store.
2. **Retrieve** — a question is embedded and matched against the same
   channel's vector store to pull back the most relevant chunks.
3. **Generate** (`POST /rags/chatting`) — a `ConversationalRetrievalChain`
   condenses the question against chat history, retrieves context, and
   prompts the LLM to answer using only that context — reducing (not
   eliminating) hallucination versus asking the model cold.
4. **Remember** — a per-session `ConversationBufferWindowMemory` (last 3
   turns) keeps follow-up questions coherent.

## Multi-tenancy: channels

Each "channel" is a separate logical knowledge base — its own vector store
namespace/table, selected via a cookie and tracked in `channels.txt`. The
same deployment can serve isolated knowledge bases for different
tenants/topics without them leaking into each other's retrieval context.

## Architecture

```
rag/
  rag_controller.py     # FastAPI routes: channels, doc upload, chat
  rag_service.py        # Ingestion: load -> split -> embed -> store
  chatting_service.py   # ConversationalRetrievalChain + memory
  channel_service.py    # Per-channel isolation (cookie + channels.txt)
common/
  lc_modules.py          # LLM, embeddings, vector store, memory factories
config.py                 # Settings (env-driven)
main.py                    # FastAPI app
```

Swappable by design: `getVectorStore` backs onto local Redis for dev and
Cassandra/Astra DB in non-local environments behind the same interface;
`getLlm` switches between Gemini (Vertex AI) and GPT without touching the
retrieval or chat logic.

## Getting started

```bash
pip install -r requirements.txt
cp .env.local.example .env.local   # fill in OPENAI_API_KEY / REDIS_URL
redis-server                        # or point REDIS_URL at an existing instance

uvicorn main:app --reload --port 8081
```

Open `http://localhost:8081/docs` for the interactive API.

```bash
# Upload a document into the "default" channel
curl -F "file=@notes.pdf" http://localhost:8081/rags/docs

# Ask a question
curl -X POST "http://localhost:8081/rags/chatting?question=What%20does%20the%20doc%20say%20about%20X%3F"
```

For a non-local deployment, set `PY_ENV` to anything other than `local` and
provide `ASTRA_DB_ID` / `ASTRA_DB_TOKEN` to use Cassandra/Astra DB instead of
Redis — see `.env.local.example`.

## Reference

This project implements the pattern described in:

> Patrick Lewis et al. **"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks."** NeurIPS 2020. arXiv:2005.11401.
>
> [Paper (arXiv)](https://arxiv.org/abs/2005.11401)

This codebase is an independent implementation of that pattern — it is not
released or endorsed by the paper's authors.
