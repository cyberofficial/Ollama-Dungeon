# Interacting with NPCs (Agents)

Ollama Dungeon's agents are AI-powered NPCs with their own personalities, memories, and contexts. This guide explains how to interact with them.

## Basic NPC Interactions

| Command | Description | Example |
|---------|-------------|---------|
| `/say <agent> <message>` | Talk to an agent | `/say alice What do you think of this tavern?` |
| `/sayto <agent> <message>` | Alternative to `/say` | `/sayto bob How long have you been here?` |
| `/talk <agent> <message>` | Alternative to `/say` | `/talk grix Tell me about the cave` |
| `/agents` or `/people` | List all NPCs in the current room | `/agents` |
| `/memory <agent>` | Show an agent's memory summary | `/memory alice` |

## Context Sharing

Agents can respond more appropriately if they have context about situations. You can share information with them using:

| Command | Description | Example |
|---------|-------------|---------|
| `/share <context>` or `/summarize <context>` | Share context with all agents in room | `/share The sky is getting dark and it looks like rain` |
| `/share <agent> <context>` | Share context with a specific agent | `/share alice I'm looking for information about a stolen artifact` |
| `/share <agent1,agent2> <context>` | Share context with multiple specific agents | `/share bob,alice I suspect someone is watching us` |

## Following Behavior

You can control whether agents follow you as you move between locations:

| Command | Description | Example |
|---------|-------------|---------|
| `/follow <agent>` | Have an agent follow you | `/follow alice` |
| `/stay <agent>` | Make an agent stop following and stay in current location | `/stay alice` |

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
| `/tokens <agent>` | Show token usage for an agent | `/tokens alice` |
| `/compress <agent>` | Manually compress an agent's context | `/compress bob` |
| `/compress_all` | Compress context for all agents in room | `/compress_all` |
| `/reset <agent>` | Reset agent's memory and context | `/reset alice` |

## Example Conversation

Here's an example of interacting with agents:

```
> /agents
People here:
- Alice (friendly): A woman with red hair wearing a tavern keeper's apron
- Bob (curious): A middle-aged man sitting at a corner table

> /say alice Hello! Can you tell me about this place?
You say to Alice: "Hello! Can you tell me about this place?"
Alice says: "Welcome to the Rusty Dragon Tavern! We're the most popular establishment in town. Folks come here for my famous honey mead and to catch up on the latest gossip. Are you new in town? I don't believe I've seen you before."

> /say alice Yes, I just arrived today. Any recommendations on what I should do?
You say to Alice: "Yes, I just arrived today. Any recommendations on what I should do?"
Alice says: "Well, you should definitely explore the market to the north. They have all sorts of interesting wares. And if you're the adventurous type, I've heard there are some interesting caves in the forest to the west. But be careful - there are rumors of strange creatures out there."

> /memory alice
Alice remembers:
Said: Welcome to the Rusty Dragon Tavern! We're the most popular establishment in town.
Said: Well, you should definitely explore the market to the north.
Observed: Met a new traveler who just arrived in town
```
