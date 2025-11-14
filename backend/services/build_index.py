# build_index.py

import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os, gc

# Paths
base_dir = os.path.dirname(os.path.dirname(__file__))
metadata_path = os.path.join(base_dir, "data", "metadata.json")
index_path = os.path.join(base_dir, "data", "faiss.index")

# Load metadata
with open(metadata_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load embedding model (CORRECT NAME)
print("🔥 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

# Create embeddings
print("🧠 Generating embeddings...")
texts = [entry["combined_text"] for entry in metadata]
embeddings = model.encode(texts, convert_to_tensor=False)

# Convert to NumPy float32
embeddings = np.array(embeddings, dtype="float32")
num_vectors, dim = embeddings.shape

print(f"📏 Embedding matrix: {num_vectors} vectors × {dim} dims")

# Build FAST & ACCURATE FAISS index
print("🔧 Building FAISS IndexFlatL2...")
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

print(f"✅ FAISS index built with {index.ntotal} vectors")

# Save index
faiss.write_index(index, index_path)
print(f"💾 Index saved → {index_path}")

# Cleanup
del embeddings
del model
gc.collect()

print("🎉 Index rebuild complete!")
