# World Building Guide

This guide will help you create your own custom areas, rooms, NPCs, and items for the Ollama Dungeon game.

## Table of Contents
1. [World Structure Overview](#world-structure-overview)
2. [Creating Areas and Rooms](#creating-areas-and-rooms)
3. [Creating NPCs (Agents)](#creating-npcs-agents)
4. [Creating Items](#creating-items)
5. [World Editor Tools](#world-editor-tools)
6. [Testing Your Creations](#testing-your-creations)

## World Structure Overview

The game world is organized as a hierarchical directory structure:

```
world/
  ├── area_name/
  │     ├── room.json             # Main area room
  │     └── sub_location/
  │           ├── room.json       # Sub-location room
  │           ├── agent_name.json # NPC in this location
  │           ├── memory_name.csv # NPC's memories
  │           └── item_name.json  # Item in this location
```

The `world_template` directory serves as a template for creating new games. When starting a new game, this template is copied to create the initial world state.

### Current World Template Structure

The default world_template includes these areas:

```
world_template/
├── sunspire_city/           # Starting location (Oasis Plaza)
│   ├── room.json
│   ├── merchant_quarter/    # Home of Zahra the Gem Merchant
│   │   ├── room.json
│   │   ├── agent_zahra.json
│   │   ├── sunfire_crystal.json
│   │   └── memory_zahra.csv
│   └── scholar_district/    # Home of Master Qasim the Lore Keeper
│       ├── room.json
│       ├── agent_qasim.json
│       ├── scroll_desert_navigation.json
│       └── memory_qasim.csv
├── crystal_caves/
│   ├── room.json
│   └── mining_tunnels/      # Home of Kael the Crystal Miner
│       ├── room.json
│       ├── agent_kael.json
│       ├── crystal_pickaxe.json
│       └── memory_kael.csv
├── sky_gardens/
│   ├── room.json
│   └── meditation_grove/    # Home of Sage Lyra the Sky Keeper
│       ├── room.json
│       ├── agent_lyra.json
│       ├── celestial_dew.json
│       └── memory_lyra.csv
└── whispering_dunes/
    ├── room.json
    ├── ancient_ruins/
    │   ├── room.json
    │   └── amulet_sun_god.json
    └── nomad_camp/          # Home of Amara the Desert Guide
        ├── room.json
        ├── agent_amara.json
        ├── desert_survival_kit.json
        └── memory_amara.csv
```

## Creating Areas and Rooms

### Step 1: Create a New Area Directory

Create a new directory under the `world_template` directory with your area name, such as "dungeon" or "mountain":

```
world_template/crystal_mines/
```

### Step 2: Create the Main Room JSON File

Each area needs a main `room.json` file that describes the entry point to that area:

```json
{
  "name": "Crystal Mine Entrance",
  "description": "A shimmering archway carved from living crystal leads into the depths. The air thrums with magical energy, and faceted walls reflect rainbow patterns from embedded gems. The sound of distant mining echoes from within.",
  "exits": {
    "north": "world/crystal_mines/main_shaft",
    "south": "world/sunspire_city",
    "east": "world/crystal_mines/storage_cavern",
    "west": "world/sky_gardens"
  },
  "ambient": {
    "sounds": ["distant mining echoes", "crystal humming"],
    "time_of_day": "dim underground",
    "weather": "dry cool air"
  }
}
```

### Room JSON Structure

| Property | Description |
|----------|-------------|
| `name` | The name of the room shown to players |
| `description` | Detailed description of the room's appearance, smells, sounds |
| `exits` | Dictionary of directions and their destinations |
| `ambient` | Optional atmospheric settings (sounds, time of day, weather) |

### Exit Paths

The exit paths follow this format: `world/area_name/sub_location`. This creates the navigation network between rooms.

#### Supported Exit Directions

The game supports 10 directional exits:

- **Cardinal directions**: `north`, `south`, `east`, `west`
- **Diagonal directions**: `northeast`, `northwest`, `southeast`, `southwest`
- **Vertical directions**: `up`, `down`

### Step 3: Create Sub-Locations

For sub-locations within your area (like a "guardroom" in a dungeon), create subdirectories:

```
world_template/crystal_mines/main_shaft/
```

Then add a `room.json` file within this directory with the appropriate details.

## Creating NPCs (Agents)

NPCs (or agents) are the characters that players can interact with in your world.

### Step 1: Create the Agent JSON File

In the room where you want the NPC to appear, create an agent file named `agent_name.json`:

```json
{
  "name": "Kael the Crystal Miner",
  "persona": "I am Kael, son of stone and keeper of the deep crystals. I've spent fifteen years in these tunnels, learning to read the veins and understand which stones hold true power versus mere pretty baubles. Every crystal has a song, and I've trained my ear to hear their melodies.",
  "background": "I came to the crystal caves as a desperate young man fleeing debt in the city above. The previous foreman took pity on me and taught me the trade, but I discovered I had a natural gift for finding the richest veins and sensing unstable tunnel sections before they collapsed.",
  "knowledge": [
    "I know the location of every major crystal vein in the cave system",
    "I can identify magical crystals by sound, color, and feel",
    "I understand cave safety and can predict dangerous areas",
    "I know which crystals are valuable versus common decorative stones"
  ],
  "goals": [
    "Keep my mining crews safe while maximizing their earnings",
    "Find the legendary Heart of the Mountain crystal",
    "Expand the tunnel network to reach deeper, richer veins"
  ],
  "location": "world/crystal_caves/mining_tunnels",
  "memory_file": "memory_kael.csv",
  "following": false,
  "mood": "hardworking and protective of his workers",
  "appearance": "A stocky, muscular man in his thirties with arms like tree trunks and hands permanently stained with rock dust.",
  "occupation": "head crystal miner and tunnel foreman",
  "relationships": {
    "player": "surface dweller who might understand the value of good crystals",
    "mining_crew": "brothers and family who depend on his leadership",
    "crystals": "living things that deserve respect"
  },
  "emotional_state": "Satisfied with his work but always alert to dangers",
  "fears": [
    "cave collapses and losing his crew",
    "greedy miners who strip-mine and destroy the crystals' natural beauty"
  ],
  "quirks": [
    "Taps crystals with his pickaxe to test their quality by sound",
    "Never enters a new tunnel without leaving an offering to the cave spirits",
    "Can navigate the caves in complete darkness by feeling the air currents"
  ]
}
```

### Agent JSON Structure

| Property | Description |
|----------|-------------|
| `name` | The name of the NPC |
| `persona` | First-person description of who they are (their self-identity) |
| `background` | Their history and important life events |
| `knowledge` | List of things this NPC knows that might be useful to the player |
| `goals` | The NPC's current objectives and motivations |
| `location` | Where they can be found in the world |
| `memory_file` | CSV file that will store their memories and interactions |
| `following` | Whether they are following the player (usually start as `false`) |
| `mood` | Their current emotional state |
| `appearance` | Physical description of the NPC |
| `occupation` | Their job or role in the world |
| `relationships` | How they view other important entities |
| `emotional_state` | More detailed description of their current feelings |
| `fears` | List of things that scare or worry this NPC |
| `quirks` | Distinctive behaviors that make them unique |

### Step 2: Create the Memory File

Create a blank CSV file with the same name as specified in the `memory_file` field:

```
world_template/crystal_caves/mining_tunnels/memory_kael.csv
```

This file will automatically be populated as the NPC interacts with the player.

#### Memory CSV Structure

The memory file uses CSV format with these columns:

| Column | Description |
|--------|-------------|
| `timestamp` | ISO format timestamp when the memory was created |
| `type` | Type of memory: `event`, `observation`, `dialogue`, or `emotion` |
| `content` | The actual memory content or conversation text |

Example memory entries:
```csv
timestamp,type,content
2026-02-20T10:30:45,event,Player arrived at the crystal mines
2026-02-20T10:31:12,dialogue,Player asked about the Heart of the Mountain crystal
2026-02-20T10:31:45,emotion,Felt hopeful when player offered to help search
2026-02-20T10:32:00,observation,Player seems experienced with underground exploration
```

## Creating Items

Items are objects that players can pick up, use, or interact with in the game world.

### Create the Item JSON File

In the room where you want the item to appear, create an item file (no `item_` prefix needed - use descriptive names like `crystal_pickaxe.json`):

```json
{
  "name": "Crystal Pickaxe",
  "description": "A masterfully crafted mining pickaxe with a head made from compressed crystal dust and steel. The handle is wrapped in leather worn smooth by years of use, and small crystals embedded in the metal head glow softly to provide light while working.",
  "type": "tool",
  "portable": true,
  "usable": true,
  "use_description": "You swing the crystal pickaxe and it strikes true, the magical crystals in the head helping guide it to extract valuable stones without damage.",
  "value": 50,
  "weight": 3.5,
  "properties": {
    "durability": 100,
    "mining_power": "enhanced",
    "light_source": true
  }
}
```

### Item JSON Structure

| Property | Description |
|----------|-------------|
| `name` | The name of the item shown to players |
| `description` | Detailed description of the item's appearance |
| `type` | Category of item (e.g., "tool", "weapon", "consumable", "treasure") |
| `portable` | Whether the item can be picked up and carried (default: true) |
| `usable` | Whether the item can be used with `/use` (default: false) |
| `use_description` | Text shown when the player uses the item |
| `value` | Gold/currency value of the item (default: 0) |
| `weight` | Weight of the item in units (default: 0) |
| `properties` | Optional object with custom item attributes |

## World Editor Tools

The game includes GUI-based editor tools to streamline world building:

### Editor Launcher

The `editor_launcher.py` script serves as the central hub for launching all editor tools:

```bash
python editor_launcher.py
```

This opens a graphical interface with buttons to launch:
- **World Editor** - Create and edit rooms, areas, and ambient settings
- **NPC Editor** - Create and edit agents/NPCs
- **System Verification** - Check Ollama connection and world integrity

### World Editor Features

Access the World Editor through the launcher or directly:

```bash
python world_editor.py
```

**Features:**
- **New World**: Create a completely new world from scratch
- **Validate**: Check all JSON files for syntax errors and missing required fields
- **Export**: Package your world for sharing or backup
- **Delete**: Remove existing worlds (with confirmation)

**Room Editing:**
- Create areas and sub-locations
- Edit room names and descriptions
- Configure exit connections between rooms
- Set ambient properties (sounds, time of day, weather)
- Visual tree view of world structure

**Advantages over manual editing:**
- Automatic JSON validation
- Visual navigation of world structure
- No syntax errors from missing commas or quotes
- Immediate feedback on missing required fields
- Easy exit linking without manual path typing

### NPC Editor Features

```bash
python npc_editor.py
```

**Features:**
- Create new agents with all required fields
- Edit existing agent personalities and knowledge
- Set agent locations and relationships
- Configure fears, quirks, and emotional states
- Preview agent personas before saving

**Memory Management:**
- View agent memories in tabular format
- Add custom memories for backstory
- Clear or archive memory files
- Import/export memory CSV files

### When to Use Manual Editing vs. GUI Tools

**Use GUI tools when:**
- Creating new areas or NPCs from scratch
- You're new to the JSON structure
- You want visual validation of connections
- Complex exit networks need visualization

**Use manual editing when:**
- Making quick text changes to descriptions
- Bulk editing multiple files
- You're comfortable with JSON syntax
- Using version control with diff tools

## Testing Your Creations

After creating your custom areas, rooms, NPCs, and items:

1. Start a new game to have your world_template copied to the active world
2. Navigate to your new area using the `go` command
3. Use `look` to see if your room description appears correctly
4. Use `agents` to check if your NPCs are present
5. Interact with your NPCs using `say` or `conv`
6. Look for your items and try to `pickup` and `use` them

### Troubleshooting Common Issues

1. **Navigation problems:** Ensure exit paths in `room.json` are correctly formatted as `world/area/location`
2. **Missing NPCs:** Check that the agent's `location` property matches exactly where you want them to appear
3. **JSON errors:** Validate your JSON files for syntax errors (missing commas, quotes, etc.)
4. **File permissions:** Make sure newly created files are readable by the game

---

With this guide, you should be able to expand the game world with your own creative areas, characters, and items. The modular structure makes it easy to build complex environments for players to explore!
