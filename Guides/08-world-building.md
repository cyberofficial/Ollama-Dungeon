# World Building Guide

This guide will help you create your own custom areas, rooms, NPCs, and items for the Ollama Dungeon game.

## Table of Contents
1. [World Structure Overview](#world-structure-overview)
2. [Creating Areas and Rooms](#creating-areas-and-rooms)
3. [Creating NPCs (Agents)](#creating-npcs-agents)
4. [Creating Items](#creating-items)
5. [Testing Your Creations](#testing-your-creations)

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

## Creating Areas and Rooms

### Step 1: Create a New Area Directory

Create a new directory under the `world_template` directory with your area name, such as "dungeon" or "mountain":

```
world_template/dungeon/
```

### Step 2: Create the Main Room JSON File

Each area needs a main `room.json` file that describes the entry point to that area:

```json
{
  "name": "Dungeon Entrance",
  "description": "A foreboding stone archway leads into darkness. The air is cool and damp, with the smell of earth and decay. Moss grows on the weathered stones, and faint echoing sounds come from within.",
  "exits": {
    "north": "world/dungeon/hallway",
    "south": "world/town",
    "east": "world/dungeon/guardroom",
    "west": "world/forest"
  },
  "ambient": {
    "sounds": ["dripping water", "distant scratching", "wind howling"],
    "time_of_day": "any",
    "weather": "sheltered"
  }
}
```

### Room JSON Structure

| Property | Description |
|----------|-------------|
| `name` | The name of the room shown to players |
| `description` | Detailed description of the room's appearance, smells, sounds |
| `exits` | Dictionary of directions and their destinations |
| `ambient` | Optional environmental details to enhance immersion |

### Exit Paths

The exit paths follow this format: `world/area_name/sub_location`. This creates the navigation network between rooms.

### Step 3: Create Sub-Locations

For sub-locations within your area (like a "guardroom" in a dungeon), create subdirectories:

```
world_template/dungeon/guardroom/
```

Then add a `room.json` file within this directory with the appropriate details.

## Creating NPCs (Agents)

NPCs (or agents) are the characters that players can interact with in your world.

### Step 1: Create the Agent JSON File

In the room where you want the NPC to appear, create an agent file named `agent_name.json`:

```json
{
  "name": "Guard Captain",
  "persona": "I'm the captain of the dungeon guard, a gruff veteran with little patience for trespassers. I take my duty seriously and have served the kingdom for 20 years. Despite my harsh exterior, I have a sense of honor and can be reasoned with.",
  "background": "I grew up in the slums of the capital city and joined the guard to escape poverty. I've worked my way up through the ranks through dedication and toughness. The other guards respect me, but also fear my temper when rules are broken.",
  "knowledge": [
    "I know all the security protocols of the dungeon",
    "I have information about the mysterious prisoner in cell block D",
    "I know which guards can be bribed and which are loyal",
    "I've heard rumors about a secret passage in the east wing"
  ],
  "goals": [
    "Maintain security in the dungeon at all costs",
    "Eventually retire with a captain's pension",
    "Keep the secret of cell block D from spreading"
  ],
  "location": "world/dungeon/guardroom",
  "memory_file": "memory_guard_captain.csv",
  "following": false,
  "mood": "vigilant",
  "appearance": "A broad-shouldered man in well-kept armor, with a scarred face and a neatly trimmed gray beard",
  "occupation": "dungeon guard captain",
  "relationships": {
    "player": "suspicious stranger",
    "kingdom": "loyal servant",
    "prisoners": "stern overseer"
  },
  "emotional_state": "Alert and somewhat stressed about recent security concerns",
  "quirks": [
    "Constantly checks his keys",
    "Rubs old sword wound when nervous",
    "Speaks in short, direct sentences"
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
| `quirks` | Distinctive behaviors that make them unique |

### Step 2: Create the Memory File

Create a blank CSV file with the same name as specified in the `memory_file` field:

```
world_template/dungeon/guardroom/memory_guard_captain.csv
```

This file will automatically be populated as the NPC interacts with the player.

## Creating Items

Items are objects that players can pick up, use, or interact with in the game world.

### Create the Item JSON File

In the room where you want the item to appear, create an item file named `item_name.json`:

```json
{
  "name": "Guard Key Ring",
  "description": "A heavy iron ring holding several large, ornate keys. Each key is labeled with small symbols indicating different areas of the dungeon.",
  "type": "key",
  "value": 100,
  "weight": 0.3,
  "properties": {
    "unlocks": ["cell_block_a", "guard_quarters", "supply_room"],
    "magic": false,
    "restricted": true
  },
  "usable": true,
  "portable": true,
  "use_description": "You use a key from the ring to unlock the door."
}
```

### Item JSON Structure

| Property | Description |
|----------|-------------|
| `name` | The name of the item shown to players |
| `description` | Detailed description of the item's appearance |
| `type` | Category of the item (weapon, armor, key, consumable, etc.) |
| `value` | Worth in gold or other currency |
| `weight` | How heavy the item is (affects inventory capacity) |
| `properties` | Special attributes of the item (varies by type) |
| `usable` | Whether the item can be used (activated) |
| `portable` | Whether the item can be picked up and carried |
| `use_description` | Text shown when the player uses the item |

### Item Types and Properties

Different item types can have different properties:

1. **Weapons**
   ```json
   "properties": {
     "damage": "2d6+1",
     "magic": true,
     "two_handed": false
   }
   ```

2. **Armor**
   ```json
   "properties": {
     "protection": 4,
     "magic": false,
     "slot": "body"
   }
   ```

3. **Consumables**
   ```json
   "properties": {
     "healing": "2d4+2",
     "uses": 1,
     "effect_duration": 60
   }
   ```

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
