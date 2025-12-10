"""
Test for superlative query detection and handling
This test validates the fix for the query retrieval inconsistency issue
"""

import sys
import os

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from services.gemini import is_superlative_query

def test_superlative_detection():
    """Test detection of superlative queries"""
    print("=" * 80)
    print("Testing Superlative Query Detection")
    print("=" * 80)
    
    test_cases = [
        # Should be detected as superlative (True)
        ("Who scored the most runs in IPL 2023?", True),
        ("Who scored the highest runs?", True),
        ("Best bowler in 2020", True),
        ("Top scorer in IPL 2023", True),
        ("Who took the most wickets?", True),
        ("Player with best strike rate", True),
        ("Who had the lowest economy rate?", True),
        ("Top 5 run scorers", True),
        ("Who scored more runs?", True),
        ("Better player between X and Y", True),
        ("Who has the highest average?", True),
        ("Leading wicket taker", True),
        ("Most sixes hit by a player", True),
        ("Greatest run scorer", True),
        ("Who scored the fewest runs?", True),
        
        # Should NOT be detected as superlative (False)
        ("Virat Kohli stats in 2023", False),
        ("Show me Rohit Sharma's performance", False),
        ("Mumbai Indians team statistics", False),
        ("IPL 2023 season overview", False),
        ("Compare Virat and Rohit", False),  # This could be debatable
    ]
    
    passed = 0
    failed = 0
    
    for i, (query, expected) in enumerate(test_cases, 1):
        result = is_superlative_query(query)
        
        print(f"\nTest {i}:")
        print(f"  Query: {query}")
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

def test_issue_scenario():
    """
    Test the specific scenario from the GitHub issue:
    Query 1: "Who scored the most runs in IPL 2023?" should detect superlative
    Query 2: "Yashasvi Jaiswal or Shubman Gill who scored higher in IPL 2023?" should detect superlative
    """
    print("\n" + "=" * 80)
    print("Testing GitHub Issue Scenario")
    print("=" * 80)
    
    query1 = "Who scored the most runs in IPL 2023?"
    query2 = "Yashasvi Jaiswal or Shubman Gill who scored higher in IPL 2023?"
    
    result1 = is_superlative_query(query1)
    result2 = is_superlative_query(query2)
    
    print(f"\nQuery 1: {query1}")
    print(f"  Superlative detected: {result1}")
    print(f"  Expected: True")
    print(f"  Status: {'✅ PASS' if result1 else '❌ FAIL'}")
    
    print(f"\nQuery 2: {query2}")
    print(f"  Superlative detected: {result2}")
    print(f"  Expected: True")
    print(f"  Status: {'✅ PASS' if result2 else '❌ FAIL'}")
    
    print("\n" + "=" * 80)
    
    return result1 and result2

if __name__ == "__main__":
    print("\n🧪 Testing Superlative Query Detection for Issue Fix\n")
    
    try:
        detection_success = test_superlative_detection()
        issue_success = test_issue_scenario()
        
        if detection_success and issue_success:
            print("\n✅ All tests passed!")
            sys.exit(0)
        else:
            print("\n⚠️ Some tests failed")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
