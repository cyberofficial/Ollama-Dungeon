#!/usr/bin/env python3
"""
Simple Test Runner for Ollama Dungeon
Provides easy access to the comprehensive test suite.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.testall import run_comprehensive_tests, TestAllOllamaDungeon
import unittest


def main():
    """Main test runner function."""
    print("🧪 Ollama Dungeon Test Runner")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ['all', 'comprehensive', 'full']:
            print("Running comprehensive test suite...")
            success = run_comprehensive_tests()
            sys.exit(0 if success else 1)
            
        elif command in ['quick', 'basic']:
            print("Running basic tests...")
            # Run a subset of tests for quick verification
            suite = unittest.TestSuite()
            
            # Add key tests
            suite.addTest(TestAllOllamaDungeon('test_agent_initialization'))
            suite.addTest(TestAllOllamaDungeon('test_world_controller_initialization'))
            suite.addTest(TestAllOllamaDungeon('test_room_navigation'))
            suite.addTest(TestAllOllamaDungeon('test_item_interaction'))
            suite.addTest(TestAllOllamaDungeon('test_token_manager_initialization'))
            
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            sys.exit(0 if result.wasSuccessful() else 1)
            
        elif command in ['help', '-h', '--help']:
            print_help()
            sys.exit(0)
            
        else:
            print(f"Unknown command: {command}")
            print_help()
            sys.exit(1)
    
    else:
        print("No command specified. Running comprehensive tests...")
        success = run_comprehensive_tests()
        sys.exit(0 if success else 1)


def print_help():
    """Print help information."""
    print("""
Usage: python test_runner.py [command]

Commands:
  all, comprehensive, full  - Run all tests (default)
  quick, basic             - Run basic functionality tests only
  help, -h, --help         - Show this help message

Examples:
  python test_runner.py                    # Run all tests
  python test_runner.py comprehensive      # Run all tests
  python test_runner.py quick             # Run basic tests only
  python test_runner.py help              # Show help
    """)


if __name__ == "__main__":
    main()
