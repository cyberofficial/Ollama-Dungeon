# Basic Commands Reference

This guide provides a comprehensive reference for all commands in Ollama Dungeon, organized by category.

## Movement & Exploration

| Command | Description | Example |
|---------|-------------|---------|
| `/look` or `/l` | Describe the current room | `/look` |
| `/go <direction>` | Move in a direction | `/go north` |
| `/move <direction>` | Alternative to `/go` | `/move east` |

**Available directions** depend on the current room, but typically include:
- Cardinal: north, south, east, west
- Vertical: up, down
- Relative: in, out

## Interaction Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/say <agent> <message>` | Talk to a specific agent | `/say zahra Hello!` |
| `/sayto <agent> <message>` | Alternative to `/say` (for immersion) | `/sayto zahra Hello!` |
| `/talk <agent> <message>` | Alternative to `/say` | `/talk zahra Hello!` |

## Conversation System

The conversation system allows for multi-agent conversations.

| Command | Description | Example |
|---------|-------------|---------|
| `/conv <participants> <topic>` | Start endless conversation mode | `/conv player,zahra,kamar discussing trade` |
| `/conversation <participants> <topic>` | Alternative to `/conv` | `/conversation zahra,kamar arguing about prices` |
| `/endconv` | End endless conversation mode | `/endconv` |
| `/invite <agent>` | Add agent to endless conversation | `/invite zahra` |
| `/remove <agent>` | Remove agent from endless conversation | `/remove kamar` |
| `/dialog <agent1,agent2> <exchanges>` | Automated dialog between 2 agents (endless mode only) | `/dialog zahra,kamar 3` |

**Conversation Mode:**

All `/conv` commands start endless conversation mode where the conversation continues until you end it with `/endconv`:
- Example: `/conv player,zahra,kamar discussing the merchant guild`
- Use `/say <message>` to talk to everyone (all respond in order)
- Use `/say <agent> <message>` to target specific agents
- Use `/say agent1,agent2 <message>` to target multiple specific agents

**Participant Format:**
- Comma-separated list: `player,zahra,kamar`
- At least 2 participants required
- Use `player` to include yourself in the conversation
- All non-player participants must be agents in the current room

## Information Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/agents` or `/people` | List all NPCs in current room | `/agents` |
| `/memory <agent>` | Show an agent's memory summary | `/memory zahra` |

## Inventory Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/inventory` or `/inv` | View your inventory | `/inventory` |
| `/pickup <item>` | Pick up an item from room | `/pickup crystal_key` |
| `/take <item>` | Alternative to `/pickup` | `/take ancient_scroll` |
| `/use <item>` | Use an item from inventory | `/use healing_potion` |

## Context Sharing

| Command | Description | Example |
|---------|-------------|---------|
| `/summarize [target(s)] <message>` | Share context with agents | `/summarize I'm looking for the merchant guild` |
| `/share [target(s)] <message>` | Alternative to `/summarize` | `/share all The caravan arrives tomorrow` |

**Target formats:**
- No target: Share with all agents in room
- `all`: Share with all agents in room
- Single agent: `/share zahra The prices are fair`
- Multiple agents: `/share zahra,kamar The market is closing soon`

## Agent Control

| Command | Description | Example |
|---------|-------------|---------|
| `/follow <agent>` | Have agent follow you between rooms | `/follow zahra` |
| `/stay <agent>` | Have agent stop following you | `/stay zahra` |
| `/reset <agent>` | Reset agent's memory and context | `/reset zahra` |

**How following works:**
- Agents set to follow will automatically move with you when you change rooms
- Following agents persist in endless conversation mode when you move
- Use `/stay` to make an agent remain in their current location

## Token Management

Monitor and manage AI context tokens to prevent memory overflow.

| Command | Description | Example |
|---------|-------------|---------|
| `/tokens [agent]` | Show token usage (all agents or specific) | `/tokens` or `/tokens zahra` |
| `/analytics [agent]` | Show detailed token analytics and usage history | `/analytics` or `/analytics zahra` |
| `/model_state [agent]` | Show current model state and context size | `/model_state` or `/model_state zahra` |
| `/compress <agent>` | Manually compress an agent's context | `/compress zahra` |
| `/compress_all` | Compress context for all agents in room | `/compress_all` |

