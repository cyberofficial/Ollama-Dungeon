# Getting Started with Ollama Dungeon

Welcome to Ollama Dungeon, a text adventure powered by local AI. This guide will help you get started with the game and understand the basics of how to play.

## Prerequisites

Before starting the game, ensure you have:

1. **Python 3.12.7** - The game is tested on Python 3.12.7
2. **Ollama installed** - The game uses Ollama for AI responses. Make sure it's running with `ollama serve` in a terminal.
3. **Required model** - The game uses `qwen3:4b` by default for both main conversation and summarization (configurable in `config.py`). Install it with `ollama pull qwen3:4b`
4. **Python dependencies** - Install all required dependencies with `pip install -r requirements.txt`

## Verification

Before launching the game for the first time, you can verify your setup is correct:

```bash
python verify_setup.py
```

This script checks:
- Ollama server connectivity
- Model availability (informational - you can use any compatible Ollama model)
- World template structure and files
- Agent and item file integrity
- Configuration and memory files
- Required directories and dependencies

Running the verification script ensures everything is properly configured before you start playing.

## Launching the Game

To start playing Ollama Dungeon:

1. Open a terminal/command prompt
2. Navigate to the game directory
3. Run the command: `python main.py`

**First Run:** On the first launch, the game will automatically copy the `world_template` directory to create your `world` directory. This ensures you always have a fresh template to start from.

You'll see the welcome screen with the game title and a prompt to type `/help` for available commands. Your starting location is `world/sunspire_city`.

## Basic Concepts

### The World

The game world is structured as a directory-based environment:
- **Rooms** are represented as directories in the filesystem
- **Movement** occurs by navigating between these directories
- **Items** and **NPCs (agents)** are JSON files within room directories
- **World locations** include: `sunspire_city` (default starting location), `crystal_caves`, `sky_gardens`, and `whispering_dunes`

### Player Actions

Every command in the game starts with a forward slash `/`. The game provides a comprehensive set of commands for all aspects of gameplay:

#### Movement Commands
- `/look` or `/l` - Describe current room and show exits, items, and people
- `/go <direction>` or `/move <direction>` - Move to another location (north, south, east, west, up, down, etc.)
  - Example: `/go north` moves you to the room north of your current location

#### Interaction Commands
- `/say <agent> <message>` - Talk to a specific agent
  - Example: `/say Zahra Hello, how are you?`
- `/sayto <agent> <message>` - Alternative to `/say` (for immersion)
- `/talk <agent> <message>` - Alternative to `/say`
- `/agents` or `/people` - List all agents in the current room with their moods
- `/memory <agent>` - View an agent's memory summary to see what they remember
- `/share [targets] <message>` or `/summarize [targets] <message>` - Share context with agents
  - `/share <message>` - Share with all agents in room
  - `/share alice <message>` - Share only with Alice
  - `/share alice,bob <message>` - Share with Alice and Bob

#### Inventory Commands
- `/inventory` or `/inv` - View your inventory
- `/pickup <item>` or `/take <item>` - Pick up an item from the current room
  - Example: `/pickup crystal_pickaxe`
- `/use <item>` - Use an item from your inventory
  - Example: `/use celestial_dew`

#### System Commands
- `/saves` - List all saved games
- `/delete <save_name>` - Delete a specific save game
- `/status` - Show comprehensive system status including AI connectivity and token usage
- `/quit`, `/exit`, or `/q` - Exit the game
- `/help` - Show all available commands with detailed descriptions

For a complete list of commands, type `/help` in the game.

### Interacting with NPCs (Agents)

Agents are AI-powered NPCs that you can talk to. The game uses an AI to generate their responses based on:
- Their personality defined in their JSON files
- Context from the current room
- Their memory of past interactions

### Saving and Loading

You can save your progress at any time with the `/save` command and load it later with `/load`.

## Advanced Features

Ollama Dungeon includes several advanced features that enhance gameplay:

### Endless Conversation Mode

The game supports multi-agent conversations where agents participate naturally:

- `/conv <agent1,agent2[,player]> <topic>` - Start an endless conversation
  - Example: `/conv player,zahra,qasim Discuss the history of Sunspire City`
  - Agents will converse with each other and respond to your input
  - Use `/endconv` to end the conversation
  - `/invite <agent>` - Add an agent to the ongoing conversation
  - `/remove <agent>` - Remove an agent from the conversation
  - `/dialog <agent1,agent2> <exchanges>` - Generate automated dialog between two agents

### Agent Following System

Agents can follow you between rooms:

- `/follow <agent>` - Ask an agent to follow you
  - The agent will move with you when you change locations
- `/stay <agent>` - Tell a following agent to stay in their current location

### Token Management

The game includes sophisticated token management to prevent AI context overflow:

- `/tokens [agent]` - View token usage for all agents or a specific agent
- `/analytics [agent]` - Show detailed token analytics and usage history
- `/model_state [agent]` - Display current model state and context size
- `/compress <agent>` - Manually compress an agent's context to save tokens
- `/compress_all` - Compress all agents in the current room

Token limits automatically expand based on usage patterns, and the system can automatically compress contexts when thresholds are reached. These settings are configurable in `config.py`.

### Context Sharing

Agents can share context and memories:

- Shared context allows agents to be aware of events and conversations
- Context is automatically shared during group conversations
- Use `/share` to manually provide context to specific agents or everyone in the room

### Configuration

The game's behavior is controlled through `config.py`, which contains four main configuration dictionaries:

#### MODELS
Defines which AI models to use:
- `main`: Model for agent conversations (default: `qwen3:4b`)
- `summary`: Model for context compression (default: `qwen3:4b`)

You can use any compatible Ollama model. Change these to use different models like `llama3`, `mistral`, or others you have installed.

#### TOKEN_SETTINGS
Controls how the game manages AI context tokens:
- `max_context_tokens`: Maximum tokens before compression (default: 40000)
- `compression_threshold`: Start compression at this token count (default: 35000)
- `starting_tokens`: Initial token limit (default: 0)
- `increase_tokens_by`: Amount to increase limit when threshold reached (default: 1000)
- `token_increase_threshold`: Percentage of current limit to trigger expansion (default: 0.9)
- `enable_auto_compression`: Automatically compress when threshold reached (default: True)
- `show_token_warnings`: Display warnings when token counts are high (default: True)

#### AGENT_SETTINGS
Controls agent behavior and memory:
- `max_memory_entries`: Maximum memory entries before summarization (default: 50)
- `context_sharing_enabled`: Allow agents to share context (default: True)
- `persistent_sessions`: Keep agent sessions between interactions (default: True)
- `temperature`: AI response randomness (default: 0.7, higher = more creative)
- `reply_length`: Response verbosity - "brief", "medium", "detailed", or "verbose" (default: "detailed")

#### GAME_SETTINGS
General game settings:
- `default_location`: Starting location (default: "world/sunspire_city")
- `auto_save_frequency`: Auto-save every N actions (default: 10)
- `debug_mode`: Enable debug output (default: True)
- `title`: Custom game title (default: "OLLAMA DUNGEON")
- `subtitle`: Custom subtitle (default: "A Text Adventure Powered by Local AI")

## Next Steps

Check out the following guides for more detailed information:
- [Basic Commands](./01-basic-commands.md)
- [Interacting with NPCs](./02-interacting-with-npcs.md)
- [Inventory System](./03-inventory-system.md)
- [Conversation System](./04-conversation-system.md)
- [Advanced Features](./05-advanced-features.md)
