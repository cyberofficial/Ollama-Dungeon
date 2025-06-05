# Configuration file for Ollama Dungeon

# Ollama Settings
OLLAMA_BASE_URL = "http://localhost:11434"

# Model configurations
MODELS = {
    "main": "qwen3:4b",      # Main conversation model (fast for testing)
    "summary": "qwen3:4b"    # Summarization model (fast for testing)
}

# Token and context management settings
TOKEN_SETTINGS = {
    "max_context_tokens": 40000,     # Maximum tokens before compression
    "compression_threshold": 35000,   # Start compression at this token count
    "starting_tokens": 0,         # Start the starting token limit
    "increase_tokens_by": 1000,      # Increase the start limit by x amount when we reach the starting token limit
    "token_increase_threshold": 0.9, # Increase tokens when reaching 80% of current limit
    "summary_chunk_size": 8000,      # Size of chunks to summarize
    "min_context_after_compression": 5000,  # Minimum context to keep after compression
    "enable_auto_compression": True,  # Automatically compress when threshold reached
    "show_token_warnings": True,     # Show token warnings to user
    "suppress_token_info": False,    # Hide token expansion/compression messages for immersion
    "emergency_compression_threshold": 38000,  # Emergency compression if regular fails
    "reload_on_lower": False,        # Only reload model when token count increases, not decreases
}

# Agent behavior settings
AGENT_SETTINGS = {
    "max_memory_entries": 50,        # Maximum memory entries before summarization
    "context_sharing_enabled": True, # Allow agents to share context
    "persistent_sessions": True,     # Keep agent sessions between interactions
    "auto_save_context": True,       # Automatically save context after interactions
    "strip_thinking_tokens": True,   # Remove <think> tags and content from AI responses
    "randomize_responses": True,     # Add random seed to agent calls
    "temperature": 0.7,              # Temperature for responses (higher = more creative and varied)
}

# Game settings
GAME_SETTINGS = {
    "default_location": "world/town",
    "auto_save_frequency": 10,  # Auto-save every N actions
    "debug_mode": True,        # Enable debug output,
    "title": "OLLAMA DUNGEON",  # Customize main title
    "subtitle": "A Text Adventure Powered by Local AI"  # Customize subtitle
}

# Logging settings
LOGGING = {
    "enabled": False,
    "log_file": "game.log",
    "log_level": "INFO",
    "log_ai_responses": False,   # Don't log AI responses (privacy)
    "log_token_usage": True,     # Log token usage for monitoring
}
