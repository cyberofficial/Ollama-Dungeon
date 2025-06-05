#!/usr/bin/env python3
"""
Test script for token info suppression functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from token_management import TokenManager
import config

def test_token_suppression():
    """Test that token info messages can be suppressed."""
    print("=== Testing Token Info Suppression ===")
    print()
    
    tm = TokenManager()
    
    # Test 1: Normal mode (messages should show)
    print("--- Test 1: Normal mode (suppress_token_info = False) ---")
    
    # Reset config to normal mode
    config.TOKEN_SETTINGS['suppress_token_info'] = False
    print(f"Current suppress setting: {config.TOKEN_SETTINGS['suppress_token_info']}")
    
    # Reset agent's token limit to starting value
    agent_name = "test_agent"
    tm.agent_token_limits[agent_name] = config.TOKEN_SETTINGS['starting_tokens']
    starting_limit = tm.get_current_token_limit(agent_name)
    print(f"Reset {agent_name} token limit to: {starting_limit}")
    
    # Create fake messages that exceed 80% threshold
    threshold_tokens = int(starting_limit * config.TOKEN_SETTINGS['token_increase_threshold'])
    print(f"Threshold for expansion: {threshold_tokens} tokens")
    
    # Create messages that will trigger expansion
    fake_messages = [
        {"role": "system", "content": "test" * (threshold_tokens // 4)},
        {"role": "user", "content": "test" * (threshold_tokens // 4)}
    ]
    
    # Test should_expand_tokens
    should_expand1, message1 = tm.should_expand_tokens(agent_name, fake_messages)
    print(f"Should expand: {should_expand1}")
    print(f"Message: '{message1}'")
    
    # Test 2: Suppressed mode (messages should be hidden)
    print("\n--- Test 2: Suppressed mode (suppress_token_info = True) ---")
    
    # Change to suppressed mode
    config.TOKEN_SETTINGS['suppress_token_info'] = True
    print(f"Changed suppress setting to: {config.TOKEN_SETTINGS['suppress_token_info']}")
    
    # Reset another agent's token limit
    agent_name2 = "test_agent2"
    tm.agent_token_limits[agent_name2] = config.TOKEN_SETTINGS['starting_tokens']
    starting_limit2 = tm.get_current_token_limit(agent_name2)
    print(f"Reset {agent_name2} token limit to: {starting_limit2}")
    
    # Test should_expand_tokens in suppressed mode
    should_expand2, message2 = tm.should_expand_tokens(agent_name2, fake_messages)
    print(f"Should expand: {should_expand2}")
    print(f"Message: '{message2}' (should be empty)")
    
    # Restore normal mode
    config.TOKEN_SETTINGS['suppress_token_info'] = False
    print(f"Restored suppress setting to: {config.TOKEN_SETTINGS['suppress_token_info']}")
    
    # Test Results
    print("\n--- Test Results ---")
    print(f"Normal mode message length: {len(message1)}")
    print(f"Suppressed mode message length: {len(message2)}")
    
    if len(message1) > 0 and len(message2) == 0:
        print("✅ Suppression working correctly!")
        print("   Normal mode: Shows expansion messages")
        print("   Suppressed mode: Hides expansion messages")
    else:
        print("❌ Suppression not working as expected")
        print(f"Expected: normal message > 0 chars, suppressed = 0 chars")
        print(f"Actual: normal = {len(message1)}, suppressed = {len(message2)}")
    
    print(f"\n💡 To suppress token info messages during gameplay:")
    print(f"   Set 'suppress_token_info': True in config.py TOKEN_SETTINGS")

if __name__ == "__main__":
    test_token_suppression()
