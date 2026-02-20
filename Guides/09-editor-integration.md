# Ollama-Dungeon Editor Integration Guide

## Overview

The Ollama-Dungeon Editor Suite provides integrated tools for building and managing your game world, NPCs, and items. The suite includes:

- **World Editor** (`world_editor.py`): Full-featured world builder with room, NPC, and item management
- **NPC Editor** (`npc_editor.py`): Dedicated NPC/Agent editor with advanced personality and memory tools
- **Editor Launcher** (`editor_launcher.py`): Central hub for accessing all editors

## Quick Start

### Launching the Editor Suite

```bash
python editor_launcher.py
```

From the launcher, you can:
- Open the **World Editor** for comprehensive world building
- Open the **NPC Editor** for focused NPC creation
- View this integration guide

### Direct Launch

You can also launch editors directly:

```bash
python world_editor.py    # World Editor with room/NPC/item management
python npc_editor.py      # Standalone NPC Editor
```

## World Editor Features

### World Tree Navigation

The left panel displays your world structure with icons:

| Icon | Type | Description |
|------|------|-------------|
| 👤 | NPC | Agent/NPC files (`agent_*.json`) |
| 📦 | Item | Item files (other `*.json`) |
| 🏠 | Room | Room files (`room.json`) |
| 📁 | Folder | Directories (locations/areas) |

### Three Editor Tabs

1. **Room Editor**: Edit room names, descriptions, exits, and ambient settings
2. **NPC Editor**: View and launch editing for selected NPCs
3. **Item Editor**: Create and edit game items

### Context Menu (Right-Click)

Right-click anywhere in the World Tree for quick actions:

- **New Room**: Create a new room directory with `room.json`
- **New NPC**: Open the NPC Editor to create a new NPC
- **New Item**: Switch to Item Editor for new item creation
- **Delete**: Remove selected file or directory

### Menu Bar Options

**File Menu:**
- New World: Create a new world template
- Open World: Switch to a different world directory
- Exit: Close the editor

**Edit Menu:**
- New Room: Create a room (same as context menu)
- New NPC: Open NPC Editor (same as context menu)
- New Item: Switch to Item Editor (same as context menu)

**Tools Menu:**
- Validate World: Check all rooms and NPCs for required fields
- Export to Game: Copy `world_template/` to `world/` for gameplay

### Room Editor

Create and edit room properties:

**Basic Information:**
- Room Name: Display name for the location
- Description: Detailed room description for players

**Exits:**
- Define connections in 10 directions: north, south, east, west, up, down, northeast, northwest, southeast, southwest
- Enter the relative path to the connected room

**Ambient Settings:**
- Sounds: Comma-separated list of ambient sounds (e.g., "dripping water, distant echoes")
- Time of Day: Current time setting (e.g., "peaceful morning", "midnight")
- Weather: Weather conditions (e.g., "pleasant and mild", "stormy")

**Important Notes:**
- **No Auto-Save**: You must click "Save Room" to persist changes
- **Manual Refresh**: The World Tree does NOT automatically update after saves

### Item Editor

Create and edit game items:

**Basic Information:**
- Item Name: Display name
- Description: What the item looks like

**Properties:**
- Type: weapon, armor, potion, key, treasure, tool, magical_crystal, scroll, food, misc
- Value: Numeric gold/value amount
- Weight: Weight in units (decimal)
- Usable: Can the item be used?
- Portable: Can the item be carried?

**Use Description:**
- Text describing what happens when the item is used

**Magical Properties:**
- Magical Item: Checkbox for magic flag
- Magic Properties (JSON): Custom properties in JSON format

**Saving Items:**
1. Select a room in the World Tree where the item should exist
2. Fill in the item properties
3. Click "Save Item"
4. The item is saved as `[name].json` in the selected room's directory

### Validate World Tool

Check your world for common issues:

**Validates:**
- All directories have `room.json` files
- All `room.json` files have required fields (`name`, `description`)
- All `agent_*.json` files have required fields (`name`, `persona`, `background`, `location`, `memory_file`)
- JSON syntax is valid

