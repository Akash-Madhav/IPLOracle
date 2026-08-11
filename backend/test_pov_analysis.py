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

    print(f"\n--- AI POV EVALUATION OUTPUT (Length: {len(answer)} chars) ---\n")
    print(answer)
    print("\n" + "-" * 80)
    print(f"Results Count: {len(results)}")
    
    # Verify no raw markdown tables in answer
    has_tables = "| ---" in answer or "|---" in answer or "| :-" in answer
    print(f"Contains Raw Table Dump: {has_tables} (Should be False)")
    assert not has_tables, "Answer should contain narrative POV, not raw tables"
    print("=" * 80 + "\n")
    return data

if __name__ == "__main__":
    print("\n🚀 VERIFYING EXPERT AI ANALYST POV & NARRATIVE GENERATION\n")

    d1 = run_test(
        "Virat Kohli vs Rohit Sharma Comparison POV",
        "draw a comparison between Virat Kohli and Rohit Sharma"
    )

    d2 = run_test(
        "Shubman Gill 2023 Season Analyst POV",
        "Who scored the most runs in IPL 2023?"
    )

    print("✨ ALL POV ANALYST GENERATION TESTS PASSED SUCCESSFULLY!")
