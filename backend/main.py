import os
import sys

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 🏏 IPL Insight Bot - FastAPI Entrypoint
print("✅ main.py loaded")
print("🧨 Startup reached", file=sys.stderr)

import os
import gc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from routes.ask import ask_router
from routes.admin import admin_router

# 🔧 Log environment variables for debugging
#print(f"🔧 PORT from env: {os.environ.get('PORT')}")
#print(f"🔐 GEMINI_API_KEY: {os.environ.get('GEMINI_API_KEY')}")
#print(f"🔐 PINECONE_API_KEY: {os.environ.get('PINECONE_API_KEY')}")
#print(f"📦 INDEX_NAME: {os.environ.get('INDEX_NAME')}")

app = FastAPI(
    title="🏏 IPL Insight Bot",
    description="Semantic IPL stats search powered by Pinecone + Gemini answers",
    version="1.0"
)

# 🌐 CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📬 Register routes
app.include_router(admin_router)
app.include_router(ask_router)

# 🔥 Warmup endpoint (no embedding now, just a simple check)
@app.get("/warmup")
async def warmup():
    print("🔍 /warmup route hit")
    try:
        return {"status": "✅ Warmup complete"}
    except Exception as e:
        print(f"⚠️ Warmup error: {e}")
        return JSONResponse(status_code=500, content={"status": "❌ Warmup failed", "error": str(e)})

# 🖼️ Favicon
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# 🚀 Startup setup and memory check
@app.on_event("startup")
async def startup_event():
    import psutil
    from services.player_store import player_store
    from config import Config

    mem_before = psutil.Process().memory_info().rss / 1024**2
    print(f"🧠 Memory before player store initialization: {mem_before:.2f} MiB")

    # Load in-memory indexed player database from CSV
    player_store.load(Config.CSV_PATH)

    gc.collect()
    mem_after = psutil.Process().memory_info().rss / 1024**2
    print(f"🧠 Total Memory after startup: {mem_after:.2f} MiB")
    print("✅ Startup setup complete")

# 🏠 Home route
@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"status": "ok", "message": "🏏 IPL Insight Bot backend is running!"}

# ❤️ Health check (keeps backend active and prevents spin-down)
@app.get("/health")
def health():
    from services.player_store import player_store
    import time
    return {
        "status": "ok",
        "service": "IPL Insight Bot Backend",
        "database_loaded": player_store.is_loaded,
        "players_count": len(player_store.get_all_player_names()),
        "timestamp": int(time.time())
    }