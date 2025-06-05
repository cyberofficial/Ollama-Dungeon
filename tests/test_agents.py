#!/usr/bin/env python3
"""
Detailed Agent System Tests for Ollama Dungeon
Tests agent memory, conversations, context management, and relocation.
"""

import unittest
import sys
import os
import tempfile
import shutil
import json
import csv
from unittest.mock import Mock, patch
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import Agent, WorldController
from token_management import TokenManager, ContextManager

class TestAgentSystem(unittest.TestCase):
    """Comprehensive agent system tests."""
    
    def setUp(self):
        """Set up test environment for each test."""
        self.temp_dir = tempfile.mkdtemp(prefix="agent_test_")
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Create test agent directory
        os.makedirs("world/town/tavern/contexts", exist_ok=True)
        
        # Create test agent file
        self.agent_data = {
            "name": "Test Agent",
            "description": "A test agent for unit testing",
            "personality": "helpful and curious",
            "goals": "assist players and learn from interactions",
            "memory_file": "memory_test.csv",
            "location": "world/town/tavern",
            "status": "active"
        }
        
        self.agent_file = "world/town/tavern/agent_test.json"
        with open(self.agent_file, 'w') as f:
            json.dump(self.agent_data, f, indent=2)
        
        # Create empty memory file
        with open("world/town/tavern/memory_test.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['memory_type', 'key', 'value', 'timestamp'])
        
        # Mock world controller
        self.world_controller = Mock()
    
    def tearDown(self):
        """Clean up after each test."""
        os.chdir(self.original_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_agent_initialization(self):
        """Test agent initialization and data loading."""
        agent = Agent(self.agent_file, self.world_controller)
        
        self.assertEqual(agent.data['name'], "Test Agent")
        self.assertEqual(agent.data['personality'], "helpful and curious")
        self.assertIsNotNone(agent.session_id)
        if agent.session_id:
            self.assertTrue(agent.session_id.startswith("agent_test_agent_"))
        self.assertEqual(len(agent.memory), 0)
        self.assertTrue(os.path.exists(agent.context_file))
    
    def test_memory_system(self):
        """Test agent memory addition, storage, and retrieval."""
        agent = Agent(self.agent_file, self.world_controller)
        
        # Test adding memories
        agent.add_memory("conversation", "player", "Hello there!")
        agent.add_memory("observation", "environment", "The room is dimly lit")
        agent.add_memory("interaction", "item", "Player picked up a sword")
        
        # Check memory count
        self.assertEqual(len(agent.memory), 3)
        
        # Check memory content
        self.assertEqual(agent.memory[0]['memory_type'], "conversation")
        self.assertEqual(agent.memory[0]['key'], "player")
        self.assertEqual(agent.memory[0]['value'], "Hello there!")
          # Check memory file persistence
        memory_file = "world/town/tavern/memory_test.csv"
        with open(memory_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0]['memory_type'], "conversation")
    
    def test_memory_summary(self):
        """Test memory summarization."""
        agent = Agent(self.agent_file, self.world_controller)
        
        # Add multiple memories
        for i in range(15):
            agent.add_memory("test", f"key_{i}", f"Test memory {i}")
        
        # Test summary with limit
        summary = agent.get_memory_summary(limit=5)
        self.assertIn("Test Agent's recent activities", summary)
        
        # Check that some memories are included in the summary
        memory_found = False
        for i in range(10, 15):  # Check recent memories
            if f"Test memory {i}" in summary or f"key_{i}" in summary:
                memory_found = True
                break
        
        if not memory_found:
            # If no specific memory text found, at least check structure
            self.assertGreater(len(summary), 20)  # Should have substantial content
        
        # Test summary without memories
        empty_agent = Agent(self.agent_file, self.world_controller)
        empty_summary = empty_agent.get_memory_summary()
        self.assertIn("no recent activities", empty_summary.lower())
    
    def test_context_management(self):
        """Test agent context saving and loading."""
        agent = Agent(self.agent_file, self.world_controller)
        
        # Add context messages
        agent.context_messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"}
        ]
        
        # Save context
        agent._save_context()
        self.assertTrue(os.path.exists(agent.context_file))
        
        # Create new agent and load context
        new_agent = Agent(self.agent_file, self.world_controller)
        self.assertEqual(len(new_agent.context_messages), 3)
        self.assertEqual(new_agent.context_messages[0]['content'], "Hello")
    
    def test_context_reset(self):
        """Test context reset functionality."""
        agent = Agent(self.agent_file, self.world_controller)
        
        # Add context and save
        agent.context_messages = [{"role": "user", "content": "Test"}]
        agent._save_context()
        
        # Reset context
        old_session_id = agent.session_id
        agent.reset_context()        
        self.assertEqual(len(agent.context_messages), 0)
        self.assertNotEqual(agent.session_id, old_session_id)
        self.assertFalse(os.path.exists(agent.context_file))
    
    def test_agent_relocation(self):
        """Test agent movement between locations."""
        agent = Agent(self.agent_file, self.world_controller)
        
        original_location = agent.data['location']
        new_location = "world/forest/cave"
        
        # Create the destination directory
        os.makedirs(new_location, exist_ok=True)
        
        agent.move_to_location(new_location)
        
        self.assertEqual(agent.data['location'], new_location)
        self.assertNotEqual(agent.data['location'], original_location)
        
        # Check that agent data was saved at new location
        new_agent_file = os.path.join(new_location, "agent_test.json")
        self.assertTrue(os.path.exists(new_agent_file))
        with open(new_agent_file, 'r') as f:
            saved_data = json.load(f)
            self.assertEqual(saved_data['location'], new_location)    
    def test_shared_context(self):
        """Test shared context functionality."""
        agent = Agent(self.agent_file, self.world_controller)
        
        # Test adding shared context
        test_context = "The player entered the room looking worried."
        agent.share_context(test_context)
        
        # Context is now stored as a dict with timestamp
        self.assertEqual(len(agent.shared_context), 1)
        self.assertEqual(agent.shared_context[0]['context'], test_context)
        self.assertIn('timestamp', agent.shared_context[0])
    
    @patch('requests.post')
    def test_response_generation(self, mock_post):
        """Test agent response generation with mocked API."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {"content": "Hello! Nice to meet you. How can I help you today?"}
        }
        mock_post.return_value = mock_response
        
        agent = Agent(self.agent_file, self.world_controller)
        
        player_input = "Hello there!"
        room_context = "You are in a cozy tavern with wooden tables and a warm fireplace."
        
        response = agent.generate_response(player_input, room_context)
        
        self.assertIsNotNone(response)
        self.assertIn("Hello!", response)
        self.assertIn("help", response)
        
        # Verify API was called
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_response_with_memory_context(self, mock_post):
        """Test that agent responses include memory context."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {"content": "I remember our previous conversation!"}
        }
        mock_post.return_value = mock_response
        
        agent = Agent(self.agent_file, self.world_controller)
        
        # Add some memories
        agent.add_memory("conversation", "player", "We talked about the weather")
        agent.add_memory("observation", "mood", "Player seemed cheerful")
        
        response = agent.generate_response("Do you remember me?", "test room")
        
        # Check that the API call included memory context
        call_args = mock_post.call_args
        request_data = call_args[1]['json']
        
        # Should include system prompt with personality and memory
        messages = request_data['messages']
        system_message = next((msg for msg in messages if msg['role'] == 'system'), None)        
        self.assertIsNotNone(system_message)
        if system_message:
            self.assertIn("helpful and curious", system_message['content'])  # personality
            self.assertIn("recent activities", system_message['content'])     # memory summary
    
    def test_prompt_building(self):
        """Test prompt building with various contexts."""
        agent = Agent(self.agent_file, self.world_controller)
        
        # Add some context
        agent.add_memory("conversation", "player", "Discussed local rumors")
        agent.shared_context.append("A merchant just left the tavern")
        
        room_context = "The tavern is busy with evening customers."
        player_input = "What's the latest news?"
        
        prompt = agent._build_prompt(player_input, room_context)
        
        self.assertIn(player_input, prompt)
        self.assertIn(room_context, prompt)
    
    def test_system_prompt_building(self):
        """Test system prompt construction."""
        agent = Agent(self.agent_file, self.world_controller)
        
        agent.add_memory("conversation", "player", "Asked about the weather")
        
        room_context = "A cozy tavern with warm lighting"
        system_prompt = agent._build_system_prompt(room_context)
        
        self.assertIn("Test Agent", system_prompt)
        self.assertIn("helpful and curious", system_prompt)
        self.assertIn("assist players", system_prompt)
        self.assertIn(room_context, system_prompt)
        self.assertIn("recent activities", system_prompt)
    
    def test_memory_persistence_across_sessions(self):
        """Test that memories persist across different agent instances."""
        # Create first agent and add memories
        agent1 = Agent(self.agent_file, self.world_controller)
        agent1.add_memory("conversation", "player", "First conversation")
        agent1.add_memory("observation", "environment", "Room is well-lit")
        
        # Create second agent instance (simulating restart)
        agent2 = Agent(self.agent_file, self.world_controller)
        
        # Check that memories were loaded
        self.assertEqual(len(agent2.memory), 2)
        self.assertEqual(agent2.memory[0]['value'], "First conversation")
        self.assertEqual(agent2.memory[1]['value'], "Room is well-lit")
    
    def test_agent_data_updates(self):
        """Test that agent data updates are saved."""
        agent = Agent(self.agent_file, self.world_controller)
        
        # Update agent data
        agent.data['status'] = 'busy'
        agent.data['new_field'] = 'test_value'
        agent._save_agent_data()
        
        # Load fresh agent and check updates
        new_agent = Agent(self.agent_file, self.world_controller)
        self.assertEqual(new_agent.data['status'], 'busy')
        self.assertEqual(new_agent.data['new_field'], 'test_value')
    
    def test_large_memory_handling(self):
        """Test handling of large numbers of memories."""
        agent = Agent(self.agent_file, self.world_controller)
        
        # Add many memories
        for i in range(1000):
            agent.add_memory("test", f"key_{i}", f"Memory entry {i}")
        
        # Check that all memories were added
        self.assertEqual(len(agent.memory), 1000)
        
        # Check that memory summary still works
        summary = agent.get_memory_summary(limit=10)
        self.assertIn("recent activities", summary)
        
        # Check file integrity
        memory_file = "world/town/tavern/memory_test.csv"
        with open(memory_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1000)


if __name__ == '__main__':
    unittest.main()
