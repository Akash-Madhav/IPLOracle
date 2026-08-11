import sys
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import json, requests

BASE = "http://localhost:8000"

def test_endpoint(name, method, path, payload=None):
    print("=" * 80)
    print(f"TEST: {name} [{method} {path}]")
    print("=" * 80)
    
    url = f"{BASE}{path}"
    if method == "GET":
        res = requests.get(url)
    else:
        res = requests.post(url, json=payload)

    assert res.status_code == 200, f"FAILED with status code {res.status_code}: {res.text}"
    data = res.json()

    print(f"Status: ✅ 200 OK")
    if "status" in data:
        print(f"Health Status: {data['status']}")
    if "total_players" in data:
        print(f"Total Players: {data['total_players']}")
    if "answer" in data:
        print(f"Answer Length: {len(data['answer'])} chars")
        print(f"Answer Preview: {data['answer'][:200]}...")
        print(f"Results Count: {len(data['results'])}")
    print("=" * 80 + "\n")
    return data

if __name__ == "__main__":
    print("\n🚀 RUNNING COMPLETE DEPLOYMENT READINESS TEST SUITE\n")

    # 1. Health Ping Endpoint
    t1 = test_endpoint("Health Check Endpoint", "GET", "/health")
    assert t1.get("status") == "ok", "Health status must be 'ok'"
    assert t1.get("database_loaded") is True, "Database must be loaded"

    # 2. Player List Endpoint
    t2 = test_endpoint("Get All Players", "GET", "/players")
    assert t2.get("total_players") > 200, "Should have 200+ players"

    # 3. Direct Player Lookup Endpoint
    t3 = test_endpoint("Direct Player Detail Lookup", "GET", "/players/Virat%20Kohli")
    assert t3.get("player_name") == "Virat Kohli", "Should return canonical player name"
    assert t3.get("total_records") == 17, "Kohli should have 17 records"

    # 4. Comparison Query via AI Router & Gemini Analysis
    t4 = test_endpoint(
        "AI Router Player Comparison Query", 
        "POST", 
        "/ask", 
        {"query": "draw a comparison between Virat Kohli and Rohit Sharma"}
    )
    assert len(t4.get("results")) == 34, f"Expected 34 records, got {len(t4.get('results'))}"

    # 5. Superlative Ranking Query
    t5 = test_endpoint(
        "AI Router Superlative Query", 
        "POST", 
        "/ask", 
        {"query": "Who scored the most runs in IPL 2023?"}
    )
    assert len(t5.get("results")) == 30, f"Expected 30 results, got {len(t5.get('results'))}"

    print("✨ ALL 5 DEPLOYMENT READINESS TESTS PASSED SUCCESSFULLY!")
    print("🎉 DEPLOYMENT APPROVAL: 100% READY FOR PRODUCTION DEPLOYMENT!")
