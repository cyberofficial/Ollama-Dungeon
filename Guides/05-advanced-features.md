# Advanced Features

This guide covers the more advanced features of Ollama Dungeon, including token management, context sharing, and system administration.

## Token Management

AI models have limitations on how much context they can process. The game includes tools to manage token usage:

| Command | Description | Example |
|---------|-------------|---------|
| `/tokens` | Show overall token usage | `/tokens` |
| `/tokens <agent>` | Show token usage for a specific agent | `/tokens alice` |
| `/compress <agent>` | Manually compress an agent's context | `/compress bob` |
| `/compress_all` | Compress context for all agents in the room | `/compress_all` |

### Understanding Token Usage

When you run `/tokens` or `/tokens <agent>`, you'll see output like this:

```
Token usage for Alice:
- Current context: 15,230 tokens
- Memory entries: 24
- Shared context entries: 8
- Tokens until compression: 10,770
- Status: ✅ Normal
```

Key metrics:
- **Current context**: How many tokens this agent is currently using
- **Memory entries**: Number of memories the agent has stored
- **Status**: Indicates if token usage is normal or high
- **Tokens until compression**: How many more tokens can be used before reaching compression threshold

### Token Management Configuration

Ollama Dungeon includes advanced token management settings that can be configured in `config.py`:

| Setting | Description | Default |
|---------|-------------|---------|
| `max_context_tokens` | Maximum tokens before compression | 40000 |
| `compression_threshold` | Start compression at this token count | 35000 |
| `starting_tokens` | Starting token limit for new agents | 10 |
| `increase_tokens_by` | Amount to increase token limit by | 1000 |
| `reload_on_lower` | Only reload model when token count increases | False |

When `reload_on_lower` is set to False (default), the system will not reload the model when switching to an agent with a lower token count. This optimization reduces unnecessary model reloads and improves response times.

### When to Compress Context

Compression is automatically applied when an agent's context reaches the configured threshold, but you can manually compress:
- When you notice slow response times from an agent
- When the token usage status shows "High"
- Before starting a complex conversation

## Agent Response Configuration

Ollama Dungeon includes settings to customize how agents respond and ensure diverse conversations:

| Setting | Description | Default |
|---------|-------------|---------|
| `randomize_responses` | Add unique random seeds to agent calls | True |
| `temperature` | Control response creativity and variation | 0.5 |
| `strip_thinking_tokens` | Remove `<think>` tags from responses | True |

### Understanding Response Settings

- **randomize_responses**: When enabled, each agent will use a unique random seed based on their name, ensuring they generate different responses even in similar situations. This prevents situations where multiple agents say exactly the same thing.

- **temperature**: Controls the creativity and randomness of agent responses:
  - Lower values (0.1-0.4): More consistent, predictable responses
  - Medium values (0.5-0.7): Good balance of creativity and coherence
  - Higher values (0.8-1.0): More creative but potentially less focused responses

- **strip_thinking_tokens**: Automatically removes any text between `<think>` tags, which agents use for internal reasoning that isn't meant to be spoken aloud.

These settings help create a more immersive experience where each character has a distinct voice and personality.

## Endless Conversation Mode Management

Endless conversation mode includes advanced features for managing long-running conversations across multiple locations:

### Location-Aware Participant Management

When you move between locations during an endless conversation:
- Agents who are not following you are automatically removed from the conversation
- Only agents present in your current location or following the player can participate
- This prevents agents from different locations from participating in conversations they shouldn't be part of

### Manual Participant Control

| Command | Description | Usage Notes |
|---------|-------------|-------------|
| `/invite <agent>` | Add an agent to the endless conversation | Agent must be in current location |
| `/remove <agent>` | Remove an agent from the endless conversation | Works with any participant |

Example session:
```
> /conv alice,bob The ancient ruins
🗣️ Endless conversation mode activated!
📋 Participants: Alice, Bob, Player

> /go north
🚶 Moving north...
⚠️ Alice and Bob were removed from endless conversation (not following)

> /invite cave_guardian
✅ Cave Guardian added to endless conversation

> /remove cave_guardian
✅ Cave Guardian removed from endless conversation
```

