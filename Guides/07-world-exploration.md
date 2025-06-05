# World Structure and Exploration Guide

This guide will help you understand how the world in Ollama Dungeon is structured and how to effectively explore it.

## World Overview

The game world is organized as a hierarchical directory structure, where:
- Each location (room) is a directory
- Locations can contain sub-locations (sub-directories)
- Each room has a `room.json` file with description and properties
- NPCs, items, and other interactive elements are files within these directories

## Default World Layout

The default world template includes:

```
world/
  ├── town/
  │   ├── room.json         # Town square
  │   ├── tavern/           # The tavern sub-location
  │   │   ├── room.json
  │   │   ├── agent_alice.json
  │   │   ├── agent_bob.json
  │   │   └── ...
  │   └── market/           # The market sub-location
  │       ├── room.json
  │       ├── health_potion.json
  │       └── ...
  └── forest/
      ├── room.json         # Forest entrance
      └── cave/             # Cave sub-location
          ├── room.json
          ├── agent_grix.json
          └── ...
```

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

## Unlocking New Locations

Some locations might be initially inaccessible. To unlock them:

1. **Complete tasks**: NPCs might ask you to do something before allowing access.

2. **Find key items**: Some areas may require specific items to enter.

3. **Solve puzzles**: Figure out the right actions or commands to proceed.

## Example Exploration Session

```
> /look
You are in the town square. There are streets leading north to the market, east to the tavern, and west to the residential area.

> /go east
You moved to the tavern. It's a lively place with people chatting and drinking.

> /agents
People here:
- Alice (friendly): A woman with red hair wearing a tavern keeper's apron
- Bob (curious): A middle-aged man sitting at a corner table

> /say alice Hello! What can you tell me about this area?
You say to Alice: "Hello! What can you tell me about this area?"
Alice says: "Welcome to the Rusty Dragon Tavern! The town is peaceful, but there have been strange noises from the forest lately. The market to the north has good supplies if you need anything."

> /go west
You moved back to the town square.

> /go north
You moved to the market. Various stalls are selling goods and produce.

> /look
The market is bustling with activity. Various merchants have set up stalls selling everything from fresh produce to handcrafted goods. A particular stall with potions catches your eye.

Exits: south (to town square)
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
