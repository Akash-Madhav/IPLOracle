# services/loader.py

import os, gc
import json
import faiss
import psutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "metadata.json")

_index, _metadata = None, None

def load_resources():
    global _metadata
    print("🔔 Loading backend resources...")
    print(f"🧠 Memory before metadata load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")

    # Load metadata
    with open(META_PATH, "r", encoding="utf-8") as f:
        raw_metadata = json.load(f)

    _metadata = [
        {
            "Player_Name": entry.get("Player_Name"),
            "Year": entry.get("Year"),
            "combined_text": entry.get("combined_text")[:1000]
        }
        for entry in raw_metadata
    ]
    del raw_metadata
    gc.collect()
    print(f"📦 Metadata entries loaded: {len(_metadata)}")
    print(f"🧠 Memory after metadata load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")
    print("✅ Metadata loaded")

def get_index():
    global _index
    if _index is None:
        print("🧠 Lazy-loading FAISS index...")
        print(f"🧠 Memory before index load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")
        _index = faiss.read_index(INDEX_PATH)
        gc.collect()
        print(f"🧠 Memory after index load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")
        print("✅ FAISS index loaded")
    return _index

def get_resources():
    return get_index(), _metadata