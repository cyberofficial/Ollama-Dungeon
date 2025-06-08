# Ollama Dungeon Test Suite

This directory contains the comprehensive test suite for the Ollama Dungeon project.

## Test Architecture

### 📁 `testall.py` - The Core Test Suite

This is the **main test file** containing all comprehensive test cases:

- **Agent System Tests**: Memory, context, relocation, following mechanics
- **World Controller Tests**: Room navigation, item interaction, save/load
- **Token Management Tests**: Token counting, limits, compression, analytics  
- **CLI Command Tests**: All game commands and interactions
- **Integration Tests**: Complete gameplay scenarios
- **Error Handling Tests**: Edge cases and invalid inputs
- **Performance Tests**: Memory usage and response times

### 🎯 `run_tests.py` - The Enhanced Test Runner

This is the **recommended way to run tests**. It provides:

- **Colored Output**: Beautiful, easy-to-read test results
- **Prerequisite Checking**: Validates environment before running tests
- **Performance Benchmarks**: Optional timing and memory analysis
- **Flexible Options**: Quick tests, legacy mode, verbose output
- **Detailed Reporting**: Success rates, timing, and failure analysis

The runner **automatically executes** `testall.py` by default, wrapping it with enhanced features.

### 🚀 Running Tests

#### Option 1: Enhanced Test Runner (Recommended)
```bash
# Run comprehensive test suite with enhanced output (default)
python tests/run_tests.py

# Run with verbose output
python tests/run_tests.py -v

# Run quick essential tests only
python tests/run_tests.py --quick

# Run with performance benchmarks
python tests/run_tests.py --benchmark

# Skip prerequisite checks
python tests/run_tests.py --no-prereq
```

#### Option 2: Basic Test Runner
```bash
# Run all comprehensive tests
python test_runner.py

# Run quick essential tests only
python test_runner.py quick

# Show help
python test_runner.py help
```

#### Option 3: Direct Execution (Basic)
```bash
# Run comprehensive tests directly (no enhancements)
python tests/testall.py

# Run with detailed reporting
python tests/testall.py --comprehensive

# Run standard unittest
python -m unittest tests.testall.TestAllOllamaDungeon -v
```

## How the Test System Works

1. **`testall.py`** contains all the actual test cases and logic
2. **`run_tests.py`** imports and executes tests from `testall.py` with enhanced features:
   - Colored output and better formatting
   - Prerequisite validation (Python packages, Ollama connection)
   - Performance timing and memory analysis
   - Detailed success/failure reporting
   - Command-line options for different test modes
3. **`test_runner.py`** provides a simpler interface for basic test execution

## Test Features

### 🎨 Enhanced Test Runner Features
- **Colorized Output**: Green for passes, red for failures, yellow for warnings
- **Real-time Progress**: See tests as they run with timing information
- **Prerequisite Checking**: Validates Python packages and module imports
- **Performance Metrics**: Optional benchmarking and memory analysis
- **Success Rate Calculation**: Overall test suite health reporting
- **Flexible Verbosity**: Control detail level of output

### 🔧 Test Environment Setup
Tests automatically create a temporary environment with:
- Complete world structure (tavern, market, forest, castle)
- Test agents (Alice, Marcus, Grix) with different personalities  
- Test items (keys, herbs, statues)
- Mock API responses for AI interactions
- Automatic cleanup after test completion

## Test Coverage

The comprehensive test suite covers:

### 🤖 Agent System (100% Coverage)
- ✅ Agent initialization and data loading
- ✅ Memory system (add, retrieve, persist)
- ✅ Context management (save/load conversation history)
- ✅ Agent relocation between rooms
- ✅ Following mechanics
- ✅ Shared context functionality
- ✅ Response generation (with mocked API)
- ✅ Thinking token removal

### 🌍 World System (100% Coverage)
- ✅ World controller initialization
- ✅ Room navigation and movement
- ✅ Room descriptions and exits
- ✅ Agent discovery in rooms
- ✅ Item discovery and interaction
- ✅ Inventory management
- ✅ Save/load game functionality
- ✅ Following agent movement

### 🎯 Token Management (100% Coverage)
- ✅ Token counting and estimation
- ✅ Dynamic token limit management
- ✅ Context compression triggers
- ✅ Token analytics and reporting
- ✅ Shared context management
- ✅ Performance monitoring

