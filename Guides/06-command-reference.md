# Command Reference

This is a quick reference guide to all available commands in Ollama Dungeon.

## Movement & Exploration
| Command | Description |
|---------|-------------|
| `/look`, `/l` | Describe current room |
| `/go <direction>` | Move to another location |
| `/move <direction>` | Alternative to `/go` |

## Interaction
| Command | Description |
|---------|-------------|
| `/say <agent> <message>` | Talk to an agent |
| `/sayto <agent> <message>` | Alternative to `/say` |
| `/talk <agent> <message>` | Alternative to `/say` |
| `/conv <agent1,agent2[,player]> [turns] <topic>` | Start a conversation |
| `/conversation <agent1,agent2[,player]> [turns] <topic>` | Alternative to `/conv` |
| `/dialog <agent1,agent2> <exchanges>` | Automated dialog between agents |
| `/endconv` | End endless conversation mode |
| `/invite <agent>` | Invite agent to endless conversation |
| `/remove <agent>` | Remove agent from endless conversation |
| `/agents`, `/people` | List people in current room |
| `/memory <agent>` | Show an agent's memory summary |
| `/summarize [target(s)] <context>` | Share context with agents |
| `/share [target(s)] <context>` | Alternative to `/summarize` |
| `/follow <agent>` | Have agent follow you |
| `/stay <agent>` | Have agent stop following you |

## Inventory
| Command | Description |
|---------|-------------|
| `/inventory`, `/inv` | View your inventory |
| `/pickup <item>` | Pick up an item |
| `/take <item>` | Alternative to `/pickup` |
| `/use <item>` | Use an item from inventory |

## System
| Command | Description |
|---------|-------------|
| `/tokens [agent]` | Show token usage |
| `/compress <agent>` | Manually compress agent's context |
| `/compress_all` | Compress context for all agents in room |
| `/status` | Show system status and connectivity |
| `/save [name]` | Save game state |
| `/load [name]` | Load game state |
| `/saves` | List saved games |
| `/delete <save_name>` | Delete a saved game |
| `/reset <agent>` | Reset agent's memory and context |
| `/model_state [agent]` | Show model loading state for agent(s) |
| `/analytics` | View token usage and API call analytics |
| `/help` | Show help message |
| `/quit`, `/exit`, `/q` | Exit the game |

## Command Format Legend

- Words in `<angle brackets>` are required parameters
- Words in `[square brackets]` are optional parameters
- Options separated by `|` mean "or" (choose one)
- Parameters with `...` can accept multiple values
- `[,player]` means the player can optionally be included in the list

## Special Command Formats

### Context Sharing

- `/share <message>` - Share with all agents in the room
- `/share <agent> <message>` - Share with a specific agent
- `/share <agent1,agent2> <message>` - Share with multiple specific agents

### Conversation Mode

- `/conv alice,bob,player 5 The weather` - 5 turns, including player
- `/conv alice,bob The magical artifacts` - Endless mode (no turn limit)
- In endless mode:
  - `/say <message>` - Everyone responds
  - `/say alice <message>` - Only Alice responds
  - `/say alice,bob <message>` - Only Alice and Bob respond
  - `/invite charlie` - Add Charlie to the conversation
  - `/remove alice` - Remove Alice from the conversation
  - Moving to a new location automatically removes non-following agents

### Dialog Command (for endless mode only)

- `/dialog alice,bob 3` - Generate 3 exchanges between Alice and Bob

## Configuration Settings

While not accessible via commands, these important settings in `config.py` control the game's behavior:

### Agent Behavior Settings
```python
AGENT_SETTINGS = {
    "max_memory_entries": 50,        # Maximum agent memory entries
    "strip_thinking_tokens": True,   # Remove <think> tags from responses
    "randomize_responses": True,     # Prevent identical responses between agents
    "temperature": 0.5,              # Response creativity (0.1-1.0)
}
```

### Token Management Settings
```python
TOKEN_SETTINGS = {
    "starting_tokens": 10,           # Initial token context size
    "increase_tokens_by": 1000,      # Growth amount when needed
    "reload_on_lower": False,        # Only reload on increased limits
}
```

For detailed information about these settings, see the [Advanced Features](./05-advanced-features.md) guide.
