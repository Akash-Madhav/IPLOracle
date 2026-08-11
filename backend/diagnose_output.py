import sys
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import json, requests
from collections import defaultdict

BASE = "http://localhost:8000"

def test_query(label, query):
    print("=" * 80)
    print(f"TEST: {label}")
    print(f"Query: {query}")
    print("=" * 80)
    res = requests.post(f"{BASE}/ask", json={"query": query})
    data = res.json()

    answer = data["answer"]
    results = data["results"]

    # Check if answer is raw context fallback
    is_fallback = answer.startswith("Based on the available data:")
    print(f"Answer type: {'RAW CONTEXT FALLBACK' if is_fallback else 'GEMINI GENERATED'}")
    print(f"Answer (first 300 chars): {answer[:300]}")
    print()

    # Results analysis
    by_player = defaultdict(list)
    for r in results:
        by_player[r.get("Player_Name", "?")].append(r.get("Year", "?"))

    print(f"Results count: {len(results)}")
    print("Players and years in results:")
    for p, years in sorted(by_player.items()):
        print(f"  {p}: {sorted(years)} ({len(years)} records)")

    # Check for missing fields (fields with None or 0 values being returned)
    if results:
        sample = results[0]
        zero_fields = [k for k, v in sample.items() if v in (None, "0", 0, "")]
        print(f"\nSample record zero/null fields: {zero_fields}")
    print()
    return data


# Import player store for completeness checks
sys.path.insert(0, ".")
from services.player_store import player_store
player_store.load("data/ipl_players.csv")

print("\n" + "=" * 80)
print("DIAGNOSTIC: Backend Query Output Verification")
print("=" * 80 + "\n")

# Test 1: Comparison (what user tried)
d1 = test_query(
    "Player Comparison",
    "draw a comparison between Virat Kohli and Rohit Sharma"
)

# Verify completeness
kohli_store = player_store.get_player_records("Virat Kohli")
rohit_store = player_store.get_player_records("Rohit Sharma")
kohli_results = [r for r in d1["results"] if r.get("Player_Name") == "Virat Kohli"]
rohit_results = [r for r in d1["results"] if r.get("Player_Name") == "Rohit Sharma"]
print(f"COMPLETENESS CHECK:")
print(f"  Kohli: store has {len(kohli_store)} records, API returned {len(kohli_results)} records")
print(f"  Rohit: store has {len(rohit_store)} records, API returned {len(rohit_results)} records")
print(f"  Missing Kohli years: {set(r['Year'] for r in kohli_store) - set(r.get('Year') for r in kohli_results)}")
print(f"  Missing Rohit years: {set(r['Year'] for r in rohit_store) - set(r.get('Year') for r in rohit_results)}")
print()

# Test 2: Superlative
d2 = test_query(
    "Superlative Query",
    "Who scored the most runs in IPL 2023?"
)

# Check if correct top scorer
if d2["results"]:
    top = d2["results"][0]
    print(f"TOP SCORER CHECK: {top.get('Player_Name')} with {top.get('Runs_Scored')} runs")
    print(f"  Expected: Shubman Gill with 890 runs")
    print(f"  CORRECT: {top.get('Player_Name') == 'Shubman Gill' and top.get('Runs_Scored') == '890'}")
print()

# Test 3: Single player stats
d3 = test_query(
    "Single Player Stats",
    "Show me Jasprit Bumrah bowling stats"
)
bumrah_store = player_store.get_player_records("Jasprit Bumrah")
bumrah_results = [r for r in d3["results"] if r.get("Player_Name") == "Jasprit Bumrah"]
print(f"COMPLETENESS: store={len(bumrah_store)} records, API={len(bumrah_results)} records")
print()

# Test 4: Generic semantic query (no player name)
d4 = test_query(
    "Generic Semantic Query (no player name)",
    "Best economy rate bowler in death overs"
)

# Test 5: Year-specific without player
d5 = test_query(
    "Year-specific without player",
    "Most sixes in IPL 2024"
)

# Test 6: Check context building for comparison
print("=" * 80)
print("CONTEXT BUILDING ANALYSIS")
print("=" * 80)
from services.gemini import classify_fields, build_context_by_player, identify_primary_stat

query = "draw a comparison between Virat Kohli and Rohit Sharma"
fields = classify_fields(query)
primary_stat = identify_primary_stat(query, fields)
print(f"Query: {query}")
print(f"Classified fields: {fields}")
print(f"Primary stat: {primary_stat}")

# Get all records for both players
all_recs = kohli_store + rohit_store
context = build_context_by_player(
    records=all_recs,
    relevant_fields=fields,
    max_per_player=5,
    target_players=["Virat Kohli", "Rohit Sharma"],
    threshold=75
)
print(f"Context (max_per_player=5):")
print(context)
print(f"\nContext lines: {len(context.splitlines())}")
print(f"Context length: {len(context)} chars")

# Now try without max_per_player limit
context_full = build_context_by_player(
    records=all_recs,
    relevant_fields=fields,
    max_per_player=None,
    target_players=["Virat Kohli", "Rohit Sharma"],
    threshold=75
)
print(f"\nContext (max_per_player=None):")
print(context_full)
print(f"\nContext lines: {len(context_full.splitlines())}")
print(f"Context length: {len(context_full)} chars")

print("\n" + "=" * 80)
print("SUMMARY OF ISSUES FOUND")
print("=" * 80)
issues = []
if len(kohli_results) < len(kohli_store):
    issues.append(f"1. INCOMPLETE RECORDS: Kohli has {len(kohli_store)} records but API returned only {len(kohli_results)} (results capped at 20 total)")
if len(rohit_results) < len(rohit_store):
    issues.append(f"2. INCOMPLETE RECORDS: Rohit has {len(rohit_store)} records but API returned only {len(rohit_results)}")
if d1["answer"].startswith("Based on the available data:"):
    issues.append("3. GEMINI FALLBACK: Answer is raw context dump instead of natural language (Gemini API may be rate-limited or failing)")
issues.append("4. CONTEXT TRUNCATION: max_per_player=5 drops records when player has 17 seasons")
issues.append("5. RESULT CAP: results[:20] in ask.py caps total returned records")
issues.append("6. REDUNDANT FIELDS IN CONTEXT: 'Player_Name: Virat Kohli' appears when line already starts with 'Virat Kohli |'")

for issue in issues:
    print(f"  {issue}")
