<div align="center">

# Ollama Dungeon
### AI-Powered Text Adventure with Filesystem-Based World

[![Python 3.12.7](https://img.shields.io/badge/python-3.12.7-brightgreen.svg)](https://python.org)
[![License AGPLv3](https://img.shields.io/badge/license-AGPLv3-green.svg)](LICENSE)
[![Ollama Powered](https://img.shields.io/badge/Ollama-Powered-orange.svg)](https://ollama.ai/)
[![Offline First](https://img.shields.io/badge/Offline-First-blue.svg)](#)

**A sophisticated, locally-hosted AI-powered text adventure where the world IS the filesystem**

Experience intelligent AI agents with persistent memories, advanced multi-agent conversations, location-aware endless conversation mode, and comprehensive analytics—all running completely offline with automatic backups and save management.

</div>

---

> **Development Status:** This project is actively in development. Some features may not function as intended. Items are currently for display purposes only and will be fully implemented in future updates. Please report any issues you encounter.

---

## Demo

### Interactive Multi-Agent Conversation

Watch a 3-way conversation between AI agents demonstrating the advanced conversation system:

https://github.com/user-attachments/assets/e9efc5b7-c276-4b24-a530-a111f8ca4bd8

### Game Interface

<div align="center">
  <img src="https://github.com/user-attachments/assets/1e0b6e0e-8793-434a-877a-a7317300bca5" alt="Ollama Dungeon Game Interface" width="80%"/>
</div>

---

## Features

### Core Capabilities

| **Filesystem-Based World** | **Intelligent AI Agents** |
|:---------------------------|:---------------------------|
| **Dynamic World Creation** - Automatically copies `world_template` to `world` on first run | **Individual Personalities** - Each agent has unique persona, background, goals, and relationships |
| **Hierarchical Structure** - Each folder represents a location, files represent agents and items | **Persistent Memory** - Agents remember conversations through CSV-based long-term memory |
| **Persistent State** - All changes to the world are saved to the filesystem | **Context Awareness** - Agents understand their environment, other people, and available items |
| **Template Protection** - Original `world_template` is never modified, ensuring clean resets | **Emotional Intelligence** - Agents have moods, fears, motivations, and personality quirks |

| **Advanced Save System** | **Smart Token Management** |
|:-------------------------|:---------------------------|
| **Complete World Saves** - Entire world state, agent contexts, and inventory preserved | **Automatic Compression** - Context automatically compressed when approaching token limits |
| **Multiple Save Slots** - Create and manage unlimited named saves | **Configurable Models** - Main and summary models configurable in config.py (defaults to qwen3:4b) |
| **Automatic Backups** - Creates timestamped backups before loading or deleting saves | **Token Monitoring** - Real-time token usage tracking and warnings |
| **Safe Operations** - All destructive operations create recovery backups | **Emergency Handling** - Graceful degradation when approaching hard limits |

### Advanced Features

| **Conversation System** | **Privacy & Analytics** |
|:------------------------|:------------------------|
| **Endless Conversation Mode** - Multi-agent conversations that flow naturally | **Fully Offline** - All processing happens on your local machine |
| **Location-Aware Conversations** - Agents automatically join/leave based on location | **No Data Collection** - Your stories and interactions remain private |
| **Following Behavior** - Control which agents follow you between locations | **Comprehensive Analytics** - Track token usage, conversation patterns, and system performance |
| **Context Sharing** - Share observations and thoughts with agents in your location | **Performance Monitoring** - Monitor model loading, response times, and system health |

## Quick Start

### Requirements

```diff
+ Python 3.12.7 with pip
+ Ollama running locally  
+ Required Model: qwen3:4b (configurable in config.py)
+ Recommended: qwen3:8b for better responses (optional)
```

### Installation

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Setup Ollama Models**
```bash
ollama pull qwen3:8b
ollama pull qwen3:4b
ollama serve
```

**3. Verify Setup**
```bash
python verify_setup.py
```

**4. Start Playing**
```bash
python main.py
```

## Commands Reference

### Movement & Exploration
| Command | Description | Example |
|---------|-------------|---------|
| `/look`, `/l` | Describe current room and contents | `/look` |
| `/go <direction>` | Move to another location | `/go north` |
| `/move <direction>` | Alternative to /go | `/move south` |

### Agent Interaction
| Command | Description | Example |
|---------|-------------|---------|
| `/say <agent> <message>` | Talk to an agent | `/say alice Hello there!` |
| `/talk <agent> <message>` | Alternative to /say | `/talk bob Hi!` |
| `/agents`, `/people` | List all people in current room | `/agents` |
| `/memory <agent>` | Show agent's recent memories | `/memory bob` |
| `/summarize [target(s)] [context]` | Share context with agents | `/summarize alice Bob looks worried` |
| `/share [target(s)] [context]` | Alternative to /summarize | `/share alice,bob Secret meeting` |
| `/follow <agent>` | Have agent follow you | `/follow alice` |
| `/stay <agent>` | Make agent stop following | `/stay alice` |

### Endless Conversation Mode
| Command | Description | Example |
|---------|-------------|---------|
| `/conv` | Start endless conversation mode | `/conv` |
| `/endconv` | End endless conversation mode | `/endconv` |
| `/invite <agent>` | Add agent to current conversation | `/invite bob` |
| `/remove <agent>` | Remove agent from conversation | `/remove alice` |
| `/dialog <message>` | Send message in conversation mode | `/dialog What should we do next?` |

### Inventory Management
| Command | Description | Example |
|---------|-------------|---------|
| `/inventory`, `/inv` | View your inventory | `/inventory` |
| `/pickup <item>` | Pick up an item | `/pickup rusty dagger` |
| `/take <item>` | Alternative to /pickup | `/take health potion` |
| `/use <item>` | Use an item from inventory | `/use health potion` |

### Save & Load System
| Command | Description | Example |
|---------|-------------|---------|
| `/save [name]` | Save current game state | `/save adventure1` |
| `/load [name]` | Load a saved game | `/load adventure1` |
| `/saves` | List all available saves | `/saves` |
| `/delete <name>` | Delete a save (creates backup) | `/delete old_save` |

### System & Debug
| Command | Description | Example |
|---------|-------------|---------|
| `/tokens [agent]` | Show token usage statistics | `/tokens alice` |
| `/compress <agent>` | Manually compress agent context | `/compress bob` |
| `/compress_all` | Compress all agents in current room | `/compress_all` |
| `/status` | Show system connectivity and stats | `/status` |
| `/reset <agent>` | Reset agent's memory and context | `/reset alice` |
| `/analytics` | Show detailed game analytics | `/analytics` |
| `/model_state` | Display model performance info | `/model_state` |
| `/help` | Show all available commands | `/help` |
| `/quit`, `/exit`, `/q` | Exit the game | `/quit` |

## World Structure

### Directory Layout

```
world_template/              # Protected template (never modified)
├── town/
│   ├── room.json           # Room description and exits
│   ├── tavern/
│   │   ├── room.json
│   │   ├── agent_alice.json     # Tavern keeper
│   │   ├── agent_bob.json       # Local scout
│   │   ├── memory_alice.csv     # Alice's memories
│   │   ├── memory_bob.csv       # Bob's memories
│   │   ├── rusty_dagger.json    # Pickupable item
│   │   └── contexts/            # Agent conversation contexts
│   │       ├── alice_context.pkl
│   │       └── bob_context.pkl
│   └── market/
│       ├── room.json
│       └── health_potion.json
└── forest/
    ├── room.json
    └── cave/
        ├── room.json
        ├── agent_grix.json     # Goblin scout
        └── memory_grix.csv

world/                       # Active world (copied from template)
├── [same structure as template]

saves/                       # Save game storage
├── save1/
│   ├── player_state.json
│   ├── world/              # Complete world snapshot
│   └── inventory/          # Player inventory snapshot
└── save2/

backups/                     # Automatic safety backups
├── world_backup_before_load_save1_20250605_143026/
└── deleted_save_old_save_20250605_144404/

inventory/                   # Player's items
└── [item files moved here when picked up]
```

### File Formats

#### Room Definition (`room.json`)
```json
{
  "name": "The Prancing Pony Tavern",
  "description": "A warm, dimly lit tavern...",
  "exits": {
    "south": "world/town",
    "up": "world/town/tavern/upstairs"
  }
}
```

#### Agent Definition (`agent_alice.json`)
```json
{
  "name": "Alice",
  "persona": "A friendly tavern keeper who knows everyone's business",
  "background": "Has run this tavern for 20 years",
  "appearance": "A middle-aged woman with graying hair and kind eyes",
  "mood": "cheerful",
  "occupation": "Tavern keeper",
  "memory_file": "memory_alice.csv",
  "knowledge": ["Local gossip", "Brewing techniques", "Town history"],
  "goals": ["Keep customers happy", "Maintain tavern reputation"],
  "fears": ["Economic downturn", "Losing regular customers"],
  "relationships": {
    "Bob": "Good friend and regular customer",
    "Mayor": "Respectful business relationship"
  }
}
```

#### Item Definition (`health_potion.json`)
```json
{
  "name": "Health Potion",
  "description": "A small vial of red liquid that glows faintly",
  "portable": true,
  "usable": true,
  "use_description": "You feel refreshed and energized!",
  "value": 50
}
```

## Technical Features

### AI Architecture
- **Local LLM Integration** - Uses Ollama for complete privacy and control
- **Flexible Model Configuration** - Configurable main and summary models via config.py
- **Context Compression** - Intelligent summarization prevents token overflow
- **Session Persistence** - Agent contexts saved and restored between sessions
- **Dynamic Token Management** - Automatic token limit expansion and compression

### Memory Systems
- **CSV-Based Storage** - Structured memory entries with timestamps
- **Memory Types** - Events, observations, dialogue, emotions
- **Automatic Summarization** - Recent memories compressed into readable summaries
- **Cross-Session Persistence** - Memories survive game restarts

### Safety & Reliability
- **Automatic Backups** - Every destructive operation creates timestamped backups
- **Template Protection** - Original world template never modified
- **Graceful Degradation** - System continues functioning even with AI failures
- **Error Recovery** - Robust error handling with informative messages

### Performance Optimization
- **Agent Caching** - Loaded agents cached for better performance
- **Token Monitoring** - Real-time tracking prevents unexpected failures
- **Lazy Loading** - Agents and items loaded only when needed
- **Compression Triggers** - Automatic context compression based on configurable thresholds
- **Analytics System** - Comprehensive token usage tracking and analysis
- **Model State Management** - Intelligent model reloading optimization

---

## Use Cases

**Interactive Storytelling** - Create dynamic narratives with persistent characters  
**AI Research** - Experiment with multi-agent interactions and memory systems  
**Game Development** - Use as a foundation for more complex text adventures  
**Education** - Learn about AI, file systems, and game architecture  
**Modding & Customization** - Easily create new worlds, agents, and items

---

## Customization

### Creating New Agents
1. Copy an existing agent file from `world_template`
2. Modify the JSON with new personality, goals, and relationships
3. Create a corresponding memory CSV file
4. Place in appropriate location folder

### Adding New Locations
1. Create a new folder in `world_template`
2. Add a `room.json` file with description and exits
3. Update parent room's exits to link to new location
4. Add agents and items as desired

### Modifying Game Behavior
- Edit `config.py` for token limits, model selection, and game settings
- Modify `cli.py` to add new commands or change interface
- Adjust `game_engine.py` for core game mechanics

---

## System Requirements

| Component | Requirement |
|-----------|------------|
| **RAM** | 8GB+ recommended (for local LLM) |
| **CPU** | 6+ cores recommended |
| **GPU** | 6GB+ VRAM recommended |
| **Network** | Required only for initial model download |

---

## Troubleshooting

### Common Issues
- **"Can't connect to Ollama"** - Ensure `ollama serve` is running
- **"Model not found"** - Run `ollama pull qwen3:4b` (default) or configure different models in config.py
- **Token warnings** - Use `/compress_all` or `/tokens` to monitor usage
- **Agent not responding** - Check `/status` for connectivity issues

### Getting Help
1. Run `python verify_setup.py` to check system health
2. Use `/status` command in-game for real-time diagnostics
3. Check agent memory with `/memory <agent>` for context issues
4. Review token usage with `/tokens` for performance problems

### Documentation
- [Getting Started Guide](Guides/00-getting-started.md) - Complete setup and basic gameplay
- [Interacting with NPCs](Guides/02-interacting-with-npcs.md) - Agent conversations and following behavior
- [Conversation System](Guides/04-conversation-system.md) - Endless conversation mode and multi-agent chats
- [Command Reference](Guides/06-command-reference.md) - Complete list of all available commands
- [Advanced Features](Guides/05-advanced-features.md) - Token management, analytics, and optimization

---

<div align="center">

**This is a fully offline, privacy-focused AI experience.**  
All data stays on your local machine, and the world persists between sessions through the filesystem-based architecture.

[**GitHub**](https://github.com/cyberofficial/Ollama-Dungeon) • [**Documentation**](Guides/00-getting-started.md) • [**License**](LICENSE)

</div>
