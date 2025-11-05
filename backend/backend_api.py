# ==========================================================
#  🏏 IPL Insight Bot - FastAPI + FAISS + Gemini Integration
# ==========================================================
import os, traceback

print("🚀 FastAPI app initializing...")
print("📂 Working directory:", os.getcwd())

# ---- Paths (no pre-assertion or sys.exit) ----
base_dir = os.path.dirname(__file__)
INDEX_PATH = os.path.join(base_dir, "data", "faiss.index")
META_PATH = os.path.join(base_dir, "data", "metadata.json")

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import faiss, numpy as np, json
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# ---- Config ----
GEMINI_KEY = os.getenv("GEMINI_API_KEY")  # set this in .env or system env

# ---- Initialize app ----
app = FastAPI(title="🏏 IPL Insight Bot + Gemini", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Load models ----
model, index, metadata = None, None, None  # Global placeholders

@app.on_event("startup")
async def load_resources():
    print("🔔 Startup event triggered")
    global model, index, metadata

    try:
        import psutil
        print(f"🧠 Memory before model load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")

        print("📦 Loading SentenceTransformer model...")
        model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
        print("✅ Model loaded")

        print("📦 Reading FAISS index...")
        index = faiss.read_index(INDEX_PATH)
        print("✅ FAISS index loaded")

        print("📦 Loading metadata...")
        with open(META_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        print("✅ Metadata loaded")

        print(f"🧠 Memory after startup: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")
        print("✅ FastAPI startup complete — ready to serve requests")

    except Exception as e:
        print("🔥 Startup crash detected:")
        traceback.print_exc()

# ---- Configure Gemini ----
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.5-flash")
else:
    gemini_model = None
    print("⚠️ GEMINI_API_KEY not found; fallback to plain FAISS results.")

# ---- Routes ----
@app.get("/")
def home():
    print("🌐 Root route accessed")
    return {"message": "🏏 IPL Insight Bot backend is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ask")
async def ask_query(request: Request):
    data = await request.json()
    query = data.get("query", "").strip()

    if not query:
        return {"answer": "⚠️ Please provide a question."}

    if not all([model, index, metadata]):
        return {"answer": "⚠️ Backend resources not loaded. Please try again later."}

    print(f"🟢 Query: {query}")
    query_emb = model.encode([query])
    D, I = index.search(np.array(query_emb).astype("float32"), k=5)
    results = [metadata[i] for i in I[0]]

    context = "\n".join(
        [
            f"{r['Player_Name']} - Runs: {r['Runs_Scored']}, Wickets: {r['Wickets_Taken']}, Matches: {r['Matches_Batted']}, Average: {r['Batting_Average']}, Economy: {r.get('Economy_Rate', 'N/A')}"
            for r in results
        ]
    )

    if gemini_model:
        prompt = f"""
        You are a cricket data analyst. Use the statistics provided below to answer
        the user's question accurately and logically. If the question involves 
        prediction (like "how many runs will Dhoni score next match"), use past 
        performance data trends to make a reasoned estimate — not an exact prediction.

        Question:
        {query}

        Player Stats:
        {context}

        Answer in the least amount of lines or words. Provide your result or conclusion alone.
        """
        try:
            response = gemini_model.generate_content(prompt)
            answer = response.text.strip()
        except Exception as e:
            print("❌ Gemini error:", e)
            answer = f"Top similar records found:\n{context}"
    else:
        answer = f"Top similar records found:\n{context}"

    return {"query": query, "answer": answer, "results": results}
''''import os, sys, traceback

print("🚀 FastAPI app initializing...")
print("📂 Working directory:", os.getcwd())

try:
    base_dir = os.path.dirname(__file__)
    INDEX_PATH = os.path.join(base_dir, "data", "faiss.index")
    META_PATH = os.path.join(base_dir, "data", "metadata.json")

    assert os.path.exists(INDEX_PATH), "❌ FAISS index not found"
    assert os.path.exists(META_PATH), "❌ Metadata file not found"
    print("✅ FAISS index and metadata loaded")

except Exception as e:
    print("🔥 Startup crash detected:")
    traceback.print_exc()
    sys.exit(1)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import faiss, numpy as np, json, os
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
# ---- Config ----

GEMINI_KEY = os.getenv("GEMINI_API_KEY")  # set this in .env or system env

# ---- Initialize app ----
app = FastAPI(title="🏏 IPL Insight Bot + Gemini", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Load models ----
@app.on_event("startup")
async def load_resources():
    print("🔔 Startup event triggered")
    global model, index, metadata

    try:
        import psutil
        print(f"🧠 Memory before model load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")

        print("📦 Loading SentenceTransformer model...")
        model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
        print("✅ Model loaded")

        print("📦 Reading FAISS index...")
        index = faiss.read_index(INDEX_PATH)
        print("✅ FAISS index loaded")

        print("📦 Loading metadata...")
        with open(META_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        print("✅ Metadata loaded")

        print(f"🧠 Memory after startup: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")

    except Exception as e:
        print("🔥 Startup crash detected:")
        import traceback
        traceback.print_exc()

# Configure Gemini (if available)
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.5-flash")
else:
    gemini_model = None
    print("⚠️ GEMINI_API_KEY not found; fallback to plain FAISS results.")

# ---- Routes ----
@app.get("/")
def home():
    print("🌐 Root route accessed")
    return {"message": "🏏 IPL Insight Bot backend is running!"}
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ask")
async def ask_query(request: Request):
    data = await request.json()
    query = data.get("query", "").strip()

    if not query:
        return {"answer": "⚠️ Please provide a question."}

    print(f"🟢 Query: {query}")
    query_emb = model.encode([query])
    D, I = index.search(np.array(query_emb).astype("float32"), k=5)
    results = [metadata[i] for i in I[0]]

    # Build context summary from top matches
    context = "\n".join(
        [
            f"{r['Player_Name']} - Runs: {r['Runs_Scored']}, Wickets: {r['Wickets_Taken']}, Matches: {r['Matches_Batted']}, Average: {r['Batting_Average']}, Economy: {r.get('Economy_Rate', 'N/A')}"
            for r in results
        ]
    )

    # -----------------------------
    # 🧠 Predictive + analytical mode
    # -----------------------------
    if gemini_model:
        prompt = f"""
        You are a cricket data analyst. Use the statistics provided below to answer
        the user's question accurately and logically. If the question involves 
        prediction (like "how many runs will Dhoni score next match"), use past 
        performance data trends to make a reasoned estimate — not an exact prediction.

        Question:
        {query}

        Player Stats:
        {context}

        Answer in the least amount of lines or words. Provide your result or conslusion alone.
        """
        try:
            response = gemini_model.generate_content(prompt)
            answer = response.text.strip()
        except Exception as e:
            print("❌ Gemini error:", e)
            answer = f"Top similar records found:\n{context}"
    else:
        answer = f"Top similar records found:\n{context}"

    return {"query": query, "answer": answer, "results": results}
'''
'''
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
'''