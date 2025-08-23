# Inventory System

Ollama Dungeon includes a simple inventory system that allows you to pick up, carry, and use items. This guide explains how to interact with the inventory system.

## Basic Inventory Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/inventory` or `/inv` | View your inventory | `/inventory` |
| `/pickup <item>` or `/take <item>` | Pick up an item from the room | `/pickup rusty_dagger` |
| `/use <item>` | Use an item from inventory | `/use health_potion` |

## Finding Items

Items are scattered throughout the world. When you enter a room, the room description might mention items you can interact with. You can also use the `/look` command to see a description of the room, which often includes available items.

Example:
```
> /look
You are in the crystal caves mining tunnels. The walls sparkle with embedded gems and you notice a crystal pickaxe leaning against the wall.

> /pickup crystal_pickaxe
You pick up the crystal pickaxe and add it to your inventory.

> /inventory
Your inventory:
- Crystal Pickaxe: A mining tool enhanced with crystal fragments that glow with inner light.
```

## Using Items

Different items have different effects when used:

1. **Consumables** like potions might have immediate effects when used
2. **Equipment** might change player stats or capabilities
3. **Key items** might unlock new areas or trigger events

To use an item:
```
/use <item_name>
```

Example:
```
> /use crystal_pickaxe
You swing the crystal pickaxe at the cave wall. The enhanced tool easily chips away at the rock, revealing a small vein of precious gems.
The pickaxe's crystal fragments glow brighter after use.

> /inventory
Your inventory:
- Crystal Pickaxe: A mining tool enhanced with crystal fragments that glow with inner light.
```

## Item Properties

Items are defined in JSON files and may have various properties:

- **Name**: The name of the item
- **Description**: A description of the item
- **Type**: What kind of item it is (consumable, weapon, key, etc.)
- **Effects**: What happens when the item is used
- **Value**: How valuable the item is (if applicable)

## Tips for Item Management

1. **Check rooms thoroughly** - Items might be mentioned in room descriptions
2. **Inventory management** - Some implementations might limit inventory capacity
3. **Strategic use** - Some items might be more valuable to save for later
4. **Item combinations** - Some puzzles might require using or combining specific items

## Example Item Interaction

```
> /look
You are in the crystal caves. The tunnels glitter with embedded gems and the air hums with magical energy. You can barely make out a crystal pickaxe leaning against the tunnel wall.

> /pickup crystal_pickaxe
You pick up the crystal pickaxe and add it to your inventory.

> /inventory
Your inventory:
- Crystal Pickaxe: A mining tool enhanced with crystal fragments that glow with inner light.

> /go north
You moved deeper into the mining tunnels. Strange crystalline formations block your path!

> /use crystal_pickaxe
You swing the crystal pickaxe at the crystalline formations. The enhanced tool easily breaks through the magical barrier, allowing you to pass.
```
