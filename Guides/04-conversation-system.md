# Conversation System

Ollama Dungeon includes an advanced conversation system that allows for complex interactions between you and the NPCs, as well as facilitating NPC-to-NPC conversations. This guide explains how to use these features.

## Basic Conversations

Before diving into multi-agent conversations, you can talk to individual agents using these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `/say <agent> <message>` | Talk to a specific agent | `/say zahra Hello there` |
| `/sayto <agent> <message>` | Alternative to `/say` (for immersion) | `/sayto zahra Greetings` |
| `/talk <agent> <message>` | Alternative to `/say` | `/talk zahra How are you?` |

## Multi-Agent Conversations

The game offers a sophisticated system for multi-participant conversations using endless mode:

| Command | Description | Example |
|---------|-------------|---------|
| `/conv <participants> <topic>` | Start an endless conversation with specified participants about a topic | `/conv zahra,kael,player The recent crystal discoveries` |
| `/conversation <participants> <topic>` | Alternative to `/conv` | `/conversation zahra,kael Magical artifacts in the caves` |

### Conversation Parameters:

- **Participants**: Comma-separated list of participant names (use "player" to include yourself). At least 2 participants required.
- **Topic**: What the conversation will be about

### Example:
```
> /conv zahra,kael,player The mysterious crystal formations
🗣️ Endless conversation mode activated!
📋 Participants: Zahra, Kael, Player
📝 Topic: The mysterious crystal formations

💡 How it works:
- Normal talk (/say <message>) = Everyone replies in order once
- Directed talk (/say alice <message>) = Only Alice replies, others listen
- Multiple targets (/say alice,bob <message>) = Alice and Bob reply, others listen
- Type /endconv to end conversation mode
```

## Context Sharing

Before starting a conversation, you can share context with agents to give them background information:

| Command | Description | Example |
|---------|-------------|---------|
| `/share <message>` | Share with all agents in current room | `/share I'm looking for rare crystals` |
| `/share all <message>` | Share with all agents (explicit) | `/share all I need information about artifacts` |
| `/share <agent> <message>` | Share with a single agent | `/share zahra Tell me about your grandmother's stories` |
| `/share <agent1,agent2> <message>` | Share with multiple agents | `/share zahra,kael What do you know about the Heart Crystal?` |

**Notes:**
- Context shared via `/share` is added to agents' memories and conversation context
- This helps agents understand the situation before a conversation starts
- Useful for setting up background information or explaining your goals

## Endless Conversation Mode

The `/conv` command always starts "endless conversation mode" where the conversation continues until you explicitly end it with `/endconv`:

| Command | Description | Example |
|---------|-------------|---------|
| `/endconv` | End an endless conversation | `/endconv` |
| `/invite <agent>` | Invite an agent to join the endless conversation | `/invite alice` |
| `/remove <agent>` | Remove an agent from the endless conversation | `/remove bob` |
| `/say <message>` | Everyone responds in order | `/say What do you all think?` |
| `/say <agent> <message>` | Only the specified agent responds | `/say zahra Tell me more` |
| `/say <agent1,agent2> <message>` | Only the specified agents respond | `/say zahra,kael What are your thoughts?` |
| `/dialog <agent1,agent2> <exchanges>` | Generate automated dialog between two agents (1-10 exchanges) | `/dialog zahra,kael 5` |

### Location-Aware Endless Mode

Endless mode is location-aware:
- When you move to a new location, agents who are not following you are automatically removed from the endless conversation
- Only agents present in your current location or agents who are following you can participate
- Use `/invite <agent>` to add agents from your current location back into the conversation
- Use `/remove <agent>` to manually remove agents from the conversation

### Agent Following Mechanics

Agents can follow you between rooms, maintaining their participation in endless conversations:

| Command | Description | Example |
|---------|-------------|---------|
| `/follow <agent>` | Have an agent follow you between rooms | `/follow zahra` |
| `/stay <agent>` | Have an agent stop following and stay in current location | `/stay zahra` |

**How Following Works:**
- When an agent is following, they automatically move with you when you change locations
- Following state is persisted in the agent's data file
- Following agents remain in endless conversations when you move to new rooms
- Non-following agents are automatically removed from endless conversations when you leave their location
- Agents remember following state in their memory (stored as 'following_player' events)

