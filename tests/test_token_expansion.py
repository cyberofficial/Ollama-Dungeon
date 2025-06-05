#!/usr/bin/env python3
"""
Test script for dynamic token expansion feature

This script tests the dynamic token expansion functionality to ensure:
- Agents start with the configured starting token limit
- Token limits automatically increase when reaching the threshold
- Multiple expansions work correctly in sequence
- Different agents maintain independent token limits
- Integration with compression thresholds works properly

Usage: python test_token_expansion.py

Useful for debugging token management issues or verifying configuration changes.
"""

from token_management import TokenManager
from config import TOKEN_SETTINGS

def test_dynamic_token_expansion():
    """Test the dynamic token expansion feature."""
    print("=== Testing Dynamic Token Expansion ===")
    print()
    
    # Create token manager
    tm = TokenManager()
    agent_name = 'test_agent'
    
    # Show settings
    print("Token settings:")
    print(f"Starting tokens: {TOKEN_SETTINGS['starting_tokens']}")
    print(f"Increase by: {TOKEN_SETTINGS['increase_tokens_by']}")
    print(f"Threshold: {TOKEN_SETTINGS['token_increase_threshold']}")
    print(f"Max tokens: {TOKEN_SETTINGS['max_context_tokens']}")
    print(f"Compression threshold: {TOKEN_SETTINGS['compression_threshold']}")
    print()
    
    # Test initial limit
    initial_limit = tm.get_current_token_limit(agent_name)
    print(f"Initial token limit for {agent_name}: {initial_limit}")
    print()
    
    # Test expansion at 90% of 5000 = 4500 tokens
    print("--- Test 1: Reaching 90% of initial limit (4500/5000) ---")
    current_tokens = 4500
    was_increased, new_limit = tm.check_and_increase_token_limit(agent_name, current_tokens)
    print(f"At {current_tokens} tokens: increased={was_increased}, new_limit={new_limit}")
    print()
    
    # Test another expansion at 90% of 6000 = 5400 tokens
    print("--- Test 2: Reaching 90% of increased limit (5400/6000) ---")
    current_tokens = 5400
    was_increased, new_limit = tm.check_and_increase_token_limit(agent_name, current_tokens)
    print(f"At {current_tokens} tokens: increased={was_increased}, new_limit={new_limit}")
    print()
    
    # Test multiple expansions
    print("--- Test 3: Multiple expansions in sequence ---")
    for test_tokens in [6300, 7200, 8100, 9000]:  # 90% of each new limit
        was_increased, new_limit = tm.check_and_increase_token_limit(agent_name, test_tokens)
        print(f"At {test_tokens} tokens: increased={was_increased}, new_limit={new_limit}")
    print()
      # Test when we reach compression threshold
    print("--- Test 4: Reaching compression threshold ---")
    compression_point = TOKEN_SETTINGS['compression_threshold']
    # Create a fake message list to test compression
    fake_messages = [{"role": "user", "content": "test" * (compression_point // 4)}]  # Rough token estimate
    should_compress = tm.should_compress(fake_messages)
    print(f"At ~{compression_point} tokens: should_compress={should_compress}")
    
    # Test getting current limit
    final_limit = tm.get_current_token_limit(agent_name)
    print(f"Final token limit for {agent_name}: {final_limit}")
    print()
    
    # Test with different agent
    print("--- Test 5: Different agent starts fresh ---")
    other_agent = 'other_agent'
    other_limit = tm.get_current_token_limit(other_agent)
    print(f"Token limit for {other_agent}: {other_limit}")

if __name__ == "__main__":
    test_dynamic_token_expansion()
