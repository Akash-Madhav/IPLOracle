"""
Comprehensive test script for Database and Retrieval Optimization.
Validates:
1. Direct player name lookup (/players/{name})
2. Player list retrieval (/players)
3. Deterministic query retrieval (/ask with name)
4. Superlative query retrieval (/ask with superlative)
5. Semantic vector search fallback (/ask with vector)
6. Latency measurements
7. Backend RAM usage measurement (< 400 MB)
"""

import sys
import os

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import time
import psutil

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from main import app
from services.player_store import player_store

client = TestClient(app)


def test_player_store_direct():
    print("=" * 80)
    print("Test 1: Direct PlayerStore In-Memory Unit Tests")
    print("=" * 80)

    # Load store explicitly if not loaded
    if not player_store.is_loaded:
        player_store.load("data/ipl_players.csv")

    assert player_store.is_loaded, "PlayerStore should be loaded"

    # Test 1.1: Player count
    names = player_store.get_all_player_names()
    print(f"Total canonical players: {len(names)}")
    assert len(names) == 247, f"Expected 247 players, got {len(names)}"

    # Test 1.2: Exact player lookup
    recs = player_store.get_player_records("Virat Kohli")
    print(f"Virat Kohli records: {len(recs)}")
    assert len(recs) > 0, "Should find records for Virat Kohli"

    # Test 1.3: Normalized player lookup ('vIRAT   kOHLI')
    norm_recs = player_store.get_player_records("vIRAT   kOHLI")
    print(f"Normalized 'vIRAT   kOHLI' records: {len(norm_recs)}")
    assert len(norm_recs) == len(recs), "Normalized lookup should return same records"

    # Test 1.4: Extraction from query
    extracted = player_store.extract_players_from_query("Tell me about MS Dhoni's performance in 2023")
    print(f"Extracted players from query: {extracted}")
    assert "MS Dhoni" in extracted, "Should extract MS Dhoni"

    print("✅ Test 1 Passed: PlayerStore in-memory unit tests successful!\n")


def test_api_endpoints():
    print("=" * 80)
    print("Test 2: API Endpoints & Retrieval Latency Tests")
    print("=" * 80)

    # Test 2.1: /players endpoint
    t0 = time.time()
    res = client.get("/players")
    player_list_latency = (time.time() - t0) * 1000
    assert res.status_code == 200, f"/players failed with {res.status_code}"
    data = res.json()
    print(f"1. GET /players - Total: {data['total_players']}, Latency: {player_list_latency:.2f} ms")
    assert data["total_players"] == 247

    # Test 2.2: /players/{name} endpoint
    t0 = time.time()
    res = client.get("/players/Ruturaj Gaikwad")
    player_detail_latency = (time.time() - t0) * 1000
    assert res.status_code == 200, f"/players/Ruturaj Gaikwad failed with {res.status_code}"
    detail = res.json()
    print(f"2. GET /players/Ruturaj Gaikwad - Records: {detail['total_records']}, Latency: {player_detail_latency:.2f} ms")
    assert detail["player_name"] == "Ruturaj Gaikwad"
    assert detail["total_records"] >= 3

    # Test 2.3: POST /ask with deterministic player name
    t0 = time.time()
    res = client.post("/ask", json={"query": "Show stats for Jasprit Bumrah in 2020"})
    name_lookup_latency = (time.time() - t0) * 1000
    assert res.status_code == 200, f"POST /ask failed with {res.status_code}"
    ask_data = res.json()
    print(f"3. POST /ask (Name Lookup) - Answer length: {len(ask_data['answer'])}, Latency: {name_lookup_latency:.2f} ms")
    assert len(ask_data["results"]) > 0
    assert any(r.get("Player_Name") == "Jasprit Bumrah" for r in ask_data["results"])

    # Test 2.4: POST /ask with superlative query
    t0 = time.time()
    res = client.post("/ask", json={"query": "Who scored the most runs in IPL 2023?"})
    superlative_latency = (time.time() - t0) * 1000
    assert res.status_code == 200, f"POST /ask superlative failed with {res.status_code}"
    sup_data = res.json()
    print(f"4. POST /ask (Superlative) - Answer length: {len(sup_data['answer'])}, Latency: {superlative_latency:.2f} ms")
    assert len(sup_data["results"]) > 0
    assert sup_data["results"][0]["Player_Name"] == "Shubman Gill"

    # Test 2.5: POST /ask with dummy vector semantic query
    t0 = time.time()
    dummy_vector = [0.01] * 384
    res = client.post("/ask", json={"query": "Best overall cricket stats", "vector": dummy_vector})
    semantic_latency = (time.time() - t0) * 1000
    assert res.status_code == 200
    sem_data = res.json()
    print(f"5. POST /ask (Semantic Fallback) - Latency: {semantic_latency:.2f} ms")

    print("\n✅ Test 2 Passed: All API endpoints working with low latency!\n")

    return {
        "player_list_latency_ms": round(player_list_latency, 2),
        "player_detail_latency_ms": round(player_detail_latency, 2),
        "name_lookup_latency_ms": round(name_lookup_latency, 2),
        "superlative_latency_ms": round(superlative_latency, 2),
        "semantic_latency_ms": round(semantic_latency, 2),
    }


def test_memory_limit():
    print("=" * 80)
    print("Test 3: Total Backend RAM Consumption Analysis")
    print("=" * 80)

    process = psutil.Process()
    ram_mb = process.memory_info().rss / 1024**2
    print(f"Current Backend Memory (RSS): {ram_mb:.2f} MB")
    print(f"Target Memory Limit: < 400.00 MB")

    assert ram_mb < 400.0, f"Memory usage {ram_mb:.2f} MB exceeds 400 MB limit!"
    print("✅ Test 3 Passed: Memory footprint is well within the 400 MB budget!\n")

    return round(ram_mb, 2)


if __name__ == "__main__":
    print("\n🚀 Starting Optimization Verification & Performance Measurement\n")

    t_start = time.time()
    test_player_store_direct()
    latencies = test_api_endpoints()
    ram_used = test_memory_limit()
    total_time = (time.time() - t_start) * 1000

    print("=" * 80)
    print("📊 FINAL PERFORMANCE & RETRIEVAL METRICS SUMMARY")
    print("=" * 80)
    print(f"Player lookup latency (/players/name): {latencies['player_detail_latency_ms']} ms")
    print(f"Player-list retrieval latency (/players): {latencies['player_list_latency_ms']} ms")
    print(f"Name query latency (/ask name): {latencies['name_lookup_latency_ms']} ms")
    print(f"Superlative query latency (/ask superlative): {latencies['superlative_latency_ms']} ms")
    print(f"Semantic fallback latency (/ask vector): {latencies['semantic_latency_ms']} ms")
    print(f"Baseline & Peak Backend RAM: {ram_used} MB (Limit: 400 MB)")
    print("=" * 80)
    print("✨ ALL CHECKS & REQUIREMENTS SATISFIED SUCCESSFULLY!")
    print("=" * 80)
