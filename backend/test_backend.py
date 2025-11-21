from sentence_transformers import SentenceTransformer
import requests

# Load MiniLM model (384-dim)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embedding
query = "Who scored the most runs in IPL 2023?"
vector = model.encode(query).tolist()  # length 384

# Send to backend
payload = {"query": query, "vector": vector}
res = requests.post("http://127.0.0.1:8000/ask", json=payload)

print(res.json())