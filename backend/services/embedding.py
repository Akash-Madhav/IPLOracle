# services/embedding.py

from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("paraphrase-MiniLM-L3-v2")  # or L3-v2 for smaller footprint

def get_embedding(text: str) -> list[float]:
    return _model.encode(text, convert_to_numpy=False).tolist()