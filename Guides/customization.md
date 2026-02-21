# Customizing Ollama Dungeon

This guide explains how to customize various aspects of Ollama Dungeon to make your adventure more personalized.

## Customizing the Game Title and Subtitle

You can easily customize the title and subtitle that appear when you start the game by modifying the `config.py` file.

1. Open the `config.py` file in your favorite text editor.

2. Find the `GAME_SETTINGS` section that looks like this:

```python
# Game settings
GAME_SETTINGS = {
    "default_location": "world/sunspire_city",
    "auto_save_frequency": 10,  # Auto-save every N actions
    "debug_mode": True,        # Enable debug output
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

## Other Configuration Options

### AI Model Settings

The `MODELS` section controls which AI models Ollama Dungeon uses:

```python
MODELS = {
    "main": "qwen3:4b",      # Main conversation model
    "summary": "qwen3:4b"    # Summarization model
}
```

- **main**: Used for all agent conversations and game responses
- **summary**: Used for compressing context and memories

You can use any model installed in Ollama. Popular choices include:
- `qwen3:4b` - Fast and efficient (default)
- `llama3.2:3b` - Small and quick
- `mistral:7b` - More detailed responses
- `qwen2.5:14b` - Higher quality but slower

### Ollama Server Connection

If your Ollama server runs on a different port or machine, change the base URL:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
```

### Token and Context Management

The `TOKEN_SETTINGS` section controls how the game manages AI context to prevent overflow:

```python
TOKEN_SETTINGS = {
    "max_context_tokens": 40000,     # Maximum tokens before compression
    "compression_threshold": 35000,   # Start compression at this token count
    "starting_tokens": 0,             # Starting token limit
    "increase_tokens_by": 1000,       # Amount to increase limit when threshold reached
    "token_increase_threshold": 0.9,  # Increase when reaching 90% of current limit
    "summary_chunk_size": 8000,       # Size of chunks to summarize
    "min_context_after_compression": 5000,  # Minimum context to keep after compression
    "enable_auto_compression": True,  # Automatically compress when threshold reached
    "show_token_warnings": True,      # Show token warnings to user
    "suppress_token_info": False,     # Hide token messages for immersion
    "emergency_compression_threshold": 38000,  # Emergency compression if regular fails
    "reload_on_lower": False,         # Only reload model when token count increases
}
```

Key settings:
- **max_context_tokens**: Raise this if you have more RAM available (40K is safe for 8GB+)
- **enable_auto_compression**: Keep True to prevent context overflow errors
- **suppress_token_info**: Set True to hide technical token messages during gameplay
- **show_token_warnings**: Toggle warnings when approaching context limits

### Agent Behavior Settings

The `AGENT_SETTINGS` section controls how NPCs behave and remember:

```python
AGENT_SETTINGS = {
    "max_memory_entries": 50,        # Maximum memory entries before summarization
    "context_sharing_enabled": True, # Allow agents to share context
    "persistent_sessions": True,     # Keep agent sessions between interactions
    "auto_save_context": True,       # Automatically save context after interactions
    "enable_thinking": True,         # Enable thinking mode in Ollama API (True = models get thinking benefit)
    "strip_thinking_tokens": True,   # Remove <thinking> tags from responses (fallback cleanup)
    "randomize_responses": True,     # Add random seed to agent calls
    "temperature": 0.7,              # Temperature for responses (0.0-1.0)
    "reply_length": "detailed",      # Response length: brief, medium, detailed, verbose
}
```

Key settings:
- **temperature**: Controls creativity
  - 0.0-0.3: More focused and deterministic
  - 0.4-0.7: Balanced (default 0.7)
  - 0.8-1.0: More creative and varied
- **reply_length**: How detailed agents respond
  - "brief": Short responses
  - "medium": Moderate detail
  - "detailed": Full responses (default)
  - "verbose": Maximum detail
- **enable_thinking**: Controls AI thinking behavior
  - **True (default)**: Enables thinking by passing `think: true`. Models get the benefit of thinking for better reasoning, with thinking content removed from final output.
  - **False**: Disables thinking at the API level by passing `think: false`. Saves tokens and processing time. Best for models that don't benefit from thinking mode (qwen3:4b, llama3, mistral).
- **strip_thinking_tokens**: Fallback that removes `<thinking>` tags from responses. Ensures clean output by stripping thinking tokens that might appear in responses.
- **max_memory_entries**: Higher values mean agents remember more before summarizing
- **persistent_sessions**: Keep True so agents remember between conversations

### Game Settings

In addition to title and subtitle, `GAME_SETTINGS` includes:

```python
GAME_SETTINGS = {
    "default_location": "world/sunspire_city",  # Starting room
    "auto_save_frequency": 10,                  # Auto-save every N actions
    "debug_mode": True,                         # Show debug information
    "title": "OLLAMA DUNGEON",
    "subtitle": "A Text Adventure Powered by Local AI"
}
```

- **auto_save_frequency**: How often the game auto-saves (higher = less frequent)
- **debug_mode**: Set False to hide debug messages for cleaner gameplay
- **default_location**: Change starting room (must exist in world/)

### Logging Settings

Control what the game logs for debugging and monitoring:

```python
LOGGING = {
    "enabled": False,
    "log_file": "game.log",
    "log_level": "INFO",
    "log_ai_responses": False,   # Don't log AI responses (privacy)
    "log_token_usage": True,     # Log token usage for monitoring
}
```

- **enabled**: Set True to enable logging
- **log_ai_responses**: Careful - this creates large log files with all AI text
- **log_token_usage**: Useful for monitoring context usage over time

## Customization Guides

### Game World

- Modify files in the `world_template` directory to create your own game world
- See the [World Building Guide](08-world-building.md) for detailed instructions

### Agent Personalities

- Edit agent JSON files to adjust their personalities, knowledge, and behavior
- See the [Conversation System Guide](04-conversation-system.md) for more details

## Tips for Customization

1. **Start small**: Change one setting at a time and test
2. **Backup first**: Copy `config.py` before making major changes
3. **Monitor performance**: If the game slows, try smaller models or lower token limits
4. **Test thoroughly**: Play through interactions after changing agent or model settings
5. **Check Ollama resources**: Ensure you have enough RAM for larger models

Remember to make a backup of your configuration files before making significant changes.
