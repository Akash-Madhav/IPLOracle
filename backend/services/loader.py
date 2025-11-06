# services/loader.py

import os, json, faiss, numpy as np
from sentence_transformers import SentenceTransformer
import psutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "metadata.json")

model, index, metadata = None, None, None

def load_resources():
    global model, index, metadata
    print("🔔 Loading backend resources...")

    print(f"🧠 Memory before load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")

    model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(f"🧠 Memory after load: {psutil.Process().memory_info().rss / 1024**2:.2f} MiB")
    print("✅ Resources loaded")

def get_resources():
    return model, index, metadata