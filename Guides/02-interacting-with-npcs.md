# Interacting with NPCs (Agents)

Ollama Dungeon's agents are AI-powered NPCs with their own personalities, memories, and contexts. This guide explains how to interact with them.

## Basic NPC Interactions

| Command | Description | Example |
|---------|-------------|---------|
| `/say <agent> <message>` | Talk to an agent | `/say zahra What do you think of this marketplace?` |
| `/sayto <agent> <message>` | Alternative to `/say` | `/sayto kael How long have you been mining here?` |
| `/talk <agent> <message>` | Alternative to `/say` | `/talk zahra Tell me about the rare crystals` |
| `/agents` or `/people` | List all NPCs in the current room | `/agents` |
| `/memory <agent>` | Show an agent's memory summary | `/memory zahra` |

**Note:** In endless conversation mode (started with `/conv`), the `/say` command behaves differently:
- `/say <message>` - Everyone HEARS the message, only targeted agents respond
- `/say <agent> <message>` - All agents hear, only the specified agent responds
- `/say agent1,agent2 <message>` - All agents hear, only the specified agents respond (comma-separated)

## Context Sharing

Agents can respond more appropriately if they have context about situations. You can share information with them using:

| Command | Description | Example |
|---------|-------------|---------|
| `/share <context>` or `/summarize <context>` | Share context with all agents in room | `/share The crystal formations are glowing brighter than usual` |
| `/share all <context>` | Share context with all agents (explicit) | `/share all The crystals are glowing` |
| `/share <agent> <context>` | Share context with a specific agent | `/share zahra I'm looking for information about rare gems` |
| `/share <agent1,agent2> <context>` | Share context with multiple specific agents | `/share kael,zahra I suspect there's something unusual about these crystals` |

## Following Behavior

You can control whether agents follow you as you move between locations:

| Command | Description | Example |
|---------|-------------|---------|
| `/follow <agent>` | Have an agent follow you | `/follow zahra` |
| `/stay <agent>` | Make an agent stop following and stay in current location | `/stay zahra` |

When an agent is following you, they'll move with you when you use the `/go` command. Use `/stay` to make them stop following and remain in their current room, which is useful for managing which NPCs participate in conversations in different locations.

## Endless Conversation Mode

Endless conversation mode allows you to have ongoing multi-agent conversations where agents participate naturally and you can control who responds. Unlike normal conversations, endless mode persists until you end it, making it perfect for extended discussions.

### Starting an Endless Conversation

| Command | Description | Example |
|---------|-------------|---------|
| `/conv <agent1,agent2[,player]> <topic>` | Start endless conversation mode with specified participants and topic | `/conv zahra,kael Discuss the recent crystal harvest` |
| `/conversation <participants> <topic>` | Alternative to `/conv` | `/conversation player,zahra,kael Share information about the caves` |

**Important:** Specify at least 2 participants separated by commas. Include `player` if you want to be part of the conversation.

### Conversation Controls

| Command | Description | Example |
|---------|-------------|---------|
| `/endconv` | End the endless conversation mode | `/endconv` |
| `/invite <agent>` | Add an agent to the ongoing conversation | `/invite kael` |
| `/remove <agent>` | Remove an agent from the conversation | `/remove zahra` |
| `/dialog <agent1,agent2> <exchanges>` | Generate automated dialog between two agents (only works in endless mode) | `/dialog zahra,kael 3` |

### How Endless Mode Works

When in endless mode:

1. **Starting the conversation** - All participating agents are initialized with the topic and context
2. **Normal talk** (`/say <message>`) - All agents HEAR your message, all participants respond once in order
3. **Directed talk** (`/say <agent> <message>`) - All agents HEAR your message, only the specified agent responds
4. **Multiple targets** (`/say agent1,agent2 <message>`) - All agents HEAR, only the specified agents respond

**Key difference:** All agents always hear what you say (they remember it), but only targeted agents respond. This maintains conversational continuity while allowing you to direct specific questions.

### Automated Dialog Generation

The `/dialog` command creates automated conversation between two agents:

```
/dialog <agent1,agent2> <number_of_exchanges>
```

- Only works in endless conversation mode
- Both agents must be in the current room and participating in the conversation
- Maximum 10 exchanges to prevent infinite loops
- Each exchange = one response from each agent (2 total messages per exchange)

Example: `/dialog zahra,kael 3` generates 3 exchanges (6 total messages) alternating between Zahra and Kael.

### Location Changes in Endless Mode

When you move to a different location while in endless conversation mode:
- **Following agents** automatically move with you and remain in the conversation
- **Non-following agents** are automatically removed from the endless conversation
- The conversation continues with remaining participants

This makes it easy to have conversations while traveling - just have agents follow you before moving!

## Agent Memory and Context

Agents remember their interactions with you and other agents. Their responses are influenced by:

1. **Personal history** - What they remember from past conversations
2. **Shared context** - Information you've shared with them
3. **Room context** - Their understanding of the current location
4. **Personal traits** - Their personality defined in their JSON file

### Memory Types

