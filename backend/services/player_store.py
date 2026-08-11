"""
In-memory indexed database for player statistics from CSV.
Provides O(1) player lookup by name, fast player search, and player list retrieval.
"""

import csv
import os
import re
import sys
import logging
from typing import Dict, List, Optional
from rapidfuzz import process, utils

logger = logging.getLogger(__name__)

def normalize_name(name: str) -> str:
    """
    Normalize player name for consistent, case-insensitive, punctuation-free lookup.
    e.g. 'M.S. Dhoni' -> 'ms dhoni', 'Virat  Kohli ' -> 'virat kohli'
    """
    if not name:
        return ""
    # Remove punctuation, extra spaces, lowercase
    cleaned = re.sub(r"[^\w\s]", "", name.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


class PlayerStore:
    def __init__(self):
        self._all_records: List[Dict] = []
        self._player_records: Dict[str, List[Dict]] = {}  # Canonical Name -> Records
        self._normalized_index: Dict[str, str] = {}      # Normalized Name -> Canonical Name
        self._all_canonical_names: List[str] = []         # Sorted canonical names list
        self._year_records: Dict[str, List[Dict]] = {}     # Year -> Records
        self._is_loaded: bool = False

    def load(self, csv_path: str = "data/ipl_players.csv") -> None:
        """Load player records from CSV into indexed in-memory data structures."""
        if not os.path.exists(csv_path):
            logger.warning(f"⚠️ CSV file not found at {csv_path}")
            return

        records = []
        player_map: Dict[str, List[Dict]] = {}
        norm_map: Dict[str, str] = {}
        year_map: Dict[str, List[Dict]] = {}

        with open(csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numbers to appropriate types while keeping string formats intact for API output
                processed_row = dict(row)
                player_name = processed_row.get("Player_Name", "").strip()
                year = processed_row.get("Year", "").strip()

                if not player_name:
                    continue

                records.append(processed_row)

                # Group by canonical name
                if player_name not in player_map:
                    player_map[player_name] = []
                player_map[player_name].append(processed_row)

                # Build normalized lookup index
                norm_name = normalize_name(player_name)
                if norm_name:
                    norm_map[norm_name] = player_name

                # Group by year
                if year:
                    if year not in year_map:
                        year_map[year] = []
                    year_map[year].append(processed_row)

        self._all_records = records
        self._player_records = player_map
        self._normalized_index = norm_map
        self._all_canonical_names = sorted(list(player_map.keys()))
        self._year_records = year_map
        self._is_loaded = True

        logger.info(f"✅ PlayerStore loaded: {len(self._all_records)} records across {len(self._all_canonical_names)} players")

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def get_all_player_names(self) -> List[str]:
        """Return a sorted list of all unique canonical player names."""
        return list(self._all_canonical_names)

    def get_player_records(self, player_name: str) -> List[Dict]:
        """
        Retrieve all records for a player by exact or normalized name.
        O(1) lookup latency.
        """
        # Direct canonical hit
        if player_name in self._player_records:
            return self._player_records[player_name]

        # Normalized hit
        norm = normalize_name(player_name)
        if norm in self._normalized_index:
            canonical = self._normalized_index[norm]
            return self._player_records[canonical]

        # Fuzzy match fallback for minor misspellings
        match = process.extractOne(norm, list(self._normalized_index.keys()), score_cutoff=85)
        if match:
            canonical = self._normalized_index[match[0]]
            return self._player_records[canonical]

        return []

    def extract_players_from_query(self, query: str, threshold: int = 88) -> List[str]:
        """
        Extract mentioned player names from user query deterministically.
        Returns a list of matching canonical player names.
        """
        if not query or not self._all_canonical_names:
            return []

        STOPWORDS = {
            "who", "what", "which", "how", "many", "most", "best", "highest", "top",
            "lowest", "worst", "better", "worse", "more", "less", "leading", "first",
            "last", "runs", "run", "wicket", "wickets", "score", "scores", "scored", "batting",
            "bowling", "strike", "rate", "average", "century", "centuries", "fifty",
            "fifties", "fours", "sixes", "catches", "stumpings", "match", "matches",
            "player", "players", "stat", "stats", "performance", "record", "records",
            "year", "years", "season", "team", "ipl", "overall", "total", "the", "in", "and", "or", "for", "with", "show", "me", "give", "tell"
        }

        query_norm = normalize_name(query)
        query_lower = query.lower()
        found_players = set()

        # Step 1: Substring search against canonical & normalized full names
        for norm_name, canonical in self._normalized_index.items():
            if len(norm_name) >= 4 and norm_name not in STOPWORDS and norm_name in query_norm:
                found_players.add(canonical)
            elif canonical.lower() in query_lower:
                found_players.add(canonical)

        if found_players:
            return list(found_players)

        # Step 2: Token-by-token comparison against player name tokens
        query_tokens = [w for w in re.split(r"\W+", query_norm) if len(w) > 3 and w not in STOPWORDS]
        if not query_tokens:
            return []

        for canonical in self._all_canonical_names:
            canonical_tokens = [t for t in re.split(r"\W+", normalize_name(canonical)) if len(t) > 3 and t not in STOPWORDS]
            for q_tok in query_tokens:
                for c_tok in canonical_tokens:
                    if q_tok == c_tok:
                        found_players.add(canonical)
                    elif process.extractOne(q_tok, [c_tok], score_cutoff=threshold):
                        found_players.add(canonical)

        return list(found_players)

    def get_records_by_years(self, years: List[int]) -> List[Dict]:
        """Retrieve all records matching any of the specified years."""
        result = []
        for year in years:
            str_year = str(year)
            if str_year in self._year_records:
                result.extend(self._year_records[str_year])
        return result

    def get_all_records(self) -> List[Dict]:
        """Return all player records in the dataset."""
        return list(self._all_records)


# Global singleton instance
player_store = PlayerStore()
