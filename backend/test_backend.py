from sentence_transformers import SentenceTransformer
import requests

# Load MiniLM model (384-dim)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embedding
query = "Who had the best strike rate in IPL 2023?"
vector = model.encode(query).tolist()  # length 384
# Send to backend
payload = {"query": query, "vector": vector}
res = requests.post("https://iploracle-2wxn.onrender.com/ask", json=payload)

print(res.json())