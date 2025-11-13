# main.py
# 🏏 IPL Insight Bot - FastAPI Entrypoint
print("✅ main.py loaded")

import os
import psutil
print(f"🔧 PORT from env: {os.environ.get('PORT')}")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routes.ask import ask_router
from routes.admin import admin_router
from services.loader import load_resources
import threading

# 🚀 FastAPI app initialization
app = FastAPI(
    title="🏏 IPL Insight Bot",
    description="Semantic IPL stats search powered by FAISS + MiniLM embeddings + Gemini answers",
    version="1.0"
)

# 🔓 CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📬 Register routes
app.include_router(admin_router)
app.include_router(ask_router, prefix="/ask")

# 🖼️ Favicon route
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# 🔁 Startup hook (NON-BLOCKING ✅)
@app.on_event("startup")
async def startup_event():
    print("🔔 Startup triggered")
    threading.Thread(target=load_resources).start()
    mem = psutil.Process().memory_info().rss / 1024**2
    print(f"🧠 Memory usage at startup: {mem:.2f} MiB")
    print("✅ Resources loaded")
    print("✅ Startup setup complete")

# 🌐 Root route
@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"status": "ok", "message": "🏏 IPL Insight Bot backend is running!"}

# ❤️ Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# 🏁 Main entry point (optional for local dev)
# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 10000))
#     uvicorn.run("main:app", host="0.0.0.0", port=port)