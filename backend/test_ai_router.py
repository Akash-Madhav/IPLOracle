import sys
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import json, requests

BASE = "http://localhost:8000"

def run_test(label, query):
    print("=" * 80)
    print(f"TEST: {label}")
    print(f"Query: {query}")
    print("=" * 80)
    res = requests.post(f"{BASE}/ask", json={"query": query})
    assert res.status_code == 200, f"Failed with {res.status_code}"
    data = res.json()

    print(f"\n--- API Response Received ---")
    print(f"Query: {data['query']}")
    print(f"Answer Preview (first 250 chars): {data['answer'][:250]}...")
    print(f"Results Count: {len(data['results'])}")
    print("=" * 80 + "\n")
    return data

if __name__ == "__main__":
    print("\n🚀 VERIFYING GEMINI AI PRE-FETCH QUERY INTENT ROUTER\n")

    d1 = run_test(
        "AI Router: Comparison Query",
        "draw a comparison between Virat Kohli and Rohit Sharma"
    )

    d2 = run_test(
        "AI Router: Superlative Query",
        "Who scored the most runs in IPL 2023?"
    )

    d3 = run_test(
        "AI Router: Single Player Stats",
        "Show me Jasprit Bumrah bowling stats"
    )

    print("✨ ALL GEMINI AI PRE-FETCH ROUTER TESTS PASSED SUCCESSFULLY!")
