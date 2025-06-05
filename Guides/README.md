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

## Quick Start

If you're new to the game, we recommend reading the guides in order. However, if you need quick information:

- For a list of all commands, see the [Command Reference](./06-command-reference.md)
- To understand how to talk to NPCs, see [Interacting with NPCs](./02-interacting-with-npcs.md)
- For help with multi-agent conversations, see [Conversation System](./04-conversation-system.md)

## Recent Updates

### Enhanced Endless Conversation Mode
- **Location-aware conversations**: Agents are automatically removed from endless mode when you move to new locations (unless they're following you)
- **Manual participant control**: Use `/invite <agent>` and `/remove <agent>` to manage who participates in endless conversations
- **Improved conversation flow**: Only relevant agents participate in conversations based on your current location

## Game Overview

Ollama Dungeon is a text adventure powered by local AI, where:

- You explore a world structured as a filesystem
- You interact with AI-powered NPCs who have memory and personality
- You can pick up and use items in your journey
- You can have complex conversations with multiple characters
- All powered by Ollama and local Large Language Models

## Command Format

All commands in the game start with a forward slash `/`. For example:
- `/look` - Look around the current room
- `/go north` - Move to the room to the north
- `/say alice Hello!` - Talk to Alice

Type `/help` at any time in the game to see available commands.

Enjoy your adventure!
