# services/loader.py

import os, json, faiss

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "metadata.json")

print("🔥 Loading resources (FAISS + metadata) once at startup...")

# ---------------------------
# Load FAISS index (ONE TIME)
# ---------------------------
print("🧠 Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)
print("✅ FAISS index loaded.")

# ---------------------------
# Load metadata (ONE TIME)
# ---------------------------
print("🔔 Loading metadata...")
with open(META_PATH, "r", encoding="utf-8") as f:
    raw = json.load(f)

metadata = [
    {
        "Player_Name": entry.get("Player_Name"),
        "Year": entry.get("Year"),
        "combined_text": entry.get("combined_text")[:1000]
    }
    for entry in raw
]

print(f"📦 Metadata loaded: {len(metadata)} entries")
print("✅ All resources preloaded.")

# ---------------------------
# Public function to access them
# ---------------------------
def get_resources():
    return index, metadata
