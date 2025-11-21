# 🏏 IPL Insight Bot - FastAPI Entrypoint
print("✅ main.py loaded")

import sys
print("🧨 Startup reached", file=sys.stderr)

import os
import gc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from routes.ask import ask_router
from routes.admin import admin_router

# 🔧 Log environment variables for debugging
print(f"🔧 PORT from env: {os.environ.get('PORT')}")
print(f"🔐 GEMINI_API_KEY: {os.environ.get('GEMINI_API_KEY')}")
print(f"🔐 PINECONE_API_KEY: {os.environ.get('PINECONE_API_KEY')}")
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

# 🚀 Startup memory check
@app.on_event("startup")
async def startup_event():
    import psutil
    mem_before = psutil.Process().memory_info().rss / 1024**2
    print(f"🧠 Memory before startup: {mem_before:.2f} MiB")
    gc.collect()
    mem_after = psutil.Process().memory_info().rss / 1024**2
    print(f"🧠 Memory after cleanup: {mem_after:.2f} MiB")
    print("✅ Startup setup complete")

# 🏠 Home route
@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"status": "ok", "message": "🏏 IPL Insight Bot backend is running!"}

# ❤️ Health check
@app.get("/health")
def health():
    return {"status": "ok"}