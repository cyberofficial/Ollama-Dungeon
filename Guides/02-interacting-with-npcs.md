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
- `/say <message>` - Everyone in the conversation responds
- `/say <agent> <message>` - Only the specified agent responds
- `/say agent1,agent2 <message>` - Only the specified agents respond (comma-separated)

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

## Agent Memory and Context

Agents remember their interactions with you and other agents. Their responses are influenced by:

1. **Personal history** - What they remember from past conversations
2. **Shared context** - Information you've shared with them
3. **Room context** - Their understanding of the current location
4. **Personal traits** - Their personality defined in their JSON file

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

## Example Conversation

Here's an example of interacting with agents:

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
Zahra remembers:
Said: Welcome to Sunspire City's merchant quarter! This is where the finest goods from across the realm find their way to discerning buyers.
Said: Well, you should definitely visit the scholar district to the east if you're interested in learning about our city's history.
Observed: Met a new visitor who just arrived in Sunspire City
```
