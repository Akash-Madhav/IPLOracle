# services/embedding.py

from sentence_transformers import SentenceTransformer
import gc
model = None

def get_model():
    global model
    if model is None:
        print("🔥 Loading MiniLM model (lazy)...")
        model = SentenceTransformer("paraphrase-MiniLm-L3-v2", device="cpu")
        print("✅ MiniLM loaded")
    return model

def get_embedding(text: str):
    model = get_model()
    return model.encode(text).tolist()
def clear_model():
    global model
    if model is not None:
        del model
        model = None
        gc.collect()
        print("🗑️ MiniLM model cleared from memory")