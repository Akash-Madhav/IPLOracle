# services/embedding.py
import gc
from sentence_transformers import SentenceTransformer
import torch
import psutil
  # or L3-v2 for smaller footprint
_model = None
def log_memory():
    process = psutil.Process()
    print(f"🧠 Memory usage: {process.memory_info().rss / 1024 ** 2:.2f} MB")

def get_embedding(text: str) -> list[float]:
    global _model
    if _model is None:
        _model = SentenceTransformer("paraphrase-MiniLM-L3-v2", device="cpu")
        gc.collect()
        log_memory() 
    with torch.no_grad():
        embedding= _model.encode(text, convert_to_numpy=False, device="cpu").tolist()
        log_memory()
        return embedding