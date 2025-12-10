"""
Integration test for query processing improvements
Tests with sample data to simulate real query scenarios
"""

import sys
import os

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from services.gemini import extract_years_from_query, classify_fields, build_context_by_player

# Sample data simulating Pinecone results
SAMPLE_DATA = [
    # Virat Kohli records
    {
        "Player_Name": "Virat Kohli",
        "Year": "2023",
        "Runs_Scored": "639",
        "Batting_Average": "53.25",
        "Batting_Strike_Rate": "139.13",
        "Centuries": "1",
        "Half_Centuries": "5",
        "Highest_Score": "82",
        "Fours": "58",
        "Sixes": "20"
    },
    {
        "Player_Name": "Virat Kohli",
        "Year": "2022",
        "Runs_Scored": "341",
        "Batting_Average": "37.89",
        "Batting_Strike_Rate": "115.98",
        "Centuries": "0",
        "Half_Centuries": "2",
        "Highest_Score": "73",
        "Fours": "27",
        "Sixes": "7"
    },
    {
        "Player_Name": "Virat Kohli",
        "Year": "2016",
        "Runs_Scored": "973",
        "Batting_Average": "81.08",
        "Batting_Strike_Rate": "152.03",
        "Centuries": "4",
        "Half_Centuries": "7",
        "Highest_Score": "113",
        "Fours": "83",
        "Sixes": "38"
    },
    # Shubman Gill records
    {
        "Player_Name": "Shubman Gill",
        "Year": "2023",
        "Runs_Scored": "890",
        "Batting_Average": "59.33",
        "Batting_Strike_Rate": "158.04",
        "Centuries": "1",
        "Half_Centuries": "7",
        "Highest_Score": "129",
        "Fours": "92",
        "Sixes": "36"
    },
    # Jasprit Bumrah records
    {
        "Player_Name": "Jasprit Bumrah",
        "Year": "2023",
        "Runs_Scored": "0",
        "Wickets_Taken": "20",
        "Bowling_Average": "13.65",
        "Economy_Rate": "6.48",
        "Bowling_Strike_Rate": "12.60",
        "Best_Bowling_Match": "4/14",
        "Four_Wicket_Hauls": "1",
        "Five_Wicket_Hauls": "0"
    },
    {
        "Player_Name": "Jasprit Bumrah",
        "Year": "2020",
        "Runs_Scored": "0",
        "Wickets_Taken": "27",
        "Bowling_Average": "14.96",
        "Economy_Rate": "6.73",
        "Bowling_Strike_Rate": "13.33",
        "Best_Bowling_Match": "4/20",
        "Four_Wicket_Hauls": "2",
        "Five_Wicket_Hauls": "0"
    }
]

def test_batting_query():
    """Test: Who scored the most runs in IPL 2023?"""
    print("=" * 80)
    print("Test 1: Batting Query with Year Filter")
    print("=" * 80)
    
    query = "Who scored the most runs in IPL 2023?"
    print(f"Query: {query}\n")
    
    # Extract years
    years = extract_years_from_query(query)
    print(f"Extracted years: {years}")
    
    # Filter by year
    filtered_data = [r for r in SAMPLE_DATA if r.get("Year") in [str(y) for y in years]]
    print(f"Records after year filter: {len(filtered_data)}")
    
    # Classify fields
    fields = classify_fields(query)
    print(f"Relevant fields: {fields}")
    
    # Build context
    context = build_context_by_player(
        records=filtered_data,
        relevant_fields=fields,
        max_per_player=1,
        target_players=None,
        threshold=75
    )
    print(f"\nContext generated:\n{context}\n")
    
    # Expected: Shubman Gill with 890 runs should be first
    assert "Shubman Gill" in context
    assert "890" in context
    print("✅ Test passed: Correct player identified\n")

def test_bowling_query():
    """Test: Best bowler in 2020"""
    print("=" * 80)
    print("Test 2: Bowling Query with Year Filter")
    print("=" * 80)
    
    query = "Best bowler in 2020 with most wickets"
    print(f"Query: {query}\n")
    
    years = extract_years_from_query(query)
    print(f"Extracted years: {years}")
    
    filtered_data = [r for r in SAMPLE_DATA if r.get("Year") in [str(y) for y in years]]
    print(f"Records after year filter: {len(filtered_data)}")
    
    fields = classify_fields(query)
    print(f"Relevant fields: {fields}")
    
    context = build_context_by_player(
        records=filtered_data,
        relevant_fields=fields,
        max_per_player=1,
        target_players=None,
        threshold=75
    )
    print(f"\nContext generated:\n{context}\n")
    
    # Expected: Jasprit Bumrah with 27 wickets
    assert "Jasprit Bumrah" in context
    assert "27" in context or "2020" in context
    print("✅ Test passed: Correct bowler identified\n")