**Run It:**
- Menu: Tools → Validate World
- Results show in a popup with specific issues listed

### Export to Game

Copy your template world to the active game directory:

**What It Does:**
- Copies `world_template/` to `world/`
- Prompts before overwriting existing `world/`
- Creates `world/` if it doesn't exist

**Run It:**
- Menu: Tools → Export to Game

## NPC Editor Integration

### Opening the NPC Editor

**From World Editor:**
1. Right-click in World Tree → New NPC (opens empty editor)
2. Double-click an NPC in the tree (opens that NPC for editing)
3. Select an NPC → Click "Edit Selected NPC" button
4. Click "Open NPC Editor" button (opens empty editor)

**Direct Launch:**
```bash
python npc_editor.py                    # Empty editor
python npc_editor.py path/to/npc.json   # Open specific NPC
```

### NPC Editor Features

**Menu Bar:**

**File Menu:**
- New NPC (Ctrl+N): Start fresh
- Open NPC... (Ctrl+O): Load existing NPC file
- Save (Ctrl+S): Save to current file
- Save As...: Save with new name/location
- Exit: Close editor

**Edit Menu:**
- Clear All: Reset all form fields
- Load Template...: Load data from another NPC file as template

**Tools Menu:**
- Validate NPC: Check for required fields and valid data
- Generate Template: Fill form with archetype template (merchant, guard, sage, etc.)
- Quick Fill: Random example data for testing

**Keyboard Shortcuts:**
- Ctrl+S: Save
- Ctrl+N: New NPC
- Ctrl+O: Open NPC

### NPC Sections

**Basic Information:**
- Name: Required
- Occupation: Job or role
- Appearance: Physical description
- Age: Numeric age
- Gender: Dropdown (Male, Female, Non-binary, Other, Unspecified)

**Personality & Background:**
- Persona: First-person description ("I am...") - Required
- Background: History and backstory - Required
- Current Mood: Emotional state
- Emotional State: Extended emotional description

**Knowledge & Goals:**
- Knowledge: One item per line - what the NPC knows
- Goals: One per line - what motivates them

**Quirks & Fears:**
- Quirks: Unique behaviors (one per line)
- Fears: What worries them (one per line)

**Relationships:**
- JSON format defining relationships with other entities
- Quick buttons for common relationships
- "Format JSON" button to clean up formatting

**Game Settings:**
- Location Path: Where the NPC exists (with Browse button)
- Memory File: CSV filename for memories
- Auto-Generate button: Creates memory filename based on NPC name
- Following Player: Checkbox for follower behavior

### Memory File Auto-Creation

When saving an NPC:
- If the specified memory file doesn't exist, it's automatically created
- CSV format with headers: `memory_type`, `key`, `value`, `timestamp`
- Empty file ready for game engine to populate

### Saving NPCs

**Important Notes:**
- **No Auto-Save**: You must explicitly save (Ctrl+S or Save button)
- World Editor tree does NOT automatically refresh when you save from NPC Editor
- To see changes in World Editor, close and reopen the NPC Editor or manually reload

**Validation:**
- Name, persona, and background are required
- Relationships must be valid JSON
- Location path is checked if it starts with `world/`

## Workflow Examples

### Creating a New Room with NPC and Item

1. **Open World Editor**: `python world_editor.py`
2. **Create Room**:
   - Right-click in World Tree → New Room
   - Enter room name (e.g., "tavern")
   - Fill in room description
   - Add exits to connect to other rooms
   - Set ambient settings (sounds, time, weather)
   - Click "Save Room"
3. **Add NPC**:
   - Right-click the new room → New NPC
   - Fill in NPC details
   - Click "Save" or "Save As..."
   - Choose the room directory as save location
4. **Add Item**:
   - Select the room in World Tree
   - Switch to Item Editor tab
   - Fill in item details
   - Click "Save Item"

### Editing Existing NPC from World Editor

1. Open World Editor
2. Navigate to the NPC in the World Tree
3. Double-click the NPC file (👤 icon)
4. NPC Editor opens with the NPC loaded
5. Make changes
6. Press Ctrl+S to save
7. Close NPC Editor
8. **Note**: Changes won't appear in World Editor tree until you reopen

