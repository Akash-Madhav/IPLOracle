# services/loader.py

import os, json, faiss
import psutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "metadata.json")

_index, _metadata = None, None  # ✅ Removed _model

def load_resources():
    global _metadata
    print("🔔 Loading backend resources...")
    print(f"🧠 Memory before load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")

    # Lazy-load FAISS index later
    with open(META_PATH, "r", encoding="utf-8") as f:
        raw_metadata = json.load(f)

    # Compress metadata: keep only essential fields
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
    return None, get_index(), _metadata  # ✅ Return None for model