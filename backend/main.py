# main.py
# 🏏 IPL Insight Bot - FastAPI Entrypoint
print("✅ main.py loaded")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ask import ask_router
from routes.admin import admin_router
from services.loader import load_resources
from services.gemini import configure_gemini
import threading
from fastapi.responses import FileResponse

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
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# 🔁 Startup hook
# 🔁 Startup hook (NON-BLOCKING ✅)
@app.on_event("startup")
async def startup_event():
    print("🔔 Startup triggered")
    # ✅ Run heavy tasks on background threads so port opens immediately
    threading.Thread(target=load_resources).start()
    configure_gemini()

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