**Endless Mode + Following Interaction:**
- Agents following you will stay in endless conversations across room changes
- When you move, the game displays which agents left the conversation (non-following)
- You can invite new agents from your current location to join the conversation
- Use `/stay <agent>` to make a following agent remain in their current location

### Conversation Response Cleaning

The game automatically cleans agent responses to maintain immersion:
- Removes thinking tokens (like `<thinking>` tags from the AI model)
- Strips speaker names from responses (e.g., "Zahra: Hello" becomes "Hello")
- Removes meta-text like "says:", "responds:", "replies:"
- Cleans up action descriptions that don't contain actual dialogue
- Removes quotation marks from quoted responses
- Limits overly long responses to the first 1-2 sentences

This ensures that agent responses appear as natural dialogue rather than AI-generated text with formatting artifacts.

## Endless Mode Example

```
> /conv zahra,kael,player The rare crystal formations
🗣️ Endless conversation mode activated!
📋 Participants: Zahra, Kael, Player
📝 Topic: The rare crystal formations

💡 How it works:
- Normal talk (/say <message>) = Everyone replies in order once
- Directed talk (/say alice <message>) = Only Alice replies, others listen
- Multiple targets (/say alice,bob <message>) = Alice and Bob reply, others listen
- Type /endconv to end conversation mode

💭 It's your turn to speak about The rare crystal formations
🗣️ **You**: I've heard rumors about incredibly rare crystal formations deep in the caves. Do either of you know anything about them?

💬 Zahra is thinking...
🗣️ **Zahra**: I've heard whispers about something called the Heart of the Mountain. An ancient crystal formation supposedly deep in the caves, with the power to amplify magical energies a hundredfold. My grandmother used to tell stories about it.

💬 Kael is thinking...
🗣️ **Kael**: That's not just stories. I've found traces of it - crystalline formations that sing with an otherworldly harmony. The legendary Heart Crystal is real, hidden in passages so deep and dangerous that few have dared to search for it.

> /say zahra Tell me more about these stories your grandmother told
You say to Zahra: "Tell me more about these stories your grandmother told"

💬 Zahra is thinking...
🗣️ **Zahra**: She spoke of a crystal so pure it could store memories, and so powerful it could amplify any spell cast near it. The Heart of the Mountain was said to be the seed from which all other crystals in these caves grew.

> /go up
🚶 Moving up...
📍 You are now in: Sunspire City - Oasis Plaza
🚶 Zahra and Kael left the endless conversation (not following)

> /invite palace_guardian
❌ Agent 'palace_guardian' not found in current location. Available: merchant_guard

> /invite merchant_guard
✅ Merchant_guard has joined the endless conversation!

💭 It's your turn to speak about The rare crystal formations
🗣️ **You**: Guardian, I seek knowledge about the legendary crystal formations. Can you tell me about them?

[Conversation continues until you use /endconv]
```

## Automated Dialog

You can make two NPCs talk to each other automatically during endless conversation mode:

| Command | Description | Example |
|---------|-------------|---------|
| `/dialog <agent1,agent2> <exchanges>` | Generate automated dialog between two agents (1-10 exchanges) | `/dialog zahra,kael 5` |

**Notes:**
- Only works during endless conversation mode
- Requires exactly 2 agents (comma-separated)
- Number of exchanges must be between 1-10 (safety limit prevents infinite loops)
- Both agents must be in the current location and part of the endless conversation
- Each exchange alternates between the two agents
- A 10-exchange limit is enforced to prevent excessive generation time and potential loops

## Tips for Effective Conversations

1. **Choose appropriate topics** - Be specific about what you want to discuss
2. **Include relevant participants** - Different agents have different knowledge
3. **Use context sharing** - Set up context before starting a conversation with `/share`
4. **Be patient** - Complex conversations may take time to generate
5. **Use following strategically** - Make key allies follow you to maintain conversations across locations
6. **Combine /share with /conv** - Share context first, then start endless mode for better-informed discussions

## Agent Response Behavior

Agents in Ollama Dungeon are designed to maintain unique personalities and response patterns. The system includes settings that ensure agents respond differently, even when presented with similar situations:

- **Randomized responses**: The game uses unique random seeds for each agent to prevent identical responses from different characters. This feature is enabled by default in the `AGENT_SETTINGS` configuration.

