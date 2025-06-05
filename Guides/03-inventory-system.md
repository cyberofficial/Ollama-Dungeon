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
You are in the market. There are various stalls selling goods. You notice a health potion on one of the tables.

> /pickup health_potion
You pick up the health potion and add it to your inventory.

> /inventory
Your inventory:
- Health Potion: A small vial containing a red liquid that restores health.
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
> /use health_potion
You drink the health potion. You feel revitalized and healthier.
The potion has been consumed and removed from your inventory.

> /inventory
Your inventory is empty.
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
You are in the cave. It's dark and damp. You can barely make out a rusty dagger on the ground.

> /pickup rusty dagger
You pick up the rusty dagger and add it to your inventory.

> /inventory
Your inventory:
- Rusty Dagger: An old, rusty dagger. It's not very sharp, but could be useful.

> /go north
You moved to a deeper part of the cave. There's a strange creature blocking your path!

> /use rusty dagger
You brandish the rusty dagger at the creature. Despite its condition, it seems to deter the creature, which backs away allowing you to pass.
```
