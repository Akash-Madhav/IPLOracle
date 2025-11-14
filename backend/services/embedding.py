# services/embedding.py

from sentence_transformers import SentenceTransformer
import torch

model = None

def get_model():
    global model
    if model is None:
        print("🔥 Loading MiniLM model (lazy)...")
        model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        print("✅ MiniLM loaded")
    return model

def get_embedding(text: str):
    m = get_model()
    with torch.no_grad():
        return m.encode(text, convert_to_numpy=False).tolist()
