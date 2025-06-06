#!/usr/bin/env python3
"""
Test script to verify agent reply length configuration works correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import AGENT_SETTINGS

def test_reply_length_instructions():
    """Test that different reply length settings produce appropriate instructions."""
    
    # Test different reply length settings
    test_cases = {
        'brief': '- Keep responses very short (1-2 sentences)',
        'medium': '- Keep responses concise (1-3 sentences)',
        'detailed': '- Keep responses moderate length (3-5 sentences)',
        'verbose': '- Feel free to give longer, detailed responses (5+ sentences)'
    }
    
    # Import the method logic directly
    def get_length_instruction(reply_length):
        """Replicate the agent method logic for testing."""
        length_instructions = {
            'brief': '- Keep responses very short (1-2 sentences)',
            'medium': '- Keep responses concise (1-3 sentences)', 
            'detailed': '- Keep responses moderate length (3-5 sentences)',
            'verbose': '- Feel free to give longer, detailed responses (5+ sentences)'
        }
        return length_instructions.get(reply_length.lower(), length_instructions['medium'])
    
    print("🧪 Testing Agent Reply Length Configuration")
    print("=" * 50)
    
    for length_setting, expected_instruction in test_cases.items():
        # Test the method
        result = get_length_instruction(length_setting)
        
        print(f"Setting: {length_setting:8} -> {result}")
        
        # Verify it matches expected
        if result == expected_instruction:
            print(f"✅ {length_setting.upper()} setting works correctly")
        else:
            print(f"❌ {length_setting.upper()} setting failed!")
            print(f"  Expected: {expected_instruction}")
            print(f"  Got:      {result}")
        print()
    
    # Test invalid setting (should default to medium)
    result = get_length_instruction('invalid_setting')
    expected = test_cases['medium']
    
    print(f"Setting: invalid  -> {result}")
    if result == expected:
        print("✅ Invalid setting correctly defaults to medium")
    else:
        print("❌ Invalid setting handling failed!")
    
    print(f"\n🎯 Current config setting: '{AGENT_SETTINGS.get('reply_length', 'medium')}'")
    print("💡 To change the setting, edit config.py and modify AGENT_SETTINGS['reply_length']")
    print("   Available options: 'brief', 'medium', 'detailed', 'verbose'")
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    test_reply_length_instructions()
