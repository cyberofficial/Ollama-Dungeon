# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ollama Dungeon is a sophisticated, locally-hosted AI-powered text adventure game where the game world IS the filesystem. It uses Ollama for local AI processing and implements advanced multi-agent conversations with persistent memories and context management.

## Architecture

### Core Design Pattern: Filesystem as World Database

The game's innovative architecture treats the filesystem directly as the game world:
- **Rooms** are directories containing `room.json` files
- **Agents** are JSON files with personalities, backgrounds, and knowledge
- **Items** are JSON files describing portable/usable objects
- **Memories** are CSV files with timestamped entries
- **Contexts** are pickle files storing conversation histories (in `contexts/` subdirectories)

### Key Modules

- **`game_engine.py`**: Core game engine, `WorldController`, `Agent` class with memory management, context persistence, and AI response generation
- **`cli.py`**: `GameCLI` class with command processing, endless conversation mode, and game loop
- **`token_management.py`**: `TokenManager`, `ContextManager`, `TokenAnalytics` classes for token monitoring, compression, and analytics
- **`config.py`**: Centralized configuration - `MODELS`, `TOKEN_SETTINGS`, `AGENT_SETTINGS`, `GAME_SETTINGS`, `LOGGING`
- **`world_editor.py`** / **`npc_editor.py`**: Tkinter-based GUI tools for world creation
- **`editor_launcher.py`**: GUI hub for launching all editors
- **`verify_setup.py`**: System health checker for development

### World Template Protection

`world_template/` is never modified - the game copies it to `world/` on first run. This ensures clean resets and protects original content.

### Default World Locations

The world template includes four main areas:
- `sunspire_city/` - Default starting location
- `crystal_caves/`
- `sky_gardens/`
- `whispering_dunes/`

## Common Development Commands

### Running the Game
```bash
python main.py                    # Start the game
python verify_setup.py            # Check system health (Ollama, files, models)
```

### Testing
```bash
python tests/run_tests.py         # Run comprehensive test suite (recommended)
python tests/run_tests.py --quick # Quick essential tests only
python tests/run_tests.py --benchmark # Performance benchmarks
python tests/run_tests.py --legacy # Run legacy test categories
```

### Starting Ollama (Required for AI features)
```bash
ollama serve                     # Start Ollama server
ollama pull qwen3:4b             # Pull default model
```

## Configuration System

All settings in `config.py` organized into five dictionaries:

1. **`MODELS`**: Main and summary model names (default: `qwen3:4b`)
2. **`TOKEN_SETTINGS`**: Context limits, compression thresholds, auto-compression, token expansion settings
3. **`AGENT_SETTINGS`**: Memory limits, temperature, response length, session persistence, thinking mode settings
4. **`GAME_SETTINGS`**: Default location (`world/sunspire_city`), auto-save frequency, debug mode, title/subtitle customization
5. **`LOGGING`**: Log file settings, AI response logging, token usage logging

The game uses two models: main for conversations, summary for context compression.

## Testing Architecture

- **Comprehensive suite**: `tests/testall.py` contains `TestAllOllamaDungeon` with full coverage
- **Mock-based**: Tests work without Ollama running using mocked AI responses
- **Enhanced runner**: `tests/run_tests.py` provides colored output, performance metrics, and categories
- **Quick tests**: Subset of essential tests for rapid iteration

## Save/Load System

Saves are complete world snapshots stored in `saves/<name>/`:
- `player_state.json`: Player location and state
- `world/`: Complete filesystem snapshot of all rooms, agents, items
- `inventory/`: Player's carried items

All destructive operations create timestamped backups in `backups/`.

## Agent System

### Agent Class Features

- **Session Management**: Unique session IDs using UUID for each agent instance
- **Context Persistence**: Conversation context saved to pickle files in `contexts/` subdirectories
- **Buffered Memory Writing**: Memory writes are buffered and flushed in batches for performance
- **Thinking Token Stripping**: Automatically removes `<thinking>` tags and `...` blocks from AI responses
- **Dynamic Temperature**: Character-specific temperature variation based on name hash
- **Following Behavior**: Agents can follow the player between rooms

### Agent Memory System

Agents use CSV-based memory with columns: `memory_type`, `key`, `value`, `timestamp`. Memory types:
- **Event**: Significant occurrences
- **Observation**: Environmental details
- **Dialogue**: Conversations
- **Emotion**: Emotional states

Memories are automatically summarized when exceeding `max_memory_entries` from `AGENT_SETTINGS`.

## Token Management

### TokenManager Class

Sophisticated token monitoring to prevent context overflow:
- Dynamic token limit expansion based on usage patterns
- Automatic compression when approaching thresholds
- Emergency compression for edge cases
- Per-agent context tracking with model state management
- Token limit expansion analytics

### ContextManager Class

Manages shared context between agents:
- Location-based context sharing
- Token-limited context retrieval
- Context trimming to prevent overflow

### TokenAnalytics Class

Tracks token usage over time:
- Per-agent API call tracking
- Token expansion and compression events
- Peak token usage monitoring
- System-wide usage summaries

## Conversation System

**Endless Conversation Mode** (`/conv`):
- Multi-agent conversations where agents participate naturally
- Location-aware - agents automatically join/leave based on room
- `/invite` and `/remove` to control participants
- `/dialog` for automated dialog between two agents
- `/say` for player messages (targeted or broadcast)

Agents can **follow** the player between rooms (`/follow <agent>`, `/stay <agent>`).

## Key Constraints & Patterns

1. **Filesystem is database**: Never hardcode world structure - always scan directories
2. **Template protection**: Never modify `world_template/`, only `world/`
3. **Backup first**: All save/delete operations create backups in `backups/`
4. **Graceful degradation**: Game continues even if AI fails (uses fallback responses)
5. **Session persistence**: Agent contexts saved to `contexts/<agent>_context.pkl`
6. **Token awareness**: Always check token counts before adding context
7. **Thinking token handling**: Strip thinking tokens from AI responses when `strip_thinking_tokens` is enabled

## Adding New Features

### New Commands
Add to `cli.py` in the `GameCLI.__init__` `self.commands` dictionary:
```python
'commandname': self.cmd_commandname,
```
Then implement `def cmd_commandname(self, args: List[str]) -> str:`.

### New Agent
Create `agent_<name>.json` in appropriate `world/` location with required fields: `name`, `persona`, `location`, `memory_file`, `mood`.

### New Location
1. Create directory in `world_template/` with `room.json`
2. Add `exits` object linking to adjacent rooms
3. Copy to `world/` (or let game auto-copy)
4. Update parent room's exits

## Dependencies

- **ollama**: Local LLM integration
- **requests**: HTTP to Ollama API
- **colorama**: Cross-platform terminal colors
- **pandas**: CSV memory management (implied)
- **prompt_toolkit**: Advanced input handling (implied)
- **tiktoken**: Token counting

No build system required - pure Python with pip install.