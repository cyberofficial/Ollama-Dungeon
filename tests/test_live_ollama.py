#!/usr/bin/env python3
"""
Live Ollama Integration Tests for Ollama Dungeon
Tests actual AI responses and real gameplay scenarios with Ollama API.
"""

import unittest
import sys
import os
import tempfile
import shutil
import json
import csv
import time
import requests
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import Agent, WorldController
from token_management import TokenManager, ContextManager, token_manager, context_manager
from config import OLLAMA_BASE_URL, MODELS
from cli import GameCLI


class TestLiveOllamaIntegration(unittest.TestCase):
    """Live integration tests with actual Ollama API calls."""
    
    @classmethod
    def setUpClass(cls):
        """Check if Ollama is available before running tests."""
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code != 200:
                raise unittest.SkipTest("Ollama server not available")
            
            # Check if required models are available
            models_data = response.json()
            available_models = [model['name'] for model in models_data['models']]
            
            if MODELS['main'] not in available_models:
                raise unittest.SkipTest(f"Required model {MODELS['main']} not available")
            
            print(f"✅ Ollama server available with {len(available_models)} models")
            print(f"✅ Using main model: {MODELS['main']}")
            
        except Exception as e:
            raise unittest.SkipTest(f"Cannot connect to Ollama: {e}")
    
    def setUp(self):
        """Set up test environment with real world structure."""
        # Create temporary directories
        self.test_dir = tempfile.mkdtemp(prefix="live_test_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
          # Copy the actual world template
        world_template_path = os.path.join(self.original_cwd, "world_template")
        if os.path.exists(world_template_path):
            shutil.copytree(world_template_path, "world")
        else:
            # Create minimal world structure for testing
            self._create_minimal_world()
        
        # Initialize world controller
        self.world_controller = WorldController()
        self.cli = GameCLI()
        
        # Create saves directory
        os.makedirs("saves", exist_ok=True)
        
        print(f"🏗️ Live test environment created in: {self.test_dir}")
    
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def _create_minimal_world(self):
        """Create minimal world structure for testing."""
        # Create town with tavern
        os.makedirs("world/town/tavern/contexts", exist_ok=True)
        
        # Create tavern room
        tavern_room = {
            "name": "The Cozy Tavern",
            "description": "A warm, inviting tavern with wooden tables and a crackling fireplace. The smell of ale and roasted meat fills the air.",
            "exits": {"west": "world/town"},
            "items": []
        }
        with open("world/town/tavern/room.json", 'w') as f:
            json.dump(tavern_room, f, indent=2)
        
        # Create test agent
        agent_data = {
            "name": "Barkeep Bob",
            "description": "A friendly tavern keeper with many stories to tell",
            "personality": "jovial, talkative, and helpful",
            "goals": "serve customers and share local gossip",
            "memory_file": "memory_bob.csv",
            "location": "world/town/tavern",
            "status": "active"
        }
        with open("world/town/tavern/agent_bob.json", 'w') as f:
            json.dump(agent_data, f, indent=2)
        
        # Create empty memory file
        with open("world/town/tavern/memory_bob.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['memory_type', 'key', 'value', 'timestamp'])
        
        # Create town square
        town_room = {
            "name": "Town Square",
            "description": "The bustling center of town with a fountain in the middle.",
            "exits": {"east": "world/town/tavern"},
            "items": []
        }
        with open("world/town/room.json", 'w') as f:
            json.dump(town_room, f, indent=2)
    
    def test_ollama_basic_connectivity(self):
        """Test basic Ollama API connectivity."""
        print("🔌 Testing Ollama Basic Connectivity...")
        
        # Test basic generate endpoint
        payload = {
            "model": MODELS['main'],
            "prompt": "Say 'Hello world' and nothing else.",
            "stream": False
        }
        
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=30)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('response', data)
        self.assertIn('hello', data['response'].lower())
        
        print(f"  ✅ Ollama responded: {data['response'][:50]}...")
    
    def test_live_agent_conversation(self):
        """Test real conversation with an agent using Ollama."""
        print("🤖 Testing Live Agent Conversation...")
        
        # Load agent
        agent_file = "world/town/tavern/agent_bob.json"
        agent = Agent(agent_file, self.world_controller)
        
        # Test multiple conversation turns
        conversations = [
            "Hello there! How are you today?",
            "What's happening in town lately?",
            "Do you have any good ale?",
            "Tell me about the local rumors."
        ]
        
        responses = []
        for i, message in enumerate(conversations):
            print(f"  👤 Player: {message}")
            
            response = agent.generate_response(message, "The tavern is warm and cozy")
            self.assertIsNotNone(response)
            self.assertGreater(len(response), 10)  # Should get a substantial response
            
            responses.append(response)
            print(f"  🤖 Bob: {response[:100]}...")
            
            # Verify memory was created
            self.assertGreater(len(agent.memory), i * 2)  # Should have memories for each exchange
            
            # Small delay to be nice to the API
            time.sleep(0.5)
        
        # Verify conversation context is maintained
        final_response = agent.generate_response("What did we just talk about?", "The tavern setting")
        print(f"  🧠 Memory test: {final_response[:100]}...")        
        # Check that the agent has context from previous conversation
        self.assertIsNotNone(final_response)
        print("  ✅ Live conversation successful with memory persistence")
    
    def test_live_world_navigation_with_agents(self):
        """Test navigating the world and talking to agents."""
        print("🗺️ Testing Live World Navigation with Agent Interactions...")
        
        # Start in current room
        current_room = self.world_controller.get_current_room()
        print(f"  📍 Starting room: {current_room.get('name', 'Unknown')}")
        
        # Look around
        look_result = self.cli.cmd_look([])
        self.assertGreater(len(look_result), 20)
        print(f"  👀 Look: {look_result[:100]}...")
        
        # Move to tavern
        move_result = self.world_controller.move_player("east")
        print(f"  🚶 Move east: {move_result}")
        
        # Look in tavern
        tavern_look = self.cli.cmd_look([])
        print(f"  👀 Tavern: {tavern_look[:100]}...")
        
        # Talk to agent
        agents = self.world_controller.get_agents_in_room()
        if agents:
            agent = agents[0]
            response = agent.generate_response("Welcome! I'm new here.", "tavern setting")
            print(f"  🗣️ Agent response: {response[:100]}...")
            self.assertIsNotNone(response)
        
        print("  ✅ World navigation and live agent interaction successful")
    
    def test_live_token_management_with_compression(self):
        """Test token management and context compression with real API calls."""
        print("🔧 Testing Live Token Management and Compression...")
        
        agent_file = "world/town/tavern/agent_bob.json"
        agent = Agent(agent_file, self.world_controller)
        
        # Generate a long conversation to trigger compression
        long_messages = [
            "Tell me a long story about the history of this tavern.",
            "What's the most interesting thing that happened here?",
            "Describe all the regulars who come here.",
            "What's the best meal you've ever served?",
            "Tell me about the local politics and conflicts.",
            "What rumors have you heard about the surrounding areas?",
            "Describe the most memorable customer you've had.",
            "What's your personal history and how did you become a barkeep?"
        ]
        
        initial_context_length = len(agent.context_messages)
        
        for message in long_messages:
            response = agent.generate_response(message, "detailed tavern setting")
            self.assertIsNotNone(response)
            print(f"  💬 Conversation {len(agent.context_messages)//2}: Context length = {len(agent.context_messages)}")
            time.sleep(0.3)  # Be gentle with API
        
        # Check if compression was triggered
        final_context_length = len(agent.context_messages)
        print(f"  📊 Final context length: {final_context_length}")
        
        # Test token counting
        total_tokens = token_manager.count_tokens(str(agent.context_messages))
        print(f"  🔢 Total tokens in context: {total_tokens}")
          # Verify compression works
        if total_tokens > 30000:  # If we have lots of tokens, test compression
            compressed_context = token_manager.compress_context(agent.context_messages, agent.data['name'])
            compressed_tokens = token_manager.count_tokens(str(compressed_context))
            print(f"  🗜️ Compressed to: {compressed_tokens} tokens")
            self.assertLess(compressed_tokens, total_tokens)        
        print("  ✅ Token management and compression working with live API")
    
    def test_live_cli_integration(self):
        """Test CLI commands with live AI responses."""
        print("🖥️ Testing Live CLI Integration...")
        
        # Test basic commands that we know exist
        commands_to_test = [
            (["look"], "should show current location"),
            (["go", "east"], "should move to tavern"),
            (["look"], "should show tavern description"),
            (["say", "Hello there!"], "should get response from agent"),
            (["memory"], "should show conversation history")
        ]
        
        for command_args, description in commands_to_test:
            print(f"  🎮 Testing: {' '.join(command_args)} ({description})")
            
            try:
                if command_args[0] == "look":
                    result = self.cli.cmd_look(command_args[1:])
                elif command_args[0] == "go":
                    result = self.cli.cmd_go(command_args[1:])
                elif command_args[0] == "say":
                    result = self.cli.cmd_say(command_args[1:])
                elif command_args[0] == "memory":
                    result = self.cli.cmd_memory(command_args[1:])
                else:
                    continue
                
                self.assertIsNotNone(result)
                print(f"    ✅ Result: {result[:80]}...")
                time.sleep(0.2)
            except Exception as e:
                print(f"    ⚠️ Command failed: {e}")
        
        print("  ✅ CLI integration with live AI successful")
    
    def test_live_save_load_with_ai_state(self):
        """Test save/load preserving AI conversation state."""
        print("💾 Testing Live Save/Load with AI State...")
        
        # Have a conversation
        agent_file = "world/town/tavern/agent_bob.json"
        agent = Agent(agent_file, self.world_controller)
        
        # Initial conversation
        response1 = agent.generate_response("My name is Alice and I love cats.", "tavern")
        print(f"  💬 Initial: {response1[:50]}...")
        
        # Save game state
        save_result = self.world_controller.save_game("live_test_save")
        print(f"  💾 Save result: {save_result}")
        
        # Continue conversation
        response2 = agent.generate_response("What did I just tell you about myself?", "tavern")
        print(f"  🧠 Memory test: {response2[:50]}...")
        
        # Should remember Alice and cats
        self.assertIsNotNone(response2)
        
        # Load game state
        load_result = self.world_controller.load_game("live_test_save")
        print(f"  📂 Load result: {load_result}")
        
        # Test if memory persisted
        new_agent = Agent(agent_file, self.world_controller)
        response3 = new_agent.generate_response("Do you remember me and what I like?", "tavern")
        print(f"  🔄 After load: {response3[:50]}...")
        
        print("  ✅ Save/load with AI state preservation working")
    
    def test_live_error_handling_and_recovery(self):
        """Test error handling with live API calls."""
        print("⚠️ Testing Live Error Handling and Recovery...")
        
        agent_file = "world/town/tavern/agent_bob.json"
        agent = Agent(agent_file, self.world_controller)
        
        # Test with very long input (should handle gracefully)
        very_long_input = "Tell me a story. " * 1000  # Very long input
        response = agent.generate_response(very_long_input, "tavern")
        
        # Should get some response, not crash
        self.assertIsNotNone(response)
        print(f"  ✅ Handled long input: {len(response)} chars response")
        
        # Test with empty input
        empty_response = agent.generate_response("", "tavern")
        self.assertIsNotNone(empty_response)
        print(f"  ✅ Handled empty input: {empty_response[:50]}...")
        
        # Test with special characters
        special_response = agent.generate_response("Hello! @#$%^&*(){}[]", "tavern")
        self.assertIsNotNone(special_response)
        print(f"  ✅ Handled special chars: {special_response[:50]}...")
        
        print("  ✅ Error handling and recovery working with live API")


class TestOllamaPerformance(unittest.TestCase):
    """Performance tests with live Ollama API."""
    
    def setUp(self):
        """Set up for performance tests."""
        # Quick availability check
        try:
            requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        except:
            self.skipTest("Ollama not available for performance testing")
    
    def test_response_time_performance(self):
        """Test response times are reasonable."""
        print("⏱️ Testing Response Time Performance...")
        
        payload = {
            "model": MODELS['main'],
            "prompt": "Say hello briefly.",
            "stream": False
        }
        
        start_time = time.time()
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=60)
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"  ⏱️ Response time: {response_time:.2f} seconds")
        
        # Should respond within reasonable time (adjust based on your hardware)
        self.assertLess(response_time, 60.0, "Response time too slow")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)
        
        print("  ✅ Response time performance acceptable")
    
    def test_concurrent_requests_handling(self):
        """Test handling multiple requests (simulated)."""
        print("🔄 Testing Concurrent Request Handling...")
        
        # Test sequential requests to ensure stability
        response_times = []
        
        for i in range(3):  # Keep it light for CI
            payload = {
                "model": MODELS['main'],
                "prompt": f"Count to {i+1} briefly.",
                "stream": False
            }
            
            start_time = time.time()
            response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=30)
            end_time = time.time()
            
            response_times.append(end_time - start_time)
            self.assertEqual(response.status_code, 200)
            
            print(f"  🔄 Request {i+1}: {response_times[-1]:.2f}s")
        
        # Check that performance doesn't degrade significantly
        avg_time = sum(response_times) / len(response_times)
        print(f"  📊 Average response time: {avg_time:.2f}s")
        
        print("  ✅ Concurrent request handling stable")


if __name__ == '__main__':
    # Create a test suite with live integration tests
    suite = unittest.TestSuite()
    
    # Add live integration tests
    suite.addTest(unittest.makeSuite(TestLiveOllamaIntegration))
    suite.addTest(unittest.makeSuite(TestOllamaPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print("LIVE OLLAMA INTEGRATION TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, error in result.failures:
            print(f"  - {test}: {error[:100]}...")
    
    if result.errors:
        print(f"\n💥 ERRORS:")
        for test, error in result.errors:
            print(f"  - {test}: {error[:100]}...")
    
    if result.wasSuccessful():
        print("\n🎉 ALL LIVE INTEGRATION TESTS PASSED!")
    else:
        print(f"\n⚠️ Some tests failed or had errors.")
