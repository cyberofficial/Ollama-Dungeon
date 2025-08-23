# Basic Commands

This guide covers the essential commands you'll use to navigate and interact with the Ollama Dungeon world.

## Movement & Exploration

| Command | Description | Example |
|---------|-------------|---------|
| `/look` or `/l` | Describe the current room | `/look` |
| `/go <direction>` | Move in a direction | `/go north` |
| `/move <direction>` | Alternative to `/go` | `/move east` |

The available directions depend on the current room, but typically include:
- north, south, east, west
- up, down
- in, out

## Getting Information

| Command | Description | Example |
|---------|-------------|---------|
| `/agents` or `/people` | List all NPCs in the room | `/agents` |
| `/help` | Show available commands | `/help` |

## System Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/save [name]` | Save game state | `/save my_game` |
| `/load [name]` | Load game state | `/load my_game` |
| `/saves` | List all saved games | `/saves` |
| `/delete <save_name>` | Delete a saved game | `/delete my_game` |
| `/quit`, `/exit`, or `/q` | Exit the game | `/quit` |
| `/status` | Show system status and connectivity | `/status` |

## Tips for Navigation

1. **Always explore** - Use `/look` whenever you enter a new room to get a description and learn what's there.

2. **Multiple command forms** - Many commands have alternative forms (like `/l` for `/look`) to make typing faster.

3. **Check exits** - The room description will usually mention available exits, so pay attention to directions.

4. **Remember where you are** - The game maintains a player location that's shown in the room description.

5. **Save frequently** - Use `/save <name>` to create save points you can return to.

Example navigation session:
```
> /look
You are in Sunspire City's Oasis Plaza. Shimmering waters reflect towering spires of golden sandstone. There are paths leading north to the palace district, south to the merchant quarter, east to the scholar district, and west to the whispering dunes.

> /go south
You moved to the merchant quarter. It's a bustling marketplace with colorful stalls and the scent of spices.

> /agents
People here:
- Zahra (shrewd): A skilled merchant trader with keen eyes for valuable goods

> /save first_marketplace_visit
Game saved as 'first_marketplace_visit'
```
