# services/loader.py

import os, json, faiss, psutil
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "metadata.json")

_index, _metadata = None, None

# ✅ Eagerly load embedding model at module level
print("🧠 Loading SentenceTransformer model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ SentenceTransformer model loaded")

def load_resources():
    global _metadata
    print("🔔 Loading backend resources...")
    print(f"🧠 Memory before load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")

    # Load metadata
    with open(META_PATH, "r", encoding="utf-8") as f:
        raw_metadata = json.load(f)

    _metadata = [
        {
            "Player_Name": entry.get("Player_Name"),
            "Year": entry.get("Year"),
            "combined_text": entry.get("combined_text")
        }
        for entry in raw_metadata
    ]

    print(f"🧠 Memory after load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")
    print("✅ Resources loaded")

def get_index():
    global _index
    if _index is None:
        print("🧠 Lazy-loading FAISS index...")
        _index = faiss.read_index(INDEX_PATH)
    return _index

def get_resources():
    return embedding_model, get_index(), _metadata