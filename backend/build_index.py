import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os

# === Paths ===
DATA_PATH = "data/ipl_players.csv"
INDEX_PATH = "data/faiss.index"
META_PATH = "data/metadata.json"

# === Load CSV ===
df = pd.read_csv(DATA_PATH)

# 🧩 Combine all info into a single text field for semantic search
df["combined_text"] = df.apply(
    lambda x: (
        f"{x['Player_Name']} played in {x['Year']} scoring {x['Runs_Scored']} runs "
        f"at an average of {x['Batting_Average']} with {x['Wickets_Taken']} wickets. "
        f"Strike Rate: {x['Batting_Strike_Rate']}. "
        f"Role: Batter/Bowler/All-Rounder (inferred)."
    ),
    axis=1
)

# === Create Embeddings ===
print("🔄 Generating embeddings...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(df["combined_text"].tolist(), convert_to_numpy=True, show_progress_bar=True)

# === Build FAISS Index ===
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# === Save Index & Metadata ===
os.makedirs("data", exist_ok=True)
faiss.write_index(index, INDEX_PATH)

with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump(df.to_dict(orient="records"), f, indent=2)

print("✅ FAISS index built and saved successfully!")