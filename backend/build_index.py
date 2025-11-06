# build_index.py
# 🏏 Build FAISS index and metadata from IPL player stats

import os
import pandas as pd
import faiss
import numpy as np
import json
import logging
from sentence_transformers import SentenceTransformer

# 🔧 Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 📁 Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "ipl_players.csv")
INDEX_PATH = os.path.join(BASE_DIR, "data", "faiss.index")
META_PATH = os.path.join(BASE_DIR, "data", "metadata.json")

def build_index():
    logger.info("📥 Reading IPL player data...")
    df = pd.read_csv(DATA_PATH)
    unique_players = df["Player_Name"].nunique()
    logger.info(f"🧠 Total unique players embedded: {unique_players}")

    sample_names = df["Player_Name"].dropna().unique()[:5]
    logger.info(f"🔎 Sample players: {sample_names}")


    # 🧩 Combine fields for semantic embedding
    df["combined_text"] = df.apply(
        lambda x: (
            f"{x['Player_Name']} played in {x['Year']} scoring {x['Runs_Scored']} runs "
            f"at an average of {x['Batting_Average']} with {x['Wickets_Taken']} wickets. "
            f"Strike Rate: {x['Batting_Strike_Rate']}. Role: Batter/Bowler/All-Rounder (inferred)."
        ),
        axis=1
    )

    logger.info("🔄 Generating embeddings...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(df["combined_text"].tolist(), convert_to_numpy=True, show_progress_bar=True)

    logger.info("📦 Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    logger.info("💾 Saving index and metadata...")
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)

    logger.info("✅ FAISS index and metadata saved successfully!")

if __name__ == "__main__":
    build_index()