from functools import lru_cache
import gc

@lru_cache()
def get_model():
    from sentence_transformers import SentenceTransformer
    print("🔥 Loading MiniLM model (lazy)...")
    model = SentenceTransformer("paraphrase-MiniLm-L3-v2", device="cpu")
    print("✅ MiniLM loaded")
    return model

def get_embedding(text: str):
    model = get_model()
    return model.encode(text).tolist()

def clear_model():
    import torch
    torch.cuda.empty_cache()  # if using GPU
    gc.collect()
    print("🗑️ MiniLM model cleared from memory")