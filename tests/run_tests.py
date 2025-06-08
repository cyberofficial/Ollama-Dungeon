#!/usr/bin/env python3
"""
Ollama Dungeon Test Runner
Runs all tests with detailed reporting and performance metrics.
Now uses the comprehensive testall.py for all testing.
"""

import unittest
import sys
import os
import time
import argparse
from io import StringIO
from colorama import init, Fore, Style
from typing import Dict, List, Any, Optional

# Initialize colorama
init()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the comprehensive test suite
from tests.testall import TestAllOllamaDungeon, run_comprehensive_tests

class ColoredTextTestResult(unittest.TextTestResult):
    """Custom test result with colored output."""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_times = {}
        self.current_test_start = None
        self.verbosity = verbosity  # Store verbosity as instance variable
    
    def startTest(self, test):
        super().startTest(test)
        self.current_test_start = time.time()
        if self.verbosity > 1:
            self.stream.write(f"{Fore.CYAN}Running: {test._testMethodName}{Style.RESET_ALL}\n")
    
    def stopTest(self, test):
        super().stopTest(test)
        if self.current_test_start:
            duration = time.time() - self.current_test_start
            self.test_times[str(test)] = duration
    
    def addSuccess(self, test):
        super().addSuccess(test)
        if self.verbosity > 1:
            duration = self.test_times.get(str(test), 0)
            self.stream.write(f"{Fore.GREEN}✅ PASS: {test._testMethodName} ({duration:.3f}s){Style.RESET_ALL}\n")
    
    def addError(self, test, err):
        super().addError(test, err)
        if self.verbosity > 1:
            duration = self.test_times.get(str(test), 0)
            self.stream.write(f"{Fore.RED}❌ ERROR: {test._testMethodName} ({duration:.3f}s){Style.RESET_ALL}\n")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        if self.verbosity > 1:
            duration = self.test_times.get(str(test), 0)
            self.stream.write(f"{Fore.YELLOW}❌ FAIL: {test._testMethodName} ({duration:.3f}s){Style.RESET_ALL}\n")

class ColoredTextTestRunner(unittest.TextTestRunner):
    """Custom test runner with colored output."""
    
    def __init__(self, verbosity=2, **kwargs):
        super().__init__(verbosity=verbosity, **kwargs)
        self.resultclass = ColoredTextTestResult
        self.verbosity = verbosity  # Store verbosity for use in run method
    
    def run(self, test):
        """Run tests with timing and colored output."""
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🚀 OLLAMA DUNGEON TEST SUITE{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        start_time = time.time()
        result = super().run(test)
        end_time = time.time()
        
        # Print summary
        total_tests = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        successes = total_tests - failures - errors
        duration = end_time - start_time
        
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}TEST SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"Total Tests: {total_tests}")
        print(f"{Fore.GREEN}Passed: {successes}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Failed: {failures}{Style.RESET_ALL}")
        print(f"{Fore.RED}Errors: {errors}{Style.RESET_ALL}")
        print(f"Duration: {duration:.2f} seconds")
          # Check if our custom result class has test_times
        if hasattr(result, 'test_times'):
            test_times = getattr(result, 'test_times', {})
            if test_times:
                slowest_tests = sorted(test_times.items(), key=lambda x: x[1], reverse=True)[:5]
                if slowest_tests:
                    print(f"\n{Fore.YELLOW}⏰ Slowest Tests:{Style.RESET_ALL}")
                    for test_name, test_time in slowest_tests:
                        print(f"  {test_time:.3f}s - {test_name}")
        
        success_rate = (successes / total_tests * 100) if total_tests > 0 else 0
        color = Fore.GREEN if success_rate >= 90 else Fore.YELLOW if success_rate >= 70 else Fore.RED
        print(f"\n{color}Success Rate: {success_rate:.1f}%{Style.RESET_ALL}")
        
        if failures > 0:
            print(f"\n{Fore.RED}FAILED TESTS:{Style.RESET_ALL}")
            for test, traceback in result.failures:
                print(f"{Fore.RED}❌ {test}{Style.RESET_ALL}")
                if self.verbosity > 1:
                    error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0] if 'AssertionError: ' in traceback else "Unknown assertion error"
                    print(f"   {error_msg}")
        
        if errors > 0:
            print(f"\n{Fore.RED}ERROR TESTS:{Style.RESET_ALL}")
            for test, traceback in result.errors:
                print(f"{Fore.RED}⚠️  {test}{Style.RESET_ALL}")
                if self.verbosity > 1:
                    error_lines = traceback.split('\n')
                    error_msg = error_lines[-2] if len(error_lines) > 1 and error_lines[-2].strip() else 'Unknown error'
                    print(f"   {error_msg}")
        
        return result