### Best Practices for Endless Mode

1. **Use `/follow <agent>`** before starting endless conversations if you plan to move around
2. **Invite relevant agents** when entering new locations to maintain conversation flow
3. **Remove agents** who are no longer relevant to the conversation topic
4. **Monitor token usage** during long endless conversations with `/tokens`

## System Status

To get a comprehensive view of the game's status:

```
/status
```

This shows:
- Current location
- Agents and items in the room
- Inventory status
- Ollama connectivity
- Model availability
- Token usage summary
- Context sharing statistics

## File System Structure

Understanding the game's file structure can help with troubleshooting:

```
world/                     # Main game world directory
  ├── forest/              # A location in the world
  │   ├── room.json        # Room description and properties
  │   └── cave/            # Sub-location
  │       ├── agent_grix.json  # Agent definition
  │       ├── memory_grix.csv  # Agent's memory
  │       └── room.json        # Room description
  │
  ├── town/                # Another location
  │   ├── room.json
  │   ├── market/          # Sub-location
  │   │   ├── health_potion.json  # Item definition
  │   │   └── room.json
  │   └── tavern/          # Sub-location
  │       ├── agent_alice.json
  │       ├── agent_bob.json
  │       ├── memory_alice.csv
  │       ├── memory_bob.csv
  │       ├── player.json      # Player definition
  │       ├── room.json
  │       └── contexts/        # Stored agent contexts
  │           ├── alice_context.pkl
  │           └── bob_context.pkl
  │
  └── ...

world_template/            # Template for resetting the world
saves/                     # Directory for saved games
inventory/                 # Global inventory items
```

## Advanced Agent Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/reset <agent>` | Reset an agent's memory and context | `/reset alice` |
| `/share <context>` | Share context with all agents | `/share The weather has turned stormy` |

## Troubleshooting

### AI Response Issues

If agents aren't responding properly:
1. Check Ollama status with `/status`
2. Verify models are available
3. Check token usage with `/tokens`
4. Try resetting agent context with `/reset <agent>`

### Similar Agent Responses

If multiple agents are giving identical or very similar responses:
1. Make sure `randomize_responses` is set to `True` in `AGENT_SETTINGS` (config.py)
2. Try increasing the `temperature` setting (0.7-0.9) for more varied responses
3. Use `/model_state` to check if agents are using unique model states
4. Consider restarting the game if the issue persists

### Saving/Loading Issues

If you encounter problems with save files:
1. Check the `saves/` directory exists
2. Use `/saves` to list available saves
3. Make sure you have write permissions to the directory

### Performance Issues

If you experience slow responses:
1. Check token usage with `/tokens`
2. Use `/compress_all` to optimize all agents in the room
3. Verify system resources aren't overloaded

## Extending the Game

The filesystem structure makes the game easy to extend:

1. **Creating new locations** - Add directories with `room.json` files
2. **Adding new NPCs** - Create agent JSON files and corresponding memory CSVs
3. **Creating new items** - Add item JSON files to rooms or the global inventory

## Example Advanced Session

```
> /status
=== SYSTEM STATUS ===

World State:
- Current location: town/tavern
- Agents in room: 2
- Items in room: 1
- Inventory items: 2

AI Models:
- Ollama: ✅ Connected
- qwen3:4b (chat): ✅ Available
- qwen3:4b (summary): ✅ Available

Token Usage:
- Total tokens in room: 28,552
- High usage agents: Alice (25,230)
- Auto-compression: ✅ Enabled

> /model_state
=== MODEL STATE INFO ===

Active Agents:
- Alice: Model=qwen3:4b, Context=3010 tokens, Last used=2025-06-06T07:53:12
- Bob: Model=qwen3:4b, Context=3010 tokens, Last used=2025-06-06T07:53:15

Agent Settings:
- Response Temperature: 0.5
- Randomized Responses: Enabled
- Context Sharing: Enabled

> /compress_all
Compressed contexts for 2 agents:
- Alice: 25,230 → 10,542 tokens (saved 14,688)
- Bob: 3,322 → 3,322 tokens (no compression needed)

Total tokens saved: 14,688
```
