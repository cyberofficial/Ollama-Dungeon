#!/usr/bin/env python3
"""
Test script for token info suppression
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from token_management import TokenManager
from config import TOKEN_SETTINGS
import logging

def test_token_suppression():
    """Test that token info messages can be suppressed."""
    print("=== Testing Token Info Suppression ===")
    print()
    
    # Setup logging to see output
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
    
    # Create token manager
    tm = TokenManager()
    agent_name = 'test_agent'
    
    print("--- Test 1: Normal mode (suppress_token_info = False) ---")
    print(f"Current suppress setting: {TOKEN_SETTINGS.get('suppress_token_info', False)}")
    
    # Test with normal mode
    current_tokens = 800  # 80% of 1000 starting tokens
    print(f"Testing expansion with {current_tokens} tokens (threshold = 80% of 1000 = 800)")
    was_increased, new_limit = tm.check_and_increase_token_limit(agent_name, current_tokens)
    print(f"Expansion triggered: {was_increased}, New limit: {new_limit}")
    
    # Test expansion message
    messages = [{"role": "user", "content": "test" * 200}]  # About 800 tokens
    should_expand, message = tm.should_expand_tokens(agent_name, messages)
    print(f"Should expand: {should_expand}")
    print(f"Message: '{message}'")
    print()
    
    print("--- Test 2: Suppressed mode (suppress_token_info = True) ---")
    # Temporarily modify the setting
    original_suppress = TOKEN_SETTINGS.get('suppress_token_info', False)
    TOKEN_SETTINGS['suppress_token_info'] = True
    print(f"Changed suppress setting to: {TOKEN_SETTINGS.get('suppress_token_info', False)}")
    
    # Test with another agent
    agent_name2 = 'test_agent2'
    current_tokens2 = 800  # 80% of 1000 starting tokens
    print(f"Testing expansion with {current_tokens2} tokens for {agent_name2}")
    was_increased2, new_limit2 = tm.check_and_increase_token_limit(agent_name2, current_tokens2)
    print(f"Expansion triggered: {was_increased2}, New limit: {new_limit2}")
    
    # Test expansion message
    should_expand2, message2 = tm.should_expand_tokens(agent_name2, messages)
    print(f"Should expand: {should_expand2}")
    print(f"Message: '{message2}' (should be empty)")
    
    # Restore original setting
    TOKEN_SETTINGS['suppress_token_info'] = original_suppress
    print(f"Restored suppress setting to: {TOKEN_SETTINGS.get('suppress_token_info', False)}")
    
    print()
    print("--- Test Results ---")
    print(f"Normal mode message length: {len(message)}")
    print(f"Suppressed mode message length: {len(message2)}")
    
    if len(message) > 0 and len(message2) == 0:
        print("✅ Suppression working correctly!")
    else:
        print("❌ Suppression not working as expected")
        print(f"Expected: normal message > 0 chars, suppressed = 0 chars")
        print(f"Actual: normal = {len(message)}, suppressed = {len(message2)}")
    
    print()
    print("💡 To suppress token info messages during gameplay:")
    print("   Set 'suppress_token_info': True in config.py TOKEN_SETTINGS")

if __name__ == "__main__":
    test_token_suppression()
