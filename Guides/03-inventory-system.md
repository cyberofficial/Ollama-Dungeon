# Inventory System

Ollama Dungeon includes a simple inventory system that allows you to pick up, carry, and use items. This guide explains how to interact with the inventory system.

## Basic Inventory Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/inventory` or `/inv` | View your inventory | `/inventory` |
| `/pickup <item>` or `/take <item>` | Pick up an item from the room | `/pickup crystal pickaxe` |
| `/use <item>` | Use an item from inventory | `/use health_potion` |

## Finding Items

Items are scattered throughout the world. When you enter a room, the room description will show available items. You can also use the `/look` command to see a description of the room, which includes items present.

Example:
```
> /look
**Crystal Caves Mining Tunnels**
The walls sparkle with embedded gems...

People here: Cassandra

Items here: crystal pickaxe

Exits: north

> /pickup crystal pickaxe
You pick up the crystal pickaxe.

> /inventory
Your inventory:
- crystal pickaxe: A mining tool enhanced with crystal fragments that glow with inner light.
```

## Using Items

Items must have the `usable` property set to `true` to be used. When you use an item, the game displays its `use_description` if one is defined.

To use an item:
```
/use <item_name>
```

Example (if the item has `usable: true`):
```
> /use crystal pickaxe
You use the crystal pickaxe. The enhanced tool easily chips away at the rock.
```

If an item is not usable:
```
> /use crystal pickaxe
You can't use the crystal pickaxe right now.
```

If you don't have the item:
```
> /use health_potion
You don't have a 'health_potion' in your inventory.
```

## Item Properties

Items are defined as JSON files in room directories. The supported properties are:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `name` | string | required | The name of the item |
| `description` | string | required | A description of the item (shown in inventory) |
| `portable` | boolean | `true` | Whether the item can be picked up |
| `usable` | boolean | `false` | Whether the item can be used with `/use` |
| `use_description` | string | "Nothing special happens." | Message shown when the item is used |

Example item JSON:
```json
{
  "name": "crystal pickaxe",
  "description": "A mining tool enhanced with crystal fragments that glow with inner light.",
  "portable": true,
  "usable": true,
  "use_description": "The enhanced tool easily chips away at the rock."
}
```

## Tips for Item Management

1. **Item names can include spaces** - Use multi-word names like `/pickup crystal pickaxe`
2. **Check the `portable` flag** - Some items cannot be picked up (e.g., fixed furniture)
3. **Set `usable: true`** - Items must be marked usable before they can be used with `/use`
4. **Case-insensitive matching** - Item names match regardless of capitalization

## Example Item Interaction

```
> /look
**Crystal Caves Mining Tunnels**
The tunnels glitter with embedded gems and the air hums with magical energy.

People here: Cassandra

Items here: crystal pickaxe

Exits: north

> /pickup crystal pickaxe
You pick up the crystal pickaxe.

> /inventory
Your inventory:
- crystal pickaxe: A mining tool enhanced with crystal fragments that glow with inner light.

> /go north
You go north.

**Crystal Caves Deep Tunnel**
Strange crystalline formations block your path!

Items here: none

Exits: south

> /use crystal pickaxe
You use the crystal pickaxe. The enhanced tool easily breaks through the magical barrier.
```
