#!/usr/bin/env python3
"""
Ultimate Test Suite for Ollama Dungeon
Tests every single interaction, memory, compression, model loading, item trading, and more.
"""

import unittest
import sys
import os
import tempfile
import shutil
import time
import json
import csv
from typing import Dict, List, Any, Optional
from unittest.mock import Mock, patch, MagicMock
from colorama import init, Fore, Style

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from game_engine import WorldController, Agent
from token_management import TokenManager, ContextManager, token_manager, context_manager
from cli import GameCLI
from config import MODELS, TOKEN_SETTINGS, AGENT_SETTINGS, GAME_SETTINGS

# Initialize colorama
init()

class TestResult:
    """Enhanced test result tracking."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = 0
        self.details = []
    
    def add_pass(self, test_name: str, message: str = ""):
        self.passed += 1
        self.details.append(f"✅ PASS: {test_name} {message}")
    
    def add_fail(self, test_name: str, message: str = ""):
        self.failed += 1
        self.details.append(f"❌ FAIL: {test_name} {message}")
    
    def add_error(self, test_name: str, error: str):
        self.errors += 1
        self.details.append(f"⚠️  ERROR: {test_name} - {error}")
    
    def print_summary(self):
        total = self.passed + self.failed + self.errors
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}TEST SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"Total Tests: {total}")
        print(f"{Fore.GREEN}Passed: {self.passed}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {self.failed}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Errors: {self.errors}{Style.RESET_ALL}")
        
        if self.failed > 0 or self.errors > 0:
            print(f"\n{Fore.RED}FAILED/ERROR DETAILS:{Style.RESET_ALL}")
            for detail in self.details:
                if "FAIL:" in detail or "ERROR:" in detail:
                    print(detail)
        
        success_rate = (self.passed / total * 100) if total > 0 else 0
        color = Fore.GREEN if success_rate >= 90 else Fore.YELLOW if success_rate >= 70 else Fore.RED
        print(f"\n{color}Success Rate: {success_rate:.1f}%{Style.RESET_ALL}")

class UltimateTestSuite:
    """The ultimate test suite for Ollama Dungeon."""
    
    def __init__(self):
        self.result = TestResult()
        self.temp_dir = None
        self.world_controller = None
        self.test_agents = {}
        self.original_dir = os.getcwd()
    
    def setup_test_environment(self):
        """Set up a clean test environment."""
        print(f"{Fore.CYAN}Setting up test environment...{Style.RESET_ALL}")
        
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp(prefix="ollama_dungeon_test_")
        os.chdir(self.temp_dir)
        
        # Create test world structure
        self._create_test_world()        
        print(f"Test environment created at: {self.temp_dir}")
    
    def cleanup_test_environment(self):
        """Clean up test environment."""
        print(f"{Fore.CYAN}Cleaning up test environment...{Style.RESET_ALL}")
        
        os.chdir(self.original_dir)
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_test_world(self):
        """Create a test world structure."""
        # Create world structure (NOT world_template)
        os.makedirs("world/town/tavern", exist_ok=True)
        os.makedirs("world/town/market", exist_ok=True)
        os.makedirs("world/forest/cave", exist_ok=True)
        os.makedirs("saves", exist_ok=True)
        
        # Create test rooms
        self._create_test_room("world/town", "Town Square", {
            "north": "forest",
            "east": "tavern",
            "west": "market"
        })
        
        self._create_test_room("world/town/tavern", "The Cozy Tavern", {
            "west": "../"
        })
        
        self._create_test_room("world/town/market", "Town Market", {
            "east": "../"
        })
        
        self._create_test_room("world/forest", "Dark Forest", {
            "south": "town",
            "north": "cave"
        })
        
        self._create_test_room("world/forest/cave", "Mysterious Cave", {
            "south": "../"
        })
        
        # Create test agents
        self._create_test_agent("world/town/tavern", "alice", "Alice", "A friendly tavern keeper")
        self._create_test_agent("world/town/tavern", "bob", "Bob", "A mysterious scout")
        self._create_test_agent("world/forest/cave", "grix", "Grix", "A goblin scout")
        
        # Create test items
        self._create_test_item("world/town/tavern", "rusty_dagger", "Rusty Dagger", "weapon")
        self._create_test_item("world/town/market", "health_potion", "Health Potion", "consumable")
    
    def _create_test_room(self, path: str, name: str, exits: Dict[str, str]):
        """Create a test room JSON file."""
        room_data = {
            "name": name,
            "description": f"You are in {name.lower()}. This is a test location.",
            "exits": exits,
            "atmosphere": "peaceful"
        }
        
        with open(os.path.join(path, "room.json"), 'w') as f:
            json.dump(room_data, f, indent=2)
    
    def _create_test_agent(self, path: str, agent_id: str, name: str, description: str):
        """Create a test agent JSON file."""
        agent_data = {
            "name": name,
            "description": description,
            "personality": "friendly and helpful",
            "goals": "help players and be useful",
            "memory_file": f"memory_{agent_id}.csv",
            "location": path,  # Use path directly since we're already in world/
            "status": "active"
        }
        
        with open(os.path.join(path, f"agent_{agent_id}.json"), 'w') as f:
            json.dump(agent_data, f, indent=2)
        
        # Create empty memory file
        memory_file = os.path.join(path, f"memory_{agent_id}.csv")
        with open(memory_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['memory_type', 'key', 'value', 'timestamp'])
    
    def _create_test_item(self, path: str, item_id: str, name: str, item_type: str):
        """Create a test item JSON file."""
        item_data = {
            "name": name,
            "description": f"A test {item_type}",
            "type": item_type,
            "value": 10,
            "usable": item_type == "consumable",
            "effects": {"health": 20} if item_type == "consumable" else {}
        }
        
        with open(os.path.join(path, f"{item_id}.json"), 'w') as f:
            json.dump(item_data, f, indent=2)
    
    def run_all_tests(self):
        """Run all test suites."""
        print(f"{Fore.CYAN}🚀 STARTING ULTIMATE OLLAMA DUNGEON TEST SUITE{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        try:
            self.setup_test_environment()
            
            # Core system tests
            self.test_model_loading()
            self.test_world_controller()
            self.test_agent_system()
            self.test_token_management()
            self.test_item_system()
            self.test_save_load_system()
            self.test_cli_interface()
            
            # Integration tests
            self.test_gameplay_scenarios()
            self.test_stress_scenarios()
            
        finally:
            self.cleanup_test_environment()
        
        self.result.print_summary()
        return self.result
    
    def test_model_loading(self):
        """Test model loading and Ollama connection."""
        print(f"\n{Fore.YELLOW}🤖 Testing Model Loading...{Style.RESET_ALL}")
        
        try:
            # Test Ollama connection
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                self.result.add_pass("Ollama Connection", "Server is running")
                
                # Check available models
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                
                for model_key, model_name in MODELS.items():
                    if any(model_name in m for m in model_names):
                        self.result.add_pass(f"Model Available: {model_key}", model_name)
                    else:
                        self.result.add_fail(f"Model Missing: {model_key}", model_name)
            else:
                self.result.add_fail("Ollama Connection", f"Status: {response.status_code}")
        
        except Exception as e:
            self.result.add_error("Ollama Connection", str(e))
        
        # Test token manager initialization
        try:
            tm = TokenManager()
            test_text = "This is a test message for token counting."
            tokens = tm.count_tokens(test_text)
            if tokens > 0:
                self.result.add_pass("Token Counting", f"Counted {tokens} tokens")
            else:
                self.result.add_fail("Token Counting", "No tokens counted")
        except Exception as e:
            self.result.add_error("Token Manager Init", str(e))
    
    def test_world_controller(self):
        """Test WorldController functionality."""
        print(f"\n{Fore.YELLOW}🌍 Testing World Controller...{Style.RESET_ALL}")
        
        try:
            # Initialize world controller
            self.world_controller = WorldController()
            self.result.add_pass("WorldController Init", "Initialized successfully")
            
            # Test room loading
            current_room = self.world_controller.get_current_room()
            if current_room:
                self.result.add_pass("Room Loading", f"Loaded: {current_room.get('name', 'Unknown')}")
            else:
                self.result.add_fail("Room Loading", "No room loaded")
            
            # Test room description
            description = self.world_controller.get_room_description()
            if description and len(description) > 10:
                self.result.add_pass("Room Description", "Generated description")
            else:
                self.result.add_fail("Room Description", "Empty or invalid description")
            
            # Test movement
            if self.world_controller:
                original_location = self.world_controller.player_location
                move_result = self.world_controller.move_player("north")
                if "moved" in move_result.lower() or "forest" in move_result.lower():
                    self.result.add_pass("Player Movement", "Successfully moved north")
                    
                    # Test return movement
                    move_back = self.world_controller.move_player("south")
                    if "moved" in move_back.lower() or "town" in move_back.lower():
                        self.result.add_pass("Return Movement", "Successfully moved back")
                    else:
                        self.result.add_fail("Return Movement", "Could not move back")
                else:
                    self.result.add_fail("Player Movement", "Movement failed")
            else:
                self.result.add_fail("Player Movement", "WorldController not initialized")
            
            # Test invalid movement
            if self.world_controller:
                invalid_move = self.world_controller.move_player("invalid_direction")
                if "can't" in invalid_move.lower() or "invalid" in invalid_move.lower():
                    self.result.add_pass("Invalid Movement", "Properly rejected invalid direction")
                else:
                    self.result.add_fail("Invalid Movement", "Did not reject invalid direction")
        
        except Exception as e:
            self.result.add_error("WorldController Test", str(e))
    
    def test_agent_system(self):
        """Test agent system functionality."""
        print(f"\n{Fore.YELLOW}🤖 Testing Agent System...{Style.RESET_ALL}")
        
        try:
            # Test agent loading
            if not self.world_controller:
                self.result.add_fail("Agent System Test", "WorldController not initialized")
                return
                
            agents = self.world_controller.get_agents_in_room()
            if agents:
                self.result.add_pass("Agent Loading", f"Found {len(agents)} agents")
                
                # Test individual agent
                agent = agents[0]
                
                # Test agent data
                if hasattr(agent, 'data') and agent.data.get('name'):
                    self.result.add_pass("Agent Data", f"Agent: {agent.data['name']}")
                else:
                    self.result.add_fail("Agent Data", "Missing agent data")
                
                # Test memory system
                try:
                    agent.add_memory("conversation", "test_player", "Hello there!")
                    self.result.add_pass("Memory Add", "Added memory entry")
                    
                    memory_summary = agent.get_memory_summary()
                    if memory_summary and len(memory_summary) > 10:
                        self.result.add_pass("Memory Summary", "Generated summary")
                    else:
                        self.result.add_fail("Memory Summary", "Empty summary")
                except Exception as e:
                    self.result.add_error("Memory System", str(e))
                
                # Test agent conversation (mock response)
                try:
                    with patch('requests.post') as mock_post:
                        mock_response = Mock()
                        mock_response.json.return_value = {
                            "message": {"content": "Hello! Nice to meet you."}
                        }
                        mock_post.return_value = mock_response
                        
                        response = agent.generate_response("Hello", "test room context")
                        if response and len(response) > 5:
                            self.result.add_pass("Agent Response", "Generated response")
                        else:
                            self.result.add_fail("Agent Response", "Empty response")
                except Exception as e:
                    self.result.add_error("Agent Response", str(e))
                
                # Test agent relocation
                try:
                    original_location = agent.data.get('location')
                    agent.move_to_location("world/forest")
                    if agent.data.get('location') != original_location:
                        self.result.add_pass("Agent Relocation", "Successfully moved agent")
                    else:
                        self.result.add_fail("Agent Relocation", "Agent did not move")
                except Exception as e:
                    self.result.add_error("Agent Relocation", str(e))
            
            else:
                self.result.add_fail("Agent Loading", "No agents found in room")
        
        except Exception as e:
            self.result.add_error("Agent System Test", str(e))
    
    def test_token_management(self):
        """Test token management and compression."""
        print(f"\n{Fore.YELLOW}🔢 Testing Token Management...{Style.RESET_ALL}")
        
        try:
            tm = TokenManager()
            
            # Test token counting
            test_messages = [
                {"role": "user", "content": "Hello there!"},
                {"role": "assistant", "content": "Hello! How can I help you today?"},
                {"role": "user", "content": "Tell me about this place."}
            ]
            
            token_count = tm.count_message_tokens(test_messages)
            if token_count > 0:
                self.result.add_pass("Message Token Counting", f"Counted {token_count} tokens")
            else:
                self.result.add_fail("Message Token Counting", "No tokens counted")
            
            # Test compression threshold
            should_compress = tm.should_compress(test_messages)
            if isinstance(should_compress, bool):
                self.result.add_pass("Compression Check", f"Should compress: {should_compress}")
            else:
                self.result.add_fail("Compression Check", "Invalid response")
            
            # Test context compression with mock
            try:
                # Create a large message list to trigger compression
                large_messages = []
                for i in range(100):
                    large_messages.append({"role": "user", "content": f"Message {i} " * 50})
                    large_messages.append({"role": "assistant", "content": f"Response {i} " * 50})
                
                with patch('requests.post') as mock_post:
                    mock_response = Mock()
                    mock_response.json.return_value = {
                        "message": {"content": "This is a summary of the conversation."}
                    }
                    mock_post.return_value = mock_response
                    
                    compressed = tm.compress_context(large_messages, "test_agent")
                    if len(compressed) < len(large_messages):
                        self.result.add_pass("Context Compression", f"Reduced from {len(large_messages)} to {len(compressed)} messages")
                    else:
                        self.result.add_fail("Context Compression", "No compression occurred")
            
            except Exception as e:
                self.result.add_error("Context Compression", str(e))
            
            # Test context manager
            cm = ContextManager()
            cm.add_shared_context("test_location", "Player entered the room", "player")
            
            shared = cm.get_shared_context("test_location")
            if shared and len(shared) > 10:
                self.result.add_pass("Shared Context", "Added and retrieved context")
            else:
                self.result.add_fail("Shared Context", "Context not working")
        
        except Exception as e:
            self.result.add_error("Token Management Test", str(e))
    
    def test_item_system(self):
        """Test item system functionality."""
        print(f"\n{Fore.YELLOW}🎒 Testing Item System...{Style.RESET_ALL}")
        
        try:
            if not self.world_controller:
                self.result.add_fail("Item System Test", "WorldController not initialized")
                return
                
            # Test item loading
            items = self.world_controller.get_items_in_room()
            if items:
                self.result.add_pass("Item Loading", f"Found {len(items)} items")
                
                # Test item pickup
                item = items[0]
                item_name = item.get('name', 'Unknown Item')
                pickup_result = self.world_controller.pickup_item(item_name)
                
                if "picked up" in pickup_result.lower() or "added" in pickup_result.lower():
                    self.result.add_pass("Item Pickup", f"Picked up {item_name}")
                    
                    # Test inventory
                    inventory = self.world_controller.get_inventory()
                    if item_name.lower() in inventory.lower():
                        self.result.add_pass("Inventory Check", "Item appears in inventory")
                    else:
                        self.result.add_fail("Inventory Check", "Item not in inventory")
                    
                    # Test item usage
                    if item.get('usable', False):
                        use_result = self.world_controller.use_item(item_name)
                        if "used" in use_result.lower() or "effect" in use_result.lower():
                            self.result.add_pass("Item Usage", f"Used {item_name}")
                        else:
                            self.result.add_fail("Item Usage", "Could not use item")
                    
                else:
                    self.result.add_fail("Item Pickup", f"Could not pick up {item_name}")
            
            else:
                # Move to a room with items
                self.world_controller.move_player("east")  # Go to tavern
                items = self.world_controller.get_items_in_room()
                if items:
                    self.result.add_pass("Item Loading (Tavern)", f"Found {len(items)} items")
                else:
                    self.result.add_fail("Item Loading", "No items found in any room")
        
        except Exception as e:
            self.result.add_error("Item System Test", str(e))
    
    def test_save_load_system(self):
        """Test save and load functionality."""
        print(f"\n{Fore.YELLOW}💾 Testing Save/Load System...{Style.RESET_ALL}")
        
        try:
            if not self.world_controller:
                self.result.add_fail("Save/Load System Test", "WorldController not initialized")
                return
                
            # Test save game
            save_result = self.world_controller.save_game("test_save")
            if "saved" in save_result.lower():
                self.result.add_pass("Game Save", "Successfully saved game")
                
                # Test list saves
                saves_list = self.world_controller.list_saves()
                if "test_save" in saves_list:
                    self.result.add_pass("List Saves", "Save appears in list")
                else:
                    self.result.add_fail("List Saves", "Save not in list")
                
                # Modify game state
                original_location = self.world_controller.player_location
                self.world_controller.move_player("north")
                
                # Test load game
                load_result = self.world_controller.load_game("test_save")
                if "loaded" in load_result.lower():
                    self.result.add_pass("Game Load", "Successfully loaded game")
                    
                    # Check if state was restored
                    if self.world_controller.player_location == original_location:
                        self.result.add_pass("State Restoration", "Game state properly restored")
                    else:
                        self.result.add_fail("State Restoration", "Game state not restored")
                else:
                    self.result.add_fail("Game Load", "Could not load game")
                
                # Test delete save
                delete_result = self.world_controller.delete_save("test_save")
                if "deleted" in delete_result.lower():
                    self.result.add_pass("Delete Save", "Successfully deleted save")
                else:
                    self.result.add_fail("Delete Save", "Could not delete save")
            
            else:
                self.result.add_fail("Game Save", "Could not save game")
        
        except Exception as e:
            self.result.add_error("Save/Load System Test", str(e))
    
    def test_cli_interface(self):
        """Test CLI interface commands."""
        print(f"\n{Fore.YELLOW}💻 Testing CLI Interface...{Style.RESET_ALL}")
        
        try:
            cli = GameCLI()
            
            # Test command parsing
            test_commands = [
                ("look", "cmd_look"),
                ("go north", "cmd_go"),
                ("say alice hello", "cmd_say"),
                ("inventory", "cmd_inventory"),
                ("help", "cmd_help")
            ]
            
            for command, expected_method in test_commands:
                parts = command.split()
                cmd = parts[0].lower()
                if cmd in cli.commands:
                    self.result.add_pass(f"Command Parse: {command}", "Command recognized")
                else:
                    self.result.add_fail(f"Command Parse: {command}", "Command not recognized")
            
            # Test individual command methods
            try:
                look_result = cli.cmd_look([])
                if look_result and len(look_result) > 10:
                    self.result.add_pass("Look Command", "Generated room description")
                else:
                    self.result.add_fail("Look Command", "No description generated")
            except Exception as e:
                self.result.add_error("Look Command", str(e))
            
            try:
                go_result = cli.cmd_go(["north"])
                if go_result:
                    self.result.add_pass("Go Command", "Movement command executed")
                else:
                    self.result.add_fail("Go Command", "No movement result")
            except Exception as e:
                self.result.add_error("Go Command", str(e))
            
            try:
                help_result = cli.cmd_help([])
                if help_result and "commands" in help_result.lower():
                    self.result.add_pass("Help Command", "Generated help text")
                else:
                    self.result.add_fail("Help Command", "No help text")
            except Exception as e:
                self.result.add_error("Help Command", str(e))
        
        except Exception as e:
            self.result.add_error("CLI Interface Test", str(e))
    
    def test_gameplay_scenarios(self):
        """Test complete gameplay scenarios."""
        print(f"\n{Fore.YELLOW}🎮 Testing Gameplay Scenarios...{Style.RESET_ALL}")
        
        try:
            if not self.world_controller:
                self.result.add_fail("Gameplay Scenarios", "WorldController not initialized")
                return
                
            # Scenario 1: Explore all rooms
            rooms_visited = []
            original_location = self.world_controller.player_location
            rooms_visited.append(original_location)
            
            # Visit tavern
            self.world_controller.move_player("east")
            rooms_visited.append(self.world_controller.player_location)
            
            # Visit market
            self.world_controller.move_player("west")
            self.world_controller.move_player("west")
            rooms_visited.append(self.world_controller.player_location)
            
            # Visit forest
            self.world_controller.move_player("east")
            self.world_controller.move_player("north")
            rooms_visited.append(self.world_controller.player_location)
            
            if len(set(rooms_visited)) >= 3:
                self.result.add_pass("Room Exploration", f"Visited {len(set(rooms_visited))} unique rooms")
            else:
                self.result.add_fail("Room Exploration", "Did not visit multiple rooms")
            
            # Scenario 2: Multi-agent interaction
            try:
                # Go back to tavern where agents are
                self.world_controller.player_location = "world/town"
                self.world_controller.move_player("east")
                
                agents = self.world_controller.get_agents_in_room()
                if len(agents) >= 2:
                    with patch('requests.post') as mock_post:
                        mock_response = Mock()
                        mock_response.json.return_value = {
                            "message": {"content": "Hello! I'm doing well, thank you for asking."}
                        }
                        mock_post.return_value = mock_response
                        
                        # Talk to first agent
                        agent1_response = agents[0].generate_response("How are you?", "tavern context")
                        
                        # Talk to second agent
                        agent2_response = agents[1].generate_response("What do you know about this place?", "tavern context")
                        
                        if agent1_response and agent2_response:
                            self.result.add_pass("Multi-Agent Interaction", "Both agents responded")
                        else:
                            self.result.add_fail("Multi-Agent Interaction", "Not all agents responded")
                else:
                    self.result.add_fail("Multi-Agent Interaction", "Not enough agents found")
            
            except Exception as e:
                self.result.add_error("Multi-Agent Interaction", str(e))
            
            # Scenario 3: Item collection and usage
            try:
                items_collected = 0
                for room in ["world/town/tavern", "world/town/market"]:
                    self.world_controller.player_location = room
                    items = self.world_controller.get_items_in_room()
                    for item in items:
                        pickup_result = self.world_controller.pickup_item(item['name'])
                        if "picked up" in pickup_result.lower():
                            items_collected += 1
                
                if items_collected > 0:
                    self.result.add_pass("Item Collection", f"Collected {items_collected} items")
                else:
                    self.result.add_fail("Item Collection", "No items collected")
            
            except Exception as e:
                self.result.add_error("Item Collection", str(e))
        
        except Exception as e:
            self.result.add_error("Gameplay Scenarios", str(e))
    
    def test_stress_scenarios(self):
        """Test stress scenarios and edge cases."""
        print(f"\n{Fore.YELLOW}⚡ Testing Stress Scenarios...{Style.RESET_ALL}")
        
        try:
            if not self.world_controller:
                self.result.add_fail("Stress Scenarios", "WorldController not initialized")
                return
                
            # Stress test 1: Many memory entries
            agents = self.world_controller.get_agents_in_room()
            if agents:
                agent = agents[0]
                for i in range(100):
                    agent.add_memory("stress_test", f"key_{i}", f"Stress test memory entry {i}")
                
                memory_count = len(agent.memory)
                if memory_count >= 100:
                    self.result.add_pass("Memory Stress Test", f"Added {memory_count} memory entries")
                else:
                    self.result.add_fail("Memory Stress Test", f"Only {memory_count} entries added")
            
            # Stress test 2: Large context simulation
            try:
                tm = TokenManager()
                large_context = []
                
                # Create messages that would exceed token limit
                for i in range(200):
                    large_context.append({
                        "role": "user",
                        "content": f"This is a very long message number {i} " * 100
                    })
                    large_context.append({
                        "role": "assistant", 
                        "content": f"This is a very long response number {i} " * 100
                    })
                
                token_count = tm.count_message_tokens(large_context)
                should_compress = tm.should_compress(large_context)
                
                if should_compress:
                    self.result.add_pass("Large Context Detection", f"{token_count} tokens detected, compression needed")
                else:
                    self.result.add_fail("Large Context Detection", "Large context not detected")
            
            except Exception as e:
                self.result.add_error("Large Context Test", str(e))
            
            # Stress test 3: Rapid save/load cycles
            try:
                for i in range(10):
                    save_name = f"stress_save_{i}"
                    self.world_controller.save_game(save_name)
                    self.world_controller.load_game(save_name)
                
                self.result.add_pass("Rapid Save/Load", "Completed 10 save/load cycles")
            
            except Exception as e:
                self.result.add_error("Rapid Save/Load", str(e))
              # Stress test 4: Invalid operations
            try:
                invalid_tests = [
                    ("Invalid movement", "invalid_direction"),
                    ("Invalid item pickup", "nonexistent_item"),
                    ("Invalid save load", "nonexistent_save")
                ]
                
                for test_name, test_param in invalid_tests:
                    try:
                        if "movement" in test_name:
                            result = self.world_controller.move_player(test_param)
                        elif "item pickup" in test_name:
                            result = self.world_controller.pickup_item(test_param)
                        elif "save load" in test_name:
                            result = self.world_controller.load_game(test_param)
                        else:
                            result = "Unknown test"
                            
                        if result and ("can't" in result.lower() or "not" in result.lower() or "invalid" in result.lower()):
                            self.result.add_pass(f"Error Handling: {test_name}", "Properly handled invalid operation")
                        else:
                            self.result.add_fail(f"Error Handling: {test_name}", "Did not handle invalid operation")
                    except Exception:
                        self.result.add_pass(f"Error Handling: {test_name}", "Exception properly raised")
            
            except Exception as e:
                self.result.add_error("Invalid Operations Test", str(e))
        
        except Exception as e:
            self.result.add_error("Stress Scenarios", str(e))


def main():
    """Run the ultimate test suite."""
    suite = UltimateTestSuite()
    result = suite.run_all_tests()
    
    # Return appropriate exit code
    if result.failed > 0 or result.errors > 0:
        sys.exit(1)
    else:
        print(f"\n{Fore.GREEN}🎉 ALL TESTS PASSED! The Ollama Dungeon system is working correctly.{Style.RESET_ALL}")
        sys.exit(0)


if __name__ == "__main__":
    main()
