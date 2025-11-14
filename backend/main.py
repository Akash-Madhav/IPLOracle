# main.py
# 🏏 IPL Insight Bot - FastAPI Entrypoint
print("✅ main.py loaded")

import sys
print("🧨 Startup reached", file=sys.stderr)

import os
import gc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routes.ask import ask_router
from routes.admin import admin_router

print(f"🔧 PORT from env: {os.environ.get('PORT')}")

# 🚀 FastAPI app initialization
app = FastAPI(
    title="🏏 IPL Insight Bot",
    description="Semantic IPL stats search powered by FAISS + MiniLM embeddings + Gemini answers",
    version="1.0"
)

# 🔓 CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📬 Register routes
app.include_router(admin_router)
app.include_router(ask_router, prefix="/ask")

@app.get("/warmup")
def warmup():
    from services.loader import get_resources
    from services.embedding import get_embedding
    get_resources()
    get_embedding("warmup")
    return {"status": "warmed"}

# 🖼️ Favicon route
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# 🔁 Startup hook (lean and memory-safe)
@app.on_event("startup")
async def startup_event():
    import psutil
    mem_before = psutil.Process().memory_info().rss / 1024**2
    print(f"🧠 Memory before startup: {mem_before:.2f} MiB")

    gc.collect()

    mem_after = psutil.Process().memory_info().rss / 1024**2
    print(f"🧠 Memory after cleanup: {mem_after:.2f} MiB")
    print("✅ Startup setup complete")

# 🌐 Root route
@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"status": "ok", "message": "🏏 IPL Insight Bot backend is running!"}

# ❤️ Health check
@app.get("/health")
def health():
    return {"status": "ok"}