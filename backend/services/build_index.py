import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Resolve absolute path to metadata
base_dir = os.path.dirname(os.path.dirname(__file__))  # project root
metadata_path = os.path.join(base_dir, "data", "metadata.json")

# Load metadata
with open(metadata_path, "r") as f:
    metadata = json.load(f)

# Load embedding model
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

# Create embeddings
texts = [entry["combined_text"] for entry in metadata]
embeddings = model.encode(texts, convert_to_tensor=False)

# Convert to FAISS-compatible float32 array using NumPy
embedding_array = np.array(embeddings, dtype="float32")
embedding_count, d = embedding_array.shape

# Build compressed FAISS index
nlist = 100
m = 8
nbits = 8

quantizer = faiss.IndexFlatL2(d)
index = faiss.IndexIVFPQ(quantizer, d, nlist, m, nbits)

print("🔧 Training compressed index...")
index.train(embedding_array)
index.add(embedding_array)

# Save index to original path
index_path = os.path.join(base_dir, "data", "faiss.index")
faiss.write_index(index, index_path)
print(f"✅ Compressed index saved to {index_path}")