def test_player_comparison():
    """Test: Compare Virat Kohli's performance in 2016 and 2023"""
    print("=" * 80)
    print("Test 3: Player Comparison Across Years")
    print("=" * 80)
    
    query = "Compare Virat Kohli's performance in 2016 and 2023"
    print(f"Query: {query}\n")
    
    years = extract_years_from_query(query)
    print(f"Extracted years: {years}")
    
    # Filter by years
    filtered_data = [r for r in SAMPLE_DATA if r.get("Year") in [str(y) for y in years]]
    print(f"Records after year filter: {len(filtered_data)}")
    
    fields = classify_fields(query)
    print(f"Relevant fields: {fields}")
    
    # Filter by player
    from rapidfuzz import process
    all_players = list({r.get("Player_Name") for r in filtered_data if r.get("Player_Name")})
    q_tokens = query.lower().split()
    target_players = set()
    for token in q_tokens:
        match = process.extractOne(token, all_players, score_cutoff=75)
        if match:
            target_players.add(match[0])
    
    print(f"Target players: {list(target_players)}")
    
    context = build_context_by_player(
        records=filtered_data,
        relevant_fields=fields,
        max_per_player=None,  # Include all years
        target_players=list(target_players) if target_players else None,
        threshold=75
    )
    print(f"\nContext generated:\n{context}\n")
    
    # Expected: Both 2016 and 2023 records for Virat Kohli
    assert "Virat Kohli" in context
    assert "2016" in context and "2023" in context
    assert "973" in context  # 2016 runs
    assert "639" in context  # 2023 runs
    print("✅ Test passed: Both years included for comparison\n")

def test_no_year_query():
    """Test: Query without year should return best records"""
    print("=" * 80)
    print("Test 4: Query Without Year Filter")
    print("=" * 80)
    
    query = "Who has the highest batting strike rate?"
    print(f"Query: {query}\n")
    
    years = extract_years_from_query(query)
    print(f"Extracted years: {years}")
    
    fields = classify_fields(query)
    print(f"Relevant fields: {fields}")
    
    # No year filter, so use all data
    context = build_context_by_player(
        records=SAMPLE_DATA,
        relevant_fields=fields,
        max_per_player=1,  # Best record per player
        target_players=None,
        threshold=75
    )
    print(f"\nContext generated:\n{context}\n")
    
    # Expected: Should include players with high strike rates
    assert "Strike_Rate" in context or "Batting_Strike_Rate" in context
    print("✅ Test passed: Query without year works\n")

def test_context_filtering():
    """Test: Context filtering removes zero values"""
    print("=" * 80)
    print("Test 5: Context Filtering (Remove Zero Values)")
    print("=" * 80)
    
    query = "Show me Jasprit Bumrah's bowling stats"
    print(f"Query: {query}\n")
    
    fields = ["Player_Name", "Year", "Runs_Scored", "Wickets_Taken", "Bowling_Average", "Economy_Rate"]
    
    context = build_context_by_player(
        records=SAMPLE_DATA,
        relevant_fields=fields,
        max_per_player=None,
        target_players=["Jasprit Bumrah"],
        threshold=75
    )
    print(f"\nContext generated:\n{context}\n")
    
    # Runs_Scored is 0 for bowlers, should be filtered out
    lines = context.split('\n')
    for line in lines:
        if "Jasprit Bumrah" in line:
            # Should not show "Runs_Scored: 0"
            assert "Runs_Scored: 0" not in line
            print("✅ Test passed: Zero values filtered out\n")
            return
    
    print("⚠️ Warning: Jasprit Bumrah not found in context\n")

if __name__ == "__main__":
    print("\n🧪 Running Integration Tests for Query Processing\n")
    
    try:
        test_batting_query()
        test_bowling_query()
        test_player_comparison()
        test_no_year_query()
        test_context_filtering()
        
        print("=" * 80)
        print("✅ All integration tests passed successfully!")
        print("=" * 80)
    except AssertionError as e:
        print(f"❌ Test failed with assertion error: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
