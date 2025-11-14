# services/loader.py

import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "metadata.json")

index = None
metadata = None
faiss = None   # <--- IMPORTANT: start as None

def get_resources():
    global index, metadata, faiss

    # Load FAISS ONLY when this function is called
    if faiss is None:
        print("🔥 Importing FAISS lazily...")
        import faiss as _fa
        faiss = _fa
        print("✅ FAISS module loaded")

    if index is None:
        print("🔥 Loading FAISS index (lazy)...")
        index = faiss.read_index(INDEX_PATH)
        print("✅ FAISS index loaded")

    if metadata is None:
        print("🔔 Loading metadata (lazy)...")
        with open(META_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        metadata = [
            {
                "Player_Name": e["Player_Name"],
                "Year": e["Year"],
                "combined_text": e["combined_text"][:1000]
            }
            for e in raw
        ]
        print(f"📦 Metadata entries: {len(metadata)}")

    return index, metadata
def clear_resources():
    global index, metadata, faiss
    if index is not None:
        del index
        index = None
    if metadata is not None:
        del metadata
        metadata = None
    if faiss is not None:
        del faiss
        faiss = None
    print("🗑️ FAISS resources cleared from memory")