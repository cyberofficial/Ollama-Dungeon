# RolePlayBot Editor Integration Guide

## Overview
The RolePlayBot Editor Suite provides integrated tools for building and managing your game world and NPCs. The World Editor and NPC Editor work together seamlessly to provide a comprehensive world-building experience.

## Quick Start

### 1. Launch the Editor Suite
```bash
python editor_launcher.py
```

### 2. Choose Your Editor
- **🌍 World Editor**: For managing rooms, items, and world structure
- **👤 NPC Editor**: For creating and editing NPCs/Agents

## Integration Features

### Editing NPCs from World Editor

When using the World Editor, you can directly edit NPCs without switching tools:

1. **Navigate the World Tree**: Browse through your world structure in the left panel
2. **Find NPCs**: NPCs appear as `agent_*.json` files in room directories
3. **Select an NPC**: Click on any NPC file in the tree
4. **View NPC Info**: The "NPC Editor" tab shows information about the selected NPC
5. **Edit the NPC**: 
   - **Double-click** the NPC in the tree, OR
   - Click the **"Edit Selected NPC"** button in the NPC Editor tab

### What Happens When You Edit an NPC

- The standalone NPC Editor opens automatically
- The selected NPC file is loaded immediately
- All NPC properties are available for editing:
  - Basic info (name, description, personality)
  - Advanced attributes (goals, background, knowledge)  
  - Relationships and dialogue patterns
  - Memory management
- Changes are saved back to the original file
- Return to World Editor to see your changes reflected

### Workflow Examples

#### Creating a New NPC
1. Open World Editor
2. Navigate to a room where you want to add an NPC
3. Right-click in the tree → "New NPC"
4. Edit the NPC properties in the opened NPC Editor
5. Save and return to World Editor

#### Editing Existing NPCs
1. Open World Editor
2. Browse to any NPC in your world
3. Double-click the NPC to open the editor
4. Make your changes
5. Save and close

#### Managing NPC Relationships
1. Edit one NPC through World Editor
2. Set up relationships with other NPCs
3. The relationships are automatically saved
4. Edit other NPCs to create bidirectional relationships

## File Structure

The editors maintain your existing file structure:

```
world_template/
├── area_name/
│   ├── room.json              # Room properties
│   └── sub_location/
│       ├── room.json          # Sub-room properties
│       ├── agent_name.json    # NPC file (editable via integration)
│       ├── memory_name.csv    # NPC memories
│       └── item_name.json     # Items
```

## Benefits of Integration

✅ **Seamless Workflow**: Edit NPCs directly from world context
✅ **Consistent Data**: All changes maintain file structure compatibility  
✅ **Context Awareness**: See NPCs in their world location while editing
✅ **No File Management**: Automatic file loading and saving
✅ **Quick Access**: Double-click to edit, no manual file browsing

## Tips

- **Use the World Editor** as your main hub for world building
- **Double-click NPCs** for the fastest editing experience
- **Check the NPC Editor tab** to see currently selected NPC info
- **Save frequently** - both editors auto-save to files
- **Test your NPCs** in the main game after editing

## Troubleshooting

If the NPC Editor doesn't open:
1. Check that `npc_editor.py` exists in the same directory
2. Ensure Python can find the file (check your PATH)
3. Look for error messages in the console

If changes don't appear:
1. Make sure you saved in the NPC Editor
2. Refresh the World Editor view if needed
3. Check file permissions

## Advanced Features

- **Command Line Support**: You can also launch the NPC Editor directly with a file:
  ```bash
  python npc_editor.py path/to/agent_file.json
  ```
- **Memory Editing**: Edit NPC memories directly from the NPC Editor
- **Validation**: Both editors validate your data before saving
- **Backup**: Original files are preserved during editing

---

Happy world building! 🌍👤
