# services/embedding.py

from services.loader import embedding_model
import logging

logger = logging.getLogger(__name__)

def get_embedding(text: str):
    try:
        embedding = embedding_model.encode(text, normalize_embeddings=True)
        logger.info(f"✅ SentenceTransformer embedding shape: {len(embedding)}")
        return embedding.tolist()
    except Exception as e:
        logger.error(f"❌ SentenceTransformer embedding failed: {e}")
        return []