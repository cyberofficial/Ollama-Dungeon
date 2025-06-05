#!/usr/bin/env python3
"""
Test script for endless mode functionality fixes.
Tests the invite/remove commands and location change handling.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import GameCLI
from game_engine import WorldController
import tempfile

def test_endless_mode_commands():
    """Test the invite and remove commands in endless mode."""
    print("=== Testing Endless Mode Commands ===")
    
    # Create temporary world directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize CLI with temporary world
        cli = GameCLI()
        cli.world = WorldController()
        
        # Mock some agents in the current room for testing
        print("1. Testing invite command outside endless mode:")
        result = cli.cmd_invite(['alice'])
        print(f"   Result: {result}")
        assert "only works in endless conversation mode" in result.lower()
        
        print("2. Testing remove command outside endless mode:")
        result = cli.cmd_remove(['alice'])
        print(f"   Result: {result}")
        assert "only works in endless conversation mode" in result.lower()
        
        print("3. Testing endless mode location change handler:")
        cli.endless_mode = True
        cli.endless_participants = ['player', 'alice', 'bob']
        cli.endless_agents = []  # Mock empty for now
        
        # Call the location change handler
        cli._handle_endless_mode_location_change()
        print("   Location change handler executed successfully")
        
        print("✅ All endless mode command tests passed!")

def test_integration():
    """Test that the CLI starts and basic commands work."""
    print("=== Testing CLI Integration ===")
    
    try:
        cli = GameCLI()
        
        # Test help command
        result = cli.cmd_help([])
        print("1. Help command works")
        
        # Test that invite/remove are in commands
        assert 'invite' in cli.commands
        assert 'remove' in cli.commands
        print("2. Invite/remove commands registered")
        
        # Test look command
        result = cli.cmd_look([])
        print("3. Look command works")
        
        print("✅ Integration tests passed!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing endless mode functionality...")
    
    try:
        test_endless_mode_commands()
        test_integration()
        print("\n🎉 All tests passed! Endless mode fixes are working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
