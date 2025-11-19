import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_REGION = os.getenv("PINECONE_REGION")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD")
INDEX_NAME = "ipl-players"                     # Your index name
DIMENSION = 384                                # Depends on your embedding model

# 🧠 Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 🧪 Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# 🛠️ Create index if it doesn't exist
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION)
    )

# 🔗 Connect to index
index = pc.Index(INDEX_NAME)

# 📄 Load CSV
df = pd.read_csv("../data/ipl_players.csv")

# 🚀 Upload in batches
batch = []
for i, row in df.iterrows():
    # Create embedding input from full row
    text = " | ".join([f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])])
    embedding = model.encode(text).tolist()

    # Convert full row to metadata
    metadata = row.to_dict()
    for k, v in metadata.items():
        if pd.isna(v):
            metadata[k] = None
        elif isinstance(v, (np.int64, np.float64)):
            metadata[k] = v.item()

    # Add to batch
    batch.append({
        "id": f"{row['Player_Name'].replace(' ', '_')}_{row['Year']}",
        "values": embedding,
        "metadata": metadata
    })

    # Upload every 100 records
    if len(batch) == 100:
        index.upsert(batch)
        batch = []

# Upload remaining
if batch:
    index.upsert(batch)

print("✅ Upload complete.")