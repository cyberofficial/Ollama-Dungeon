# Getting Started with Ollama Dungeon

Welcome to Ollama Dungeon, a text adventure powered by local AI. This guide will help you get started with the game and understand the basics of how to play.

## Prerequisites

Before starting the game, ensure you have:

1. **Ollama installed** - The game uses Ollama for AI responses. Make sure it's running with `ollama serve` in a terminal.
2. **Required models** - The game uses different models for different functions (chat, summarization, etc.) which should be configured in your `config.py` file.
3. **Python dependencies** - Install all required dependencies with `pip install -r requirements.txt`

## Launching the Game

To start playing Ollama Dungeon:

1. Open a terminal/command prompt
2. Navigate to the game directory
3. Run the command: `python main.py`

You'll see the welcome screen with the game title and a prompt to type `/help` for available commands.

## Basic Concepts

### The World

The game world is structured as a directory-based environment:
- **Rooms** are represented as directories in the filesystem
- **Movement** occurs by navigating between these directories
- **Items** and **NPCs (agents)** are JSON files within room directories

### Player Actions

Every command in the game starts with a forward slash `/`, for example:
- `/look` - Look around the current room
- `/go north` - Move to the room to the north
- `/help` - Show available commands

### Interacting with NPCs (Agents)

Agents are AI-powered NPCs that you can talk to. The game uses an AI to generate their responses based on:
- Their personality defined in their JSON files
- Context from the current room
- Their memory of past interactions

### Saving and Loading

You can save your progress at any time with the `/save` command and load it later with `/load`.

## Next Steps

Check out the following guides for more detailed information:
- [Basic Commands](./01-basic-commands.md)
- [Interacting with NPCs](./02-interacting-with-npcs.md)
- [Inventory System](./03-inventory-system.md)
- [Conversation System](./04-conversation-system.md)
- [Advanced Features](./05-advanced-features.md)
