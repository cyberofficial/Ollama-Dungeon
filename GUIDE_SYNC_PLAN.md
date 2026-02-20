# Guide Synchronization Plan

## Objective
Ensure all guides in the `Guides/` folder match the actual codebase exactly. No features in code should be missing from guides, and no features in guides should be missing from code.

## Commands Found in cli.py (All Commands)

### Commands Dictionary (lines 27-68)
```python
self.commands = {
    'look': self.cmd_look,
    'l': self.cmd_look,
    'go': self.cmd_go,
    'move': self.cmd_go,
    'say': self.cmd_say,
    'sayto': self.cmd_say,
    'talk': self.cmd_say,
    'conv': self.cmd_conv,
    'conversation': self.cmd_conv,
    'agents': self.cmd_agents,
    'people': self.cmd_agents,
    'memory': self.cmd_memory,
    'summarize': self.cmd_summarize,
    'share': self.cmd_summarize,
    'inventory': self.cmd_inventory,
    'inv': self.cmd_inventory,
    'pickup': self.cmd_pickup,
    'take': self.cmd_pickup,
    'use': self.cmd_use,
    'follow': self.cmd_follow,
    'stay': self.cmd_stay,
    'help': self.cmd_help,
    'save': self.cmd_save,
    'load': self.cmd_load,
    'saves': self.cmd_list_saves,
    'delete': self.cmd_delete_save,
    'reset': self.cmd_reset_agent,
    'tokens': self.cmd_tokens,
    'compress': self.cmd_compress_agent,
    'compress_all': self.cmd_compress_all,
    'status': self.cmd_system_status,
    'model_state': self.cmd_model_state,
    'dialog': self.cmd_dialog,
    'endconv': self.cmd_endconv,
    'invite': self.cmd_invite,
    'remove': self.cmd_remove,
    'quit': self.cmd_quit,
    'exit': self.cmd_quit,
    'q': self.cmd_quit,
    'analytics': self.cmd_analytics,
}
```

## Guide File Assignments

### Agent 1: 00-getting-started.md
**Task**: Update getting started guide to match current codebase
- Ensure prerequisites match actual requirements (Python 3.12.7, Ollama, qwen3:4b model)
- Update launching instructions if changed
- Verify world setup description matches actual code behavior

### Agent 2: 01-basic-commands.md & 06-command-reference.md
**Task**: Ensure all commands are documented correctly
- Verify all commands from the commands dictionary are listed
- Check command formats match actual usage
- Ensure no obsolete commands are listed
- Add missing commands if any

### Agent 3: 02-interacting-with-npcs.md & 04-conversation-system.md
**Task**: Update NPC interaction and conversation system guides
- Verify `/say` command behavior matches actual implementation
- Update `/conv` endless conversation mode documentation
- Verify `/invite`, `/remove`, `/endconv`, `/dialog` commands
- Check following behavior (`/follow`, `/stay`) documentation

### Agent 4: 03-inventory-system.md
**Task**: Update inventory system guide
- Verify `/inventory`, `/pickup`, `/take`, `/use` commands
- Check item system behavior matches code

### Agent 5: 05-advanced-features.md
**Task**: Update advanced features guide
- Verify `/tokens` command output format
- Check `/compress`, `/compress_all` commands
- Verify `/status` command output
- Update `/analytics` command documentation
- Verify `/model_state` command documentation
- Check `/reset` command documentation

### Agent 6: 07-world-exploration.md, 08-world-building.md, 09-editor-integration.md, customization.md, README.md
**Task**: Update remaining guides
- Verify world structure documentation
- Check editor integration if still relevant
- Update customization guide
- Verify all guides reference correct world locations (sunspire_city, crystal_caves, sky_gardens, whispering_dunes)

## Key Code Facts to Reference

### Default Location (config.py line 42)
```python
"default_location": "world/sunspire_city"
```

### World Template Locations (verify_setup.py)
- world_template/crystal_caves/
- world_template/crystal_caves/mining_tunnels/
- world_template/sky_gardens/
- world_template/sky_gardens/meditation_grove/
- world_template/sunspire_city/
- world_template/sunspire_city/merchant_quarter/
- world_template/sunspire_city/scholar_district/
- world_template/whispering_dunes/
- world_template/whispering_dunes/ancient_ruins/
- world_template/whispering_dunes/nomad_camp/

### Model Configuration (config.py)
```python
MODELS = {
    "main": "qwen3:4b",
    "summary": "qwen3:4b"
}
```

### Important Settings
- `reply_length`: "brief", "medium", "detailed", or "verbose" (default: "detailed")
- `strip_thinking_tokens`: True (default)
- `randomize_responses`: True (default)
- `temperature`: 0.7 (default)

## Instructions for Each Agent

1. **Read your assigned guide files completely**
2. **Compare against the actual code implementation**
3. **Make precise edits**:
   - Add features that exist in code but not in guide
   - Remove features that exist in guide but not in code
   - Update any inaccurate descriptions
4. **Maintain the guide's existing structure and tone**
5. **Ensure 1:1 accuracy** - no wishlist items, no missing features

## Success Criteria

Each guide should:
- Document exactly what exists in the code
- Use correct command names and formats
- Reference correct world locations
- Show accurate example output
- Have no obsolete features
- Have no missing features