### Building a Complete World

1. **Plan Structure**: Sketch out your world layout
2. **Create Rooms**: Use New Room to build the structure
3. **Connect Rooms**: Add exits in Room Editor to link locations
4. **Add NPCs**: Create NPCs in relevant rooms
5. **Add Items**: Place items in rooms for players to find
6. **Validate**: Run Tools → Validate World to check for issues
7. **Export**: Run Tools → Export to Game when ready to play

## File Structure

The editors maintain this file structure:

```
world_template/
├── area_name/
│   ├── room.json              # Room properties
│   ├── agent_name.json        # NPC file (editable)
│   ├── memory_agent.csv       # NPC memories (auto-created)
│   ├── item_name.json         # Items (editable)
│   └── sub_location/
│       ├── room.json          # Sub-room properties
│       ├── agent_guard.json   # NPC in sub-location
│       └── memory_guard.csv   # Guard's memories
```

## Important Limitations

### No Auto-Save

**Both editors require manual saving:**
- World Editor: Click "Save Room" or "Save Item" buttons
- NPC Editor: Press Ctrl+S or click "Save" button
- **Unsaved changes are lost if you close the editor**

### No Automatic Refresh

**Changes made in one editor are NOT automatically visible in others:**
- Saving an NPC in NPC Editor won't update World Editor tree
- Saving a room in World Editor won't update NPC Editor's view
- **Workaround**: Close and reopen editors to see changes

### Multiple Editor Instances

**You can run multiple editors simultaneously:**
- Launch World Editor and NPC Editor side by side
- Edit multiple rooms at once by opening multiple World Editors
- **Note**: Changes won't sync between instances - each has its own view

## Tips

### World Building

- Use **Validate World** frequently to catch issues early
- Set up **ambient settings** to make rooms more immersive
- Create **exit connections** in both directions (e.g., north AND south)
- Use **Export to Game** to test your world in the actual game

### NPC Creation

- Use **Generate Template** for quick archetypes (merchant, guard, sage)
- Use **Quick Fill** to test the editor with random data
- Always set **location** to match where the NPC file is saved
- Let the editor **auto-generate memory file names** for consistency

### Item Design

- Set **portable: false** for fixed items (furniture, scenery)
- Use **usable: true** for items that do something when used
- Add **magic properties** as JSON for special behaviors
- Set appropriate **weight** to affect player inventory limits

## Troubleshooting

### NPC Editor Won't Open

**If double-clicking an NPC doesn't open the editor:**

1. Check that `npc_editor.py` exists in the same directory
2. Try launching it directly: `python npc_editor.py`
3. Check console for error messages

### Changes Not Appearing

**If saved changes aren't visible:**

1. Make sure you actually saved (Ctrl+S or Save button)
2. Close and reopen the editor
3. Check you're editing the correct file (look at title bar)
4. Verify file permissions allow writing

### Validation Errors

**Common validation issues:**

- Missing `name` or `description` in room files
- Missing `persona`, `background`, `location`, or `memory_file` in NPC files
- Invalid JSON in relationships or magic properties
- Location paths that don't exist

### Export Issues

**If Export to Game fails:**

1. Make sure `world_template/` exists and has content
2. Check that no other program is locking the `world/` directory
3. Try closing any running game instances

## Advanced Features

### Template System

**NPC Editor has built-in archetypes:**
- Tools → Generate Template
- Enter: merchant, guard, sage, blacksmith, or innkeeper
- Form fills with archetype-appropriate values

### Quick Fill for Testing

**Generate random test data:**
- Click "Quick Fill" button in NPC Editor
- Creates complete random NPC instantly
- Useful for testing editor functionality

### Location Browsing

**NPC Editor location browser:**
- Click "Browse" button next to Location field
- Navigate through `world_template/` structure
- Automatically converts to `world/` path format

### JSON Formatting

**Relationships JSON helper:**
- Fill in relationships manually
- Click "Format JSON" button
- Automatically formats and validates JSON

---

Happy world building! 🌍👤📦
