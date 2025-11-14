# services/embedding.py

from sentence_transformers import SentenceTransformer
import torch

print("🔥 Loading MiniLM model once at startup...")
model = SentenceTransformer("paraphrase-MiniLM-L3-v2", device="cpu")
print("✅ MiniLM model loaded.")

def get_embedding(text: str):
    with torch.no_grad():
        return model.encode(text, convert_to_numpy=False).tolist()