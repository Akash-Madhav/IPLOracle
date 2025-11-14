# services/loader.py

import os, gc, json, faiss, psutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "metadata.json")

def log_mem(tag=""):
    mem = psutil.Process().memory_info().rss / 1024**2
    print(f"🧠 Memory {tag}: {mem:.2f} MiB")

def load_metadata():
    print("🔔 Loading metadata...")
    log_mem("before metadata load")

    with open(META_PATH, "r", encoding="utf-8") as f:
        raw_metadata = json.load(f)

    metadata = [
        {
            "Player_Name": entry.get("Player_Name"),
            "Year": entry.get("Year"),
            "combined_text": entry.get("combined_text")[:1000]
        }
        for entry in raw_metadata
    ]
    del raw_metadata
    gc.collect()
    print(f"📦 Metadata entries loaded: {len(metadata)}")
    log_mem("after metadata load")
    return metadata

def load_index():
    print("🧠 Loading FAISS index...")
    log_mem("before index load")
    index = faiss.read_index(INDEX_PATH)
    gc.collect()
    log_mem("after index load")
    return index

def get_resources():
    index = load_index()
    metadata = load_metadata()
    return index, metadata