# main.py
# 🏏 IPL Insight Bot - FastAPI Entrypoint
print("✅ main.py loaded")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.ask import ask_router
from backend.routes.admin import admin_router
from backend.services.loader import load_resources
from backend.services.gemini import configure_gemini
import threading
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
# 🔁 Startup hook (NON-BLOCKING ✅)
@app.on_event("startup")
async def startup_event():
    print("🔔 Startup triggered")

    # ✅ Run heavy tasks on background threads so port opens immediately
    threading.Thread(target=load_resources).start()
    threading.Thread(target=configure_gemini).start()

    print("✅ Startup setup complete")

# 🌐 Root route
@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"status": "ok", "message": "🏏 IPL Insight Bot backend is running!"}

# ❤️ Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# 📬 Register routes
app.include_router(ask_router, prefix="/ask")