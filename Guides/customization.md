# Customizing Ollama Dungeon

This guide explains how to customize various aspects of Ollama Dungeon to make your adventure more personalized.

## Customizing the Game Title and Subtitle

You can easily customize the title and subtitle that appear when you start the game by modifying the `config.py` file.

1. Open the `config.py` file in your favorite text editor.

2. Find the `GAME_SETTINGS` section that looks like this:

```python
# Game settings
GAME_SETTINGS = {
    "default_location": "world/town",
    "auto_save_frequency": 10,  # Auto-save every N actions
    "debug_mode": True,        # Enable debug output,
    "title": "OLLAMA DUNGEON",  # Customize main title
    "subtitle": "A Text Adventure Powered by Local AI"  # Customize subtitle
}
```

3. Change the `"title"` and `"subtitle"` values to whatever you prefer:

```python
    "title": "MY FANTASY REALM",  # Change to your preferred title
    "subtitle": "An Epic Adventure Awaits"  # Change to your preferred subtitle
```

4. Save the file and restart the game to see your changes.

Note that the title will be centered automatically in the title box when the game starts.

## Other Customization Options

### Game World

- Modify files in the `world_template` directory to create your own game world
- See the [World Building Guide](08-world-building.md) for detailed instructions

### Agent Personalities

- Edit agent JSON files to adjust their personalities, knowledge, and behavior
- See the [Conversation System Guide](04-conversation-system.md) for more details

### System Settings

- Adjust token limits and model preferences in the `TOKEN_SETTINGS` section of `config.py`
- Change logging behavior in the `LOGGING` section
- Modify agent behavior settings in the `AGENT_SETTINGS` section

Remember to make a backup of your configuration files before making significant changes.
