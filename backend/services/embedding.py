# services/embedding.py

import gc
import torch
import psutil

def log_memory(tag=""):
    mem = psutil.Process().memory_info().rss / 1024**2
    print(f"🧠 Memory {tag}: {mem:.2f} MiB")

def get_embedding(text: str) -> list[float]:
    from sentence_transformers import SentenceTransformer

    log_memory("before loading model")
    model = SentenceTransformer("paraphrase-MiniLM-L3-v2", device="cpu")
    gc.collect()
    log_memory("after loading model")

    with torch.no_grad():
        embedding = model.encode(text, convert_to_numpy=False, device="cpu").tolist()

    log_memory("after embedding")

    # ✅ Cleanup
    del model
    gc.collect()
    log_memory("after cleanup")

    return embedding