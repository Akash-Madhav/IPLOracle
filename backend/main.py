# main.py
# 🏏 IPL Insight Bot - FastAPI Entrypoint

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.ask import ask_router
from backend.routes.admin import admin_router
from backend.services.loader import load_resources
from backend.services.gemini import configure_gemini

# 🚀 FastAPI app initialization
app = FastAPI(
    title="🏏 IPL Insight Bot + Gemini",
    description="Semantic IPL stats search powered by FAISS and Gemini",
    version="1.0"
)
app.include_router(admin_router)
# 🔓 CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔁 Startup hook
@app.on_event("startup")
async def startup_event():
    print("🔔 Startup triggered")
    load_resources()
    configure_gemini()

# 🌐 Root route
@app.get("/")
def home():
    return {"message": "🏏 IPL Insight Bot backend is running!"}

# ❤️ Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# 📬 Register routes
app.include_router(ask_router, prefix="/ask")