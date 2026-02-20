# Inventory System

Ollama Dungeon includes a simple inventory system that allows you to pick up, carry, and use items. This guide explains how to interact with the inventory system.

## Basic Inventory Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/inventory` or `/inv` | View your inventory | `/inventory` |
| `/pickup <item>` or `/take <item>` | Pick up an item from the room | `/pickup Crystal Pickaxe` |
| `/use <item>` | Use an item from inventory | `/use health_potion` |

## Finding Items

Items are scattered throughout the world. When you enter a room, the room description will show available items. You can also use the `/look` command to see a description of the room, which includes items present.

Example:
```
> /look
**Crystal Caves Mining Tunnels**
The walls sparkle with embedded gems...

People here: Cassandra

Items here: Crystal Pickaxe

Exits: north

> /pickup Crystal Pickaxe
You pick up the Crystal Pickaxe.

> /inventory
Your inventory:
- Crystal Pickaxe: A mining tool enhanced with crystal fragments that glow with inner light.
```

## Using Items

Items must have the `usable` property set to `true` to be used. When you use an item, the game displays its `use_description` if one is defined.

To use an item:
```
/use <item_name>
```

Example (if the item has `usable: true`):
```
> /use Crystal Pickaxe
You use the Crystal Pickaxe. The enhanced tool easily chips away at the rock.
```

If an item is not usable:
```
> /use Crystal Pickaxe
You can't use the Crystal Pickaxe right now.
```

If you don't have the item:
```
> /use health_potion
You don't have a 'health_potion' in your inventory.
```

## Dropping Items

**Note:** The game does not currently have a `/drop` command. Once you pick up an item, it remains in your inventory permanently. Items cannot be dropped or removed from your inventory after being picked up. This is an intentional design choice - players should be selective about what they carry.

## Item Properties

Items are defined as JSON files in room directories. The supported properties are:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `name` | string | required | The name of the item |
| `description` | string | required | A description of the item (shown in inventory) |
| `type` | string | required | Item category: `tool`, `consumable`, `artifact`, or `survival_gear` |
| `value` | number | `0` | Monetary/gold value of the item |
| `weight` | number | `0.0` | Weight of the item (may affect carrying capacity) |
| `properties` | object | `{}` | Detailed attributes/effects specific to the item |
| `portable` | boolean | `true` | Whether the item can be picked up |
| `usable` | boolean | `false` | Whether the item can be used with `/use` |
| `use_description` | string | "Nothing special happens." | Message shown when the item is used |

### The Properties Object

The `properties` object contains detailed attributes specific to each item type. This is a flexible structure that can include:

**For tools:**
- `durability`: Current durability value
- `max_durability`: Maximum durability before breaking
- `effect`: What the tool does (e.g., "mining", "cutting")

**For consumables:**
- `effect_type`: Type of effect (e.g., "healing", "buff", "cure")
- `magnitude`: Strength of the effect (e.g., healing amount)
- `duration`: How long the effect lasts (for buffs)

**For artifacts:**
- `magical_property`: Special magical ability
- `lore_backstory`: Historical or lore information
- `activation_condition`: How to activate the artifact

**For survival_gear:**
- `protection_type`: What it protects against (e.g., "cold", "heat")
- `protection_level`: Quality of protection

Example item JSON (complete with all fields):
```json
{
  "name": "Crystal Pickaxe",
  "description": "A mining tool enhanced with crystal fragments that glow with inner light.",
  "type": "tool",
  "value": 150,
  "weight": 3.0,
  "properties": {
    "durability": 100,
    "max_durability": 100,
    "effect": "mining",
    "special_ability": "Can harvest crystalline materials"
  },
  "portable": true,
  "usable": true,
  "use_description": "The enhanced tool easily chips away at the rock."
}
```

## Tips for Item Management

1. **Item names can include spaces** - Use multi-word names like `/pickup Crystal Pickaxe`
2. **Check the `portable` flag** - Some items cannot be picked up (e.g., fixed furniture)
3. **Set `usable: true`** - Items must be marked usable before they can be used with `/use`
4. **Case-insensitive matching** - Item names match regardless of capitalization

## Example Item Interaction

```
> /look
**Crystal Caves Mining Tunnels**
The tunnels glitter with embedded gems and the air hums with magical energy.

People here: Cassandra

Items here: Crystal Pickaxe

Exits: north

> /pickup Crystal Pickaxe
You pick up the Crystal Pickaxe.

> /inventory
Your inventory:
- Crystal Pickaxe: A mining tool enhanced with crystal fragments that glow with inner light.

> /go north
You go north.

**Crystal Caves Deep Tunnel**
Strange crystalline formations block your path!

Items here: none

Exits: south

> /use Crystal Pickaxe
You use the Crystal Pickaxe. The enhanced tool easily breaks through the magical barrier.
```
