# World Structure and Exploration Guide

This guide will help you understand how the world in Ollama Dungeon is structured and how to effectively explore it.

## World Overview

The game world is organized as a hierarchical directory structure, where:
- Each location (room) is a directory
- Locations can contain sub-locations (sub-directories)
- Each room has a `room.json` file with description and properties
- NPCs, items, and other interactive elements are files within these directories

## Default World Layout

The default world template includes four main areas, each with unique sub-locations:

```
world/
  ├── sunspire_city/
  │   ├── room.json         # Oasis Plaza (main area)
  │   ├── merchant_quarter/ # The marketplace sub-location
  │   │   ├── room.json
  │   │   ├── agent_zahra.json
  │   │   ├── sunfire_crystal.json
  │   │   └── memory_zahra.csv
  │   └── scholar_district/ # The scholar area sub-location
  │       ├── room.json
  │       ├── agent_qasim.json
  │       ├── scroll_desert_navigation.json
  │       └── memory_qasim.csv
  ├── crystal_caves/
  │   ├── room.json         # Cave entrance
  │   └── mining_tunnels/   # Mining area sub-location
  │       ├── room.json
  │       ├── agent_kael.json
  │       ├── crystal_pickaxe.json
  │       └── memory_kael.csv
  ├── sky_gardens/
  │   ├── room.json         # Sky Gardens entrance
  │   └── meditation_grove/ # Meditation sub-location
  │       ├── room.json
  │       ├── agent_lyra.json
  │       ├── celestial_dew.json
  │       └── memory_lyra.csv
  └── whispering_dunes/
      ├── room.json         # Dunes entrance
      ├── ancient_ruins/    # Ancient ruins sub-location
      │   ├── room.json
      │   └── amulet_sun_god.json
      └── nomad_camp/       # Nomad camp sub-location
          ├── room.json
          ├── agent_amara.json
          ├── desert_survival_kit.json
          └── memory_amara.csv
```

### Main Areas and Their Characters

1. **Sunspire City** (starting location)
   - Oasis Plaza - Central gathering point
   - Merchant Quarter - Home to **Zahra the Gem Merchant**
   - Scholar District - Home to **Master Qasim the Lore Keeper**

2. **Crystal Caves**
   - Cave entrance
   - Mining Tunnels - Home to **Kael the Crystal Miner**

3. **Sky Gardens**
   - Sky Gardens entrance
   - Meditation Grove - Home to **Sage Lyra the Sky Keeper**

4. **Whispering Dunes**
   - Dunes entrance
   - Ancient Ruins - Mysterious location with ancient treasures
   - Nomad Camp - Home to **Amara the Desert Guide**

## Navigation

To move between locations, use the `/go` or `/move` command followed by a direction:

```
/go north
/move east
```

Common directions include:
- Cardinal: north, south, east, west
- Vertical: up, down
- Special: in, out

The available directions depend on how the room is configured in its `room.json` file.

## Room Information

When you enter a room, use `/look` or `/l` to get a description. This typically includes:
- A description of the room
- Available exits (directions you can go)
- NPCs present
- Items you can interact with

Example:
```
> /look
You are in the tavern. It's a warm, cozy place with a crackling fireplace and the smell of fresh bread and ale. There are several patrons drinking and chatting.

Exits: west (to town square), north (to inn rooms)

You see two people here:
- Alice, the tavern keeper
- Bob, a town local
```

## Exploring the World

Here are some effective strategies for exploring the world:

1. **Systematic Exploration**: Visit each location and make a mental map of how they connect.

2. **Talk to NPCs**: Use `/say` to talk to NPCs. They often provide helpful information about the world and might suggest places to explore.
   ```
   /say alice What can you tell me about this town?
   ```

3. **Look for Items**: In each room, try to identify items you can pick up. They might be useful later.
   ```
   /pickup health_potion
   ```

4. **Share Context**: When encountering something interesting, use `/share` to inform NPCs about it.
   ```
   /share alice I found a strange symbol in the cave
   ```

5. **Use Memory**: Check what NPCs remember with the `/memory` command.
   ```
   /memory grix
   ```

## Example Exploration Session

```
> /look
You are in Sunspire City's Oasis Plaza. Shimmering waters of the Sacred Oasis reflect towering spires of golden sandstone. Palm trees provide blessed shade while colorful silk canopies flutter in the desert breeze.

Exits: north (to palace district), south (to merchant quarter), east (to scholar district), west (to whispering dunes), up (to sky gardens), down (to crystal caves)

> /go south
You moved to the merchant quarter. It's a bustling marketplace with colorful stalls and the scent of spices.

> /agents
People here:
- Zahra the Gem Merchant

> /say zahra Hello! What can you tell me about this area?
You say to Zahra: "Hello! What can you tell me about this area?"
Zahra says: "Welcome to Sunspire City's merchant quarter! This is where the finest gems and crystals from across the realm find their way to discerning buyers. The crystal caves below hold incredible treasures if you're brave enough to explore them."

> /go north
You moved back to the Oasis Plaza.

> /go east
You moved to the scholar district. Ancient tomes and scrolls fill the libraries here.

> /agents
People here:
- Master Qasim the Lore Keeper

> /look
The scholar district is a place of learning and ancient knowledge. Tall spires house vast libraries filled with the accumulated wisdom of ages.

Exits: west (to Oasis Plaza)

> /go up
You moved to the Sky Gardens. Floating islands of lush greenery hover in the air, connected by bridges of woven cloud-stuff.

> /agents
People here:
- Sage Lyra the Sky Keeper
```

## Tips for Effective Exploration

1. **Use your inventory**: Items you collect might be useful in different locations.

2. **Follow agents**: If an NPC seems interesting, use `/follow <agent>` to have them come with you.

3. **Map making**: Consider drawing a map on paper to track locations.

4. **Save points**: Create save points before exploring dangerous areas with `/save <name>`.

5. **Conversations**: Use the conversation system to discuss locations between NPCs.
   ```
   /conv alice,bob The forest and its dangers
   ```

6. **Context sharing**: Share important discoveries with NPCs.
   ```
   /share I found a hidden passage in the cave
   ```

Happy exploring!
