# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ollama-Dungeon is a sophisticated, locally-hosted AI-powered text adventure game where the game world IS the filesystem. It uses Ollama for local AI processing and implements advanced multi-agent conversations with persistent memories and context management.

## Architecture

### Core Design Pattern: Filesystem as World Database

The game's innovative architecture treats the filesystem directly as the game world:
- **Rooms** are directories containing `room.json` files
- **Agents** are JSON files with personalities, backgrounds, and knowledge
- **Items** are JSON files describing portable/usable objects
- **Memories** are CSV files with timestamped entries
- **Contexts** are pickle files storing conversation histories

### Key Modules

- **`game_engine.py`**: Core game engine, world controller, agent management, and save/load system
- **`cli.py`**: Command-line interface with command processing and game loop
- **`token_management.py`**: AI context token monitoring and compression system
- **`config.py`**: Centralized configuration (models, token limits, agent behavior, game settings)
- **`world_editor.py`** / **`npc_editor.py`**: Tkinter-based GUI tools for world creation
- **`editor_launcher.py`**: GUI hub for launching all editors
- **`verify_setup.py`**: System health checker for development

### World Template Protection

`world_template/` is never modified - the game copies it to `world/` on first run. This ensures clean resets and protects original content.

## Common Development Commands

### Running the Game
```bash
python main.py                    # Start the game
python verify_setup.py            # Check system health (Ollama, files, models)
```

### Testing
```bash
python tests/run_tests.py         # Run comprehensive test suite (recommended)
python test_runner.py             # Simple test runner
python tests/run_tests.py --quick # Quick essential tests only
python tests/run_tests.py --benchmark # Performance benchmarks
```

### Starting Ollama (Required for AI features)
```bash
ollama serve                     # Start Ollama server
ollama pull qwen3:4b             # Pull default model
```

## Configuration System

All settings in `config.py` organized into four dictionaries:

1. **`MODELS`**: Main and summary model names (default: `qwen3:4b`)
2. **`TOKEN_SETTINGS`**: Context limits, compression thresholds, auto-compression
3. **`AGENT_SETTINGS`**: Memory limits, temperature, response length, session persistence
4. **`GAME_SETTINGS`**: Default location, auto-save frequency, debug mode

The game uses two models: main for conversations, summary for context compression.

## Testing Architecture

- **Comprehensive suite**: `tests/testall.py` contains `TestAllOllamaDungeon` with 100% coverage
- **Mock-based**: Tests work without Ollama running using mocked AI responses
- **Enhanced runner**: `tests/run_tests.py` provides colored output, performance metrics, and categories
- **Quick tests**: Subset of essential tests for rapid iteration

## Save/Load System

Saves are complete world snapshots stored in `saves/<name>/`:
- `player_state.json`: Player location and state
- `world/`: Complete filesystem snapshot of all rooms, agents, items
- `inventory/`: Player's carried items

All destructive operations create timestamped backups in `backups/`.

## Agent Memory System

Agents use CSV-based memory with columns: `timestamp`, `type`, `content`. Memory types:
- **Event**: Significant occurrences
- **Observation**: Environmental details
- **Dialogue**: Conversations
- **Emotion**: Emotional states

Memories are automatically summarized when exceeding `max_memory_entries` from `AGENT_SETTINGS`.

## Token Management

Sophisticated token monitoring to prevent context overflow:
- Dynamic token limit expansion based on usage patterns
- Automatic compression when approaching thresholds
- Emergency compression for edge cases
- Per-agent context tracking in pickle files

## Conversation System

**Endless Conversation Mode** (`/conv`):
- Multi-agent conversations where agents participate naturally
- Location-aware - agents automatically join/leave based on room
- `/invite` and `/remove` to control participants
- `/dialog` for sending messages to the group

Agents can **follow** the player between rooms (`/follow <agent>`, `/stay <agent>`).

## Key Constraints & Patterns

1. **Filesystem is database**: Never hardcode world structure - always scan directories
2. **Template protection**: Never modify `world_template/`, only `world/`
3. **Backup first**: All save/delete operations create backups in `backups/`
4. **Graceful degradation**: Game continues even if AI fails (uses fallback responses)
5. **Session persistence**: Agent contexts saved to `contexts/<agent>_context.pkl`
6. **Token awareness**: Always check token counts before adding context

## Adding New Features

### New Commands
Add to `cli.py` command dictionary in `main()` function. Follow pattern:
```python
'/commandname': lambda args: handle_command(args),
```

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
- **pandas**: CSV memory management
- **prompt_toolkit**: Advanced input handling
- **tiktoken**: Token counting

No build system required - pure Python with pip install.
