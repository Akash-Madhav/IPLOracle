"""
Test for identify_primary_stat function
"""

import sys
import os

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from services.gemini import identify_primary_stat

def test_primary_stat_identification():
    print("=" * 80)
    print("Testing Primary Stat Identification")
    print("=" * 80)
    
    test_cases = [
        {
            "query": "Who scored the most runs in IPL 2023?",
            "fields": ["Player_Name", "Year", "Runs_Scored", "Batting_Average"],
            "expected": "Runs_Scored"
        },
        {
            "query": "Player with best strike rate",
            "fields": ["Player_Name", "Year", "Batting_Strike_Rate", "Runs_Scored"],
            "expected": "Batting_Strike_Rate"
        },
        {
            "query": "Most wickets taken in 2020",
            "fields": ["Player_Name", "Year", "Wickets_Taken", "Economy_Rate"],
            "expected": "Wickets_Taken"
        },
        {
            "query": "Best economy rate bowler",
            "fields": ["Player_Name", "Year", "Economy_Rate", "Wickets_Taken"],
            "expected": "Economy_Rate"
        },
        {
            "query": "Who hit the most sixes?",
            "fields": ["Player_Name", "Year", "Sixes", "Runs_Scored"],
            "expected": "Sixes"
        },
        {
            "query": "Highest batting average",
            "fields": ["Player_Name", "Year", "Batting_Average", "Runs_Scored"],
            "expected": "Batting_Average"
        },
        {
            "query": "Most centuries scored",
            "fields": ["Player_Name", "Year", "Centuries", "Half_Centuries"],
            "expected": "Centuries"
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        query = test["query"]
        fields = test["fields"]
        expected = test["expected"]
        
        result = identify_primary_stat(query, fields)
        
        print(f"\nTest {i}:")
        print(f"  Query: {query}")
        print(f"  Fields: {fields}")
        print(f"  Expected: {expected}")
        print(f"  Got: {result}")
        
        if result == expected:
            print(f"  ✅ PASS")
            passed += 1
        else:
            print(f"  ❌ FAIL")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    return failed == 0

if __name__ == "__main__":
    print("\n🧪 Testing Primary Stat Identification\n")
    
    try:
        success = test_primary_stat_identification()
        if success:
            print("\n✅ All tests passed!")
        else:
            print("\n⚠️ Some tests failed")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
