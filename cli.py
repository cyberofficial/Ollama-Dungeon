import os
import sys
import shutil
from typing import List
from colorama import init, Fore, Style
import game_engine  # Import the entire module first
from game_engine import strip_thinking_tokens  # Then import specific functions
# Import and rename for clarity
WorldController = game_engine.WorldController  # Explicit assignment to fix VS Code issue
from token_management import token_manager, context_manager
from config import MODELS, TOKEN_SETTINGS

# Initialize colorama for cross-platform colored output
init()

class GameCLI:
    """Command-line interface for Ollama Dungeon."""
    
    def __init__(self):
        self.world: game_engine.WorldController = WorldController()
        self.running = True
        # Conversation endless mode state
        self.endless_mode = False
        self.endless_participants = []  # List of participant names in order
        self.endless_topic = ""
        self.endless_agents = []  # List of agent objects
        self.commands = {
            'look': self.cmd_look,
            'l': self.cmd_look,
            'go': self.cmd_go,
            'move': self.cmd_go,
            'say': self.cmd_say,
            'sayto': self.cmd_say,
            'talk': self.cmd_say,
            'conv': self.cmd_conv,
            'conversation': self.cmd_conv,
            'agents': self.cmd_agents,
            'people': self.cmd_agents,
            'memory': self.cmd_memory,
            'summarize': self.cmd_summarize,
            'share': self.cmd_summarize,
            'inventory': self.cmd_inventory,
            'inv': self.cmd_inventory,
            'pickup': self.cmd_pickup,
            'take': self.cmd_pickup,
            'use': self.cmd_use,
            'follow': self.cmd_follow,
            'stay': self.cmd_stay,
            'help': self.cmd_help,
            'save': self.cmd_save,
            'load': self.cmd_load,
            'saves': self.cmd_list_saves,
            'delete': self.cmd_delete_save,
            'reset': self.cmd_reset_agent,
            'tokens': self.cmd_tokens,
            'compress': self.cmd_compress_agent,
            'compress_all': self.cmd_compress_all,
            'status': self.cmd_system_status,
            'model_state': self.cmd_model_state,
            'dialog': self.cmd_dialog,
            'endconv': self.cmd_endconv,
            'invite': self.cmd_invite,
            'remove': self.cmd_remove,
            'quit': self.cmd_quit,
            'exit': self.cmd_quit,
            'q': self.cmd_quit,
            'analytics': self.cmd_analytics,
            'model_state': self.cmd_model_state
        }
    
    def print_colored(self, text: str, color: str = Fore.WHITE):
        """Print colored text."""
        print(f"{color}{text}{Style.RESET_ALL}")
    
    def print_title(self):
        """Print the game title."""
        from config import GAME_SETTINGS
        
        # Get customized title and subtitle from config
        game_title = GAME_SETTINGS.get("title", "OLLAMA DUNGEON")
        game_subtitle = GAME_SETTINGS.get("subtitle", "A Text Adventure Powered by Local AI")
        
        # Box width (internal content width)
        box_width = 62
        
        # Center the title and subtitle in the box
        centered_title = game_title.center(box_width)
        centered_subtitle = game_subtitle.center(box_width)
        
        # Create the title box with the custom text
        title = f"""
╔══════════════════════════════════════════════════════════════╗
║{centered_title}║
║                                                              ║
║{centered_subtitle}║
╚══════════════════════════════════════════════════════════════╝
        """
        self.print_colored(title, Fore.CYAN)
        self.print_colored("Type '/help' for commands or '/quit' to exit.", Fore.YELLOW)
        print()

    def run(self):
        """Main game loop."""
        self.print_title()
        
        # Show initial room description
        self.print_colored(self.world.get_room_description(), Fore.GREEN)
        
        while self.running:
            try:
                # Get user input
                user_input = input(f"{Fore.BLUE}> {Style.RESET_ALL}").strip()                
                if not user_input:
                    continue
                  # Parse command
                if user_input.startswith('/'):
                    self.handle_command(user_input[1:])
                else:
                    self.print_colored("Commands must start with '/'. Type '/help' for available commands.", Fore.RED)
            except KeyboardInterrupt:
                self.print_colored("\nGoodbye!", Fore.YELLOW)
                break
            except EOFError:
                break
    
    def handle_command(self, command_input: str):
        """Handle a command input."""
        parts = command_input.split()
        if not parts:
            return
        
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if command in self.commands:
            try:
                result = self.commands[command](args)
                if result:
                    self.print_colored(result, Fore.WHITE)
            except Exception as e:
                self.print_colored(f"Error executing command: {e}", Fore.RED)
        else:
            self.print_colored(f"Unknown command: {command}. Type '/help' for available commands.", Fore.RED)
    
    def cmd_look(self, args: List[str]) -> str:
        """Look around the current room."""
        return self.world.get_room_description()
    
    def cmd_go(self, args: List[str]) -> str:
        """Move to another location."""
        if not args:
            return "Go where? Specify a direction (e.g., '/go north')."
        
        direction = args[0].lower()
        
        # Move the player first
        result = self.world.move_player(direction)
        
        # If in endless mode and move was successful, handle agent removal for non-following agents
        if self.endless_mode and "You go" in result:
            self._handle_endless_mode_location_change()
        
        return result
    
    def cmd_say(self, args: List[str]) -> str:
        """Talk to an agent or handle endless conversation mode."""
        if not args:
            if self.endless_mode:
                return "In endless mode: Use '/say <message>' to talk to everyone, or '/say <agent(s)> <message>' for specific targets."
            else:
                return "Say what to whom? Use '/say <agent_name> <message>'."
        
        if self.endless_mode:
            return self._handle_endless_say(args)
        else:
            return self._handle_normal_say(args)
    
    def _handle_normal_say(self, args: List[str]) -> str:
        """Handle normal say command (non-endless mode)."""
        if len(args) < 2:
            return "Say what to whom? Use '/say <agent_name> <message>'."
        
        agent_name = args[0]
        message = " ".join(args[1:])
        
        agent = self.world.find_agent_by_name(agent_name)
        if not agent:
            return f"There's no one named '{agent_name}' here."
          # Get room context for the agent
        room_context = self.world.get_room_description()
        
        self.print_colored(f"You say to {agent.data['name']}: \"{message}\"", Fore.CYAN)
        
        # Generate AI response
        response = agent.generate_response(message, room_context)
        
        return f"{Fore.MAGENTA}{agent.data['name']} says: \"{response}\"{Style.RESET_ALL}"
    
    def _handle_endless_say(self, args: List[str]) -> str:
        """Handle say command in endless conversation mode."""
        # Check if first argument looks like agent targeting
        first_arg = args[0].lower()
        agent_names = [agent.data['name'].lower() for agent in self.endless_agents]
        
        # Check if first arg is targeting
        is_targeting = False
        
        if first_arg in agent_names:
            # Single agent targeting: /say alice Hello
            is_targeting = True
        elif ',' in first_arg:            # Potential multiple agent targeting: /say alice,bob Hello
            # Only treat as targeting if the first part before comma is a valid agent name
            first_target = first_arg.split(',')[0].strip()
            if first_target in agent_names:
                is_targeting = True
        
        if is_targeting:
            # Targeted message
            if len(args) < 2:
                return "What do you want to say?"
              # Parse targets
            if ',' in first_arg:
                target_names = [name.strip() for name in first_arg.split(',')]
            else:
                target_names = [first_arg]
            
            # Get the message content
            message = " ".join(args[1:])
            
            # Validate all targets exist in endless mode participants
            invalid_targets = []
            for target in target_names:
                if target not in agent_names:
                    invalid_targets.append(target)
            
            if invalid_targets:
                valid_targets = [name for name in agent_names]
                return f"Invalid target(s): {', '.join(invalid_targets)}. Valid targets: {', '.join(valid_targets)}"
            
            # Display player's message
            target_display = ', '.join([name.title() for name in target_names])
            self.print_colored(f"You say to {target_display}: \"{message}\"", Fore.CYAN)
            print()
            
            # Share context with all agents (they all hear it)
            for agent in self.endless_agents:
                agent.share_context(f"In group conversation, Player said to {target_display}: \"{message}\"")
                agent.add_memory('dialogue', 'player_conversation', f"Player said to {target_display}: {message}")
            
            # Only targeted agents respond
            for target_name in target_names:
                for agent in self.endless_agents:
                    if agent.data['name'].lower() == target_name:
                        response = self._generate_endless_response(agent, message, target_names)
                        self.print_colored(f"🗣️ **{agent.data['name']}**: {response}", Fore.MAGENTA)
                        print()
                        
                        # Share response with all other agents
                        for other_agent in self.endless_agents:
                            if other_agent != agent:
                                other_agent.share_context(f"In group conversation, {agent.data['name']} said: \"{response}\"")
                                other_agent.add_memory('dialogue', 'agent_conversation', f"Heard {agent.data['name']} say: {response}")
                        
                        agent.add_memory('dialogue', 'agent_conversation', f"Said in group conversation: {response}")
                        break
            
            return ""  # Already printed responses above
        
        else:
            # No targeting - everyone replies in order
            message = " ".join(args)
            
            self.print_colored(f"You say: \"{message}\"", Fore.CYAN)
            print()
            
            # Share context with all agents
            for agent in self.endless_agents:
                agent.share_context(f"In group conversation, Player said: \"{message}\"")
                agent.add_memory('dialogue', 'player_conversation', f"Player said: {message}")
            
            # Each agent responds in order
            for participant_name in self.endless_participants:
                if participant_name != 'player':
                    for agent in self.endless_agents:
                        if agent.data['name'].lower() == participant_name:
                            response = self._generate_endless_response(agent, message, [])
                            self.print_colored(f"🗣️ **{agent.data['name']}**: {response}", Fore.MAGENTA)
                            print()
                            
                            # Share response with all other agents
                            for other_agent in self.endless_agents:
                                if other_agent != agent:
                                    other_agent.share_context(f"In group conversation, {agent.data['name']} said: \"{response}\"")
                                    other_agent.add_memory('dialogue', 'agent_conversation', f"Heard {agent.data['name']} say: {response}")
                            
                            agent.add_memory('dialogue', 'agent_conversation', f"Said in group conversation: {response}")
                            break
            
            return ""  # Already printed responses above

    def _generate_endless_response(self, agent, message: str, target_names = None, is_dialog: bool = False) -> str:
        """Generate a response for an agent in endless conversation mode."""
        # Handle both agent objects and agent names for dialog mode
        if isinstance(agent, str):
            # For dialog mode, agent is passed as a string name
            agent_name = agent
            agent_obj = self.world.find_agent_by_name(agent_name)
            if not agent_obj:
                return f"*{agent_name.title()} is not available*"
        else:
            # Normal mode, agent is an object
            agent_obj = agent
            agent_name = agent.data['name']
        
        # Create list of other participants for context
        other_participants = [name.title() if name != 'player' else 'Player' 
                            for name in self.endless_participants if name != agent_name.lower()]
        others_str = ', '.join(other_participants)
        
        if is_dialog:
            # Dialog mode - agent responding in automated conversation
            prompt = message  # Message is already the full dialog prompt
        elif target_names:
            # Targeted message
            targets_str = ', '.join([name.title() for name in target_names])
            prompt = f"""You are {agent_name} in a group conversation about: {self.endless_topic}
            
Other participants: {others_str}

Player just said to {targets_str}: "{message}"

Respond naturally as {agent_name}. Stay focused on the conversation topic: {self.endless_topic}."""
        else:
            # General message to everyone
            prompt = f"""You are {agent_name} in a group conversation about: {self.endless_topic}
            
Other participants: {others_str}

Player just said: "{message}"

Respond naturally as {agent_name}. Stay focused on the conversation topic: {self.endless_topic}."""
        
        try:
            # Generate response
            response = agent_obj.generate_response(prompt, self.world.get_room_description())
            
            if not response or response.strip() == "":
                response = f"*{agent_name} seems lost in thought*"
                
        except Exception as e:
            print(f"⚠️ {agent_name} had trouble responding: {e}")
            response = f"*{agent_name} looks confused and remains silent*"
        
        # Strip thinking tokens and clean response
        response = strip_thinking_tokens(response)
        cleaned_response = self._clean_conversation_response(response, agent_name, "everyone")
        
        return cleaned_response
    def cmd_agents(self, args: List[str]) -> str:
        """List all agents in the current room."""
        agents = self.world.get_agents_in_room()
        
        if not agents:
            return "There's no one else here."
        
        agent_list = []
        for agent in agents:
            mood_info = f"({agent.data['mood']})" if agent.data.get('mood') else ""
            agent_list.append(f"- {agent.data['name']} {mood_info}: {agent.data.get('appearance', 'A person')}")
        
        return "People here:\n" + "\n".join(agent_list)
    
    def cmd_memory(self, args: List[str]) -> str:
        """Show an agent's memory summary."""
        if not args:
            return "Whose memory? Use '/memory <agent_name>'."
        
        agent_name = args[0]
        agent = self.world.find_agent_by_name(agent_name)        
        if not agent:
            return f"There's no one named '{agent_name}' here."
        
        return agent.get_memory_summary()
    
    def cmd_summarize(self, args: List[str]) -> str:
        """Share context with specific agents or all agents in the room."""
        if not args:
            return "Share what? Use '/share [target(s)] <message>' or '/share <message>' for everyone."
        
        # Get all agents in room for reference
        agents_in_room = self.world.get_agents_in_room()
        if not agents_in_room:
            return "There's no one here to share with."
        
        agent_names = [agent.data['name'].lower() for agent in agents_in_room]
        
        # Check if first argument is a target specification
        first_arg = args[0].lower()
        targets = []
        context_start_index = 1
        
        # Parse different target formats
        if first_arg == "all":
            # /share all <message>
            if len(args) < 2:
                return "What should I share with everyone? Provide a message after 'all'."
            targets = "all"
            context_start_index = 1
        elif "," in first_arg:
            # /share alice,bob <message>
            if len(args) < 2:
                return "What should I share? Provide a message after the target list."
            target_names = [name.strip().lower() for name in first_arg.split(",")]
            # Verify all target names exist
            valid_targets = []
            for target_name in target_names:
                if target_name in agent_names:
                    valid_targets.append(target_name)
                else:
                    return f"There's no one named '{target_name}' here."
            targets = valid_targets
            context_start_index = 1
        elif first_arg in agent_names:
            # /share alice <message> - but only if there's a message after it
            if len(args) < 2:
                return f"What should I share with {args[0]}? Provide a message."
            targets = [first_arg]
            context_start_index = 1
        else:
            # First argument is not a recognized target, treat entire input as message for all
            targets = "all"
            context_start_index = 0
        
        # Extract the context message
        context = " ".join(args[context_start_index:])
        
        if not context.strip():
            return "The message cannot be empty."
        
        # Handle sharing based on targets
        if targets == "all":
            # Share with all agents in room
            result = self.world.share_context_with_agents(context)
            if "You share your thoughts with" in result:
                result += f"\n📢 Shared with all: \"{context}\""
            return result
        else:
            # Share with specific agents
            target_agents = []
            
            for target_name in targets:
                target_agent = self.world.find_agent_by_name(target_name)
                if target_agent:
                    target_agents.append(target_agent)
                else:
                    return f"There's no one named '{target_name}' here."
            
            if not target_agents:
                return "No valid targets found to share with."
            
            # Share context with specific agents
            for agent in target_agents:
                agent.share_context(context)
            
            # Also add to shared context manager for the location
            from token_management import context_manager
            context_manager.add_shared_context(self.world.player_location, context, "player")
            
            target_names = [agent.data['name'] for agent in target_agents]
            if len(target_agents) == 1:
                result = f"You quietly share your thoughts with {target_names[0]}."
                result += f"\n📢 Shared with {target_names[0]}: \"{context}\""
            else:
                result = f"You quietly share your thoughts with {', '.join(target_names)}."
                result += f"\n📢 Shared with {', '.join(target_names)}: \"{context}\""
            
            return result
    
    def cmd_inventory(self, args: List[str]) -> str:
        """Show player inventory."""
        return self.world.get_inventory()
    
    def cmd_pickup(self, args: List[str]) -> str:
        """Pick up an item."""
        if not args:
            return "Pick up what? Use '/pickup <item_name>'."
        
        item_name = " ".join(args)
        return self.world.pickup_item(item_name)
    
    def cmd_use(self, args: List[str]) -> str:
        """Use an item from inventory."""
        if not args:
            return "Use what? Use '/use <item_name>'."
        
        item_name = " ".join(args)
        return self.world.use_item(item_name)
    
    def cmd_follow(self, args: List[str]) -> str:
        """Have an agent follow you."""
        if not args:
            return "Who should follow you? Use '/follow <agent_name>'."
        
        agent_name = args[0]
        agent = self.world.find_agent_by_name(agent_name)
        
        if not agent:
            return f"There's no one named '{agent_name}' here."        
        agent.data['following'] = True
        agent._save_agent_data()
        agent.add_memory('event', 'following_player', 'agreed to follow the player')
        return f"{agent.data['name']} agrees to follow you."

    def cmd_stay(self, args: List[str]) -> str:
        """Have an agent stop following you and stay in current location."""
        if not args:
            return "Who should stay? Use '/stay <agent_name>'."
        
        agent_name = args[0]
        agent = self.world.find_agent_by_name(agent_name)
        
        if not agent:
            return f"There's no one named '{agent_name}' here."
        
        if not agent.data.get('following', False):
            return f"{agent.data['name']} is not following you."
        
        agent.data['following'] = False
        agent._save_agent_data()
        agent.add_memory('event', 'stopped_following_player', 'decided to stay in current location')
        return f"{agent.data['name']} will stay here and no longer follow you."

    def cmd_help(self, args: List[str]) -> str:
        """Show available commands."""
        help_text = f"""
{Fore.CYAN}Available Commands:{Style.RESET_ALL}

{Fore.GREEN}Movement & Exploration:{Style.RESET_ALL}
  /look, /l                 - Describe current room
  /go <direction>           - Move to another location (north, south, east, west, etc.)
  /move <direction>         - Alternative to /go

{Fore.GREEN}Interaction:{Style.RESET_ALL}  /say <agent> <message>    - Talk to an agent
  /sayto <agent> <message>  - Alternative to /say (for immersion)
  /talk <agent> <message>   - Alternative to /say  /conv <agent1,agent2[,player]> [turns] <topic> - Make agents talk (optionally include player)
                              Omit turns for endless mode (end with /endconv)
  /conversation             - Alternative to /conv
  /dialog <agent1,agent2> <exchanges> - Automated dialog between 2 agents (endless mode only)
  /endconv                  - End an endless conversation (only during your turn)
  /agents, /people          - List people in current room
  /memory <agent>           - Show an agent's memory summary
  /summarize [context]      - Share context with agents in room
  /share [context]          - Alternative to /summarize
  /follow <agent>           - Have agent follow you
  /stay <agent>             - Have agent stop following you

{Fore.GREEN}Inventory:{Style.RESET_ALL}
  /inventory, /inv          - View your inventory
  /pickup <item>            - Pick up an item
  /take <item>              - Alternative to /pickup
  /use <item>               - Use an item from inventory

{Fore.GREEN}System:{Style.RESET_ALL}
  /tokens [agent]           - Show token usage (overall or specific agent)
  /analytics [agent]        - Show detailed token analytics and usage history
  /model_state [agent]      - Show current model state and context size
  /compress <agent>         - Manually compress an agent's context
  /compress_all             - Compress context for all agents in room
  /status                   - Show system status and connectivity
  /save [name]              - Save game state
  /load [name]              - Load game state
  /saves                    - List saved games
  /delete <save_name>       - Delete a saved game
  /reset <agent>            - Reset agent's memory and context
  /help                     - Show this help message
  /quit, /exit, /q          - Exit the game

{Fore.YELLOW}Tips:{Style.RESET_ALL}
- Agent responses are generated by AI and may take a moment
- Agents have their own memories and personalities
- The world persists between sessions
- Try talking to agents to learn about the world
- Use /share to give context to all agents in the current room
        """
        return help_text
    
    def cmd_quit(self, args: List[str]) -> str:
        """Quit the game."""
        self.running = False
        return "Farewell, adventurer!"
    
    def cmd_save(self, args: List[str]) -> str:
        """Save the current game state."""
        save_name = args[0] if args else "default"
        return self.world.save_game(save_name)
    
    def cmd_load(self, args: List[str]) -> str:
        """Load a saved game state."""
        save_name = args[0] if args else "default"
        result = self.world.load_game(save_name)
        if "successfully" in result:
            # Show new location after loading
            return result + "\n\n" + self.world.get_room_description()
        return result
    
    def cmd_list_saves(self, args: List[str]) -> str:
        """List all available save games."""
        return self.world.list_saves()
    
    def cmd_delete_save(self, args: List[str]) -> str:
        """Delete a saved game."""
        if not args:
            return "Delete which save? Use '/delete <save_name>'."
        
        save_name = args[0]
        return self.world.delete_save(save_name)
    
    def cmd_reset_agent(self, args: List[str]) -> str:
        """Reset an agent's context/memory."""
        if not args:
            return "Reset which agent? Use '/reset <agent_name>'."
        
        agent_name = args[0]
        agent = self.world.find_agent_by_name(agent_name)
        
        if not agent:
            return f"There's no one named '{agent_name}' here."
        
        agent.reset_context()
        return f"{agent.data['name']}'s memory and context have been reset."
    
    def cmd_show_tokens(self, args: List[str]) -> str:
        """Show token usage information."""
        if args and len(args) > 0:
            # Show tokens for specific agent
            agent_name = args[0]
            agent = self.world.find_agent_by_name(agent_name)
            
            if not agent:
                return f"There's no one named '{agent_name}' here."
            
            from token_management import token_manager
            token_count = token_manager.count_message_tokens(agent.context_messages)
            
            return f"""Token usage for {agent.data['name']}:
- Current context: {token_count} tokens
- Memory entries: {len(agent.memory)}
- Shared context entries: {len(agent.shared_context)}
- Status: {'⚠️ High' if token_count > 30000 else '✅ Normal'}"""
        else:
            # Show overall token usage
            agents = self.world.get_agents_in_room()
            total_tokens = 0
            agent_info = []
            
            from token_management import token_manager
            
            for agent in agents:
                tokens = token_manager.count_message_tokens(agent.context_messages)
                total_tokens += tokens
                agent_info.append(f"- {agent.data['name']}: {tokens} tokens")
            
            result = f"Token Usage Summary:\n"
            result += f"Total tokens in room: {total_tokens}\n"
            if agent_info:                result += "\nBy agent:\n" + "\n".join(agent_info)
            
            return result
    
    def cmd_tokens(self, args: List[str]) -> str:
        """Show comprehensive token usage information."""
        if args and len(args) > 0:
            # Show tokens for specific agent
            agent_name = args[0]
            agent = self.world.find_agent_by_name(agent_name)
            
            if not agent:
                return f"There's no one named '{agent_name}' here."
            
            from token_management import token_manager, get_token_usage_warning, estimate_tokens_remaining
            token_count = token_manager.count_message_tokens(agent.context_messages)
            current_limit = token_manager.get_current_token_limit(agent.data['name'])
            warning = get_token_usage_warning(token_count)
            remaining = estimate_tokens_remaining(token_count)
            
            status_color = Fore.GREEN if token_count < 25000 else Fore.YELLOW if token_count < 35000 else Fore.RED
            
            result = f"""Token usage for {agent.data['name']}:
{status_color}- Current context: {token_count:,} tokens{Style.RESET_ALL}
- Current token limit: {current_limit:,} tokens
- Memory entries: {len(agent.memory)}
- Shared context entries: {len(agent.shared_context)}
- Tokens until compression: {remaining:,}
- Status: {'⚠️ High' if token_count > 30000 else '✅ Normal'}"""
            
            if warning:
                result += f"\n{Fore.YELLOW}- Warning: {warning}{Style.RESET_ALL}"
            
            # Show expansion info
            threshold = int(current_limit * 0.9)
            if token_count >= threshold:
                result += f"\n{Fore.CYAN}- Next expansion at: {threshold:,} tokens (reached){Style.RESET_ALL}"
            else:
                result += f"\n{Fore.CYAN}- Next expansion at: {threshold:,} tokens{Style.RESET_ALL}"
            
            return result
        else:
            # Show comprehensive token usage across all agents
            agents = self.world.get_agents_in_room()
            
            if not agents:
                return "No agents in current room to monitor."
            
            from token_management import token_manager, monitor_token_usage_across_agents
            
            stats = monitor_token_usage_across_agents(agents)
            
            result = f"{Fore.CYAN}Comprehensive Token Usage Summary:{Style.RESET_ALL}\n"
            result += f"Total tokens in room: {stats['total_tokens']:,}\n"
            result += f"Agents monitored: {stats['agent_count']}\n"
            
            if stats['compression_needed']:
                result += f"{Fore.RED}⚠️ Compression needed for: {', '.join(stats['high_usage_agents'])}{Style.RESET_ALL}\n"
            
            result += "\nBy agent:\n"
            for agent_stat in stats['agent_stats']:
                color = Fore.GREEN if agent_stat['status'] == '✅ Normal' else Fore.YELLOW if agent_stat['status'] == '🟡 Medium' else Fore.RED
                result += f"{color}- {agent_stat['name']}: {agent_stat['tokens']:,} tokens {agent_stat['status']}{Style.RESET_ALL}\n"
            
            return result
    
    def cmd_compress_agent(self, args: List[str]) -> str:
        """Manually compress an agent's context."""
        if not args:
            return "Compress which agent? Use '/compress <agent_name>'."
        
        agent_name = args[0]
        agent = self.world.find_agent_by_name(agent_name)
        
        if not agent:
            return f"There's no one named '{agent_name}' here."
        
        from token_management import token_manager
        
        old_count = token_manager.count_message_tokens(agent.context_messages)
        agent.context_messages = token_manager.compress_context(agent.context_messages, agent.data['name'])
        new_count = token_manager.count_message_tokens(agent.context_messages)
        agent._save_context()
        
        return f"Compressed {agent.data['name']}'s context: {old_count} -> {new_count} tokens (saved {old_count - new_count} tokens)"
    
    def cmd_compress_all(self, args: List[str]) -> str:
        """Compress context for all agents in the room."""
        agents = self.world.get_agents_in_room()
        
        if not agents:
            return "No agents in current room to compress."
        
        from token_management import token_manager
        
        results = []
        total_saved = 0
        
        for agent in agents:
            old_count = token_manager.count_message_tokens(agent.context_messages)
            if old_count > TOKEN_SETTINGS['compression_threshold'] * 0.5:  # Only compress if over 50% threshold
                agent.context_messages = token_manager.compress_context(agent.context_messages, agent.data['name'])
                new_count = token_manager.count_message_tokens(agent.context_messages)
                saved = old_count - new_count
                total_saved += saved
                agent._save_context()
                results.append(f"- {agent.data['name']}: {old_count:,} → {new_count:,} tokens (saved {saved:,})")
            else:
                results.append(f"- {agent.data['name']}: {old_count:,} tokens (no compression needed)")
        
        result = f"Compressed contexts for {len(agents)} agents:\n"
        result += "\n".join(results)
        if total_saved > 0:
            result += f"\n\nTotal tokens saved: {total_saved:,}"
        
        return result
    
    def cmd_system_status(self, args: List[str]) -> str:
        """Show overall system status."""
        from token_management import token_manager, context_manager
        import requests
        
        status = f"""
{Fore.CYAN}=== SYSTEM STATUS ==={Style.RESET_ALL}

{Fore.GREEN}World State:{Style.RESET_ALL}
- Current location: {self.world.player_location}
- Agents in room: {len(self.world.get_agents_in_room())}
- Items in room: {len(self.world.get_items_in_room())}
- Inventory items: {len(self.world.player_inventory)}

{Fore.GREEN}AI Models:{Style.RESET_ALL}"""
        
        # Check Ollama connectivity
        try:
            response = requests.get('http://localhost:11434/api/version', timeout=3)
            if response.status_code == 200:
                status += "\n- Ollama: ✅ Connected"
                
                # Check if models are available
                try:
                    from config import MODELS
                    models_response = requests.get('http://localhost:11434/api/tags', timeout=3)
                    if models_response.status_code == 200:
                        available_models = [m['name'] for m in models_response.json().get('models', [])]
                        for model_type, model_name in MODELS.items():
                            if model_name in available_models:
                                status += f"\n- {model_name} ({model_type}): ✅ Available"
                            else:
                                status += f"\n- {model_name} ({model_type}): ❌ Not found"
                except:
                    status += "\n- Model check: ❌ Failed"
            else:
                status += "\n- Ollama: ❌ Connection failed"
        except:
            status += "\n- Ollama: ❌ Not responding"
        
        # Token usage summary
        agents = self.world.get_agents_in_room()
        total_tokens = 0
        high_usage_agents = []
        
        for agent in agents:
            tokens = token_manager.count_message_tokens(agent.context_messages)
            total_tokens += tokens
            if tokens > 25000:
                high_usage_agents.append(f"{agent.data['name']} ({tokens})")
        
        status += f"""

{Fore.GREEN}Token Usage:{Style.RESET_ALL}
- Total tokens in room: {total_tokens}
- High usage agents: {', '.join(high_usage_agents) if high_usage_agents else 'None'}
- Auto-compression: {'✅ Enabled' if TOKEN_SETTINGS['enable_auto_compression'] else '❌ Disabled'}

{Fore.GREEN}Context Sharing:{Style.RESET_ALL}
- Shared contexts: {len(context_manager.shared_contexts)}
- Current location contexts: {context_manager.get_context_stats(self.world.player_location)['count']}        """
        
        return status
    
    def cmd_conv(self, args: List[str]) -> str:
        """Start endless conversation mode with specified participants."""
        if len(args) < 2:
            return "Usage: /conv player,bob,alice,jake <conversation description>"
        
        # Parse participants (first argument)
        participant_names = args[0].lower().split(',')
        if len(participant_names) < 2:
            return "Please specify at least 2 participants separated by comma (e.g., player,alice,bob)"
        
        # Conversation description (remaining arguments)
        topic = ' '.join(args[1:])
        if not topic:
            return "Please provide a conversation description"
        
        # Find all agents in current room
        agents = self.world.get_agents_in_room()
        agent_dict = {agent.data['name'].lower(): agent for agent in agents}
        
        # Validate that all non-player participants exist
        missing_agents = []
        agent_participants = []
        for name in participant_names:
            if name != 'player':
                if name not in agent_dict:
                    missing_agents.append(name)
                else:
                    agent_participants.append(agent_dict[name])
        
        if missing_agents:
            available = list(agent_dict.keys())
            available.append('player')
            return f"Agent(s) not found: {', '.join(missing_agents)}. Available: {', '.join(available)}"
        
        # Set up endless mode state
        self.endless_mode = True
        self.endless_participants = participant_names
        self.endless_topic = topic
        self.endless_agents = agent_participants
        
        # Initialize conversation context for all agents
        for agent in agent_participants:
            current_room = self.world.get_current_room()
            room_name = current_room.get('name', 'Unknown Location')
            conversation_setup = f"""You are joining an endless group conversation.

Topic: {topic}
Participants: {', '.join([name.title() if name != 'player' else 'Player' for name in participant_names])}

You are currently in {room_name}. Stay focused on the conversation topic and respond naturally to what others say."""
            agent.share_context(conversation_setup)
        
        participant_display = ', '.join([name.title() if name != 'player' else 'Player' for name in participant_names])
        
        return f"""🗣️ Endless conversation mode activated!
📋 Participants: {participant_display}
📝 Topic: {topic}

💡 How it works:
- Normal talk (/say <message>) = Everyone replies in order once
- Directed talk (/say alice <message>) = Only Alice replies, others listen
- Multiple targets (/say alice,bob <message>) = Alice and Bob reply, others listen
- Type /endconv to end conversation mode"""

    def cmd_endconv(self, args: List[str]) -> str:
        """End endless conversation mode."""
        if not self.endless_mode:
            return "❌ Not currently in endless conversation mode."
        
        # Save participant info before clearing
        participant_display = ', '.join([name.title() if name != 'player' else 'Player' 
                                       for name in self.endless_participants])
        topic = self.endless_topic
        
        # Clear endless mode state
        self.endless_mode = False
        self.endless_participants = []
        self.endless_topic = ""
        self.endless_agents = []
        
        return f"""✅ Endless conversation mode ended.
📋 Previous participants: {participant_display}
📝 Previous topic: {topic}

You can now use normal commands again."""

    def _handle_endless_mode_location_change(self):
        """Handle agent removal from endless mode when player moves locations."""
        if not self.endless_mode or not self.endless_agents:
            return
        
        # Get current room agents
        current_agents = self.world.get_agents_in_room()
        current_agent_names = {agent.data['name'].lower() for agent in current_agents}
          # Find agents that are following the player
        following_agents = []
        for agent in self.endless_agents:
            agent_name = agent.data['name'].lower()
            if agent_name in current_agent_names:
                # Check if agent is following
                if agent.data.get('following', False):
                    following_agents.append(agent)
        
        # Remove non-following agents from endless mode
        removed_agents = []
        new_endless_agents = []
        new_endless_participants = ['player']  # Always keep player
        
        for agent in self.endless_agents:
            agent_name = agent.data['name'].lower()
            # Keep agent if they're following or still in current location
            if (agent.data.get('following', False) or 
                agent_name in current_agent_names):
                new_endless_agents.append(agent)
                new_endless_participants.append(agent_name)
            else:
                removed_agents.append(agent.data['name'])
        
        # Update endless mode state
        self.endless_agents = new_endless_agents
        self.endless_participants = new_endless_participants
        
        # Notify about removed agents
        if removed_agents:
            removed_display = ', '.join([name.title() for name in removed_agents])
            self.print_colored(f"🚶 {removed_display} left the endless conversation (not following)", Fore.YELLOW)

    def cmd_invite(self, args: List[str]) -> str:
        """Invite an agent to join endless conversation mode."""
        if not self.endless_mode:
            return "❌ Invite command only works in endless conversation mode. Use /conv first."
        
        if not args:
            return "Usage: /invite <agent_name>"
        
        agent_name = args[0].lower()
        
        # Check if agent is already in endless mode
        if agent_name in [p.lower() for p in self.endless_participants]:
            return f"❌ {agent_name.title()} is already participating in the conversation."
        
        # Find agent in current room
        agents = self.world.get_agents_in_room()
        agent_dict = {agent.data['name'].lower(): agent for agent in agents}
        
        if agent_name not in agent_dict:
            available = list(agent_dict.keys())
            return f"❌ Agent '{agent_name}' not found in current location. Available: {', '.join(available) if available else 'none'}"
        
        # Add agent to endless mode
        agent = agent_dict[agent_name]
        self.endless_agents.append(agent)
        self.endless_participants.append(agent_name)
        
        # Initialize conversation context for the agent
        current_room = self.world.get_current_room()
        room_name = current_room.get('name', 'Unknown Location')
        conversation_setup = f"""You are joining an ongoing group conversation.

Topic: {self.endless_topic}
Participants: {', '.join([name.title() if name != 'player' else 'Player' for name in self.endless_participants])}

You are currently in {room_name}. Stay focused on the conversation topic and respond naturally to what others say."""
        
        agent.share_context(conversation_setup)
        
        return f"✅ {agent_name.title()} has joined the endless conversation!"

    def cmd_remove(self, args: List[str]) -> str:
        """Remove an agent from endless conversation mode."""
        if not self.endless_mode:
            return "❌ Remove command only works in endless conversation mode. Use /conv first."
        
        if not args:
            return "Usage: /remove <agent_name>"
        
        agent_name = args[0].lower()
        
        if agent_name == 'player':
            return "❌ Cannot remove player from conversation. Use /endconv to end the conversation."
        
        # Check if agent is in endless mode
        if agent_name not in [p.lower() for p in self.endless_participants]:
            current_participants = [name.title() if name != 'player' else 'Player' 
                                  for name in self.endless_participants if name != 'player']
            return f"❌ {agent_name.title()} is not participating in the conversation. Current participants: {', '.join(current_participants) if current_participants else 'none'}"
        
        # Remove agent from endless mode
        self.endless_participants = [p for p in self.endless_participants if p.lower() != agent_name]
        self.endless_agents = [agent for agent in self.endless_agents if agent.data['name'].lower() != agent_name]
        
        return f"✅ {agent_name.title()} has been removed from the endless conversation."

    def cmd_dialog(self, args: List[str]) -> str:
        """Create automated dialog between agents in endless mode."""
        if not self.endless_mode:
            return "❌ Dialog command only works in endless conversation mode. Use /conv first."
        
        if len(args) < 2:
            return "❌ Usage: /dialog agent1,agent2 <number_of_exchanges>"
        
        try:
            # Parse agents and number of exchanges
            agents_part = args[0]
            num_exchanges = int(args[1])
            
            if num_exchanges < 1:
                return "❌ Number of exchanges must be at least 1."
            
            if num_exchanges > 10:
                return "❌ Number of exchanges cannot exceed 10 to prevent infinite loops."
            
            # Parse the agents
            agent_names = [name.strip().lower() for name in agents_part.split(',')]
            
            if len(agent_names) != 2:
                return "❌ Dialog requires exactly 2 agents. Usage: /dialog agent1,agent2 <number>"              # Validate agents are in the current room and endless participants
            room_agents = self.world.get_agents_in_room()
            available_agents = [agent.data['name'].lower() for agent in room_agents]
            endless_agent_names = [p.lower() for p in self.endless_participants if p != 'player']
            
            missing_agents = []
            for agent_name in agent_names:
                if agent_name not in available_agents:
                    missing_agents.append(f"{agent_name.title()} (not in room)")
                elif agent_name not in endless_agent_names:
                    missing_agents.append(f"{agent_name.title()} (not in conversation)")
            
            if missing_agents:
                return f"❌ Cannot find agents or they're not in the conversation: {', '.join(missing_agents)}"
            
            # Generate context summary for the dialog
            context_summary = self._generate_dialog_context()
            
            self.print_colored(f"🎭 Starting automated dialog between {agent_names[0].title()} and {agent_names[1].title()}", Fore.MAGENTA)
            self.print_colored(f"🔄 {num_exchanges} exchanges will be generated...", Fore.YELLOW)
            print()
            
            # Alternate between the two agents for the specified number of exchanges
            current_speaker = 0  # 0 for first agent, 1 for second agent
            
            for exchange in range(num_exchanges):
                speaker = agent_names[current_speaker]
                listener = agent_names[1 - current_speaker]
                
                # Generate response based on context and previous dialog
                dialog_prompt = f"""Continue the conversation between {speaker.title()} and {listener.title()}.
Context: {context_summary}
Current topic: {self.endless_topic}

{speaker.title()} should respond naturally to continue the conversation with {listener.title()}."""
                
                response = self._generate_endless_response(speaker, dialog_prompt, is_dialog=True)
                
                if response:
                    self.print_colored(f"🗣️ **{speaker.title()}**: {response}", Fore.CYAN)
                    print()
                else:
                    self.print_colored(f"❌ Failed to generate response for {speaker.title()}", Fore.RED)
                    break
                
                # Switch to the other agent
                current_speaker = 1 - current_speaker
            
            return f"✅ Automated dialog completed ({num_exchanges} exchanges between {agent_names[0].title()} and {agent_names[1].title()})"
            
        except ValueError:
            return "❌ Invalid number format. Usage: /dialog agent1,agent2 <number>"
        except Exception as e:
            return f"❌ Error during dialog: {str(e)}"

    def _generate_dialog_context(self) -> str:
        """Generate context summary for automated dialog."""
        try:
            from config import MODELS
            import ollama
              # Get recent conversation history and room context
            room = self.world.get_current_room()
            room_description = room.get('description', 'Unknown location')
            
            # Build context from endless conversation state
            context_parts = [
                f"Location: {room_description}",
                f"Conversation topic: {self.endless_topic}",
                f"Participants in conversation: {', '.join([p.title() if p != 'player' else 'Player' for p in self.endless_participants])}"
            ]
            
            # Add any recent agent memories or interactions
            room_agents = room.get('people', [])
            for agent_name in room_agents:
                if agent_name.lower() in [p.lower() for p in self.endless_participants if p != 'player']:
                    try:
                        agent_path = os.path.join(self.world.player_location, f"agent_{agent_name.lower()}.json")
                        if os.path.exists(agent_path):
                            with open(agent_path, 'r') as f:
                                import json
                                agent_data = json.load(f)
                                recent_memory = agent_data.get('recent_interactions', '')
                                if recent_memory:
                                    context_parts.append(f"{agent_name}'s recent context: {recent_memory}")
                    except:
                        pass  # Skip if can't read agent data
            
            context_text = "\n".join(context_parts)
            
            # Use summary model to create focused context
            summary_prompt = f"""Summarize the key points and current situation for an ongoing conversation:

{context_text}

Provide a brief, focused summary that captures the essential context for continuing the conversation."""
            
            try:
                response = ollama.chat(
                    model=MODELS['summary'],
                    messages=[{
                        'role': 'user',
                        'content': summary_prompt
                    }]                )
                summary = response['message']['content'].strip()
                # Strip thinking tokens from summary
                from game_engine import strip_thinking_tokens
                summary = strip_thinking_tokens(summary)
                return summary
            except:
                # Fallback to basic context if summary model fails
                return f"Current situation: {self.endless_topic} at {room_description}"
                
        except Exception as e:
            return f"Conversation in progress about: {self.endless_topic}"

    def _conduct_agent_conversation(self, agent1, agent2, topic: str, turns: int, summary_context: str) -> List[str]:
        """Conduct a conversation between two agents."""
        conversation_log = []
        
        # Prepare conversation context for both agents
        conversation_setup = f"Conversation context: {summary_context}\n\nYou are now having a conversation with {agent2.data['name']} about: {topic}"
        agent1_setup = conversation_setup.replace(agent2.data['name'], agent1.data['name'])
        agent2_setup = conversation_setup.replace(agent1.data['name'], agent2.data['name'])
        
        # Start conversation - agent1 speaks first
        current_speaker = agent1
        current_listener = agent2
        current_setup = agent1_setup
        
        for turn in range(turns * 2):  # Each turn = both agents speak once
            speaker_name = current_speaker.data['name']
            listener_name = current_listener.data['name']
            
            if turn == 0:
                # First message - include setup context
                prompt = f"{current_setup}\n\nStart the conversation by speaking to {listener_name}."
            else:
                # Subsequent messages - just respond to previous
                prompt = f"Continue your conversation with {listener_name} about {topic}."
            
            print(f"💬 {speaker_name} is thinking...")
            
            # Generate response with timeout protection
            try:
                response = current_speaker.generate_response(prompt, self.world.get_current_room())
                
                if not response or response.strip() == "":
                    response = f"*{speaker_name} seems lost in thought*"
                    
            except Exception as e:
                print(f"⚠️ {speaker_name} had trouble responding: {e}")
                response = f"*{speaker_name} looks confused and remains silent*"
            
            # Strip thinking tokens first to maintain immersion
            response = strip_thinking_tokens(response)
            
            # Clean up the response (remove any meta-text)
            cleaned_response = self._clean_conversation_response(response, speaker_name, listener_name)
            
            # Display the message
            print(f"🗣️ **{speaker_name}**: {cleaned_response}")
            
            # Add to conversation log
            conversation_log.append(f"{speaker_name}: {cleaned_response}")
            
            # Share this message with the listener as context
            listener_context = f"In conversation, {speaker_name} said to you: \"{cleaned_response}\""
            current_listener.share_context(listener_context)
            
            # Add memory for both agents
            current_speaker.add_memory('dialogue', 'agent_conversation', f"Said to {listener_name}: {cleaned_response}")
            current_listener.add_memory('dialogue', 'agent_conversation', f"Heard from {speaker_name}: {cleaned_response}")
            
            # Switch speakers
            current_speaker, current_listener = current_listener, current_speaker
            current_setup = agent2_setup if current_speaker == agent2 else agent1_setup
            
            print()
            
            # Stop if we've reached the desired number of turns
            if turn + 1 >= turns * 2:
                break
        
        return conversation_log
    
    def _clean_conversation_response(self, response: str, speaker_name: str, listener_name: str) -> str:
        """Clean up agent response to focus on the actual dialogue."""
        # Remove common meta-text patterns
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Skip lines that seem to be narration about the other speaker
            if line.lower().startswith(listener_name.lower()):
                continue
                
            # Remove speaker name from start if present
            if line.lower().startswith(speaker_name.lower()):
                # Find where the actual speech starts
                colon_pos = line.find(':')
                if colon_pos != -1:
                    line = line[colon_pos + 1:].strip()
            
            # Remove common narrative patterns
            line = line.replace('*', '')
            line = line.replace('says:', '').replace('responds:', '').replace('replies:', '')
            
            # Remove quotes if the entire line is quoted
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            
            # Skip pure action descriptions
            if (line.lower().startswith(('looks at', 'turns to', 'glances at', 'leans', 'nods', 'shakes')) 
                and not any(punct in line for punct in ['"', "'", "!", "?"])):
                continue
                
            if line:
                cleaned_lines.append(line)
          # Join non-empty lines and return the first substantial response
        result = ' '.join(cleaned_lines)
        # If result is too long, take the first sentence or two
        sentences = result.split('. ')
        if len(sentences) > 2:
            result = '. '.join(sentences[:2]) + '.'
        
        return result.strip()
    def _conduct_player_conversation(self, agents: List, topic: str, turns: int, summary_context: str, ordered_participant_names: List[str]) -> List[str]:
        """Conduct a conversation involving the player and agents."""
        conversation_log = []
        
        # Use the ordered participant names as specified by the user
        participant_names = ordered_participant_names
        
        print(f"🎭 You are now part of a conversation about: {topic}")
        print(f"📝 Context: {summary_context}")
        print()        # Initialize conversation with context for all agents
        for agent in agents:
            current_room = self.world.get_current_room()
            room_name = current_room.get('name', 'Unknown Location')
            conversation_setup = f"""You are about to join a group conversation.

Topic: {topic}
Context: {summary_context}

Important: Focus on the conversation topic and respond naturally to what others say. 
Don't bring up unrelated memories unless they're directly relevant to what's being discussed.
You are currently in {room_name} with other people."""
            agent.share_context(conversation_setup)
        
        # Conduct rounds of conversation
        # turns = total number of messages, not turns per participant
        total_messages = turns
        current_participant_index = 0
        
        for message_num in range(total_messages):
            current_participant_name = participant_names[current_participant_index]
            
            if current_participant_name == "player":
                # Player's turn
                print(f"💭 It's your turn to speak about {topic}")
                player_input = input("🗣️ **You**: ").strip()
                
                if not player_input:
                    player_input = "*nods thoughtfully*"
                
                print()
                conversation_log.append(f"Player: {player_input}")
                
                # Share player's input with all agents
                for agent in agents:
                    agent.share_context(f"In conversation, Player said: \"{player_input}\"")
                    agent.add_memory('dialogue', 'player_conversation', f"Player said in group conversation: {player_input}")
                
            else:
                # Agent's turn - find the agent by name
                current_agent = None
                for agent in agents:
                    if agent.data['name'].lower() == current_participant_name:
                        current_agent = agent
                        break
                
                if current_agent:
                    # Create list of other participants for context
                    other_participant_names = [name for name in participant_names if name != current_participant_name]
                    # Convert 'player' to 'Player' for display
                    display_names = ['Player' if name == 'player' else name.title() for name in other_participant_names]
                    others_str = ', '.join(display_names)
                    
                    # Include recent conversation history for context
                    recent_conversation = ""
                    if conversation_log:
                        # Show the last 2-3 messages for context
                        recent_messages = conversation_log[-3:] if len(conversation_log) >= 3 else conversation_log
                        recent_conversation = "\n".join([f"- {msg}" for msg in recent_messages])
                        recent_conversation = f"\n\nRecent conversation:\n{recent_conversation}"
                    
                    prompt = f"""You are {current_agent.data['name']} in a group conversation about: {topic}
                    
Other participants: {others_str}{recent_conversation}

Respond naturally to what was just said. Stay focused on the current conversation topic: {topic}. 
Don't bring up unrelated memories or backstory unless directly relevant to what someone just said.
Give a direct, conversational response as {current_agent.data['name']}."""
                    
                    print(f"💬 {current_agent.data['name']} is thinking...")
                    
                    try:
                        # Generate response
                        response = current_agent.generate_response(prompt, self.world.get_current_room())
                        
                        if not response or response.strip() == "":
                            response = f"*{current_agent.data['name']} seems lost in thought*"
                            
                    except Exception as e:
                        print(f"⚠️ {current_agent.data['name']} had trouble responding: {e}")
                        response = f"*{current_agent.data['name']} looks confused and remains silent*"
                    
                    # Strip thinking tokens and clean response
                    response = strip_thinking_tokens(response)
                    cleaned_response = self._clean_conversation_response(response, current_agent.data['name'], "everyone")
                    
                    # Display the message
                    print(f"🗣️ **{current_agent.data['name']}**: {cleaned_response}")
                    print()
                    
                    conversation_log.append(f"{current_agent.data['name']}: {cleaned_response}")
                    
                    # Share with other agents and add memories
                    for other_agent in agents:
                        if other_agent != current_agent:
                            other_agent.share_context(f"In group conversation, {current_agent.data['name']} said: \"{cleaned_response}\"")
                            other_agent.add_memory('dialogue', 'agent_conversation', f"Heard {current_agent.data['name']} say in group: {cleaned_response}")
                    
                    current_agent.add_memory('dialogue', 'agent_conversation', f"Said in group conversation: {cleaned_response}")
            
            # Move to next participant
            current_participant_index = (current_participant_index + 1) % len(participant_names)
            
            # Check if we've completed the desired number of turns
            if message_num + 1 >= total_messages:
                break
        
        print("🎯 Conversation concluded!")
        return conversation_log
    def _conduct_endless_player_conversation(self, agents: List, topic: str, summary_context: str, ordered_participant_names: List[str]) -> List[str]:
        """Conduct an endless conversation involving the player and agents until /endconv is typed."""
        conversation_log = []
        
        # Use the ordered participant names as specified by the user
        participant_names = ordered_participant_names
        
        print(f"🎭 You are now part of an endless conversation about: {topic}")
        print(f"📝 Context: {summary_context}")
        print(f"💡 Type '/endconv' during your turn to end the conversation.")
        print()
        
        # Initialize conversation with context for all agents
        for agent in agents:
            current_room = self.world.get_current_room()
            room_name = current_room.get('name', 'Unknown Location')
            conversation_setup = f"""You are about to join a group conversation.

Topic: {topic}
Context: {summary_context}

Important: Focus on the conversation topic and respond naturally to what others say. 
Don't bring up unrelated memories unless they're directly relevant to what's being discussed.
You are currently in {room_name} with other people."""
            agent.share_context(conversation_setup)
        
        # Conduct rounds of conversation
        current_participant_index = 0
        message_num = 0
        
        while True:
            current_participant_name = participant_names[current_participant_index]
            
            if current_participant_name == "player":
                # Player's turn
                print(f"💭 It's your turn to speak about {topic} (or type '/endconv' to end)")
                player_input = input("🗣️ **You**: ").strip()
                
                # Check for end conversation command
                if player_input.lower() == '/endconv':
                    print("🎯 Conversation ended by player!")
                    break
                
                if not player_input:
                    player_input = "*nods thoughtfully*"
                
                print()
                conversation_log.append(f"Player: {player_input}")
                
                # Share player's input with all agents
                for agent in agents:
                    agent.share_context(f"In conversation, Player said: \"{player_input}\"")
                    agent.add_memory('dialogue', 'player_conversation', f"Player said in group conversation: {player_input}")
                
            else:
                # Agent's turn - find the agent by name
                current_agent = None
                for agent in agents:
                    if agent.data['name'].lower() == current_participant_name:
                        current_agent = agent
                        break
                
                if current_agent:
                    # Create list of other participants for context
                    other_participant_names = [name for name in participant_names if name != current_participant_name]
                    # Convert 'player' to 'Player' for display
                    display_names = ['Player' if name == 'player' else name.title() for name in other_participant_names]
                    others_str = ', '.join(display_names)
                    
                    # Include recent conversation history for context
                    recent_conversation = ""
                    if conversation_log:
                        # Show the last 2-3 messages for context
                        recent_messages = conversation_log[-3:] if len(conversation_log) >= 3 else conversation_log
                        recent_conversation = "\n".join([f"- {msg}" for msg in recent_messages])
                        recent_conversation = f"\n\nRecent conversation:\n{recent_conversation}"
                    
                    prompt = f"""You are {current_agent.data['name']} in a group conversation about: {topic}
                    
Other participants: {others_str}{recent_conversation}

Respond naturally to what was just said. Stay focused on the current conversation topic: {topic}. 
Don't bring up unrelated memories or backstory unless directly relevant to what someone just said.
Give a direct, conversational response as {current_agent.data['name']}."""
                    
                    print(f"💬 {current_agent.data['name']} is thinking...")
                    
                    try:
                        # Generate response
                        response = current_agent.generate_response(prompt, self.world.get_current_room())
                        
                        if not response or response.strip() == "":
                            response = f"*{current_agent.data['name']} seems lost in thought*"
                            
                    except Exception as e:
                        print(f"⚠️ {current_agent.data['name']} had trouble responding: {e}")
                        response = f"*{current_agent.data['name']} looks confused and remains silent*"
                    
                    # Strip thinking tokens and clean response
                    response = strip_thinking_tokens(response)
                    cleaned_response = self._clean_conversation_response(response, current_agent.data['name'], "everyone")
                    
                    # Display the message
                    print(f"🗣️ **{current_agent.data['name']}**: {cleaned_response}")
                    print()
                    
                    conversation_log.append(f"{current_agent.data['name']}: {cleaned_response}")
                    
                    # Share with other agents and add memories
                    for other_agent in agents:
                        if other_agent != current_agent:
                            other_agent.share_context(f"In group conversation, {current_agent.data['name']} said: \"{cleaned_response}\"")
                            other_agent.add_memory('dialogue', 'agent_conversation', f"Heard {current_agent.data['name']} say in group: {cleaned_response}")
                    
                    current_agent.add_memory('dialogue', 'agent_conversation', f"Said in group conversation: {cleaned_response}")
            
            # Move to next participant
            current_participant_index = (current_participant_index + 1) % len(participant_names)
            message_num += 1
            
            # Safety check to prevent infinite loops (optional)
            if message_num > 100:
                print("⚠️ Conversation has reached 100 messages. Automatically ending for safety.")
                break
        
        print("🎯 Conversation concluded!")
        return conversation_log

    def cmd_analytics(self, args: List[str]) -> str:
        """Show detailed token analytics and usage statistics."""
        from token_management import token_analytics
        
        if args and args[0] == 'save':
            # Force save analytics
            token_analytics.save_analytics()
            return "📊 Analytics data saved to token_analytics.json"
        
        if args and len(args) > 0:
            # Show analytics for specific agent
            agent_name = args[0]
            agent = self.world.find_agent_by_name(agent_name)
            
            if not agent:
                return f"There's no one named '{agent_name}' here."
            
            analytics = token_analytics.get_agent_analytics(agent.data['name'])
            
            result = f"""
{Fore.CYAN}📊 Detailed Analytics for {agent.data['name']}:{Style.RESET_ALL}

{Fore.GREEN}📈 Usage Statistics:{Style.RESET_ALL}
- Total tokens used: {analytics['total_tokens_used']:,}
- API calls made: {analytics['api_calls']}
- Conversation turns: {analytics['conversation_turns']}
- Average tokens per call: {analytics['avg_tokens_per_call']}

{Fore.YELLOW}🔄 Token Management:{Style.RESET_ALL}
- Token limit expansions: {analytics['expansions']}
- Context compressions: {analytics['compressions']}
- Peak tokens in single call: {analytics['peak_tokens']:,}

{Fore.BLUE}⏱️ Activity Timeline:{Style.RESET_ALL}
- First seen: {analytics['first_seen'] or 'Never'}
- Last active: {analytics['last_active'] or 'Never'}
            """
            return result.strip()
        else:
            # Show system-wide analytics
            summary = token_analytics.get_system_summary()
            top_users = token_analytics.get_top_token_users(5)
            
            result = f"""
{Fore.CYAN}📊 System-Wide Token Analytics:{Style.RESET_ALL}

{Fore.GREEN}🌍 Overall Statistics:{Style.RESET_ALL}
- Total agents tracked: {summary['total_agents_tracked']}
- Total tokens used: {summary['total_tokens_used']:,}
- Total API calls: {summary['total_api_calls']}
- Average tokens per call: {summary['avg_tokens_per_call']}

{Fore.YELLOW}🔄 System Activity:{Style.RESET_ALL}
- Total token expansions: {summary['total_expansions']}
- Total compressions: {summary['total_compressions']}

{Fore.MAGENTA}🏆 Top Token Users:{Style.RESET_ALL}"""
            
            for i, user in enumerate(top_users, 1):
                result += f"\n{i}. {user['name']}: {user['total_tokens']:,} tokens ({user['api_calls']} calls)"
            
            result += f"\n\n{Fore.CYAN}💡 Use '/analytics <agent_name>' for detailed agent stats{Style.RESET_ALL}"
            result += f"\n{Fore.CYAN}💡 Use '/analytics save' to save current data{Style.RESET_ALL}"
            
            return result.strip()
    def cmd_model_state(self, args: List[str]) -> str:
        """Show model state information for agents."""
        from token_management import token_manager
        
        if args and len(args) > 0:
            # Show state for specific agent
            agent_name = args[0]
            agent = self.world.find_agent_by_name(agent_name)
            
            if not agent:
                return f"There's no one named '{agent_name}' here."
            
            state_info = token_manager.get_model_state_info(agent.data['name'])
            return f"""
{Fore.CYAN}🤖 Model State for {agent.data['name']}:{Style.RESET_ALL}
{state_info}
            """.strip()
        else:
            # Show state for all agents in room
            agents = self.world.get_agents_in_room()
            if not agents:
                return "No agents in this location."
            
            result = f"{Fore.CYAN}🤖 Model States for All Agents:{Style.RESET_ALL}\n"
            for agent in agents:
                state_info = token_manager.get_model_state_info(agent.data['name'])
                result += f"\n{Fore.YELLOW}{agent.data['name']}:{Style.RESET_ALL} {state_info}"
            
            return result.strip()

def main():
    """Main entry point."""
    # Check if world directory exists, if not copy from world_template
    if not os.path.exists("world"):
        if os.path.exists("world_template"):
            print("🌍 Setting up world from template...")
            try:
                import shutil
                shutil.copytree("world_template", "world")
                print("✅ World created successfully from template!")
            except Exception as e:
                print(f"❌ Error creating world from template: {e}")
                sys.exit(1)
        else:
            print("Error: Neither 'world' nor 'world_template' directory found. Make sure you're running from the game directory.")
            sys.exit(1)
    
    # Check if Ollama is available
    try:
        import requests
        response = requests.get('http://localhost:11434/api/version', timeout=5)
        if response.status_code != 200:
            print("Warning: Ollama server doesn't seem to be running.")
            print("Please start Ollama with 'ollama serve' and ensure you have a model installed.")
            print("You can still play, but AI responses won't work.")
            print()
    except:
        print("Warning: Can't connect to Ollama. AI responses won't work.")
        print("Please start Ollama with 'ollama serve' and ensure you have a model installed.")
        print()
    
    # Start the game
    game = GameCLI()
    game.run()


if __name__ == "__main__":
    main()
