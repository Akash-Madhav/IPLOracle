"""
Test script for query processing improvements
Tests the new features: year extraction, field classification, and context building
"""

import sys
import os

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from services.gemini import extract_years_from_query, classify_fields, build_context_by_player

def test_year_extraction():
    """Test year extraction from various queries"""
    print("=" * 60)
    print("Testing Year Extraction")
    print("=" * 60)
    
    test_cases = [
        "Who scored the most runs in IPL 2023?",
        "Compare Virat Kohli's performance in 2016 and 2023",
        "Best bowler in 2020",
        "Who had the highest strike rate?",  # No year
        "Show me stats from 2018, 2019 and 2020",
    ]
    
    for query in test_cases:
        years = extract_years_from_query(query)
        print(f"Query: {query}")
        print(f"Extracted years: {years}")
        print()

def test_field_classification():
    """Test field classification for various query types"""
    print("=" * 60)
    print("Testing Field Classification")
    print("=" * 60)
    
    test_cases = [
        "Who scored the most runs in IPL 2023?",
        "Best bowler with most wickets",
        "Highest strike rate batsman",
        "Most catches taken by a fielder",
        "Player with best economy rate",
        "Who hit the most sixes?",
    ]
    
    for query in test_cases:
        fields = classify_fields(query)
        print(f"Query: {query}")
        print(f"Classified fields: {fields}")
        print()

def test_context_building():
    """Test context building with sample records"""
    print("=" * 60)
    print("Testing Context Building")
    print("=" * 60)
    
    # Sample records
    sample_records = [
        {
            "Player_Name": "Virat Kohli",
            "Year": "2023",
            "Runs_Scored": "639",
            "Batting_Average": "53.25",
            "Batting_Strike_Rate": "139.13",
            "Centuries": "1",
            "Half_Centuries": "5"
        },
        {
            "Player_Name": "Virat Kohli",
            "Year": "2022",
            "Runs_Scored": "341",
            "Batting_Average": "37.89",
            "Batting_Strike_Rate": "115.98",
            "Centuries": "0",
            "Half_Centuries": "2"
        },
        {
            "Player_Name": "Rohit Sharma",
            "Year": "2023",
            "Runs_Scored": "332",
            "Batting_Average": "33.20",
            "Batting_Strike_Rate": "150.68",
            "Centuries": "0",
            "Half_Centuries": "3"
        }
    ]
    
    relevant_fields = ["Player_Name", "Year", "Runs_Scored", "Batting_Average", "Batting_Strike_Rate"]
    
    # Test 1: All records
    print("Test 1: Include all records")
    context = build_context_by_player(
        records=sample_records,
        relevant_fields=relevant_fields,
        max_per_player=None,
        target_players=None,
        threshold=80
    )
    print(context)
    print()
    
    # Test 2: Limit to 1 record per player
    print("Test 2: Max 1 record per player (should show best year)")
    context = build_context_by_player(
        records=sample_records,
        relevant_fields=relevant_fields,
        max_per_player=1,
        target_players=None,
        threshold=80
    )
    print(context)
    print()
    
    # Test 3: Filter by specific player
    print("Test 3: Filter by specific player (Virat Kohli)")
    context = build_context_by_player(
        records=sample_records,
        relevant_fields=relevant_fields,
        max_per_player=None,
        target_players=["Virat Kohli"],
        threshold=80
    )
    print(context)
    print()

if __name__ == "__main__":
    print("\n🧪 Testing Query Processing Improvements\n")
    
    try:
        test_year_extraction()
        test_field_classification()
        test_context_building()
        
        print("=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
