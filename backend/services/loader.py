# services/loader.py

import os, json, faiss
from sentence_transformers import SentenceTransformer
import psutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "metadata.json")

_model, _index, _metadata = None, None, None

def load_resources():
    global _index, _metadata
    print("🔔 Loading backend resources...")

    print(f"🧠 Memory before load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")

    # Lazy-load model later
    _index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "r", encoding="utf-8") as f:
        _metadata = json.load(f)

    print(f"🧠 Memory after load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")
    print("✅ Resources loaded")

def get_model():
    global _model
    if _model is None:
        print("🧠 Lazy-loading SentenceTransformer...")
        _model = SentenceTransformer("paraphrase-MiniLM-L6-v2", device="cpu")
    return _model

def get_resources():
    return get_model(), _index, _metadata