Agents store different types of memories in CSV format with these technical categories:

| Memory Type | Description | Example Usage |
|-------------|-------------|---------------|
| **dialogue** | Conversations with player or other agents | Player said: "Hello" - I responded: "Greetings!" |
| **observation** | Environmental details and events witnessed | Observed: Met a new visitor who just arrived in Sunspire City |
| **event** | Actions the agent performed | Did: agreed to follow the player |
| **emotion** | Emotional states and feelings | Felt: excited about the crystal discovery |

These memory types help agents understand the context and nature of their experiences, allowing them to respond more appropriately based on what they remember.

You can view an agent's memories with:
```
/memory <agent_name>
```

## Managing Agent Context

Over time, agents accumulate a lot of context which may consume tokens. Use these commands to manage this:

| Command | Description | Example |
|---------|-------------|---------|
| `/tokens <agent>` | Show token usage for an agent | `/tokens zahra` |
| `/compress <agent>` | Manually compress an agent's context | `/compress kael` |
| `/compress_all` | Compress context for all agents in room | `/compress_all` |
| `/reset <agent>` | Reset agent's memory and context | `/reset zahra` |

## AI Thinking Behavior

Agents use AI models that may generate "thinking" content - internal reasoning that helps them formulate better responses. The game provides two levels of control over this behavior:

### Primary Control: `enable_thinking`
The `enable_thinking` setting in `config.py` controls whether thinking is generated at the API level:

- **When `enable_thinking: True`**: The game passes `think: true` to the Ollama API, enabling the model to use its thinking capabilities. Some models (like deepseek-r1) use a separate "thinking" field in their JSON response rather than `<thinking>` tags. This gives models the benefit of thinking for better reasoning.

- **When `enable_thinking: False` (default)**: The game passes `think: false` to the Ollama API, which prevents the model from generating thinking content in the first place. This saves tokens and processing time.

### Fallback Control: `strip_thinking_tokens`
As a safety measure, `strip_thinking_tokens: True` (default) removes any `<thinking>` tags that might appear in responses, providing clean output. This works as a fallback cleanup even when thinking is enabled at the API level.

### Default Behavior

With the default settings (`enable_thinking: False` and `strip_thinking_tokens: True`):
- Thinking is disabled at the API level to save tokens and processing time
- Any `<thinking>` tags that might still appear are removed as fallback cleanup
- You get faster responses with lower token usage

### When to Enable Thinking

Enable thinking (`enable_thinking: True`) when:
- Using models that benefit from thinking mode (like deepseek-r1)
- You want more detailed reasoning in responses
- You need complex problem-solving capabilities

## Analytics and Monitoring

Monitor agent performance, token usage, and system health with these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `/analytics [agent_name]` | Show detailed token analytics and usage statistics | `/analytics zahra` |
| `/analytics save` | Save analytics data to file | `/analytics save` |
| `/model_state [agent_name]` | Show current model state and context size for agents | `/model_state zahra` |
| `/status` | Show overall system status and connectivity | `/status` |

### Understanding Analytics

The `/analytics` command provides comprehensive statistics:

**For specific agents:**
- Total tokens used and API calls made
- Conversation turns participated in
- Average tokens per call
- Token limit expansions and context compressions
- Peak tokens in single call
- Activity timeline (first seen, last active)

**System-wide (no arguments):**
- Total agents tracked across all sessions
- Aggregate token usage and API calls
- Total expansions and compressions
- Top token users ranking

### Model State Information

The `/model_state` command shows:
- Current model loaded for the agent
- Token context size (num_ctx)
- Last time model was loaded/reloaded
- Whether parameters match current settings

### System Status

The `/status` command provides:
- Current location and room info
- Agent and item counts
- Ollama connectivity status
- Available models
- Token usage summary across all agents
- Auto-compression status
- Context sharing statistics

## Example Conversation

```
> /agents
People here:
- Zahra (shrewd): A skilled merchant trader with keen eyes for valuable goods

> /say zahra Hello! Can you tell me about this marketplace?
You say to Zahra: "Hello! Can you tell me about this marketplace?"
Zahra says: "Welcome to Sunspire City's merchant quarter! This is where the finest goods from across the realm find their way to discerning buyers. I specialize in rare crystals and magical artifacts. Are you perhaps looking for something specific, or just browsing today?"

> /say zahra Yes, I just arrived in the city. Any recommendations on what I should see first?
You say to Zahra: "Yes, I just arrived in the city. Any recommendations on what I should see first?"
Zahra says: "Well, you should definitely visit the scholar district to the east if you're interested in learning about our city's history. And if you're the adventurous type, the crystal caves below hold incredible treasures - though they can be dangerous. Kael down there knows those tunnels better than anyone."

> /memory zahra
Zahra's recent activities:
Said: Welcome to Sunspire City's merchant quarter! This is where the finest goods from across the realm find their way to discerning buyers.
Said: Well, you should definitely visit the scholar district to the east if you're interested in learning about our city's history.
Observed: Met a new visitor who just arrived in Sunspire City
```