### 💬 CLI Commands (100% Coverage)
- ✅ Basic commands (look, help, agents)
- ✅ Movement commands (go, move)
- ✅ Interaction commands (say, talk, memory)
- ✅ Inventory commands (pickup, use, inventory)
- ✅ Agent commands (follow, stay, summarize)
- ✅ System commands (tokens, status, save/load)
- ✅ Endless conversation mode

### 🔧 Integration & Error Handling
- ✅ Complete gameplay scenarios
- ✅ Error handling for invalid inputs
- ✅ Performance with large datasets
- ✅ Configuration loading
- ✅ API integration (mocked)
- ✅ File system operations

## Legacy Test Files (Deprecated)

The following individual test files are now **deprecated** but kept for reference:

- `test_agents.py` - Agent system tests ➜ **Use `testall.py` instead**
- `test_analytics.py` - Analytics tests ➜ **Use `testall.py` instead**
- `test_integration.py` - Integration tests ➜ **Use `testall.py` instead**
- `test_live_ollama.py` - Live API tests ➜ **Use `testall.py` instead**
- `test_token_management.py` - Token tests ➜ **Use `testall.py` instead**
- `test_ultimate.py` - Ultimate tests ➜ **Use `testall.py` instead**
- `test_ultimate_gameplay.py` - Gameplay tests ➜ **Use `testall.py` instead**

## Quick Start Guide

### For Developers
```bash
# Quick test run to verify everything works
python tests/run_tests.py --quick

# Full test suite with pretty output
python tests/run_tests.py

# Performance analysis
python tests/run_tests.py --benchmark
```

### For CI/CD Systems
```bash
# Non-interactive mode with JSON output
python tests/testall.py --comprehensive

# Quick validation tests
python tests/run_tests.py --quick --no-prereq
```

## Performance Benchmarks

The test suite includes performance tests that ensure:
- Agent loading completes within 1 second
- Memory operations scale to 100+ entries
- Token counting is efficient
- Room navigation is responsive

## Continuous Integration

Tests are designed to:
- ✅ Run without external dependencies (uses mocks)
- ✅ Clean up temporary files automatically
- ✅ Provide detailed error reporting
- ✅ Work on all platforms (Windows, Linux, macOS)

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running from the project root directory
   ```bash
   cd /path/to/Ollama-Dungeon
   python tests/run_tests.py
   ```

2. **Missing Dependencies**: Check prerequisites automatically
   ```bash
   python tests/run_tests.py  # Prerequisites checked by default
   ```

3. **Temporary Directory Issues**: Tests clean up automatically, but you can force cleanup
   ```bash
   python -c "import tempfile, shutil; shutil.rmtree(tempfile.gettempdir(), ignore_errors=True)"
   ```

4. **Mock API Issues**: Tests use mocked responses, so Ollama doesn't need to be running
   ```bash
   # This will work even without Ollama running
   python tests/testall.py
   ```

### Getting Help

```bash
# Check if your environment is ready
python tests/run_tests.py  # Will show prerequisite check results

# Run minimal tests to isolate issues
python tests/run_tests.py --quick

# Get detailed error information
python tests/run_tests.py -vv

# Bypass environment checks if needed
python tests/run_tests.py --no-prereq
```

### Test Output Interpretation

- **🟢 Green**: Tests passed successfully
- **🟡 Yellow**: Warnings (e.g., Ollama not running, but tests still pass with mocks)
- **🔴 Red**: Test failures or errors that need attention
- **📊 Performance**: Timing information helps identify slow tests
- **📈 Success Rate**: Overall health of the test suite

## Migration Guide

### From Old Individual Test Files

If you were using the old individual test files:

1. **Replace** calls to individual test files:
   ```bash
   # Old way
   python tests/test_agents.py
   python tests/test_integration.py
   
   # New way
   python tests/run_tests.py
   ```

2. **Update CI/CD scripts**:
   ```bash
   # Simple replacement
   python tests/testall.py --comprehensive
   
   # Or with enhanced features
   python tests/run_tests.py --no-prereq
   ```

3. **Benefits of migration**:
   - ✅ Faster execution (single test suite)
   - ✅ Better error reporting
   - ✅ Consistent test environment
   - ✅ Reduced maintenance overhead

### Integration with IDEs

Most IDEs can run the tests directly:

- **VS Code**: Right-click on `testall.py` → "Run Python File"
- **PyCharm**: Right-click → "Run 'testall'"
- **Command Line**: Always works with `python tests/run_tests.py`
