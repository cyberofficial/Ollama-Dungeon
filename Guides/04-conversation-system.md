# Conversation System

Ollama Dungeon includes an advanced conversation system that allows for complex interactions between you and the NPCs, as well as facilitating NPC-to-NPC conversations. This guide explains how to use these features.

## Multi-Agent Conversations

The game offers a sophisticated system for multi-participant conversations:

| Command | Description | Example |
|---------|-------------|---------|
| `/conv <participants> [turns] <topic>` | Start a conversation with specified participants about a topic | `/conv alice,bob,player 5 The recent thefts in town` |
| `/conversation <participants> [turns] <topic>` | Alternative to `/conv` | `/conversation alice,bob Magical artifacts` |

### Conversation Parameters:

- **Participants**: Comma-separated list of participant names (use "player" to include yourself)
- **Turns** (optional): Number of conversation exchanges (if omitted, endless mode is activated)
- **Topic**: What the conversation will be about

### Example:
```
> /conv alice,bob,player 3 The history of the town
🗣️ Starting conversation about: The history of the town
Participants: Alice, Bob, Player
```

## Example Multi-Agent Conversation

```
> /conv alice,bob,player 3 The strange noises from the forest
🗣️ Starting conversation about: The strange noises from the forest
Participants: Alice, Bob, Player

💭 It's your turn to speak about The strange noises from the forest
🗣️ **You**: Have either of you heard those strange howling sounds coming from the forest at night?

💬 Alice is thinking...
🗣️ **Alice**: Yes, I've heard them for the past three nights. It doesn't sound like any wolf or animal I'm familiar with. Bob, you live closer to the forest edge - have you seen anything unusual?

💬 Bob is thinking...
🗣️ **Bob**: Indeed I have. Last night I saw strange lights among the trees, and the howling seemed to come from that direction. I'm too afraid to investigate alone, but someone should definitely look into it.

🎯 Conversation concluded!
```

## Endless Conversation Mode

When you omit the turns parameter in the `/conv` command, you enter "endless conversation mode" where the conversation continues until you explicitly end it:

| Command | Description | Example |
|---------|-------------|---------|
| `/endconv` | End an endless conversation (only during your turn) | `/endconv` |
| `/invite <agent>` | Invite an agent to join the endless conversation | `/invite alice` |
| `/remove <agent>` | Remove an agent from the endless conversation | `/remove bob` |

In endless mode, you can use special commands:
- `/say <message>` - Everyone responds in order
- `/say <agent> <message>` - Only the specified agent responds
- `/say <agent1,agent2> <message>` - Only the specified agents respond

### Location-Aware Endless Mode

Endless mode is now location-aware:
- When you move to a new location, agents who are not following you are automatically removed from the endless conversation
- Only agents present in your current location or agents who are following you can participate
- Use `/invite <agent>` to add agents from your current location back into the conversation
- Use `/remove <agent>` to manually remove agents from the conversation

## Endless Mode Example

```
> /conv alice,bob,player The magical artifact
🗣️ Endless conversation mode activated!
📋 Participants: Alice, Bob, Player
📝 Topic: The magical artifact

💭 It's your turn to speak about The magical artifact
🗣️ **You**: I've heard rumors about an ancient artifact hidden somewhere in these parts. Do either of you know anything about it?

💬 Alice is thinking...
🗣️ **Alice**: I've heard whispers about something like that. An old relic from before the great war, supposedly with the power to control weather. My grandmother used to tell stories about it.

💬 Bob is thinking...
🗣️ **Bob**: Control weather? That's not what I heard. The artifact I know of is said to reveal hidden truths. It's supposedly locked away in a cave system north of here, guarded by ancient traps.

💭 It's your turn to speak about The magical artifact
🗣️ **You**: That's fascinating. Have either of you ever tried to find it?

> /go north
🚶 Moving north...
📍 You are now in: Cave Entrance
⚠️ Alice and Bob were removed from endless conversation (not following)

> /invite cave_guardian
✅ Cave Guardian added to endless conversation

💭 It's your turn to speak about The magical artifact
🗣️ **You**: Guardian, I seek knowledge about the ancient artifact. Can you tell me about it?

[Conversation continues until you use /endconv]
```

## Automated Dialog

You can also make two NPCs talk to each other automatically:

| Command | Description | Example |
|---------|-------------|---------|
| `/dialog <agent1,agent2> <exchanges>` | Generate automated dialog between two agents | `/dialog alice,bob 5` |

This works only during endless conversation mode and creates a natural dialog between the specified agents.

## Tips for Effective Conversations

1. **Choose appropriate topics** - Be specific about what you want to discuss
2. **Include relevant participants** - Different agents have different knowledge
3. **Use context sharing** - Set up context before starting a conversation with `/share`
4. **Be patient** - Complex conversations may take time to generate

## Agent Response Behavior

Agents in Ollama Dungeon are designed to maintain unique personalities and response patterns. The system includes settings that ensure agents respond differently, even when presented with similar situations:

- **Randomized responses**: The game uses unique random seeds for each agent to prevent identical responses from different characters. This feature is enabled by default in the `AGENT_SETTINGS` configuration.

- **Response temperature**: The temperature setting (default: 0.7) controls how creative and varied agent responses are. A higher temperature (closer to 1.0) produces more diverse responses, while a lower temperature creates more predictable ones.

If you notice agents occasionally giving similar responses, try checking that the `randomize_responses` setting is enabled in `config.py`. These settings help prevent the issue where different characters might generate identical responses.

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
- Shared context can be viewed with `/context <agent_name>`

### Tips for Managing Context

- Use `/compress <agent_name>` to manually compress an agent's context if they seem to be forgetting important information
- The `reload_on_lower` setting (default: `False`) optimizes model loading by not reloading when switching to an agent with a lower token count
- For long sessions, occasional use of `/save` can help preserve important context
