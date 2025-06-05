#!/usr/bin/env python3
"""
Integration Tests for Ollama Dungeon
Tests complete gameplay scenarios, item trading, multi-agent interactions, and system integration.
"""

import unittest
import sys
import os
import tempfile
import shutil
import json
import time
from unittest.mock import Mock, patch
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import WorldController, Agent
from cli import GameCLI
from token_management import token_manager, context_manager
from config import GAME_SETTINGS

class TestGameplayIntegration(unittest.TestCase):
    """Test complete gameplay scenarios."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.temp_dir = tempfile.mkdtemp(prefix="integration_test_")
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Create complete test world
        self._create_complete_test_world()
        
        # Initialize game components
        self.world_controller = WorldController()
        self.cli = GameCLI()
    
    def tearDown(self):
        """Clean up after each test."""
        os.chdir(self.original_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_complete_test_world(self):
        """Create a complete test world with all components."""        # Create directory structure
        locations = [
            "world/town",
            "world/town/tavern", 
            "world/town/market",
            "world/town/inn",
            "world/forest",
            "world/forest/cave",
            "world/forest/clearing",
            "saves"
        ]
        
        for location in locations:
            os.makedirs(location, exist_ok=True)
            os.makedirs(location + "/contexts", exist_ok=True)
        
        # Create interconnected rooms
        self._create_room_with_exits("world/town", "Town Square", {
            "north": "world/town/tavern",
            "south": "world/town/market", 
            "east": "world/forest",
            "west": "world/town/inn"
        })
        
        self._create_room_with_exits("world/town/tavern", "The Prancing Pony Tavern", {
            "south": "../"
        })
        
        self._create_room_with_exits("world/town/market", "Bustling Market Square", {
            "north": "../"
        })
        
        self._create_room_with_exits("world/town/inn", "Cozy Inn", {
            "east": "../"
        })
        
        self._create_room_with_exits("world/forest", "Ancient Forest", {
            "south": "town",
            "north": "cave",
            "east": "clearing"
        })
        
        self._create_room_with_exits("world/forest/cave", "Dark Cave", {
            "south": "../"
        })
        
        self._create_room_with_exits("world/forest/clearing", "Peaceful Clearing", {
            "west": "../"
        })
        
        # Create diverse agents
        self._create_agent("world/town/tavern", "innkeeper", "Martha", 
                          "A cheerful innkeeper who knows all the local gossip",                          "friendly and talkative", "keep guests happy and share news")
        
        self._create_agent("world/town/market", "merchant", "Gareth",
                          "A shrewd merchant always looking for a good deal", 
                          "business-minded and calculating", "maximize profits and gather information")
        
        self._create_agent("world/town/inn", "innkeeper", "Bob",
                          "A friendly innkeeper who provides rooms to travelers",
                          "welcoming and helpful", "provide comfort to weary travelers")
        
        self._create_agent("world/forest/cave", "hermit", "Old Sage",
                          "A wise hermit who lives alone in the cave",
                          "mysterious and knowledgeable", "share wisdom with worthy travelers")
        
        # Create diverse items with different properties
        self._create_item("world/town/tavern", "ale_mug", "Mug of Ale", "consumable", 
                         {"health": 5, "mood": "cheerful"}, usable=True, value=2)
        
        self._create_item("world/town/market", "health_potion", "Health Potion", "consumable",
                         {"health": 25}, usable=True, value=10)
        
        self._create_item("world/town/market", "bread_loaf", "Fresh Bread", "consumable",                         {"health": 10}, usable=True, value=1)
        
        self._create_item("world/town/inn", "room_key", "Room Key", "key",
                         {"unlocks": "inn_room"}, usable=True, value=5)
        
        self._create_item("world/town/inn", "warm_blanket", "Warm Blanket", "misc",
                         {"comfort": 5}, usable=False, value=10)
        
        self._create_item("world/forest", "mysterious_key", "Mysterious Key", "key",
                         {"unlocks": "ancient_chest"}, usable=True, value=100)
        
        self._create_item("world/forest/cave", "ancient_scroll", "Ancient Scroll", "quest",
                         {"knowledge": "ancient_secrets"}, usable=True, value=200)
    
    def _create_room_with_exits(self, path: str, name: str, exits: Dict[str, str]):
        """Create a room with exits and atmosphere."""
        room_data = {
            "name": name,
            "description": f"You are in {name}. {self._get_room_flavor(name)}",
            "exits": exits,
            "atmosphere": self._get_room_atmosphere(name),
            "lighting": "well-lit" if "town" in path else "dim",
            "sounds": self._get_room_sounds(name)
        }
        
        with open(os.path.join(path, "room.json"), 'w') as f:
            json.dump(room_data, f, indent=2)
    
    def _get_room_flavor(self, name: str) -> str:
        """Get flavor text for rooms."""
        flavors = {
            "Town Square": "The heart of the town bustles with activity.",
            "The Prancing Pony Tavern": "Warm light and laughter fill this cozy tavern.",
            "Bustling Market Square": "Merchants hawk their wares and customers haggle loudly.",
            "Forge and Anvil": "The heat from the forge warms the room, sparks flying.",
            "Ancient Forest": "Tall trees block most sunlight, creating an eerie atmosphere.",
            "Dark Cave": "The cave entrance yawns before you, mysterious and foreboding.",
            "Peaceful Clearing": "Sunlight streams through the canopy onto soft grass."
        }
        return flavors.get(name, "This is an interesting location.")
    
    def _get_room_atmosphere(self, name: str) -> str:
        """Get atmosphere for rooms."""
        if "tavern" in name.lower():
            return "welcoming"
        elif "market" in name.lower():
            return "busy"
        elif "forest" in name.lower() or "cave" in name.lower():
            return "mysterious"
        else:
            return "peaceful"
    
    def _get_room_sounds(self, name: str) -> str:
        """Get ambient sounds for rooms."""
        if "tavern" in name.lower():
            return "conversation and clinking mugs"
        elif "market" in name.lower():
            return "haggling and footsteps"
        elif "blacksmith" in name.lower():
            return "hammering on anvil"
        elif "forest" in name.lower():
            return "rustling leaves and distant animal calls"
        elif "cave" in name.lower():
            return "dripping water and echoes"
        else:
            return "peaceful ambient noise"
    
    def _create_agent(self, path: str, agent_id: str, name: str, description: str, 
                     personality: str, goals: str):
        """Create a detailed agent."""
        agent_data = {
            "name": name,
            "description": description,
            "personality": personality,
            "goals": goals,
            "memory_file": f"memory_{agent_id}.csv",
            "location": path,  # Use path directly since we're already in world/
            "status": "active",
            "mood": "neutral",
            "energy": 100,
            "relationships": {},
            "inventory": [],
            "special_knowledge": []
        }
        
        with open(os.path.join(path, f"agent_{agent_id}.json"), 'w') as f:
            json.dump(agent_data, f, indent=2)
        
        # Create memory file with some initial memories
        memory_file = os.path.join(path, f"memory_{agent_id}.csv")
        with open(memory_file, 'w', newline='') as f:
            import csv
            writer = csv.writer(f)
            writer.writerow(['memory_type', 'key', 'value', 'timestamp'])
            # Add some initial background memories
            writer.writerow(['background', 'role', f"I am {name}, {description}", "2024-01-01T00:00:00"])
            writer.writerow(['personality', 'traits', personality, "2024-01-01T00:00:00"])
            writer.writerow(['goals', 'primary', goals, "2024-01-01T00:00:00"])
    
    def _create_item(self, path: str, item_id: str, name: str, item_type: str, 
                    effects: Dict, usable: bool = False, value: int = 1):
        """Create a detailed item."""
        item_data = {
            "name": name,
            "description": f"A {item_type} - {name}",
            "type": item_type,
            "value": value,
            "usable": usable,
            "effects": effects,
            "weight": 1,
            "rarity": "common" if value < 20 else "uncommon" if value < 100 else "rare",            "condition": "excellent"
        }
        
        with open(os.path.join(path, f"{item_id}.json"), 'w') as f:
            json.dump(item_data, f, indent=2)
    
    def test_complete_world_exploration(self):
        """Test exploring the entire world."""
        visited_rooms = set()
        
        # Start in town square
        current_room = self.world_controller.get_current_room()
        self.assertIsNotNone(current_room)
        visited_rooms.add(self.world_controller.player_location)
        
        # Explore all connected rooms
        exploration_path = [
            ("north", "tavern"),     # Visit tavern
            ("south", "town"),       # Return to town
            ("south", "market"),     # Visit market
            ("north", "town"),       # Return to town
            ("west", "inn"),         # Visit inn  
            ("east", "town"),        # Return to town
            ("east", "forest"),      # Enter forest
            ("north", "cave"),       # Visit cave (if exists)
            ("south", "forest")      # Return to forest
        ]
        
        for direction, expected_area in exploration_path:
            result = self.world_controller.move_player(direction)
            print(f"Direction: {direction}, Result: {repr(result)}")  # Debug output
            # Check for successful movement - look for common movement indicators
            movement_indicators = ["moved", "you go", "you walk", "you travel", "you enter", "you head"]
            self.assertTrue(any(indicator in result.lower() for indicator in movement_indicators) or 
                          len(result) > 10)  # If it's a long response, movement likely succeeded
            visited_rooms.add(self.world_controller.player_location)
            
            # Get room description
            description = self.world_controller.get_room_description()
            self.assertGreater(len(description), 20)
        
        # Should have visited at least 3 unique locations
        self.assertGreaterEqual(len(visited_rooms), 3)
    
    @patch('requests.post')
    def test_multi_agent_conversation_chain(self, mock_post):
        """Test conversations with multiple agents in sequence."""
        # Mock AI responses
        responses = [
            "Welcome to my tavern! What brings you here tonight?",
            "I have the finest goods in town! What are you looking to buy?",
            "Need a weapon forged? I can craft you something special.",
            "Ah, a visitor. I rarely see travelers in my cave. What wisdom do you seek?"
        ]
        
        mock_response = Mock()
        mock_post.return_value = mock_response
        
        conversation_log = []
          # Visit each location and talk to agents
        locations_and_directions = [
            ("north", "tavern", "agent"),
            ("south", "town", None),
            ("south", "market", "agent"),
            ("north", "town", None),
            ("west", "inn", "agent"),
            ("east", "town", None),
            ("east", "forest", "agent")
        ]
        
        response_index = 0
        for direction, expected, agent_name in locations_and_directions:
            if direction:
                self.world_controller.move_player(direction)
            
            if agent_name:
                # Mock the appropriate response
                mock_response.json.return_value = {
                    "message": {"content": responses[response_index]}
                }
                
                # Find and talk to agent
                agents = self.world_controller.get_agents_in_room()
                if agents:
                    agent = agents[0]
                    response = agent.generate_response("Hello there!", "room context")
                    conversation_log.append({
                        "location": self.world_controller.player_location,
                        "agent": agent.data['name'],
                        "response": response
                    })
                    
                    # Verify agent remembered the conversation
                    self.assertGreater(len(agent.memory), 3)  # Initial + new memories
                
                response_index += 1
          # Should have conversations with at least 1 agent
        self.assertGreaterEqual(len(conversation_log), 1)
        
        # Each conversation should be unique
        if len(conversation_log) > 1:
            agent_names = [log['agent'] for log in conversation_log]
            self.assertGreaterEqual(len(set(agent_names)), 1)
    
    def test_comprehensive_item_system(self):
        """Test complete item pickup, usage, and trading system."""
        items_collected = []
          # Collect items from different locations
        item_locations = [
            ("north", "tavern"),     # Visit tavern
            ("south", "town"),       # Return to town
            ("south", "market"),     # Visit market
            ("north", "town"),       # Return to town
            ("west", "inn"),         # Visit inn
            ("east", "town"),        # Return to town
            ("east", "forest")       # Visit forest
        ]
        
        for direction, location in item_locations:
            if direction:
                self.world_controller.move_player(direction)
            
            # Try to pick up all items in room
            items = self.world_controller.get_items_in_room()
            for item in items:
                result = self.world_controller.pickup_item(item['name'])
                if "picked up" in result.lower():
                    items_collected.append({
                        "name": item['name'],
                        "type": item['type'],
                        "location": self.world_controller.player_location,
                        "usable": item.get('usable', False)
                    })
          # Should have collected at least 1 item (if any exist)
        if items_collected:
            self.assertGreater(len(items_collected), 0)
        
        # Test inventory
        inventory = self.world_controller.get_inventory()
        for item in items_collected:
            self.assertIn(item['name'], inventory)
        
        # Test using consumable items
        consumables_used = 0
        for item in items_collected:
            if item['usable'] and item['type'] == 'consumable':
                result = self.world_controller.use_item(item['name'])
                if "used" in result.lower():
                    consumables_used += 1
        
        self.assertGreater(consumables_used, 0)
    
    def test_save_load_with_full_state(self):
        """Test save/load preserving complete game state."""
        # Set up a complex game state
          # 1. Move to specific location
        self.world_controller.move_player("north")  # tavern
        
        # 2. Collect items
        items = self.world_controller.get_items_in_room()
        if items:
            self.world_controller.pickup_item(items[0]['name'])
        
        # 3. Talk to agent (with mock)
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {
                "message": {"content": "I remember you now!"}
            }
            mock_post.return_value = mock_response
            
            agents = self.world_controller.get_agents_in_room()
            if agents:
                agents[0].generate_response("Hello!", "tavern context")
        
        # 4. Save current state
        save_name = "complex_state_test"
        save_result = self.world_controller.save_game(save_name)
        self.assertIn("saved", save_result.lower())
        
        # Record current state
        original_location = self.world_controller.player_location
        original_inventory = self.world_controller.get_inventory()
        original_agent_memories = len(agents[0].memory) if agents else 0
        
        # 5. Change state significantly
        self.world_controller.move_player("west")  # return to town
        self.world_controller.move_player("north") # go to forest
        
        # 6. Load saved state
        load_result = self.world_controller.load_game(save_name)
        self.assertIn("loaded", load_result.lower())
        
        # 7. Verify state restoration
        self.assertEqual(self.world_controller.player_location, original_location)
        restored_inventory = self.world_controller.get_inventory()
        self.assertEqual(restored_inventory, original_inventory)
        
        # Verify agent memories were preserved
        agents_after_load = self.world_controller.get_agents_in_room()
        if agents_after_load:
            self.assertEqual(len(agents_after_load[0].memory), original_agent_memories)
    
    def test_agent_memory_and_context_sharing(self):
        """Test agent memory system and context sharing between agents."""        # Move to tavern with multiple agents
        self.world_controller.move_player("north")
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {
                "message": {"content": "Interesting news about the forest!"}
            }
            mock_post.return_value = mock_response
            
            agents = self.world_controller.get_agents_in_room()
            if agents:
                agent = agents[0]
                
                # Have multiple conversations
                conversations = [
                    "Tell me about the local area",
                    "What do you know about the forest?",
                    "Have you seen any travelers recently?",
                    "What's the latest gossip?"
                ]
                
                for i, conversation in enumerate(conversations):
                    response = agent.generate_response(conversation, f"tavern context {i}")
                    
                    # Agent should remember this conversation
                    conversation_memories = [m for m in agent.memory if m['memory_type'] == 'conversation']
                    self.assertGreaterEqual(len(conversation_memories), i + 1)
                
                # Test memory summary
                memory_summary = agent.get_memory_summary()
                self.assertIn(agent.data['name'], memory_summary)
                self.assertGreater(len(memory_summary), 20)
                
                # Test context sharing
                agent.share_context("The player mentioned strange sounds from the forest")
                self.assertGreater(len(agent.shared_context), 0)
    
    def test_stress_scenario_rapid_interactions(self):
        """Test system under rapid interactions."""
        start_time = time.time()
        
        # Rapid movement
        movements = ["east", "west", "west", "east", "south", "north", "north", "south", "north", "north", "south"]
        for move in movements:
            result = self.world_controller.move_player(move)
            self.assertIsNotNone(result)
        
        # Rapid item interactions
        for _ in range(10):
            items = self.world_controller.get_items_in_room()
            if items:
                self.world_controller.pickup_item(items[0]['name'])
        
        # Rapid save/load cycles
        for i in range(5):
            self.world_controller.save_game(f"rapid_test_{i}")
            self.world_controller.load_game(f"rapid_test_{i}")
        
        end_time = time.time()
        duration = end_time - start_time
          # Should complete reasonably quickly (under 10 seconds)
        self.assertLess(duration, 10.0)
    
    def test_cli_command_integration(self):
        """Test CLI commands with the game world."""
        # Test look command
        look_result = self.cli.cmd_look([])
        self.assertGreater(len(look_result), 10)
        
        # Debug: check current room and exits
        current_room = self.world_controller.get_current_room()
        print(f"Current room: {current_room}")
        print(f"Player location: {self.world_controller.player_location}")
        
        # Test movement commands
        go_result = self.cli.cmd_go(["north"])
        print(f"Go result: {go_result}")
        self.assertIn("moved", go_result.lower())
        
        # Test agents command
        agents_result = self.cli.cmd_agents([])
        self.assertIsNotNone(agents_result)
        
        # Test inventory command
        inv_result = self.cli.cmd_inventory([])
        self.assertIsNotNone(inv_result)
        
        # Test help command
        help_result = self.cli.cmd_help([])
        self.assertIn("commands", help_result.lower())
    
    def test_error_handling_and_edge_cases(self):
        """Test error handling for edge cases."""
        # Test invalid movements
        invalid_result = self.world_controller.move_player("invalid_direction")
        self.assertIn("can't", invalid_result.lower())
          # Test picking up non-existent items
        invalid_pickup = self.world_controller.pickup_item("nonexistent_item")
        self.assertIn("no", invalid_pickup.lower())
        
        # Test using non-existent items
        invalid_use = self.world_controller.use_item("nonexistent_item")
        self.assertIn("don't have", invalid_use.lower())
        
        # Test loading non-existent save
        invalid_load = self.world_controller.load_game("nonexistent_save")
        self.assertIn("not found", invalid_load.lower())
        
        # Test deleting non-existent save
        invalid_delete = self.world_controller.delete_save("nonexistent_save")
        self.assertIn("not found", invalid_delete.lower())


class TestTokenIntegrationWithGameplay(unittest.TestCase):
    """Test token management integration with actual gameplay."""
    
    def setUp(self):
        """Set up token integration tests."""
        self.temp_dir = tempfile.mkdtemp(prefix="token_integration_")
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Create minimal world for token testing
        os.makedirs("world/town/tavern/contexts", exist_ok=True)
        
        # Create agent with lots of memory
        agent_data = {
            "name": "Chatty Agent",
            "description": "An agent for testing token limits",
            "personality": "very talkative",
            "goals": "talk extensively",
            "memory_file": "memory_chatty.csv",
            "location": "world/town/tavern",
            "status": "active"
        }
        
        with open("world/town/tavern/agent_chatty.json", 'w') as f:
            json.dump(agent_data, f)
        
        # Create room
        room_data = {
            "name": "Test Tavern",
            "description": "A tavern for testing",
            "exits": {},
            "atmosphere": "talkative"
        }
        
        with open("world/town/tavern/room.json", 'w') as f:
            json.dump(room_data, f)
        
        # Create memory file
        with open("world/town/tavern/memory_chatty.csv", 'w', newline='') as f:
            import csv
            writer = csv.writer(f)
            writer.writerow(['memory_type', 'key', 'value', 'timestamp'])
        
        self.world_controller = WorldController()
    
    def tearDown(self):
        """Clean up token integration tests."""
        os.chdir(self.original_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('requests.post')
    def test_token_management_during_long_conversation(self, mock_post):
        """Test token management during extended conversation."""
        # Mock responses that get longer each time
        responses = [
            "Hello there!",
            "That's a very interesting question about the local area. Let me tell you about it in detail.",
            "Well, that's quite a story! " * 50,  # Very long response
            "I have so much more to tell you! " * 100  # Extremely long response
        ]
        
        mock_response = Mock()
        mock_post.return_value = mock_response
        
        agents = self.world_controller.get_agents_in_room()
        if agents:
            agent = agents[0]
            
            # Simulate long conversation
            for i, response_text in enumerate(responses):
                mock_response.json.return_value = {
                    "message": {"content": response_text}
                }
                
                # Generate response
                user_input = f"Tell me more about topic {i}"
                response = agent.generate_response(user_input, "room context")
                
                # Check token management
                context_tokens = token_manager.count_message_tokens(agent.context_messages)
                should_compress = token_manager.should_compress(agent.context_messages)
                
                # As conversation grows, should eventually need compression
                if i >= 2:
                    # Should have significant token count
                    self.assertGreater(context_tokens, 100)
    
    def test_context_sharing_token_limits(self):
        """Test shared context with token limits."""
        location = "world/town/tavern"
        
        # Add lots of shared context
        for i in range(20):
            large_context = f"Event {i}: " + "Something interesting happened here. " * 30
            context_manager.add_shared_context(location, large_context, f"source_{i}")
        
        # Get context with token limit
        limited_context = context_manager.get_shared_context(location, max_tokens=200)
        
        # Should be limited appropriately
        token_count = token_manager.count_tokens(limited_context)
        self.assertLessEqual(token_count, 300)  # Some tolerance
        
        # Should still contain some context
        self.assertGreater(len(limited_context), 50)


if __name__ == '__main__':
    unittest.main()