**Token monitoring:**
- Tokens represent AI memory usage
- High token counts (25,000+) trigger warnings
- Auto-compression runs when approaching limits (if enabled)
- Manual compression can free up tokens immediately

## System Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/status` | Show system status and Ollama connectivity | `/status` |
| `/save [name]` | Save game state (default: "default") | `/save my_game` |
| `/load [name]` | Load game state (default: "default") | `/load my_game` |
| `/saves` | List all saved games | `/saves` |
| `/delete <save_name>` | Delete a saved game | `/delete old_save` |
| `/help` | Show available commands | `/help` |
| `/quit`, `/exit`, or `/q` | Exit the game | `/quit` |

## Tips for New Players

### Navigation
1. **Always explore** - Use `/look` when entering new rooms to learn about your surroundings
2. **Multiple command forms** - Many commands have shortcuts (like `/l` for `/look`) for faster typing
3. **Check exits** - Room descriptions mention available directions
4. **Save frequently** - Use `/save <name>` to create save points

### Conversation
1. **Start simple** - Use `/say <agent> <message>` for one-on-one conversations
2. **Group discussions** - Use `/conv` for multi-agent conversations about specific topics
3. **Endless mode** - Omit the turn count for conversations that continue until you end them
4. **Target responses** - In endless mode, use `/say <agent> <message>` to have only that agent respond

### Token Management
1. **Monitor usage** - Use `/tokens` to check context sizes before long conversations
2. **Compress when needed** - Use `/compress_all` if agents are slow or unresponsive
3. **Check analytics** - Use `/analytics` to see which agents use the most tokens

### Agent Management
1. **Build relationships** - Agents remember conversations through their memory system
2. **Travel companions** - Use `/follow` to have agents accompany you
3. **Reset if needed** - Use `/reset` to clear an agent's memory if needed

## Example Sessions

### Basic Exploration
```
> /look
You are in Sunspire City's Oasis Plaza. Shimmering waters reflect towering spires of golden sandstone. There are paths leading north to the palace district, south to the merchant quarter, east to the scholar district, and west to the whispering dunes.

> /go south
You moved to the merchant quarter. It's a bustling marketplace with colorful stalls and the scent of spices.

> /agents
People here:
- Zahra (shrewd): A skilled merchant trader with keen eyes for valuable goods

> /say zahra Hello! What do you have for sale today?
You say to Zahra: "Hello! What do you have for sale today?"
Zahra says: "Ah, welcome traveler! I have rare spices from the eastern deserts, silks from the mountain weavers, and curiosities from the crystal caves. What catches your eye?"

> /save first_marketplace_visit
Game saved as 'first_marketplace_visit'
```

### Multi-Agent Conversation
```
> /conv player,zahra,kamar discussing the crystal trade
🗣️ Endless conversation mode activated!
📋 Participants: Player, Zahra, Kamar
📝 Topic: discussing the crystal trade

> /say I've heard crystals from the caves are valuable
You say: "I've heard crystals from the caves are valuable"

🗣️ **Zahra**: Indeed! The resonance crystals fetch high prices in the palace district.

🗣️ **Kamar**: But dangerous to harvest. The cave spirits don't give them up easily.

> /say kamar How do you harvest them safely?
You say to Kamar: "How do you harvest them safely?"

🗣️ **Kamar**: You must sing to the spirits. Old songs. My grandmother taught me.

> /endconv
✅ Endless conversation mode ended.
```

### Managing Token Usage
```
> /tokens
Comprehensive Token Usage Summary:
Total tokens in room: 45,234
Agents monitored: 3
By agent:
- Zahra: 18,456 tokens ✅ Normal
- Kamar: 22,120 tokens 🟡 Medium
- Mira: 4,658 tokens ✅ Normal

> /compress kamar
Compressed Kamar's context: 22120 -> 12450 tokens (saved 9670 tokens)

> /analytics kamar
📊 Detailed Analytics for Kamar:

📈 Usage Statistics:
- Total tokens used: 145,678
- API calls made: 234
- Conversation turns: 156
- Average tokens per call: 622.7

🔄 Token Management:
- Token limit expansions: 2
- Context compressions: 5
- Peak tokens in single call: 28,450
```