- **Response temperature**: The temperature setting (default: 0.7) controls how creative and varied agent responses are. A higher temperature (closer to 1.0) produces more diverse responses, while a lower temperature creates more predictable ones.

If you notice agents occasionally giving similar responses, try checking that the `randomize_responses` setting is enabled in `config.py`. These settings help prevent the issue where different characters might generate identical responses.

## Conversation System Workflow

Understanding how the conversation system works under the hood can help you use it more effectively:

### Normal Conversations (Outside Endless Mode)

1. **Player speaks** - Use `/say <agent> <message>` to talk to an agent
2. **Agent processes** - The agent receives your message with room context
3. **Response generation** - AI generates a response based on agent's personality, memory, and context
4. **Response cleaning** - System strips meta-text and formats the response
5. **Memory storage** - Conversation is stored in agent's memory for future reference

### Endless Conversation Mode

1. **Start conversation** - Use `/conv <participants> <topic>` to begin
2. **Context setup** - All agents receive conversation context and topic
3. **Turn-based dialogue** - Participants speak in order (or targeted with specific agents)
4. **Context sharing** - All participants hear what others say (added to their context)
5. **Memory updates** - Each conversation turn is stored in agent memories
6. **Location changes** - Moving to new rooms removes non-following agents from conversation
7. **End conversation** - Use `/endconv` to return to normal mode

### Response Generation Process

When an agent generates a response:

1. **Gather context** - Agent's memory, conversation history, room description
2. **Build prompt** - Create a prompt with current situation and conversation state
3. **AI generation** - Send to Ollama model with agent's personality
4. **Token stripping** - Remove thinking tokens (e.g., `<thinking>...</thinking>`)
5. **Response cleaning** - Strip meta-text, speaker names, and formatting artifacts
6. **Display** - Show cleaned response to player
7. **Context update** - Add response to all participants' context and memory

## Conversation Context Management

The game manages conversation context intelligently to provide coherent conversations:

### Token Management for Conversations

During conversations, the system automatically manages token limits for each agent:

- Token limits start small (`starting_tokens` setting, currently set to 10) and automatically increase as needed
- The system displays messages when token limits are increased
- If you notice messages about token limits increasing during gameplay, this is normal behavior

### Agent Memory

Agents remember their conversations with you and with other NPCs:

- Recent interactions are stored in the agent's memory
- Older memories are automatically summarized to save space
- You can view an agent's memory with `/memory <agent_name>`

### Tips for Managing Context

- Use `/compress <agent_name>` to manually compress an agent's context if they seem to be forgetting important information
- The `reload_on_lower` setting (default: `False`) optimizes model loading by not reloading when switching to an agent with a lower token count
- For long sessions, occasional use of `/save` can help preserve important context
- Agent memories are automatically summarized when they exceed `max_memory_entries` from `AGENT_SETTINGS`

## Quick Reference: Conversation Commands

**Basic Conversations:**
- `/say <agent> <message>` - Talk to an agent
- `/sayto <agent> <message>` - Alternative (for immersion)
- `/talk <agent> <message>` - Alternative

**Context Sharing:**
- `/share <message>` - Share with all agents in room
- `/share all <message>` - Share with all agents (explicit)
- `/share <agent> <message>` - Share with one agent
- `/share <agent1,agent2> <message>` - Share with multiple agents

**Endless Conversations:**
- `/conv <participants> <topic>` - Start endless mode
- `/conversation <participants> <topic>` - Alternative to `/conv`
- `/endconv` - End endless mode
- `/invite <agent>` - Add agent to conversation
- `/remove <agent>` - Remove agent from conversation

**Endless Mode Speaking:**
- `/say <message>` - Everyone responds
- `/say <agent> <message>` - Only that agent responds
- `/say <agent1,agent2> <message>` - Only those agents respond
- `/dialog <agent1,agent2> <exchanges>` - Automated NPC dialog (1-10 exchanges)

**Agent Following:**
- `/follow <agent>` - Agent follows you between rooms
- `/stay <agent>` - Agent stops following

**Memory & Context:**
- `/memory <agent>` - View agent's memory
- `/compress <agent>` - Compress agent's context
- `/compress_all` - Compress all agents in room
