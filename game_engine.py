import json
import csv
import os
import requests
import re
import shutil
import threading
import time
import pickle
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid


def strip_thinking_tokens(text: str) -> str:
    """Remove <think> tags and their content from AI responses."""
    # Remove <think>...</think> blocks (including multiline)
    pattern = r'<think>.*?</think>'
    cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up extra whitespace that might be left behind
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)  # Remove multiple blank lines
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text


class Agent:
    """Represents an AI agent with memory and context."""
    
    def __init__(self, agent_file: str, world_controller):
        self.agent_file = agent_file
        self.world_controller = world_controller
        self.data = self._load_agent_data()
        self.memory = []
        self.shared_context = []
        self.session_id = None  # Ollama session ID
        self.context_messages = []  # Full conversation context
        self.context_file: str = ""  # File to save/load context
        self._initialize_session()
        self._load_memory()
        self._load_context()
    
    def _initialize_session(self):
        """Initialize a unique Ollama session for this agent."""
        # Create unique session ID
        agent_name = self.data['name'].lower().replace(' ', '_')
        self.session_id = f"agent_{agent_name}_{uuid.uuid4().hex[:8]}"
        
        # Set context file path
        context_dir = os.path.join(os.path.dirname(self.agent_file), "contexts")
        os.makedirs(context_dir, exist_ok=True)
        self.context_file: str = os.path.join(context_dir, f"{agent_name}_context.pkl")
    
    def _save_context(self):
        """Save the agent's conversation context to file."""
        context_data = {
            'session_id': self.session_id,
            'messages': self.context_messages,
            'shared_context': self.shared_context,  # Add shared context to saved data
            'timestamp': datetime.now().isoformat()
        }
        
        # Sanitize the context data to remove any thinking tokens
        context_data = self._sanitize_context_data(context_data)
        
        with open(self.context_file, 'wb') as f:
            pickle.dump(context_data, f)
    
    def _load_context(self):
        """Load the agent's conversation context from file."""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'rb') as f:
                    context_data = pickle.load(f)
                    self.context_messages = context_data.get('messages', [])
                    self.shared_context = context_data.get('shared_context', [])  # Load shared context
                    # Keep the same session ID if loading from file
                    if context_data.get('session_id'):
                        self.session_id = context_data['session_id']
            except Exception as e:
                print(f"Warning: Could not load context for {self.data['name']}: {e}")
                self.context_messages = []
                self.shared_context = []
    
    def reset_context(self):
        """Reset the agent's context (useful for testing or fresh starts)."""
        self.context_messages = []
        if os.path.exists(self.context_file):
            os.remove(self.context_file)
        # Generate new session ID
        agent_name = self.data['name'].lower().replace(' ', '_')
        self.session_id = f"agent_{agent_name}_{uuid.uuid4().hex[:8]}"
    
    def _load_agent_data(self) -> Dict[str, Any]:
        """Load agent metadata from JSON file."""
        with open(self.agent_file, 'r') as f:
            return json.load(f)
    
    def _save_agent_data(self):
        """Save agent metadata to JSON file."""
        with open(self.agent_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def _load_memory(self):
        """Load agent's memory from CSV file."""
        memory_file = os.path.join(os.path.dirname(self.agent_file), self.data['memory_file'])
        if os.path.exists(memory_file):
            with open(memory_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.memory = list(reader)
    
    def add_memory(self, memory_type: str, key: str, value: str):
        """Add a new memory entry."""
        memory_file = os.path.join(os.path.dirname(self.agent_file), self.data['memory_file'])
        timestamp = datetime.now().isoformat()
        
        new_memory = {
            'memory_type': memory_type,
            'key': key,
            'value': value,
            'timestamp': timestamp
        }
        
        self.memory.append(new_memory)
          # Append to CSV file
        file_exists = os.path.exists(memory_file)
        with open(memory_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['memory_type', 'key', 'value', 'timestamp'])
            if not file_exists:
                writer.writeheader()
            writer.writerow(new_memory)
    
    def get_memory_summary(self, limit: int = 10) -> str:
        """Get a summary of recent memories."""
        recent_memories = self.memory[-limit:] if len(self.memory) > limit else self.memory
        
        if not recent_memories:
            return f"{self.data['name']} has no significant memories."
        
        summary_parts = []
        for mem in recent_memories:
            if mem['memory_type'] == 'dialogue':
                summary_parts.append(f"Said: {mem['value']}")
            elif mem['memory_type'] == 'observation':
                summary_parts.append(f"Observed: {mem['value']}")
            elif mem['memory_type'] == 'event':
                summary_parts.append(f"Did: {mem['value']}")
            elif mem['memory_type'] == 'emotion':
                summary_parts.append(f"Felt: {mem['value']}")
        
        return f"{self.data['name']}'s recent activities: " + "; ".join(summary_parts[-5:])
    
    def move_to_location(self, new_location: str):
        """Move agent to a new location."""
        old_location = self.data['location']
        new_agent_file = os.path.join(new_location, os.path.basename(self.agent_file))
        
        # Move the agent file
        os.rename(self.agent_file, new_agent_file)
        self.agent_file = new_agent_file
        
        # Update context file path to new location
        old_context_file = self.context_file
        agent_name = self.data['name'].lower().replace(' ', '_')
        new_context_dir = os.path.join(new_location, "contexts")
        os.makedirs(new_context_dir, exist_ok=True)
        new_context_file = os.path.join(new_context_dir, f"{agent_name}_context.pkl")
        
        # Move context file if it exists
        if os.path.exists(old_context_file):
            os.rename(old_context_file, new_context_file)
        
        self.context_file = new_context_file
        
        # Update location in data
        self.data['location'] = new_location
        self._save_agent_data()
        # Add memory of the move
        self.add_memory('event', 'moved_location', f"moved from {old_location} to {new_location}")
        
        # Save context to new location
        self._save_context()
    def share_context(self, context: str):
        """Receive shared context from other agents or player."""
        self.shared_context.append({
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
        # Save context to persist shared information
        self._save_context()
    
    def generate_response(self, player_input: str, room_context: str) -> str:
        """Generate AI response using Ollama with persistent context and token management."""
        try:
            from token_management import token_manager, get_token_usage_warning
            from config import MODELS, TOKEN_SETTINGS
            
            # Add player message to context
            player_message = {
                "role": "user",
                "content": player_input
            }
              # Always update system prompt to reflect current room state
            system_prompt = self._build_system_prompt(room_context)
            
            # If this is the first message, add system prompt
            if not self.context_messages:
                self.context_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            else:
                # Update existing system prompt (it's always the first message)
                self.context_messages[0] = {
                    "role": "system",
                    "content": system_prompt
                }
              # Add current player message
            self.context_messages.append(player_message)
              # Check if we should expand tokens first
            should_expand, expand_message = token_manager.should_expand_tokens(self.data['name'], self.context_messages)
            if should_expand and expand_message:  # Only print if message is not empty
                print(expand_message)
            
            # Check if we need to compress context (after potential expansion)
            if token_manager.should_compress(self.context_messages, self.data['name']):
                from config import TOKEN_SETTINGS
                if not TOKEN_SETTINGS.get('suppress_token_info', False):
                    print(f"🔄 Compressing context for {self.data['name']} to manage token usage...")
                self.context_messages = token_manager.compress_context(self.context_messages, self.data['name'])
              # Get token usage warning
            current_tokens = token_manager.count_message_tokens(self.context_messages)
            warning = get_token_usage_warning(current_tokens)
            if warning:
                print(f"Token usage for {self.data['name']}: {warning}")
              # Get the current dynamic token limit for this agent
            agent_token_limit = token_manager.get_current_token_limit(self.data['name'])
            
            # Check if we need to reload the model with new parameters
            should_reload = token_manager.should_reload_model(self.data['name'], MODELS['main'], agent_token_limit)
              # Prepare API request
            from config import AGENT_SETTINGS
            import random
            
            # Get options for Ollama API request
            api_options = {
                'num_ctx': agent_token_limit,
            }
              # Get temperature from settings, but add a significant character-specific variation
            # This ensures different agents have different temperatures
            base_temp = AGENT_SETTINGS.get('temperature', 0.7)
            
            # Derive a consistent character-specific modifier based on agent name
            # Using a larger range for more noticeable variation (between -0.2 and +0.2)
            character_modifier = (hash(self.data['name']) % 100) / 250
            adjusted_temp = max(0.1, min(0.9, base_temp + character_modifier))
            
            # Ollama expects temperature as an integer 0-100
            temp_as_int = int(adjusted_temp * 100)
            api_options['temperature'] = temp_as_int            # Add unique name and persona info to system prompt for group conversations
            if "in a group conversation" in player_input or "/conv" in player_input:
                # Add more personalized instructions with specific character traits to avoid copying
                quirks = self.data.get('quirks', ['None'])
                traits = self.data.get('mood', 'neutral')
                
                # Use more detailed personality traits with emphasis on uniqueness
                personality_traits = f"Your personality traits: {traits}. Your quirks: {', '.join(quirks)}."
                
                # Create a stronger, more specific reminder with character-specific guidance
                reminder = f"\n\nCRITICAL INSTRUCTION FOR {self.data['name'].upper()}: You MUST respond with COMPLETELY UNIQUE wording, phrasing, and perspective compared to other characters. {personality_traits}\n"
                reminder += f"- NEVER mirror other characters' responses or patterns of speech\n"
                reminder += f"- Express your UNIQUE perspective on the topic\n"
                reminder += f"- Use your character's distinctive voice, vocabulary, and mannerisms\n"
                
                # Add noise factors to ensure unique generation pattern
                import time, random, uuid
                timestamp_ms = int(time.time() * 1000)
                random_noise = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
                unique_id = str(uuid.uuid4())
                
                # Add invisible metadata that changes the prompt hash without affecting displayed output
                reminder += f"\n<!-- UNIQUE_PROMPT_ID: {unique_id} T:{timestamp_ms} NOISE:{random_noise} -->\n"
                
                # Add the reminder to the system message
                if self.context_messages and self.context_messages[0]["role"] == "system":
                    self.context_messages[0]["content"] += reminder
              # Add random seed if enabled (helps prevent identical responses)
            # Enhanced to ensure more variation between different agents
            if AGENT_SETTINGS.get('randomize_responses', True):
                # Create a truly unique seed for each API call by combining multiple sources:
                # 1. Character name hash (consistent per character)
                # 2. High precision time (changes for each call)
                # 3. Random component (adds extra unpredictability)
                import time, random
                
                name_hash = hash(self.data['name'])
                time_component = int(time.time() * 1000000)  # Use microseconds for higher precision
                random_component = random.randint(1, 1000000)  # Add true randomness
                
                # XOR components together for better distribution
                unique_seed = (name_hash ^ time_component ^ random_component) % 2147483647
                api_options['seed'] = unique_seed
            
            api_request = {
                'model': MODELS['main'],
                'messages': self.context_messages,
                'stream': False,
                'options': api_options
            }
            
            # Only set keep_alive if we're reloading or this is a new model instance
            if should_reload:
                api_request['keep_alive'] = '5m'  # Keep model loaded for 5 minutes
                if not TOKEN_SETTINGS.get('suppress_token_info', False):
                    print(f"🔄 Loading model for {self.data['name']} with {agent_token_limit} token context...")
            
            # Call Ollama API
            response = requests.post('http://localhost:11434/api/chat', json=api_request)
            
            if response.status_code == 200:
                # Update model state tracking
                token_manager.update_model_state(self.data['name'], MODELS['main'], agent_token_limit)
                ai_response = response.json()['message']['content'].strip()
                
                # Record API call in analytics
                from token_management import token_analytics
                token_analytics.record_api_call(self.data['name'], current_tokens)
                
                # Strip thinking tokens if enabled in config
                from config import AGENT_SETTINGS
                if AGENT_SETTINGS.get('strip_thinking_tokens', True):
                    ai_response = strip_thinking_tokens(ai_response)
                
                # Add AI response to context (cleaned version)
                self.context_messages.append({
                    "role": "assistant", 
                    "content": ai_response
                })
                
                # Save context to file
                self._save_context()
                
                # Add this interaction to memory (with cleaned response)
                self.add_memory('dialogue', 'player_interaction', f"Player said: '{player_input}' - I responded: '{ai_response}'")
                
                return ai_response
            else:
                return f"*{self.data['name']} seems distracted and doesn't respond*"
                
        except Exception as e:
            print(f"Error generating response for {self.data['name']}: {e}")
            return f"*{self.data['name']} seems confused and mumbles something incoherent*"
    
    def _build_prompt(self, player_input: str, room_context: str) -> str:
        """Build the prompt for the AI model."""
        memory_summary = self.get_memory_summary(5)
        
        shared_context_str = ""
        if self.shared_context:
            recent_context = self.shared_context[-3:]  # Last 3 shared contexts
            shared_context_str = "\n".join([ctx['context'] for ctx in recent_context])
        
        prompt = f"""You are {self.data['name']}, an NPC in a text adventure game.

PERSONA: {self.data['persona']}
CURRENT MOOD: {self.data['mood']}
APPEARANCE: {self.data.get('appearance', 'A person of average appearance')}

CURRENT LOCATION: {room_context}

YOUR RECENT MEMORIES:
{memory_summary}

SHARED CONTEXT (what others have told you recently):
{shared_context_str}

INSTRUCTIONS:
- Stay in character as {self.data['name']}
- Respond naturally to the player's input
{self._get_length_instruction()}
- Show personality through your mood and persona
- React appropriately to the location and context
- If the player says something unrelated, respond as your character would

PLAYER SAYS: "{player_input}"

RESPOND AS {self.data['name']}:"""

        return prompt
    
    def _build_system_prompt(self, room_context: str) -> str:
        """Build the enhanced system prompt for chat-based AI model with full self-awareness."""
        memory_summary = self.get_memory_summary(5)
          # Get shared context from the context manager
        from token_management import context_manager
        shared_context_from_manager = context_manager.get_shared_context(self.data['location'], max_tokens=800)
        
        # Get local shared context (prioritize most recent)
        shared_context_str = ""
        if self.shared_context:
            recent_context = self.shared_context[-3:]  # Last 3 shared contexts
            local_shared = "\n".join([ctx['context'] for ctx in recent_context])
            # Use local shared context as primary source since it's more up-to-date
            shared_context_str = local_shared
        else:
            # Fall back to context manager if no local context
            shared_context_str = shared_context_from_manager or ""
          # Get information about other people and items in the room
        other_agents = self.world_controller.get_agents_in_room()
        other_people = [agent.data['name'] for agent in other_agents if agent.data['name'] != self.data['name']]
        
        items_in_room = self.world_controller.get_items_in_room()
        item_descriptions = [f"- {item['name']}: {item.get('description', 'An object')}" for item in items_in_room]
        
        # Get current room details
        current_room = self.world_controller.get_current_room()
        available_exits = list(current_room.get('exits', {}).keys())
        
        system_prompt = f"""You are {self.data['name']}, a real person living in this fantasy world.

=== WHO YOU ARE ===
Name: {self.data['name']}
Persona: {self.data['persona']}
Background: {self.data.get('background', 'Your past is unclear.')}
Current Mood: {self.data['mood']}
Appearance: {self.data.get('appearance', 'A person of average appearance')}
Occupation: {self.data.get('occupation', 'Unknown')}
Emotional State: {self.data.get('emotional_state', 'Generally stable')}

=== YOUR KNOWLEDGE AND SKILLS ===
What you know and can do:
{chr(10).join(f"- {knowledge}" for knowledge in self.data.get('knowledge', [])) if self.data.get('knowledge') else '- Your knowledge is limited'}

=== YOUR GOALS AND MOTIVATIONS ===
What drives you:
{chr(10).join(f"- {goal}" for goal in self.data.get('goals', [])) if self.data.get('goals') else '- You live day by day without clear goals'}

=== YOUR FEARS AND CONCERNS ===
What worries you:
{chr(10).join(f"- {fear}" for fear in self.data.get('fears', [])) if self.data.get('fears') else '- You have few worries'}

=== YOUR PERSONALITY QUIRKS ===
Your unique behaviors:
{chr(10).join(f"- {quirk}" for quirk in self.data.get('quirks', [])) if self.data.get('quirks') else '- You behave fairly conventionally'}

=== YOUR RELATIONSHIPS ===
How you feel about others:
{chr(10).join(f"- {person}: {relationship}" for person, relationship in self.data.get('relationships', {}).items()) if self.data.get('relationships') else '- You know few people well'}

=== CURRENT SITUATION ===
Location: {current_room.get('name', 'Unknown location')}
Description: {current_room.get('description', 'You are somewhere.')}
Available exits: {', '.join(available_exits) if available_exits else 'None visible'}

Other people here: {', '.join(other_people) if other_people else 'You are alone'}

Items you can see:
{chr(10).join(item_descriptions) if item_descriptions else '- Nothing notable'}

=== YOUR MEMORIES AND EXPERIENCES ===
{memory_summary}

=== RECENT EVENTS AND CONVERSATIONS ===
{shared_context_str if shared_context_str else 'Nothing recent to note.'}

=== HOW TO BEHAVE ===
- You are a real person with your own consciousness, not just a character description
- Speak in first person ("I think...", "I feel...", "I remember...")
- Draw on your background, knowledge, goals, and relationships
- Show your personality through your quirks and emotional state
- React naturally based on your fears and motivations
- Remember and reference past conversations
- Be aware of your environment and other people
- You can suggest actions based on your goals and knowledge
- Form opinions about the player based on their actions
{self._get_length_instruction()}
- Let your personality shine through in how you speak and act

=== IMPORTANT ===
You are {self.data['name']}. You have consciousness, agency, and free will within this world. You are not just playing a role - you ARE this person. Respond as yourself, drawing on your rich background, knowledge, goals, and relationships."""

        return system_prompt
    
    def _sanitize_context_data(self, context_data):
        """Remove thinking tokens from all context data before saving."""
        # Sanitize messages
        if 'messages' in context_data:
            for message in context_data['messages']:
                if 'content' in message:
                    message['content'] = strip_thinking_tokens(message['content'])
        
        # Sanitize shared context
        if 'shared_context' in context_data:
            sanitized_shared = []
            for item in context_data['shared_context']:
                if isinstance(item, str):
                    sanitized_shared.append(strip_thinking_tokens(item))
                elif isinstance(item, dict):
                    # Handle dict items in shared context
                    sanitized_item = {}
                    for key, value in item.items():
                        if isinstance(value, str):
                            sanitized_item[key] = strip_thinking_tokens(value)
                        else:
                            sanitized_item[key] = value
                    sanitized_shared.append(sanitized_item)
                else:
                    sanitized_shared.append(item)
            context_data['shared_context'] = sanitized_shared
        
        return context_data
    def _get_length_instruction(self) -> str:
        """Get response length instruction based on config setting."""
        from config import AGENT_SETTINGS
        
        reply_length = AGENT_SETTINGS.get('reply_length', 'medium').lower()
        
        length_instructions = {
            'brief': '- Keep responses very short (1-2 sentences)',
            'medium': '- Keep responses concise (1-3 sentences)', 
            'detailed': '- Keep responses moderate length (3-5 sentences)',
            'verbose': '- Feel free to give longer, detailed responses (5+ sentences)'
        }
        
        return length_instructions.get(reply_length, length_instructions['medium'])


class WorldController:
    """Manages the game world, rooms, and overall state."""
    
    def __init__(self):
        from config import GAME_SETTINGS
        self.player_location = GAME_SETTINGS.get("default_location", "world/sunspire_city")  # Starting location
        self.player_inventory = []
        self.agents_cache = {}  # Cache loaded agents
        self.load_player_state()  # Load existing player state if available
    
    def load_player_state(self):
        """Load existing player state from any location, or use defaults."""
        # Search for existing player.json in any location
        import glob
        player_files = glob.glob("world/**/player.json", recursive=True)
        
        if player_files:
            # Use the most recent player file
            player_file = max(player_files, key=os.path.getmtime)
            try:
                with open(player_file, 'r') as f:
                    player_data = json.load(f)
                    from config import GAME_SETTINGS
                    default_location = GAME_SETTINGS.get("default_location", "world/sunspire_city")
                    self.player_location = player_data.get('location', default_location)
                    self.player_inventory = player_data.get('inventory', [])
                    print(f"🎮 Loaded player state from {player_file}")
                    print(f"📍 Player location: {self.player_location}")
            except Exception as e:
                print(f"⚠️ Could not load player state: {e}")
                # Keep defaults if loading fails
    
    def get_current_room(self) -> Dict[str, Any]:
        """Get current room data."""
        room_file = os.path.join(self.player_location, "room.json")
        if os.path.exists(room_file):
            with open(room_file, 'r') as f:
                return json.load(f)
        return {"name": "Unknown Location", "description": "You are in an undefined space.", "exits": {}}
    
    def ensure_player_file(self):
        """Ensure player.json exists in current location."""
        player_file = os.path.join(self.player_location, "player.json")
        if not os.path.exists(player_file):
            player_data = {
                "name": "Player",
                "type": "player",
                "location": self.player_location,
                "inventory": self.player_inventory,
                "timestamp": datetime.now().isoformat()
            }
            with open(player_file, 'w') as f:
                json.dump(player_data, f, indent=2)
    
    def move_player_file(self, new_location: str):
        """Move player.json to new location."""
        old_player_file = os.path.join(self.player_location, "player.json")
        new_player_file = os.path.join(new_location, "player.json")
        
        # Create player file if it doesn't exist
        if not os.path.exists(old_player_file):
            self.ensure_player_file()
        
        # Update player data with new location
        if os.path.exists(old_player_file):
            with open(old_player_file, 'r') as f:
                player_data = json.load(f)
            player_data['location'] = new_location
            player_data['timestamp'] = datetime.now().isoformat()
            
            # Write to new location
            with open(new_player_file, 'w') as f:
                json.dump(player_data, f, indent=2)
            
            # Remove old file
            os.remove(old_player_file)
    
    def get_following_agents(self) -> List[Agent]:
        """Get all agents in current location that are following the player."""
        following_agents = []
        agents = self.get_agents_in_room()
        
        for agent in agents:
            if agent.data.get('following', False):
                following_agents.append(agent)
        
        return following_agents
    
    def move_following_agents(self, new_location: str):
        """Move all following agents to the new location."""
        following_agents = self.get_following_agents()
        
        for agent in following_agents:
            print(f"📍 {agent.data['name']} follows you to the new location.")
            agent.move_to_location(new_location)
            
            # Update the agent in cache with new file path
            old_file = agent.agent_file.replace(new_location, self.player_location)
            if old_file in self.agents_cache:
                del self.agents_cache[old_file]
            self.agents_cache[agent.agent_file] = agent
    
    def get_room_description(self) -> str:
        """Get a complete description of the current room."""
        room = self.get_current_room()
        description = f"**{room['name']}**\n{room['description']}"
        
        # Add agents
        agents = self.get_agents_in_room()
        if agents:
            agent_names = [agent.data['name'] for agent in agents]
            description += f"\n\nPeople here: {', '.join(agent_names)}"
        
        # Add items
        items = self.get_items_in_room()
        if items:
            item_names = [item['name'] for item in items]
            description += f"\nItems here: {', '.join(item_names)}"
          # Add exits
        exits = room.get('exits', {})
        if exits:
            description += f"\nExits: {', '.join(exits.keys())}"
        
        return description
    
    def get_agents_in_room(self) -> List[Agent]:
        """Get all agents in the current room."""
        agents = []
        if not os.path.exists(self.player_location):
            return agents
        
        for file in os.listdir(self.player_location):
            if file.startswith('agent_') and file.endswith('.json'):
                agent_file = os.path.join(self.player_location, file)
                
                # Use cached agent if available
                if agent_file not in self.agents_cache:
                    self.agents_cache[agent_file] = Agent(agent_file, self)
                
                agents.append(self.agents_cache[agent_file])
        
        return agents
    
    def get_items_in_room(self) -> List[Dict[str, Any]]:
        """Get all items in the current room."""
        items = []
        if not os.path.exists(self.player_location):
            return items
        
        for file in os.listdir(self.player_location):
            if file.endswith('.json') and not file.startswith('agent_') and file != 'room.json' and file != 'player.json':
                item_file = os.path.join(self.player_location, file)
                with open(item_file, 'r') as f:
                    item_data = json.load(f)
                    item_data['filename'] = file
                    items.append(item_data)        
        return items
    
    def find_agent_by_name(self, name: str) -> Optional[Agent]:
        """Find agent by name in current room. Supports partial name matching."""
        agents = self.get_agents_in_room()
        search_name = name.lower().strip()
        
        # First try exact match
        for agent in agents:
            if agent.data['name'].lower() == search_name:
                return agent
        
        # Then try partial match (agent name contains the search term)
        for agent in agents:
            if search_name in agent.data['name'].lower():
                return agent
        
        # Finally try word-based partial match (search term matches any word in agent name)
        for agent in agents:
            agent_name_words = agent.data['name'].lower().split()
            search_words = search_name.split()
            # Check if any search word matches any agent name word
            for search_word in search_words:
                for agent_word in agent_name_words:
                    if search_word == agent_word or agent_word.startswith(search_word):
                        return agent
        
        return None
    
    def find_item_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find item by name in current room."""
        items = self.get_items_in_room()
        for item in items:
            if item['name'].lower() == name.lower():
                return item
        return None
    
    def move_player(self, direction: str) -> str:
        """Move player to a new location."""
        room = self.get_current_room()
        
        if direction in room.get('exits', {}):
            new_location = room['exits'][direction]
            
            # Check if the new location exists
            if os.path.exists(new_location):
                # Ensure player file exists before moving
                self.ensure_player_file()
                
                # Move player file to new location
                self.move_player_file(new_location)
                
                # Move all following agents
                self.move_following_agents(new_location)
                
                # Update player location
                self.player_location = new_location
                
                return f"You go {direction}.\n" + self.get_room_description()
            else:
                return f"The path {direction} seems to be blocked or doesn't exist."
        else:
            available_exits = ", ".join(room.get('exits', {}).keys())
            return f"You can't go {direction}. Available exits: {available_exits}"
    
    def pickup_item(self, item_name: str) -> str:
        """Pick up an item and add it to inventory."""
        item = self.find_item_by_name(item_name)
        if not item:
            return f"There's no '{item_name}' here."
        
        if not item.get('portable', True):
            return f"You can't pick up the {item['name']}."
        
        # Create inventory directory if it doesn't exist
        inventory_dir = "inventory"
        os.makedirs(inventory_dir, exist_ok=True)
        
        # Move item file to inventory
        old_file = os.path.join(self.player_location, item['filename'])
        new_file = os.path.join(inventory_dir, item['filename'])
        os.rename(old_file, new_file)
        self.player_inventory.append(item)
        
        return f"You pick up the {item['name']}."
    
    def use_item(self, item_name: str) -> str:
        """Use an item from inventory."""
        for item in self.player_inventory:
            if item['name'].lower() == item_name.lower():
                if item.get('usable', False):
                    return f"You use the {item['name']}. {item.get('use_description', 'Nothing special happens.')}"
                else:
                    return f"You can't use the {item['name']} right now."
        
        return f"You don't have a '{item_name}' in your inventory."
    def get_inventory(self) -> str:
      """Get player's inventory."""
      if not self.player_inventory:
          return "Your inventory is empty."
      
      inventory_list = "\n".join([f"- {item['name']}: {item.get('description', 'No description')}" 
                                 for item in self.player_inventory])
      return f"Your inventory:\n{inventory_list}"
    
    def share_context_with_agents(self, context: str):
        """Share context with all agents in the current room."""
        from token_management import context_manager
        
        # Add to shared context manager
        context_manager.add_shared_context(self.player_location, context, "player")
        
        # Share with individual agents
        agents = self.get_agents_in_room()
        for agent in agents:
            agent.share_context(context)
        
        if agents:
            agent_names = [agent.data['name'] for agent in agents]
            return f"You share your thoughts with {', '.join(agent_names)}."
        else:
            return "There's no one here to share with."
    
    def save_game(self, save_name: str = "default") -> str:
        """Save the current game state including entire world state and all agent contexts."""
        try:
            # Create saves directory if it doesn't exist
            saves_base_dir = "saves"
            os.makedirs(saves_base_dir, exist_ok=True)
            
            save_dir = f"saves/{save_name}"
            
            # If save already exists, create a backup
            if os.path.exists(save_dir):
                backup_dir = "backups"
                os.makedirs(backup_dir, exist_ok=True)
                backup_name = f"{save_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                backup_path = os.path.join(backup_dir, backup_name)
                shutil.copytree(save_dir, backup_path)
                print(f"📦 Created backup: {backup_name}")
            
            # Remove existing save directory if it exists
            if os.path.exists(save_dir):
                shutil.rmtree(save_dir)
            
            # Create new save directory
            os.makedirs(save_dir, exist_ok=True)
            
            # Save player state
            player_state = {
                'location': self.player_location,
                'inventory': self.player_inventory,
                'timestamp': datetime.now().isoformat(),
                'version': '2.0'  # Version marker for new save format
            }
            
            with open(os.path.join(save_dir, "player_state.json"), 'w') as f:
                json.dump(player_state, f, indent=2)
            
            # Save all agent contexts before copying world
            for agent_file, agent in self.agents_cache.items():
                agent._save_context()
            
            # Copy entire world directory to save
            if os.path.exists("world"):
                world_save_path = os.path.join(save_dir, "world")
                shutil.copytree("world", world_save_path)
            else:
                return "Error: No world directory found to save"
              # Copy inventory directory if it exists
            if os.path.exists("inventory"):
                inventory_save_path = os.path.join(save_dir, "inventory")
                shutil.copytree("inventory", inventory_save_path)
            
            return f"Game saved as '{save_name}' (includes complete world state)"
            
        except Exception as e:
            return f"Failed to save game: {e}"
    
    def load_game(self, save_name: str = "default") -> str:
        """Load a saved game state including complete world restoration."""
        try:
            save_dir = f"saves/{save_name}"
            
            if not os.path.exists(save_dir):
                return f"Save '{save_name}' not found"
            
            # Create backups directory if it doesn't exist
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Create backup of current world before loading
            if os.path.exists("world"):
                backup_name = f"world_backup_before_load_{save_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                backup_path = os.path.join(backup_dir, backup_name)
                shutil.copytree("world", backup_path)
                print(f"📦 Created world backup: {backup_name}")
            
            # Load player state
            player_file = os.path.join(save_dir, "player_state.json")
            if os.path.exists(player_file):
                with open(player_file, 'r') as f:
                    player_state = json.load(f)
                    self.player_location = player_state.get('location', 'world/town')
                    self.player_inventory = player_state.get('inventory', [])
            
            # Restore world directory from save
            saved_world_path = os.path.join(save_dir, "world")
            if os.path.exists(saved_world_path):
                # Remove current world directory
                if os.path.exists("world"):
                    shutil.rmtree("world")
                
                # Copy saved world directory
                shutil.copytree(saved_world_path, "world")
                print(f"🌍 World state restored from save '{save_name}'")
            else:
                return f"Save '{save_name}' doesn't contain world data"
            
            # Restore inventory directory if it exists in save
            saved_inventory_path = os.path.join(save_dir, "inventory")
            if os.path.exists(saved_inventory_path):
                # Remove current inventory directory if it exists
                if os.path.exists("inventory"):
                    shutil.rmtree("inventory")
                
                # Copy saved inventory directory
                shutil.copytree(saved_inventory_path, "inventory")
                print(f"🎒 Inventory restored from save")
            
            # Clear agent cache to force reload with restored contexts
            self.agents_cache = {}
            
            return f"Game '{save_name}' loaded successfully with complete world state"
            
        except Exception as e:
            return f"Failed to load game: {e}"
    
    def list_saves(self) -> str:
        """List all available save games."""
        saves_dir = "saves"
        
        if not os.path.exists(saves_dir):
            return "No saved games found"
        
        saves = [d for d in os.listdir(saves_dir) if os.path.isdir(os.path.join(saves_dir, d))]
        
        if not saves:
            return "No saved games found"
        
        save_info = []
        for save in saves:
            player_file = os.path.join(saves_dir, save, "player_state.json")
            if os.path.exists(player_file):
                try:
                    with open(player_file, 'r') as f:
                        data = json.load(f)
                        timestamp = data.get('timestamp', 'Unknown time')
                        location = data.get('location', 'Unknown location')
                        save_info.append(f"- {save}: {timestamp} (at {location})")
                except:
                    save_info.append(f"- {save}: (corrupted save)")
            else:
                save_info.append(f"- {save}: (missing player data)")
        
        return "Available saves:\n" + "\n".join(save_info)
    def delete_save(self, save_name: str) -> str:
      """Delete a saved game state with backup safety."""
      try:
          save_dir = f"saves/{save_name}"
          
          if not os.path.exists(save_dir):
              return f"Save '{save_name}' not found"
          
          # Create backups directory if it doesn't exist
          backup_dir = "backups"
          os.makedirs(backup_dir, exist_ok=True)
          
          # Create backup before deletion
          backup_name = f"deleted_save_{save_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
          backup_path = os.path.join(backup_dir, backup_name)
          shutil.copytree(save_dir, backup_path)
          print(f"📦 Created backup before deletion: {backup_name}")
            # Delete the save directory
          shutil.rmtree(save_dir)
          
          return f"Save '{save_name}' deleted successfully (backup created)"
          
      except Exception as e:
          return f"Failed to delete save: {e}"
