#!/usr/bin/env python3
"""
World Editor GUI for Ollama Dungeon
Creates a visual interface for editing rooms, NPCs, and items.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
import shutil
from typing import Dict, List, Any, Optional
import csv
from datetime import datetime
import subprocess
import sys


class WorldEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama Dungeon - World Editor")
        self.root.geometry("1200x800")
          # Current working directory (world_template by default)
        self.current_world_path = "world_template"
        self.current_room_path = None
        self.current_room_data = None
        self.current_npc_path = None
        
        self.setup_ui()
        self.refresh_world_tree()
    
    def setup_ui(self):
        """Setup the main UI components."""
        # Create main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create paned window for layout
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - World tree
        self.setup_left_panel(paned)
        
        # Right panel - Editor
        self.setup_right_panel(paned)
        
        # Menu bar
        self.setup_menu()
    
    def setup_menu(self):
        """Setup the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New World...", command=self.new_world)
        file_menu.add_command(label="Open World...", command=self.open_world)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="New Room...", command=self.new_room)
        edit_menu.add_command(label="New NPC...", command=self.new_npc)
        edit_menu.add_command(label="New Item...", command=self.new_item)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Validate World", command=self.validate_world)
        tools_menu.add_command(label="Export to Game", command=self.export_to_game)
    
    def setup_left_panel(self, parent):
        """Setup the left panel with world tree."""
        left_frame = ttk.Frame(parent)
        parent.add(left_frame, weight=1)
        
        # Title
        ttk.Label(left_frame, text="World Structure", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Treeview for world structure
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.world_tree = ttk.Treeview(tree_frame)
        self.world_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.world_tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.world_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Bind events
        self.world_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.world_tree.bind('<Double-1>', self.on_tree_double_click)
        
        # Context menu
        self.setup_context_menu()
    
    def setup_context_menu(self):
        """Setup right-click context menu for tree."""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="New Room", command=self.new_room)
        self.context_menu.add_command(label="New NPC", command=self.new_npc)
        self.context_menu.add_command(label="New Item", command=self.new_item)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        
        self.world_tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Show context menu on right click."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def setup_right_panel(self, parent):
        """Setup the right panel with editor."""
        right_frame = ttk.Frame(parent)
        parent.add(right_frame, weight=2)
        
        # Notebook for different editor tabs
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Room editor tab
        self.setup_room_editor()
        
        # NPC editor tab
        self.setup_npc_editor()
        
        # Item editor tab
        self.setup_item_editor()
    
    def setup_room_editor(self):
        """Setup the room editor tab."""
        self.room_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.room_frame, text="Room Editor")
        
        # Create scrollable frame
        canvas = tk.Canvas(self.room_frame)
        scrollbar = ttk.Scrollbar(self.room_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Room fields
        ttk.Label(scrollable_frame, text="Room Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.room_name_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.room_name_var, width=50).grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        ttk.Label(scrollable_frame, text="Description:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.room_description = tk.Text(scrollable_frame, height=6, width=60, wrap=tk.WORD)
        self.room_description.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Exits frame
        exits_frame = ttk.LabelFrame(scrollable_frame, text="Exits")
        exits_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        
        self.exits_vars = {}
        exit_directions = ["north", "south", "east", "west", "up", "down", "northeast", "northwest", "southeast", "southwest"]
        
        for i, direction in enumerate(exit_directions):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(exits_frame, text=f"{direction.title()}:").grid(row=row, column=col, sticky="w", padx=5, pady=2)
            self.exits_vars[direction] = tk.StringVar()
            ttk.Entry(exits_frame, textvariable=self.exits_vars[direction], width=30).grid(row=row, column=col+1, padx=5, pady=2, sticky="ew")
        
        # Ambient settings
        ambient_frame = ttk.LabelFrame(scrollable_frame, text="Ambient Settings")
        ambient_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        
        ttk.Label(ambient_frame, text="Sounds (comma-separated):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.ambient_sounds_var = tk.StringVar()
        ttk.Entry(ambient_frame, textvariable=self.ambient_sounds_var, width=50).grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(ambient_frame, text="Time of Day:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.ambient_time_var = tk.StringVar()
        ttk.Entry(ambient_frame, textvariable=self.ambient_time_var, width=50).grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(ambient_frame, text="Weather:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.ambient_weather_var = tk.StringVar()
        ttk.Entry(ambient_frame, textvariable=self.ambient_weather_var, width=50).grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Save Room", command=self.save_room).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_room_editor).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights        scrollable_frame.columnconfigure(1, weight=1)
        exits_frame.columnconfigure(1, weight=1)
        exits_frame.columnconfigure(3, weight=1)
        ambient_frame.columnconfigure(1, weight=1)
    
    def setup_npc_editor(self):
        """Setup the NPC editor tab."""
        self.npc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.npc_frame, text="NPC Editor")
        
        # NPC info frame
        info_frame = ttk.LabelFrame(self.npc_frame, text="Selected NPC")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.selected_npc_label = ttk.Label(info_frame, text="No NPC selected", font=("Arial", 10))
        self.selected_npc_label.pack(pady=10)
        
        # Buttons frame
        button_frame = ttk.Frame(self.npc_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Open NPC Editor", 
                  command=self.open_npc_editor).pack(side=tk.LEFT, padx=5)
        
        self.edit_selected_npc_btn = ttk.Button(button_frame, text="Edit Selected NPC", 
                                               command=self.edit_selected_npc, state=tk.DISABLED)
        self.edit_selected_npc_btn.pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instructions = ttk.Label(self.npc_frame, 
                               text="• Select an NPC from the world tree to edit it\n• Double-click an NPC in the tree to open the editor\n• Use 'Open NPC Editor' to create a new NPC or open any NPC file",
                               justify=tk.LEFT, font=("Arial", 9))
        instructions.pack(pady=20, padx=10, anchor="w")
    
    def setup_item_editor(self):
        """Setup the item editor tab."""
        self.item_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.item_frame, text="Item Editor")
        
        # Create scrollable frame
        canvas = tk.Canvas(self.item_frame)
        scrollbar = ttk.Scrollbar(self.item_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Item fields
        ttk.Label(scrollable_frame, text="Item Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.item_name_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.item_name_var, width=50).grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        ttk.Label(scrollable_frame, text="Description:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.item_description = tk.Text(scrollable_frame, height=4, width=60, wrap=tk.WORD)
        self.item_description.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Basic properties
        props_frame = ttk.LabelFrame(scrollable_frame, text="Basic Properties")
        props_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        
        ttk.Label(props_frame, text="Type:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.item_type_var = tk.StringVar()
        type_combo = ttk.Combobox(props_frame, textvariable=self.item_type_var, 
                                 values=["weapon", "armor", "potion", "key", "treasure", "tool", "magical_crystal", "scroll", "food", "misc"])
        type_combo.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(props_frame, text="Value:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.item_value_var = tk.IntVar()
        ttk.Entry(props_frame, textvariable=self.item_value_var, width=10).grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(props_frame, text="Weight:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.item_weight_var = tk.DoubleVar()
        ttk.Entry(props_frame, textvariable=self.item_weight_var, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        # Checkboxes
        self.item_usable_var = tk.BooleanVar()
        ttk.Checkbutton(props_frame, text="Usable", variable=self.item_usable_var).grid(row=1, column=2, padx=5, pady=2)
        
        self.item_portable_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(props_frame, text="Portable", variable=self.item_portable_var).grid(row=1, column=3, padx=5, pady=2)
        
        # Use description
        ttk.Label(scrollable_frame, text="Use Description:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.item_use_description = tk.Text(scrollable_frame, height=3, width=60, wrap=tk.WORD)
        self.item_use_description.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Magic properties
        magic_frame = ttk.LabelFrame(scrollable_frame, text="Magical Properties")
        magic_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        
        self.item_magic_var = tk.BooleanVar()
        ttk.Checkbutton(magic_frame, text="Magical Item", variable=self.item_magic_var).grid(row=0, column=0, padx=5, pady=2)
        
        ttk.Label(magic_frame, text="Magic Properties (JSON):").grid(row=1, column=0, sticky="nw", padx=5, pady=2)
        self.item_properties = tk.Text(magic_frame, height=5, width=60, wrap=tk.WORD)
        self.item_properties.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Save Item", command=self.save_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_item_editor).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        scrollable_frame.columnconfigure(1, weight=1)
        props_frame.columnconfigure(1, weight=1)
        magic_frame.columnconfigure(1, weight=1)
    
    def refresh_world_tree(self):
        """Refresh the world tree display."""
        # Clear existing items
        for item in self.world_tree.get_children():
            self.world_tree.delete(item)
        
        if not os.path.exists(self.current_world_path):
            return
        
        # Add root item
        root_item = self.world_tree.insert("", "end", text=os.path.basename(self.current_world_path), 
                                          values=[self.current_world_path], open=True)
        
        # Recursively add items
        self._add_tree_items(root_item, self.current_world_path)
    
    def _add_tree_items(self, parent_item, path):
        """Recursively add items to the tree."""
        if not os.path.exists(path):
            return
        
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                items.append((item, item_path, "folder"))
            elif item.endswith('.json'):
                if item == 'room.json':
                    items.append((item, item_path, "room"))
                elif item.startswith('agent_'):
                    items.append((item, item_path, "npc"))
                else:
                    items.append((item, item_path, "item"))
        
        # Sort items: folders first, then files
        items.sort(key=lambda x: (x[2] != "folder", x[0]))
        
        for item_name, item_path, item_type in items:
            if item_type == "folder":
                folder_item = self.world_tree.insert(parent_item, "end", text=item_name, 
                                                   values=[item_path, item_type])
                self._add_tree_items(folder_item, item_path)
            else:
                # Format display name based on type
                display_name = item_name
                if item_type == "npc":
                    display_name = f"👤 {item_name}"
                elif item_type == "item":
                    display_name = f"📦 {item_name}"
                elif item_type == "room":
                    display_name = f"🏠 {item_name}"
                
                self.world_tree.insert(parent_item, "end", text=display_name, 
                                     values=[item_path, item_type])
    
    def on_tree_select(self, event):
        """Handle tree selection."""
        selection = self.world_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.world_tree.item(item, "values")
        if not values:
            return
        
        file_path = values[0]
        item_type = values[1] if len(values) > 1 else ""
        
        # Load appropriate editor based on file type
        if item_type == "room":
            self.load_room(file_path)
            self.notebook.select(0)  # Select room editor tab
            self.current_npc_path = None
            self.update_npc_selection()
        elif item_type == "item":
            self.load_item(file_path)
            self.notebook.select(2)  # Select item editor tab
            self.current_npc_path = None
            self.update_npc_selection()
        elif item_type == "npc":
            self.current_npc_path = file_path
            self.notebook.select(1)  # Select NPC editor tab
            self.update_npc_selection()
    
    def on_tree_double_click(self, event):
        """Handle tree double-click."""
        selection = self.world_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.world_tree.item(item, "values")
        if not values:
            return
        
        file_path = values[0]
        item_type = values[1] if len(values) > 1 else ""
        
        if item_type == "npc":
            self.edit_npc(file_path)
    
    def load_room(self, room_file):
        """Load a room file into the editor."""
        try:
            with open(room_file, 'r', encoding='utf-8') as f:
                room_data = json.load(f)
            
            self.current_room_path = room_file
            self.current_room_data = room_data
            
            # Populate room editor fields
            self.room_name_var.set(room_data.get('name', ''))
            
            self.room_description.delete('1.0', tk.END)
            self.room_description.insert('1.0', room_data.get('description', ''))
            
            # Load exits
            exits = room_data.get('exits', {})
            for direction, var in self.exits_vars.items():
                var.set(exits.get(direction, ''))
            
            # Load ambient settings
            ambient = room_data.get('ambient', {})
            sounds = ambient.get('sounds', [])
            if isinstance(sounds, list):
                self.ambient_sounds_var.set(', '.join(sounds))
            else:
                self.ambient_sounds_var.set(str(sounds))
            
            self.ambient_time_var.set(ambient.get('time_of_day', ''))
            self.ambient_weather_var.set(ambient.get('weather', ''))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load room: {e}")
    
    def save_room(self):
        """Save the current room data."""
        if not self.current_room_path:
            # New room - ask for location and name
            self.new_room()
            return
        
        try:
            # Collect data from form
            room_data = {
                'name': self.room_name_var.get(),
                'description': self.room_description.get('1.0', tk.END).strip(),
                'exits': {},
                'ambient': {
                    'sounds': [],
                    'time_of_day': self.ambient_time_var.get(),
                    'weather': self.ambient_weather_var.get()
                }
            }
            
            # Process exits
            for direction, var in self.exits_vars.items():
                value = var.get().strip()
                if value:
                    room_data['exits'][direction] = value
            
            # Process sounds
            sounds_text = self.ambient_sounds_var.get().strip()
            if sounds_text:
                room_data['ambient']['sounds'] = [s.strip() for s in sounds_text.split(',') if s.strip()]
            
            # Save to file
            with open(self.current_room_path, 'w', encoding='utf-8') as f:
                json.dump(room_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", "Room saved successfully!")
            self.refresh_world_tree()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save room: {e}")
    
    def load_item(self, item_file):
        """Load an item file into the editor."""
        try:
            with open(item_file, 'r', encoding='utf-8') as f:
                item_data = json.load(f)
            
            # Populate item editor fields
            self.item_name_var.set(item_data.get('name', ''))
            
            self.item_description.delete('1.0', tk.END)
            self.item_description.insert('1.0', item_data.get('description', ''))
            
            self.item_type_var.set(item_data.get('type', 'misc'))
            self.item_value_var.set(item_data.get('value', 0))
            self.item_weight_var.set(item_data.get('weight', 0.0))
            self.item_usable_var.set(item_data.get('usable', False))
            self.item_portable_var.set(item_data.get('portable', True))
            
            self.item_use_description.delete('1.0', tk.END)
            self.item_use_description.insert('1.0', item_data.get('use_description', ''))
            
            # Handle properties
            properties = item_data.get('properties', {})
            self.item_magic_var.set(properties.get('magic', False))
            
            # Convert properties to JSON string for editing
            self.item_properties.delete('1.0', tk.END)
            if properties:
                self.item_properties.insert('1.0', json.dumps(properties, indent=2))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load item: {e}")
    
    def save_item(self):
        """Save the current item data."""
        # Get current room path for saving
        selection = self.world_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a room to save the item to.")
            return
        
        item = selection[0]
        values = self.world_tree.item(item, "values")
        if not values:
            return
        
        # Determine save location
        file_path = values[0]
        if values[1] == "room":
            # Save to same directory as room.json
            save_dir = os.path.dirname(file_path)
        elif os.path.isdir(file_path):
            # Save to selected directory
            save_dir = file_path
        else:
            # Get parent directory
            save_dir = os.path.dirname(file_path)
        
        # Get item name for filename
        item_name = self.item_name_var.get().strip()
        if not item_name:
            messagebox.showwarning("Warning", "Please enter an item name.")
            return
        
        # Create filename
        safe_name = "".join(c for c in item_name.lower() if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        filename = f"{safe_name}.json"
        save_path = os.path.join(save_dir, filename)
        
        try:
            # Collect data from form
            item_data = {
                'name': item_name,
                'description': self.item_description.get('1.0', tk.END).strip(),
                'type': self.item_type_var.get(),
                'value': self.item_value_var.get(),
                'weight': self.item_weight_var.get(),
                'usable': self.item_usable_var.get(),
                'portable': self.item_portable_var.get()
            }
            
            # Add use description if provided
            use_desc = self.item_use_description.get('1.0', tk.END).strip()
            if use_desc:
                item_data['use_description'] = use_desc
            
            # Handle properties
            properties_text = self.item_properties.get('1.0', tk.END).strip()
            if properties_text:
                try:
                    properties = json.loads(properties_text)
                    item_data['properties'] = properties
                except json.JSONDecodeError:
                    # If JSON is invalid, create basic properties dict
                    item_data['properties'] = {'magic': self.item_magic_var.get()}
            else:
                item_data['properties'] = {'magic': self.item_magic_var.get()}
            
            # Save to file
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(item_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Item saved as {filename}!")
            self.refresh_world_tree()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save item: {e}")
    
    def clear_room_editor(self):
        """Clear all room editor fields."""
        self.room_name_var.set('')
        self.room_description.delete('1.0', tk.END)
        for var in self.exits_vars.values():
            var.set('')
        self.ambient_sounds_var.set('')
        self.ambient_time_var.set('')
        self.ambient_weather_var.set('')
        self.current_room_path = None
        self.current_room_data = None
    
    def clear_item_editor(self):
        """Clear all item editor fields."""
        self.item_name_var.set('')
        self.item_description.delete('1.0', tk.END)
        self.item_type_var.set('misc')
        self.item_value_var.set(0)
        self.item_weight_var.set(0.0)
        self.item_usable_var.set(False)
        self.item_portable_var.set(True)
        self.item_use_description.delete('1.0', tk.END)
        self.item_magic_var.set(False)
        self.item_properties.delete('1.0', tk.END)
    
    def new_world(self):
        """Create a new world template."""
        world_name = simpledialog.askstring("New World", "Enter world name:")
        if not world_name:
            return
        
        # Create new directory
        new_world_path = f"world_template_{world_name}"
        if os.path.exists(new_world_path):
            messagebox.showerror("Error", "World already exists!")
            return
        
        try:
            os.makedirs(new_world_path)
            
            # Create initial room.json
            initial_room = {
                "name": f"{world_name} - Starting Area",
                "description": "A new area waiting to be explored and developed.",
                "exits": {},
                "ambient": {
                    "sounds": ["gentle breeze", "distant sounds"],
                    "time_of_day": "peaceful morning",
                    "weather": "pleasant and mild"
                }
            }
            
            with open(os.path.join(new_world_path, "room.json"), 'w') as f:
                json.dump(initial_room, f, indent=2)
            
            self.current_world_path = new_world_path
            self.refresh_world_tree()
            messagebox.showinfo("Success", f"New world '{world_name}' created!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create world: {e}")
    
    def open_world(self):
        """Open an existing world."""
        world_path = filedialog.askdirectory(title="Select World Directory")
        if world_path:
            self.current_world_path = world_path
            self.refresh_world_tree()
    
    def new_room(self):
        """Create a new room."""
        # Get current selection to determine where to create the room
        selection = self.world_tree.selection()
        if not selection:
            parent_dir = self.current_world_path
        else:
            item = selection[0]
            values = self.world_tree.item(item, "values")
            if values and os.path.isdir(values[0]):
                parent_dir = values[0]
            else:
                parent_dir = os.path.dirname(values[0]) if values else self.current_world_path
        
        room_name = simpledialog.askstring("New Room", "Enter room directory name:")
        if not room_name:
            return
        
        # Create safe directory name
        safe_name = "".join(c for c in room_name.lower() if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        room_dir = os.path.join(parent_dir, safe_name)
        
        if os.path.exists(room_dir):
            messagebox.showerror("Error", "Room directory already exists!")
            return
        
        try:
            os.makedirs(room_dir)
              # Create room.json
            room_data = {
                "name": room_name,
                "description": "A new room waiting to be described.",
                "exits": {},
                "ambient": {
                    "sounds": [],
                    "time_of_day": "",
                    "weather": ""
                }
            }
            
            room_file = os.path.join(room_dir, "room.json")
            with open(room_file, 'w') as f:
                json.dump(room_data, f, indent=2)
            
            self.refresh_world_tree()
            self.load_room(room_file)
            messagebox.showinfo("Success", f"New room '{room_name}' created!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create room: {e}")
    
    def new_npc(self):
        """Create a new NPC - opens the NPC editor."""
        self.open_npc_editor()
    
    def new_item(self):
        """Create a new item."""
        self.clear_item_editor()
        self.notebook.select(2)  # Select item editor tab
    
    def edit_npc(self, npc_file):
        """Edit an existing NPC."""
        self.open_npc_editor(npc_file)
    
    def open_npc_editor(self, npc_file=None):
        """Open the dedicated NPC editor."""
        try:
            # Try to import and launch the standalone NPC editor
            try:
                from npc_editor import NPCEditorStandalone
                npc_window = tk.Toplevel(self.root)
                npc_editor = NPCEditorStandalone(npc_window)
                if npc_file and os.path.exists(npc_file):
                    npc_editor.load_npc_file(npc_file)
            except ImportError:                # Fallback to subprocess if import fails
                if npc_file and os.path.exists(npc_file):
                    subprocess.Popen([sys.executable, "npc_editor.py", npc_file])
                else:
                    subprocess.Popen([sys.executable, "npc_editor.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open NPC editor: {str(e)}")
            # Fallback to the built-in NPC editor
            npc_window = tk.Toplevel(self.root)
            npc_editor = NPCEditor(npc_window, npc_file, self)
    
    def edit_selected_npc(self):
        """Edit the currently selected NPC."""
        if self.current_npc_path and os.path.exists(self.current_npc_path):
            self.open_npc_editor(self.current_npc_path)
        else:
            messagebox.showwarning("No NPC Selected", "Please select an NPC from the world tree first.")
    
    def update_npc_selection(self):
        """Update the NPC editor tab UI based on current selection."""
        if hasattr(self, 'selected_npc_label') and hasattr(self, 'edit_selected_npc_btn'):
            if self.current_npc_path:
                # Extract NPC name from file path
                npc_name = os.path.basename(os.path.dirname(self.current_npc_path))
                if npc_name.startswith('agent_'):
                    npc_name = npc_name[6:]  # Remove 'agent_' prefix
                
                # Try to load NPC data to get the real name
                try:
                    with open(self.current_npc_path, 'r', encoding='utf-8') as f:
                        npc_data = json.load(f)
                        if 'name' in npc_data:
                            npc_name = npc_data['name']
                except:
                    pass  # Use the filename-based name as fallback
                
                self.selected_npc_label.config(text=f"Selected: {npc_name}")
                self.edit_selected_npc_btn.config(state=tk.NORMAL)
            else:
                self.selected_npc_label.config(text="No NPC selected")
                self.edit_selected_npc_btn.config(state=tk.DISABLED)
    
    def delete_selected(self):
        """Delete the selected item."""
        selection = self.world_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.world_tree.item(item, "values")
        if not values:
            return
        
        file_path = values[0]
        item_name = self.world_tree.item(item, "text")
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_name}'?"):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                
                self.refresh_world_tree()
                messagebox.showinfo("Success", f"'{item_name}' has been deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete '{item_name}': {str(e)}")

    def validate_world(self):
        """Validate the world structure."""
        issues = []
        
        def check_directory(path, level=0):
            if not os.path.exists(path):
                return
            
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                
                if os.path.isdir(item_path):
                    # Check if directory has room.json
                    room_file = os.path.join(item_path, "room.json")
                    if not os.path.exists(room_file):
                        issues.append(f"Missing room.json in {item_path}")
                    else:
                        # Validate room.json structure
                        try:
                            with open(room_file, 'r') as f:
                                room_data = json.load(f)
                            
                            required_fields = ['name', 'description']
                            for field in required_fields:
                                if field not in room_data:
                                    issues.append(f"Missing '{field}' in {room_file}")
                                    
                        except json.JSONDecodeError:
                            issues.append(f"Invalid JSON in {room_file}")
                        except Exception as e:
                            issues.append(f"Error reading {room_file}: {e}")
                    
                    # Recursively check subdirectories
                    check_directory(item_path, level + 1)
                
                elif item.startswith('agent_') and item.endswith('.json'):
                    # Validate agent file
                    try:
                        with open(item_path, 'r') as f:
                            agent_data = json.load(f)
                        
                        required_fields = ['name', 'persona', 'background', 'location', 'memory_file']
                        for field in required_fields:
                            if field not in agent_data:
                                issues.append(f"Missing '{field}' in {item_path}")
                                
                    except json.JSONDecodeError:
                        issues.append(f"Invalid JSON in {item_path}")
                    except Exception as e:
                        issues.append(f"Error reading {item_path}: {e}")
        
        check_directory(self.current_world_path)
        
        if issues:
            issue_text = "\n".join(issues)
            messagebox.showwarning("Validation Issues Found", f"Found {len(issues)} issues:\n\n{issue_text}")
        else:
            messagebox.showinfo("Validation Complete", "No issues found! World structure is valid.")
    
    def export_to_game(self):
        """Export the current world to the game's world directory."""
        if not os.path.exists("world"):
            if messagebox.askyesno("Create World", "Game world directory doesn't exist. Create it?"):
                try:
                    shutil.copytree(self.current_world_path, "world")
                    messagebox.showinfo("Success", "World exported successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to export world: {e}")
        else:
            if messagebox.askyesno("Overwrite World", "Game world already exists. Overwrite it?"):
                try:
                    shutil.rmtree("world")
                    shutil.copytree(self.current_world_path, "world")
                    messagebox.showinfo("Success", "World exported successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to export world: {e}")


class NPCEditor:
    def __init__(self, parent, npc_file=None, world_editor=None):
        self.parent = parent
        self.npc_file = npc_file
        self.world_editor = world_editor
        self.npc_data = {}
        
        self.parent.title("NPC Editor")
        self.parent.geometry("800x900")
        
        self.setup_ui()
        
        if npc_file and os.path.exists(npc_file):
            self.load_npc(npc_file)
    
    def setup_ui(self):
        """Setup the NPC editor UI."""
        # Create main scroll frame
        canvas = tk.Canvas(self.parent)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Basic Information
        basic_frame = ttk.LabelFrame(scrollable_frame, text="Basic Information")
        basic_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(basic_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.name_var, width=50).grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(basic_frame, text="Appearance:").grid(row=1, column=0, sticky="nw", padx=5, pady=2)
        self.appearance_text = tk.Text(basic_frame, height=3, width=50, wrap=tk.WORD)
        self.appearance_text.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(basic_frame, text="Occupation:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.occupation_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.occupation_var, width=50).grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        
        # Personality
        personality_frame = ttk.LabelFrame(scrollable_frame, text="Personality & Background")
        personality_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(personality_frame, text="Persona (1st person):").grid(row=0, column=0, sticky="nw", padx=5, pady=2)
        self.persona_text = tk.Text(personality_frame, height=4, width=50, wrap=tk.WORD)
        self.persona_text.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(personality_frame, text="Background:").grid(row=1, column=0, sticky="nw", padx=5, pady=2)
        self.background_text = tk.Text(personality_frame, height=4, width=50, wrap=tk.WORD)
        self.background_text.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(personality_frame, text="Mood:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.mood_var = tk.StringVar()
        ttk.Entry(personality_frame, textvariable=self.mood_var, width=50).grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(personality_frame, text="Emotional State:").grid(row=3, column=0, sticky="nw", padx=5, pady=2)
        self.emotional_state_text = tk.Text(personality_frame, height=2, width=50, wrap=tk.WORD)
        self.emotional_state_text.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        
        # Knowledge & Goals
        knowledge_frame = ttk.LabelFrame(scrollable_frame, text="Knowledge & Goals")
        knowledge_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(knowledge_frame, text="Knowledge (one per line):").grid(row=0, column=0, sticky="nw", padx=5, pady=2)
        self.knowledge_text = tk.Text(knowledge_frame, height=6, width=50, wrap=tk.WORD)
        self.knowledge_text.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(knowledge_frame, text="Goals (one per line):").grid(row=1, column=0, sticky="nw", padx=5, pady=2)
        self.goals_text = tk.Text(knowledge_frame, height=4, width=50, wrap=tk.WORD)
        self.goals_text.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        # Quirks & Fears
        traits_frame = ttk.LabelFrame(scrollable_frame, text="Quirks & Fears")
        traits_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(traits_frame, text="Quirks (one per line):").grid(row=0, column=0, sticky="nw", padx=5, pady=2)
        self.quirks_text = tk.Text(traits_frame, height=4, width=50, wrap=tk.WORD)
        self.quirks_text.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(traits_frame, text="Fears (one per line):").grid(row=1, column=0, sticky="nw", padx=5, pady=2)
        self.fears_text = tk.Text(traits_frame, height=3, width=50, wrap=tk.WORD)
        self.fears_text.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        # Relationships
        relationships_frame = ttk.LabelFrame(scrollable_frame, text="Relationships")
        relationships_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(relationships_frame, text="Relationships (JSON format):").grid(row=0, column=0, sticky="nw", padx=5, pady=2)
        self.relationships_text = tk.Text(relationships_frame, height=5, width=50, wrap=tk.WORD)
        self.relationships_text.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        # Location & Settings
        location_frame = ttk.LabelFrame(scrollable_frame, text="Location & Settings")
        location_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(location_frame, text="Location:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.location_var = tk.StringVar()
        ttk.Entry(location_frame, textvariable=self.location_var, width=50).grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(location_frame, text="Memory File:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.memory_file_var = tk.StringVar()
        ttk.Entry(location_frame, textvariable=self.memory_file_var, width=50).grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        self.following_var = tk.BooleanVar()
        ttk.Checkbutton(location_frame, text="Following Player", variable=self.following_var).grid(row=2, column=0, columnspan=2, padx=5, pady=2, sticky="w")
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill="x", padx=10, pady=20)
        
        ttk.Button(button_frame, text="Save NPC", command=self.save_npc).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save As...", command=self.save_npc_as).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.parent.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Configure grid weights
        basic_frame.columnconfigure(1, weight=1)
        personality_frame.columnconfigure(1, weight=1)
        knowledge_frame.columnconfigure(1, weight=1)
        traits_frame.columnconfigure(1, weight=1)
        relationships_frame.columnconfigure(1, weight=1)
        location_frame.columnconfigure(1, weight=1)
    
    def load_npc(self, npc_file):
        """Load NPC data from file."""
        try:
            with open(npc_file, 'r', encoding='utf-8') as f:
                self.npc_data = json.load(f)
            
            # Populate form fields
            self.name_var.set(self.npc_data.get('name', ''))
            
            self.appearance_text.delete('1.0', tk.END)
            self.appearance_text.insert('1.0', self.npc_data.get('appearance', ''))
            
            self.occupation_var.set(self.npc_data.get('occupation', ''))
            
            self.persona_text.delete('1.0', tk.END)
            self.persona_text.insert('1.0', self.npc_data.get('persona', ''))
            
            self.background_text.delete('1.0', tk.END)
            self.background_text.insert('1.0', self.npc_data.get('background', ''))
            
            self.mood_var.set(self.npc_data.get('mood', ''))
            
            self.emotional_state_text.delete('1.0', tk.END)
            self.emotional_state_text.insert('1.0', self.npc_data.get('emotional_state', ''))
            
            # Handle lists
            knowledge = self.npc_data.get('knowledge', [])
            self.knowledge_text.delete('1.0', tk.END)
            if knowledge:
                self.knowledge_text.insert('1.0', '\n'.join(knowledge))
            
            goals = self.npc_data.get('goals', [])
            self.goals_text.delete('1.0', tk.END)
            if goals:
                self.goals_text.insert('1.0', '\n'.join(goals))
            
            quirks = self.npc_data.get('quirks', [])
            self.quirks_text.delete('1.0', tk.END)
            if quirks:
                self.quirks_text.insert('1.0', '\n'.join(quirks))
            
            fears = self.npc_data.get('fears', [])
            self.fears_text.delete('1.0', tk.END)
            if fears:
                self.fears_text.insert('1.0', '\n'.join(fears))
            
            # Relationships
            relationships = self.npc_data.get('relationships', {})
            self.relationships_text.delete('1.0', tk.END)
            if relationships:
                self.relationships_text.insert('1.0', json.dumps(relationships, indent=2))
            
            # Location settings
            self.location_var.set(self.npc_data.get('location', ''))
            self.memory_file_var.set(self.npc_data.get('memory_file', ''))
            self.following_var.set(self.npc_data.get('following', False))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load NPC: {e}")
    
    def save_npc(self):
        """Save the NPC data."""
        if self.npc_file:
            self._save_to_file(self.npc_file)
        else:
            self.save_npc_as()
    
    def save_npc_as(self):
        """Save the NPC with a new name/location."""
        # Get NPC name for filename
        npc_name = self.name_var.get().strip()
        if not npc_name:
            messagebox.showwarning("Warning", "Please enter an NPC name.")
            return
        
        # Get save location
        if self.world_editor:
            # Get current selection from world editor
            selection = self.world_editor.world_tree.selection()
            if selection:
                item = selection[0]
                values = self.world_editor.world_tree.item(item, "values")
                if values:
                    file_path = values[0]
                    if values[1] == "room":
                        save_dir = os.path.dirname(file_path)
                    elif os.path.isdir(file_path):
                        save_dir = file_path
                    else:
                        save_dir = os.path.dirname(file_path)
                else:
                    save_dir = self.world_editor.current_world_path
            else:
                save_dir = self.world_editor.current_world_path
        else:
            save_dir = filedialog.askdirectory(title="Select directory to save NPC")
            if not save_dir:
                return
        
        # Create filename
        safe_name = "".join(c for c in npc_name.lower() if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        filename = f"agent_{safe_name}.json"
        save_path = os.path.join(save_dir, filename)
        
        self._save_to_file(save_path)
    
    def _save_to_file(self, file_path):
        """Save NPC data to specified file."""
        try:
            # Collect data from form
            npc_data = {
                'name': self.name_var.get(),
                'persona': self.persona_text.get('1.0', tk.END).strip(),
                'background': self.background_text.get('1.0', tk.END).strip(),
                'location': self.location_var.get(),
                'memory_file': self.memory_file_var.get(),
                'following': self.following_var.get(),
                'mood': self.mood_var.get(),
                'appearance': self.appearance_text.get('1.0', tk.END).strip(),
                'occupation': self.occupation_var.get(),
                'emotional_state': self.emotional_state_text.get('1.0', tk.END).strip()
            }
            
            # Handle lists
            knowledge_text = self.knowledge_text.get('1.0', tk.END).strip()
            if knowledge_text:
                npc_data['knowledge'] = [line.strip() for line in knowledge_text.split('\n') if line.strip()]
            else:
                npc_data['knowledge'] = []
            
            goals_text = self.goals_text.get('1.0', tk.END).strip()
            if goals_text:
                npc_data['goals'] = [line.strip() for line in goals_text.split('\n') if line.strip()]
            else:
                npc_data['goals'] = []
            
            quirks_text = self.quirks_text.get('1.0', tk.END).strip()
            if quirks_text:
                npc_data['quirks'] = [line.strip() for line in quirks_text.split('\n') if line.strip()]
            else:
                npc_data['quirks'] = []
            
            fears_text = self.fears_text.get('1.0', tk.END).strip()
            if fears_text:
                npc_data['fears'] = [line.strip() for line in fears_text.split('\n') if line.strip()]
            else:
                npc_data['fears'] = []
            
            # Handle relationships
            relationships_text = self.relationships_text.get('1.0', tk.END).strip()
            if relationships_text:
                try:
                    npc_data['relationships'] = json.loads(relationships_text)
                except json.JSONDecodeError:
                    npc_data['relationships'] = {}
            else:
                npc_data['relationships'] = {}
            
            # Auto-generate memory file name if not provided
            if not npc_data['memory_file']:
                safe_name = "".join(c for c in npc_data['name'].lower() if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_name = safe_name.replace(' ', '_')
                npc_data['memory_file'] = f"memory_{safe_name}.csv"
            
            # Auto-generate location if not provided
            if not npc_data['location']:
                # Try to determine from file path
                if self.world_editor:
                    rel_path = os.path.relpath(os.path.dirname(file_path), self.world_editor.current_world_path)
                    if rel_path != '.':
                        npc_data['location'] = f"world/{rel_path.replace(os.sep, '/')}"
                    else:
                        npc_data['location'] = "world"
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(npc_data, f, indent=2, ensure_ascii=False)
            
            # Create memory file if it doesn't exist
            memory_file_path = os.path.join(os.path.dirname(file_path), npc_data['memory_file'])
            if not os.path.exists(memory_file_path):
                with open(memory_file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['memory_type', 'key', 'value', 'timestamp'])
            
            self.npc_file = file_path
            messagebox.showinfo("Success", f"NPC saved successfully!")
            
            # Refresh world editor if available
            if self.world_editor:
                self.world_editor.refresh_world_tree()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save NPC: {e}")
    
    def clear_form(self):
        """Clear all form fields."""
        self.name_var.set('')
        self.appearance_text.delete('1.0', tk.END)
        self.occupation_var.set('')
        self.persona_text.delete('1.0', tk.END)
        self.background_text.delete('1.0', tk.END)
        self.mood_var.set('')
        self.emotional_state_text.delete('1.0', tk.END)
        self.knowledge_text.delete('1.0', tk.END)
        self.goals_text.delete('1.0', tk.END)
        self.quirks_text.delete('1.0', tk.END)
        self.fears_text.delete('1.0', tk.END)
        self.relationships_text.delete('1.0', tk.END)
        self.location_var.set('')
        self.memory_file_var.set('')
        self.following_var.set(False)


def main():
    root = tk.Tk()
    app = WorldEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
