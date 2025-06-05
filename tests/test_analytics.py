#!/usr/bin/env python3
"""
Test script for token analytics functionality
"""

from token_management import TokenAnalytics
import os

def test_token_analytics():
    """Test the token analytics functionality."""
    print("=== Testing Token Analytics ===")
    print()
    
    # Create a test analytics instance with a temporary file
    test_file = "test_analytics.json"
    analytics = TokenAnalytics(test_file)
    
    # Test recording API calls
    print("--- Test 1: Recording API calls ---")
    analytics.record_api_call("alice", 1500)
    analytics.record_api_call("bob", 2000)
    analytics.record_api_call("alice", 1800)
    analytics.record_api_call("grix", 3000)
    
    # Test recording expansions
    print("--- Test 2: Recording token expansions ---")
    analytics.record_token_expansion("alice", 5000, 6000)
    analytics.record_token_expansion("grix", 5000, 6000)
    analytics.record_token_expansion("grix", 6000, 7000)
    
    # Test recording compressions
    print("--- Test 3: Recording compressions ---")
    analytics.record_compression("grix", 35000, 20000)
    
    # Test agent analytics
    print("--- Test 4: Agent-specific analytics ---")
    alice_stats = analytics.get_agent_analytics("alice")
    print(f"Alice stats: {alice_stats}")
    
    # Test top users
    print("--- Test 5: Top token users ---")
    top_users = analytics.get_top_token_users(3)
    for i, user in enumerate(top_users, 1):
        print(f"{i}. {user['name']}: {user['total_tokens']} tokens")
    
    # Test system summary
    print("--- Test 6: System summary ---")
    summary = analytics.get_system_summary()
    print(f"System summary: {summary}")
    
    # Test save/load
    print("--- Test 7: Save and reload ---")
    analytics.save_analytics()
    
    # Create new instance and load
    analytics2 = TokenAnalytics(test_file)
    alice_stats2 = analytics2.get_agent_analytics("alice")
    print(f"Alice stats after reload: {alice_stats2}")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"Cleaned up test file: {test_file}")
    
    print("\n✅ All analytics tests passed!")

if __name__ == "__main__":
    test_token_analytics()
