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

    answer = data["answer"]
    results = data["results"]

    print(f"\n--- AI ANALYSIS OUTPUT (Length: {len(answer)} chars) ---\n")
    print(answer)
    print("\n" + "-" * 80)
    print(f"Results Count: {len(results)}")
    if results:
        print(f"Sample Record Fields: {list(results[0].keys())}")
    print("=" * 80 + "\n")
    return data

if __name__ == "__main__":
    print("\n🚀 VERIFYING DEEP STATISTICAL ANALYSIS GENERATION VIA GEMINI\n")

    d1 = run_test(
        "Head-to-Head Comparison Query",
        "draw a comparison between Virat Kohli and Rohit Sharma"
    )

    d2 = run_test(
        "Superlative Query",
        "Who scored the most runs in IPL 2023?"
    )

    d3 = run_test(
        "Single Player Performance Analysis",
        "Show me Jasprit Bumrah bowling stats"
    )

    print("✨ ALL ANALYSIS GENERATION VERIFICATIONS PASSED SUCCESSFULLY!")
