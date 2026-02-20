# Ollama Dungeon
## Player's Guide Index

Welcome to the Ollama Dungeon player guides. These documents will help you understand how to play the game and make the most of its features.

## Guide Contents

### Getting Started
1. [**Getting Started**](./00-getting-started.md) - Introduction and basic concepts
2. [**Basic Commands**](./01-basic-commands.md) - Essential commands for movement and interaction

### Core Gameplay
3. [**Interacting with NPCs**](./02-interacting-with-npcs.md) - How to talk with and relate to AI agents
4. [**Inventory System**](./03-inventory-system.md) - Using items and managing your inventory
5. [**Conversation System**](./04-conversation-system.md) - Advanced conversation features

### Advanced Features
6. [**Advanced Features**](./05-advanced-features.md) - Token management and other advanced functionality
7. [**Command Reference**](./06-command-reference.md) - Complete listing of all game commands
8. [**World Exploration**](./07-world-exploration.md) - Guide to exploring and understanding the world

### World Building
9. [**World Building**](./08-world-building.md) - Creating custom areas, rooms, NPCs, and items
10. [**Editor Integration**](./09-editor-integration.md) - Using the World and NPC Editor tools
11. [**Customization**](./customization.md) - Customizing game settings and behavior

## Quick Start

If you're new to the game, we recommend reading the guides in order. However, if you need quick information:

- For a list of all commands, see the [Command Reference](./06-command-reference.md)
- To understand how to talk to NPCs, see [Interacting with NPCs](./02-interacting-with-npcs.md)
- For help with multi-agent conversations, see [Conversation System](./04-conversation-system.md)

## Key Features

### Endless Conversation Mode
The game features a sophisticated endless conversation system:
- **Location-aware conversations**: Agents are automatically removed from endless mode when you move to new locations (unless they're following you)
- **Manual participant control**: Use `/invite <agent>` and `/remove <agent>` to manage who participates in endless conversations
- **Dynamic conversation flow**: Only relevant agents participate in conversations based on your current location
- **Agent following system**: Agents can follow you between rooms using `/follow <agent>` and stay behind using `/stay <agent>`

### Advanced Token Management
- **Dynamic token limits**: Context automatically expands based on usage patterns
- **Auto-compression**: Agents automatically compress their context when approaching token limits
- **Manual control**: Use `/tokens`, `/compress`, and `/analytics` to monitor and manage token usage
- **Per-agent tracking**: Each agent maintains their own context with intelligent memory summarization

## Game Overview

Ollama Dungeon is a text adventure powered by local AI, where:

- You explore a world structured as a filesystem
- You interact with AI-powered NPCs who have memory and personality
- You can pick up and use items in your journey
- You can have complex conversations with multiple characters
- All powered by Ollama and local Large Language Models

## Command Format

All commands in the game start with a forward slash `/`. For example:

**Movement & Exploration:**
- `/look` or `/l` - Look around the current room
- `/go north` - Move to the room to the north

**Interaction:**
- `/say zahra Hello!` - Talk to Zahra the Gem Merchant
- `/agents` or `/people` - List all agents in the current room
- `/memory zahra` - View what Zahra remembers

**Conversations:**
- `/conv zahra,qasim,player The history of Sunspire` - Start an endless conversation
- `/invite qasim` - Add Qasim to the ongoing conversation
- `/remove zahra` - Remove Zahra from the conversation
- `/endconv` - End the endless conversation mode

**Inventory:**
- `/inventory` or `/inv` - View your inventory
- `/pickup crystal` - Pick up an item
- `/use celestial_dew` - Use an item

**System:**
- `/save` - Save your game
- `/load` - Load a saved game
- `/status` - Check system status and token usage
- `/tokens` - View token usage for all agents

Type `/help` at any time in the game to see all available commands.

Enjoy your adventure!