def discover_tests(test_dir: Optional[str] = None) -> unittest.TestSuite:
    """Discover all test files."""
    if test_dir is None:
        test_dir = os.path.dirname(os.path.abspath(__file__))
    
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    return suite

def run_specific_test_file(test_file: str, verbosity: int = 2):
    """Run a specific test file."""
    print(f"{Fore.CYAN}Running tests from: {test_file}{Style.RESET_ALL}")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_file)
    
    runner = ColoredTextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_test_category(category: str, verbosity: int = 2):
    """Run tests from a specific category."""
    test_files = {
        'agents': 'test_agents',
        'tokens': 'test_token_management', 
        'integration': 'test_integration',
        'ultimate': 'test_ultimate'
    }
    
    if category not in test_files:
        print(f"{Fore.RED}Unknown test category: {category}{Style.RESET_ALL}")
        print(f"Available categories: {', '.join(test_files.keys())}")
        return False
    
    return run_specific_test_file(test_files[category], verbosity)

def check_prerequisites():
    """Check if all prerequisites are met for testing."""
    print(f"{Fore.CYAN}🔍 Checking Prerequisites...{Style.RESET_ALL}")
    
    issues = []
    
    # Check Python packages
    required_packages = ['colorama', 'requests', 'unittest']
    for package in required_packages:
        try:
            __import__(package)
            print(f"{Fore.GREEN}✅ {package} available{Style.RESET_ALL}")
        except ImportError:
            issues.append(f"Missing package: {package}")
            print(f"{Fore.RED}❌ {package} missing{Style.RESET_ALL}")
    
    # Check if main modules can be imported
    main_modules = ['game_engine', 'token_management', 'cli', 'config']
    for module in main_modules:
        try:
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            __import__(module)
            print(f"{Fore.GREEN}✅ {module} importable{Style.RESET_ALL}")
        except ImportError as e:
            issues.append(f"Cannot import {module}: {e}")
            print(f"{Fore.RED}❌ {module} import failed: {e}{Style.RESET_ALL}")
    
    # Check Ollama connection (optional)
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ Ollama server available{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  Ollama server not responding (tests will use mocks){Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}⚠️  Ollama connection failed (tests will use mocks): {e}{Style.RESET_ALL}")
    
    if issues:
        print(f"\n{Fore.RED}Prerequisites check failed:{Style.RESET_ALL}")
        for issue in issues:
            print(f"{Fore.RED}  - {issue}{Style.RESET_ALL}")
        return False
    else:
        print(f"\n{Fore.GREEN}✅ All prerequisites met!{Style.RESET_ALL}")
        return True

def run_performance_benchmarks():
    """Run performance benchmarks."""
    print(f"\n{Fore.CYAN}🚀 Running Performance Benchmarks...{Style.RESET_ALL}")
    
    try:
        # Use the comprehensive testall.py test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(TestAllOllamaDungeon)
        
        # Run some basic performance tests
        benchmarks = [
            ("Token Management", "test_token_manager_initialization"),
            ("Agent System", "test_agent_initialization"),
            ("World Controller", "test_world_controller_initialization"),
        ]
        
        for name, test_method in benchmarks:
            start_time = time.time()
            try:
                # Create a test instance and run the specific test
                test_instance = TestAllOllamaDungeon()
                test_instance.setUp()
                getattr(test_instance, test_method)()
                duration = time.time() - start_time
                color = Fore.GREEN if duration < 1.0 else Fore.YELLOW if duration < 3.0 else Fore.RED
                print(f"{color}{name}: {duration:.3f}s{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}{name}: FAILED - {e}{Style.RESET_ALL}")
    
    except ImportError as e:
        print(f"{Fore.RED}Could not run benchmarks: {e}{Style.RESET_ALL}")

def main():
    """Main test runner function - now uses comprehensive testall.py."""
    parser = argparse.ArgumentParser(description='Ollama Dungeon Test Runner')
    parser.add_argument('--comprehensive', '-c', action='store_true', 
                       help='Run comprehensive test suite (default)')
    parser.add_argument('--legacy', '-l', action='store_true', 
                       help='Run legacy individual test files')
    parser.add_argument('--verbose', '-v', action='count', default=1, help='Increase verbosity')
    parser.add_argument('--no-prereq', action='store_true', help='Skip prerequisite check')
    parser.add_argument('--benchmark', '-b', action='store_true', help='Run performance benchmarks')
    parser.add_argument('--quick', '-q', action='store_true', help='Run only essential tests')
    
    args = parser.parse_args()
    
    # Check prerequisites unless skipped
    if not args.no_prereq:
        if not check_prerequisites():
            print(f"{Fore.RED}Prerequisites not met. Use --no-prereq to skip this check.{Style.RESET_ALL}")
            return 1
    
    print(f"\n{Fore.CYAN}🧪 OLLAMA DUNGEON TEST RUNNER{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    if args.legacy:
        print(f"{Fore.YELLOW}⚠️  Running legacy individual test files...{Style.RESET_ALL}")
        # Run legacy tests by category (keeping old functionality)
        success = True
        categories = ['agents', 'tokens', 'integration']
        if not args.quick:
            categories.append('ultimate')
        
        for category in categories:
            print(f"\n{Fore.CYAN}Running {category.upper()} tests...{Style.RESET_ALL}")
            category_success = run_test_category(category, args.verbose)
            if not category_success:
                success = False
    else:
        # Use the new comprehensive test suite (default)
        print(f"{Fore.GREEN}🚀 Running comprehensive test suite...{Style.RESET_ALL}")
        
        if args.quick:
            # Run quick subset of tests
            print(f"{Fore.YELLOW}⚡ Quick test mode - running essential tests only{Style.RESET_ALL}")
            suite = unittest.TestSuite()
            suite.addTest(TestAllOllamaDungeon('test_agent_initialization'))
            suite.addTest(TestAllOllamaDungeon('test_world_controller_initialization'))
            suite.addTest(TestAllOllamaDungeon('test_room_navigation'))
            suite.addTest(TestAllOllamaDungeon('test_item_interaction'))
            suite.addTest(TestAllOllamaDungeon('test_token_manager_initialization'))
            suite.addTest(TestAllOllamaDungeon('test_cli_basic_commands'))
            suite.addTest(TestAllOllamaDungeon('test_save_load_system'))
            
            runner = ColoredTextTestRunner(verbosity=args.verbose)
            result = runner.run(suite)
            success = result.wasSuccessful()
        else:
            # Run full comprehensive test suite
            success = run_comprehensive_tests()
    
    # Run benchmarks if requested
    if args.benchmark:
        run_performance_benchmarks()
    
    # Final summary
    if success:
        print(f"\n{Fore.GREEN}🎉 ALL TESTS PASSED! The Ollama Dungeon system is working correctly.{Style.RESET_ALL}")
        return 0
    else:
        print(f"\n{Fore.RED}💥 SOME TESTS FAILED! Please check the output above for details.{Style.RESET_ALL}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
