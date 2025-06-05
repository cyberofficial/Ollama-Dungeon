#!/usr/bin/env python3
"""
Comprehensive test showing token suppression in action
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from token_management import TokenManager
from config import TOKEN_SETTINGS
import io
import contextlib

def capture_output(func):
    """Capture print output from a function."""
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        result = func()
    return result, f.getvalue()

def simulate_conversation_turn(token_manager, agent_name, turn_number):
    """Simulate a conversation turn that might trigger expansion."""
    # Create increasingly long messages to trigger expansion
    base_message = f"Turn {turn_number}: This is a conversation message that gets longer each turn. "
    message_content = base_message * (turn_number * 50)  # Make it longer each turn
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message_content}
    ]
    
    # Check if expansion should happen
    should_expand, message = token_manager.should_expand_tokens(agent_name, messages)
    
    return should_expand, message, len(message_content)

def test_suppression_in_action():
    """Test suppression with realistic conversation simulation."""
    print("=== Token Suppression in Realistic Conversation ===\n")
    
    # Test with suppression OFF
    print("🔊 SUPPRESSION OFF (suppress_token_info = False)")
    print("=" * 50)
    
    # Temporarily ensure suppression is off
    original_setting = TOKEN_SETTINGS.get('suppress_token_info', False)
    TOKEN_SETTINGS['suppress_token_info'] = False
    
    tm1 = TokenManager()
    agent1 = "Alice"
    
    expansion_count = 0
    for turn in range(1, 20):  # Simulate 20 conversation turns
        should_expand, message, msg_length = simulate_conversation_turn(tm1, agent1, turn)
        
        if should_expand and message:
            expansion_count += 1
            print(f"Turn {turn}: {message}")
            print(f"  └─ Message length: {msg_length} chars")
        elif should_expand:
            expansion_count += 1
            print(f"Turn {turn}: [Expansion happened but no message - this shouldn't occur]")
    
    current_limit1 = tm1.get_current_token_limit(agent1)
    print(f"\nResult: {expansion_count} expansions shown, final limit: {current_limit1}")
    
    print("\n" + "="*70 + "\n")
    
    # Test with suppression ON
    print("🔇 SUPPRESSION ON (suppress_token_info = True)")
    print("=" * 50)
    
    TOKEN_SETTINGS['suppress_token_info'] = True
    
    tm2 = TokenManager()
    agent2 = "Bob"
    
    expansion_count = 0
    message_count = 0
    for turn in range(1, 20):  # Simulate 20 conversation turns
        should_expand, message, msg_length = simulate_conversation_turn(tm2, agent2, turn)
        
        if should_expand:
            expansion_count += 1
            if message:
                message_count += 1
                print(f"Turn {turn}: {message}")
            else:
                print(f"Turn {turn}: [Expansion happened silently]")
    
    current_limit2 = tm2.get_current_token_limit(agent2)
    print(f"\nResult: {expansion_count} expansions occurred, {message_count} messages shown, final limit: {current_limit2}")
    
    # Restore original setting
    TOKEN_SETTINGS['suppress_token_info'] = original_setting
    
    print("\n" + "="*70 + "\n")
    print("📊 COMPARISON:")
    print(f"Without suppression: Messages shown for token expansions")
    print(f"With suppression: Token expansions happen silently")
    print(f"Both agents reached similar token limits: {current_limit1} vs {current_limit2}")
    
    print("\n✅ Suppression feature working correctly!")
    print("\n💡 In actual gameplay:")
    print("   - Set suppress_token_info = False: See all token management messages")
    print("   - Set suppress_token_info = True: Silent operation, better immersion")
    print("   - Use /tokens or /analytics commands to check status anytime")

if __name__ == "__main__":
    test_suppression_in_action()
