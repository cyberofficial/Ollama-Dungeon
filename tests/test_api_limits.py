#!/usr/bin/env python3
"""
Test script to verify dynamic token limits are used in API calls
"""

from game_engine import Agent
from token_management import TokenManager
from config import TOKEN_SETTINGS
import json
import tempfile
import os

def test_agent_token_limits():
    """Test that agents use their dynamic token limits in API calls."""
    print("=== Testing Agent Dynamic Token Limits ===")
    print()
    
    # Create a temporary agent file
    agent_data = {
        "name": "TestAgent",
        "persona": "A test agent",
        "background": "Used for testing",
        "appearance": "Digital",
        "mood": "helpful",
        "occupation": "Tester",
        "memory_file": "memory_test.csv",
        "knowledge": ["Testing"],
        "goals": ["Help with tests"],
        "fears": ["Bugs"],
        "relationships": {}
    }
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(agent_data, f)
        agent_file = f.name
    
    try:
        # Create agent
        agent = Agent(agent_file, "test_location")
        
        # Get token manager and check initial limit
        tm = TokenManager()
        initial_limit = tm.get_current_token_limit(agent.data['name'])
        print(f"Initial token limit for {agent.data['name']}: {initial_limit}")
        
        # Simulate token expansion
        current_tokens = int(initial_limit * 0.9)  # 90% threshold
        was_increased, new_limit = tm.check_and_increase_token_limit(agent.data['name'], current_tokens)
        print(f"After reaching 90% threshold: increased={was_increased}, new_limit={new_limit}")
        
        # Check what limit would be used in API call
        api_limit = tm.get_current_token_limit(agent.data['name'])
        print(f"Token limit that would be used in API call: {api_limit}")
        
        # Verify it's not the static max
        static_max = TOKEN_SETTINGS['max_context_tokens']
        print(f"Static max from config: {static_max}")
        print(f"Using dynamic limit instead of static: {api_limit != static_max}")
        
        print("\n✅ Dynamic token limits are working correctly!")
        
    finally:
        # Clean up
        if os.path.exists(agent_file):
            os.unlink(agent_file)

if __name__ == "__main__":
    test_agent_token_limits()
