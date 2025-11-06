# 🏏 IPL Insight Bot Backend

Semantic IPL stats search powered by FAISS and Gemini.

## Features
- FastAPI backend
- FAISS semantic search
- Gemini generative answers
- Modular architecture
- Admin route to rebuild index

## Routes
- `GET /` → Root health
- `GET /health` → Status check
- `POST /ask` → Query IPL stats
- `POST /rebuild-index` → Rebuild FAISS index

## Deployment
- Render-compatible via `render.yaml`
- Requires `GEMINI_API_KEY` in environment