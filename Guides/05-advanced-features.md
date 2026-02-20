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
Token usage for Zahra:
- Current context: 15,230 tokens
- Current token limit: 26,000 tokens
- Memory entries: 24
- Shared context entries: 8
- Tokens until compression: 10,770
- Status: ✅ Normal
- Next expansion at: 23,400 tokens
```

Key metrics:
- **Current context**: How many tokens this agent is currently using
- **Current token limit**: The current token limit for this agent (expands dynamically)
- **Memory entries**: Number of memories the agent has stored
- **Shared context entries**: Number of shared context entries the agent has received
- **Status**: Indicates if token usage is normal or high
- **Tokens until compression**: How many more tokens can be used before reaching compression threshold
- **Next expansion at**: Token count that will trigger the next token limit expansion

### Token Management Configuration

Ollama Dungeon includes advanced token management settings that can be configured in `config.py`:

| Setting | Description | Default |
|---------|-------------|---------|
| `max_context_tokens` | Maximum tokens before compression | 40000 |
| `compression_threshold` | Start compression at this token count | 35000 |
| `starting_tokens` | Starting token limit for new agents | 0 |
| `increase_tokens_by` | Amount to increase token limit by | 1000 |
| `token_increase_threshold` | Percentage of limit to trigger expansion (0.9) | 0.9 |
| `summary_chunk_size` | Size of chunks to summarize | 8000 |
| `min_context_after_compression` | Minimum context to keep after compression | 5000 |
| `enable_auto_compression` | Automatically compress when threshold reached | True |
| `show_token_warnings` | Show token warnings to user | True |
| `suppress_token_info` | Hide token expansion/compression messages for immersion | False |
| `emergency_compression_threshold` | Emergency compression if regular fails | 38000 |
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
| `temperature` | Control response creativity and variation | 0.7 |
| `strip_thinking_tokens` | Remove<think> tags from responses | True |
| `reply_length` | Response length: brief, medium, detailed, or verbose | detailed |

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
> /conv zahra,kael,player The magical crystal formations
🗣️ Endless conversation mode activated!
📋 Participants: Zahra, Kael, Player

> /go up
🚶 Moving up...
⚠️ Zahra and Kael were removed from endless conversation (not following)

> /invite scholar_maven
✅ Scholar Maven added to endless conversation

> /remove scholar_maven
✅ Scholar Maven removed from endless conversation
```

### Best Practices for Endless Mode

1. **Use `/follow <agent>`** before starting endless conversations if you plan to move around
2. **Invite relevant agents** when entering new locations to maintain conversation flow
3. **Remove agents** who are no longer relevant to the conversation topic
4. **Monitor token usage** during long endless conversations with `/tokens`

## Token Analytics

For detailed tracking and analysis of token usage over time:

| Command | Description | Example |
|---------|-------------|---------|
| `/analytics` | Show system-wide token analytics | `/analytics` |
| `/analytics <agent>` | Show detailed analytics for a specific agent | `/analytics alice` |
| `/analytics save` | Save analytics data to file | `/analytics save` |

### System-Wide Analytics

Running `/analytics` without arguments shows overall statistics:

```
📊 System-Wide Token Analytics:

🌍 Overall Statistics:
- Total agents tracked: 5
- Total tokens used: 145,230
- Total API calls: 342
- Average tokens per call: 424

🔄 System Activity:
- Total token expansions: 8
- Total compressions: 3

🏆 Top Token Users:
1. Zahra: 52,340 tokens (124 calls)
2. Kael: 38,120 tokens (98 calls)
3. Scholar Maven: 28,450 tokens (67 calls)
```

### Agent-Specific Analytics

Running `/analytics <agent>` shows detailed statistics for that agent:

```
📊 Detailed Analytics for Zahra:

📈 Usage Statistics:
- Total tokens used: 52,340
- API calls made: 124
- Conversation turns: 86
- Average tokens per call: 422

🔄 Token Management:
- Token limit expansions: 3
- Context compressions: 1
- Peak tokens in single call: 28,450

⏱️ Activity Timeline:
- First seen: 2025-06-06T07:30:15
- Last active: 2025-06-06T09:45:22
```

### Saving Analytics Data

Use `/analytics save` to persist the current analytics data to `token_analytics.json`. This allows you to:
- Track token usage over multiple sessions
- Analyze patterns in agent behavior
- Identify which agents consume the most tokens
- Optimize your configuration based on actual usage

## System Status

To get a comprehensive view of the game's status:

```
/status
```

This displays organized sections:

```
=== SYSTEM STATUS ===

World State:
- Current location: world/sunspire_city
- Agents in room: 2
- Items in room: 1
- Inventory items: 2

AI Models:
- Ollama: ✅ Connected
- qwen3:4b (chat): ✅ Available
- qwen3:4b (summary): ✅ Available

Token Usage:
- Total tokens in room: 28,552
- High usage agents: Zahra (25,230)
- Auto-compression: ✅ Enabled

Context Sharing:
- Shared contexts: 5
- Current location contexts: 2
```

The status command provides:
- **World State**: Current location and counts of agents, items, and inventory
- **AI Models**: Ollama connectivity and model availability
- **Token Usage**: Total tokens, high usage agents, and auto-compression status
- **Context Sharing**: Statistics about shared contexts across agents

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
| `/model_state [agent]` | Show model state for all agents or specific agent | `/model_state` or `/model_state alice` |
| `/share <context>` | Share context with all agents | `/share The weather has turned stormy` |

### Model State Command

The `/model_state` command shows detailed information about the AI model state:

```
🤖 Model States for All Agents:

Zahra: Model=qwen3:4b, Context=15,230 tokens, Last used=2025-06-06T09:45:22
Kael: Model=qwen3:4b, Context=8,450 tokens, Last used=2025-06-06T09:43:10
```

For a specific agent, use `/model_state <agent>`:

```
🤖 Model State for Zahra:
Model=qwen3:4b, Context=15,230 tokens, Last used=2025-06-06T09:45:22
```

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
- Current location: world/sunspire_city
- Agents in room: 2
- Items in room: 1
- Inventory items: 2

AI Models:
- Ollama: ✅ Connected
- qwen3:4b (chat): ✅ Available
- qwen3:4b (summary): ✅ Available

Token Usage:
- Total tokens in room: 28552
- High usage agents: Zahra (25230)
- Auto-compression: ✅ Enabled

Context Sharing:
- Shared contexts: 5
- Current location contexts: 2

> /model_state
🤖 Model States for All Agents:

Zahra: Model=qwen3:4b, Context=15230 tokens, Last used=2025-06-06T09:45:22
Kael: Model=qwen3:4b, Context=8450 tokens, Last used=2025-06-06T09:43:10

> /compress_all
Compressed contexts for 2 agents:
- Zahra: 25,230 → 10,542 tokens (saved 14,688)
- Kael: 3,322 → 3,322 tokens (no compression needed)

Total tokens saved: 14,688
```
