#!/usr/bin/env python3
"""
NPC Editor GUI for Ollama Dungeon
Creates a visual interface for creating and editing NPCs with all their attributes.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
import csv
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys


class NPCEditorStandalone:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama Dungeon - NPC Editor")
        self.root.geometry("900x1000")
        
        self.current_npc_file = None
        self.npc_data = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI components."""
        # Menu bar
        self.setup_menu()
        
        # Main container with scrolling
        self.setup_main_frame()
        
        # Load default values
        self.load_defaults()
    
    def setup_menu(self):
        """Setup the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New NPC", command=self.new_npc)
        file_menu.add_command(label="Open NPC...", command=self.open_npc)
        file_menu.add_command(label="Save", command=self.save_npc, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_npc_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear All", command=self.clear_all)
        edit_menu.add_command(label="Load Template...", command=self.load_template)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Validate NPC", command=self.validate_npc)
        tools_menu.add_command(label="Generate Template", command=self.generate_template)
        tools_menu.add_command(label="Quick Fill", command=self.quick_fill)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-s>', lambda e: self.save_npc())
        self.root.bind('<Control-n>', lambda e: self.new_npc())
        self.root.bind('<Control-o>', lambda e: self.open_npc())
    
    def setup_main_frame(self):
        """Setup the main scrollable frame."""
        # Create main canvas and scrollbar
        main_canvas = tk.Canvas(self.root)
        main_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = ttk.Frame(main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Create all the form sections
        self.create_form_sections()
    
    def create_form_sections(self):
        """Create all the form sections."""
        # Title
        title_frame = ttk.Frame(self.scrollable_frame)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(title_frame, text="NPC Character Editor", 
                 font=("Arial", 16, "bold")).pack()
        
        # Current file indicator
        self.file_label = ttk.Label(title_frame, text="New NPC", 
                                   font=("Arial", 10, "italic"))
        self.file_label.pack()
        
        # Basic Information Section
        self.create_basic_info_section()
        
        # Personality Section
        self.create_personality_section()
        
        # Knowledge & Goals Section
        self.create_knowledge_goals_section()
        
        # Traits & Quirks Section
        self.create_traits_section()
        
        # Relationships Section
        self.create_relationships_section()
        
        # Game Settings Section
        self.create_game_settings_section()
        
        # Action Buttons
        self.create_action_buttons()
    
    def create_basic_info_section(self):
        """Create the basic information section."""
        basic_frame = ttk.LabelFrame(self.scrollable_frame, text="📝 Basic Information")
        basic_frame.pack(fill="x", padx=10, pady=5)
        
        # Name
        ttk.Label(basic_frame, text="Name:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(basic_frame, textvariable=self.name_var, width=50, font=("Arial", 10))
        name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Occupation
        ttk.Label(basic_frame, text="Occupation:").grid(
            row=1, column=0, sticky="w", padx=5, pady=2)
        self.occupation_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.occupation_var, width=50).grid(
            row=1, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        
        # Appearance
        ttk.Label(basic_frame, text="Appearance:").grid(
            row=2, column=0, sticky="nw", padx=5, pady=5)
        self.appearance_text = tk.Text(basic_frame, height=4, width=60, wrap=tk.WORD, font=("Arial", 9))
        self.appearance_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Age and other quick details
        details_frame = ttk.Frame(basic_frame)
        details_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        ttk.Label(details_frame, text="Age:").grid(row=0, column=0, sticky="w", padx=5)
        self.age_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.age_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(details_frame, text="Gender:").grid(row=0, column=2, sticky="w", padx=5)
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(details_frame, textvariable=self.gender_var, width=12,
                                   values=["Male", "Female", "Non-binary", "Other", "Unspecified"])
        gender_combo.grid(row=0, column=3, padx=5)
        
        # Configure grid weights
        basic_frame.columnconfigure(1, weight=1)
        details_frame.columnconfigure(1, weight=1)
    
    def create_personality_section(self):
        """Create the personality section."""
        personality_frame = ttk.LabelFrame(self.scrollable_frame, text="🎭 Personality & Background")
        personality_frame.pack(fill="x", padx=10, pady=5)
        
        # Persona (1st person description)
        ttk.Label(personality_frame, text="Persona (1st person - 'I am...'):").grid(
            row=0, column=0, sticky="nw", padx=5, pady=5)
        self.persona_text = tk.Text(personality_frame, height=5, width=60, wrap=tk.WORD, font=("Arial", 9))
        self.persona_text.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Background
        ttk.Label(personality_frame, text="Background & History:").grid(
            row=1, column=0, sticky="nw", padx=5, pady=5)
        self.background_text = tk.Text(personality_frame, height=5, width=60, wrap=tk.WORD, font=("Arial", 9))
        self.background_text.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Current state
        state_frame = ttk.Frame(personality_frame)
        state_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        ttk.Label(state_frame, text="Current Mood:").grid(row=0, column=0, sticky="w", padx=5)
        self.mood_var = tk.StringVar()
        ttk.Entry(state_frame, textvariable=self.mood_var, width=25).grid(row=0, column=1, padx=5, sticky="ew")
        
        ttk.Label(state_frame, text="Emotional State:").grid(row=1, column=0, sticky="nw", padx=5, pady=2)
        self.emotional_state_text = tk.Text(state_frame, height=2, width=50, wrap=tk.WORD, font=("Arial", 9))
        self.emotional_state_text.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        # Configure grid weights
        personality_frame.columnconfigure(1, weight=1)
        state_frame.columnconfigure(1, weight=1)
    
    def create_knowledge_goals_section(self):
        """Create the knowledge and goals section."""
        knowledge_frame = ttk.LabelFrame(self.scrollable_frame, text="🧠 Knowledge & Goals")
        knowledge_frame.pack(fill="x", padx=10, pady=5)
        
        # Create two-column layout
        left_frame = ttk.Frame(knowledge_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        right_frame = ttk.Frame(knowledge_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Knowledge
        ttk.Label(left_frame, text="Knowledge (one item per line):").pack(anchor="w", pady=(0, 2))
        knowledge_help = ttk.Label(left_frame, text="What this NPC knows that players might find useful", 
                                  font=("Arial", 8), foreground="gray")
        knowledge_help.pack(anchor="w")
        
        self.knowledge_text = tk.Text(left_frame, height=8, width=40, wrap=tk.WORD, font=("Arial", 9))
        self.knowledge_text.pack(fill="both", expand=True, pady=2)
        
        # Goals
        ttk.Label(right_frame, text="Goals & Motivations (one per line):").pack(anchor="w", pady=(0, 2))
        goals_help = ttk.Label(right_frame, text="What drives this NPC, their objectives", 
                              font=("Arial", 8), foreground="gray")
        goals_help.pack(anchor="w")
        
        self.goals_text = tk.Text(right_frame, height=8, width=40, wrap=tk.WORD, font=("Arial", 9))
        self.goals_text.pack(fill="both", expand=True, pady=2)
        
        # Configure grid weights
        knowledge_frame.columnconfigure(0, weight=1)
        knowledge_frame.columnconfigure(1, weight=1)
        knowledge_frame.rowconfigure(0, weight=1)
    
    def create_traits_section(self):
        """Create the traits and quirks section."""
        traits_frame = ttk.LabelFrame(self.scrollable_frame, text="✨ Quirks & Fears")
        traits_frame.pack(fill="x", padx=10, pady=5)
        
        # Create two-column layout
        left_frame = ttk.Frame(traits_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        right_frame = ttk.Frame(traits_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Quirks
        ttk.Label(left_frame, text="Quirks & Habits (one per line):").pack(anchor="w", pady=(0, 2))
        quirks_help = ttk.Label(left_frame, text="Distinctive behaviors that make them unique", 
                               font=("Arial", 8), foreground="gray")
        quirks_help.pack(anchor="w")
        
        self.quirks_text = tk.Text(left_frame, height=6, width=40, wrap=tk.WORD, font=("Arial", 9))
        self.quirks_text.pack(fill="both", expand=True, pady=2)
        
        # Fears
        ttk.Label(right_frame, text="Fears & Concerns (one per line):").pack(anchor="w", pady=(0, 2))
        fears_help = ttk.Label(right_frame, text="What worries or frightens this NPC", 
                              font=("Arial", 8), foreground="gray")
        fears_help.pack(anchor="w")
        
        self.fears_text = tk.Text(right_frame, height=6, width=40, wrap=tk.WORD, font=("Arial", 9))
        self.fears_text.pack(fill="both", expand=True, pady=2)
        
        # Configure grid weights
        traits_frame.columnconfigure(0, weight=1)
        traits_frame.columnconfigure(1, weight=1)
        traits_frame.rowconfigure(0, weight=1)
    
    def create_relationships_section(self):
        """Create the relationships section."""
        relationships_frame = ttk.LabelFrame(self.scrollable_frame, text="👥 Relationships")
        relationships_frame.pack(fill="x", padx=10, pady=5)
        
        # Relationship helper
        help_text = ("Define how this NPC views other people/entities. Use JSON format:\n"
                    '{"player": "potential ally", "guards": "trusted colleagues", "merchants": "competitors"}')
        ttk.Label(relationships_frame, text=help_text, font=("Arial", 8), foreground="gray").pack(
            anchor="w", padx=5, pady=(5, 2))
        
        # Relationships text area
        self.relationships_text = tk.Text(relationships_frame, height=8, width=70, wrap=tk.WORD, font=("Consolas", 9))
        self.relationships_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Quick relationship buttons
        quick_frame = ttk.Frame(relationships_frame)
        quick_frame.pack(fill="x", padx=5, pady=2)
        
        ttk.Button(quick_frame, text="Add Player Relation", 
                  command=lambda: self.add_quick_relationship("player")).pack(side="left", padx=2)
        ttk.Button(quick_frame, text="Add Family Relation", 
                  command=lambda: self.add_quick_relationship("family")).pack(side="left", padx=2)
        ttk.Button(quick_frame, text="Format JSON", command=self.format_relationships_json).pack(side="right", padx=2)
    
    def create_game_settings_section(self):
        """Create the game settings section."""
        settings_frame = ttk.LabelFrame(self.scrollable_frame, text="⚙️ Game Settings")
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Location
        ttk.Label(settings_frame, text="Location Path:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        location_frame = ttk.Frame(settings_frame)
        location_frame.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=2)
        
        self.location_var = tk.StringVar()
        location_entry = ttk.Entry(location_frame, textvariable=self.location_var, width=40)
        location_entry.pack(side="left", fill="x", expand=True)
        
        ttk.Button(location_frame, text="Browse", command=self.browse_location).pack(side="right", padx=(5, 0))
        
        # Memory file
        ttk.Label(settings_frame, text="Memory File:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.memory_file_var = tk.StringVar()
        memory_entry = ttk.Entry(settings_frame, textvariable=self.memory_file_var, width=40)
        memory_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Button(settings_frame, text="Auto-Generate", 
                  command=self.auto_generate_memory_file).grid(row=1, column=2, padx=5, pady=2)
        
        # Following player checkbox
        self.following_var = tk.BooleanVar()
        ttk.Checkbutton(settings_frame, text="Following Player", 
                       variable=self.following_var).grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        
        # Configure grid weights
        settings_frame.columnconfigure(1, weight=1)
    
    def create_action_buttons(self):
        """Create the action buttons at the bottom."""
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.pack(fill="x", padx=10, pady=20)
        
        # Left side buttons
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side="left")
        
        ttk.Button(left_buttons, text="💾 Save", command=self.save_npc).pack(side="left", padx=5)
        ttk.Button(left_buttons, text="📁 Save As...", command=self.save_npc_as).pack(side="left", padx=5)
        ttk.Button(left_buttons, text="🔄 Reload", command=self.reload_npc).pack(side="left", padx=5)
        
        # Right side buttons
        right_buttons = ttk.Frame(button_frame)
        right_buttons.pack(side="right")
        
        ttk.Button(right_buttons, text="🧹 Clear All", command=self.clear_all).pack(side="right", padx=5)
        ttk.Button(right_buttons, text="✅ Validate", command=self.validate_npc).pack(side="right", padx=5)
        ttk.Button(right_buttons, text="🎲 Quick Fill", command=self.quick_fill).pack(side="right", padx=5)
    
    def load_defaults(self):
        """Load default values into the form."""
        self.relationships_text.insert('1.0', '''{\n  "player": "curious stranger to evaluate",\n  "townsfolk": "neighbors and community",\n  "authorities": "respected leaders"\n}''')
        self.memory_file_var.set("memory_npc.csv")
        self.location_var.set("world/town")
        self.mood_var.set("neutral")
        self.gender_var.set("Unspecified")
    
    def new_npc(self):
        """Create a new NPC."""
        if self.has_unsaved_changes():
            if not messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Continue anyway?"):
                return
        
        self.clear_all()
        self.current_npc_file = None
        self.file_label.config(text="New NPC")
        self.load_defaults()
    
    def open_npc(self):
        """Open an existing NPC file."""
        if self.has_unsaved_changes():
            if not messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Continue anyway?"):
                return
        
        file_path = filedialog.askopenfilename(
            title="Open NPC File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir="world_template"
        )
        
        if file_path:
            self.load_npc_file(file_path)
    
    def load_npc_file(self, file_path):
        """Load an NPC file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.npc_data = json.load(f)
            
            self.current_npc_file = file_path
            self.file_label.config(text=f"File: {os.path.basename(file_path)}")
            
            # Populate form fields
            self.name_var.set(self.npc_data.get('name', ''))
            self.occupation_var.set(self.npc_data.get('occupation', ''))
            self.age_var.set(self.npc_data.get('age', ''))
            self.gender_var.set(self.npc_data.get('gender', 'Unspecified'))
            
            # Text fields
            self.appearance_text.delete('1.0', tk.END)
            self.appearance_text.insert('1.0', self.npc_data.get('appearance', ''))
            
            self.persona_text.delete('1.0', tk.END)
            self.persona_text.insert('1.0', self.npc_data.get('persona', ''))
            
            self.background_text.delete('1.0', tk.END)
            self.background_text.insert('1.0', self.npc_data.get('background', ''))
            
            self.mood_var.set(self.npc_data.get('mood', ''))
            
            self.emotional_state_text.delete('1.0', tk.END)
            self.emotional_state_text.insert('1.0', self.npc_data.get('emotional_state', ''))
            
            # List fields
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
            
            # Game settings
            self.location_var.set(self.npc_data.get('location', ''))
            self.memory_file_var.set(self.npc_data.get('memory_file', ''))
            self.following_var.set(self.npc_data.get('following', False))
            
            messagebox.showinfo("Success", f"Loaded NPC: {self.npc_data.get('name', 'Unknown')}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load NPC file: {e}")
    
    def save_npc(self):
        """Save the current NPC."""
        if self.current_npc_file:
            self._save_to_file(self.current_npc_file)
        else:
            self.save_npc_as()
    
    def save_npc_as(self):
        """Save the NPC with a new filename."""
        npc_name = self.name_var.get().strip()
        if not npc_name:
            messagebox.showwarning("Warning", "Please enter an NPC name before saving.")
            return
        
        # Generate default filename
        safe_name = "".join(c for c in npc_name.lower() if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        default_filename = f"agent_{safe_name}.json"
        
        file_path = filedialog.asksaveasfilename(
            title="Save NPC As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir="world_template",
            initialfile=default_filename
        )
        
        if file_path:
            self._save_to_file(file_path)
    
    def _save_to_file(self, file_path):
        """Save NPC data to specified file."""
        try:
            # Collect data from form
            npc_data = {
                'name': self.name_var.get(),
                'persona': self.persona_text.get('1.0', tk.END).strip(),
                'background': self.background_text.get('1.0', tk.END).strip(),
                'appearance': self.appearance_text.get('1.0', tk.END).strip(),
                'occupation': self.occupation_var.get(),
                'mood': self.mood_var.get(),
                'emotional_state': self.emotional_state_text.get('1.0', tk.END).strip(),
                'location': self.location_var.get(),
                'memory_file': self.memory_file_var.get(),
                'following': self.following_var.get()
            }
            
            # Add optional fields
            if self.age_var.get():
                npc_data['age'] = self.age_var.get()
            
            if self.gender_var.get() != "Unspecified":
                npc_data['gender'] = self.gender_var.get()
            
            # Handle list fields
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
                except json.JSONDecodeError as e:
                    messagebox.showerror("JSON Error", f"Invalid JSON in relationships: {e}")
                    return
            else:
                npc_data['relationships'] = {}
            
            # Auto-generate memory file name if not provided
            if not npc_data['memory_file']:
                safe_name = "".join(c for c in npc_data['name'].lower() if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_name = safe_name.replace(' ', '_')
                npc_data['memory_file'] = f"memory_{safe_name}.csv"
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(npc_data, f, indent=2, ensure_ascii=False)
            
            # Create memory file if it doesn't exist
            memory_file_path = os.path.join(os.path.dirname(file_path), npc_data['memory_file'])
            if not os.path.exists(memory_file_path):
                with open(memory_file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['memory_type', 'key', 'value', 'timestamp'])
            
            self.current_npc_file = file_path
            self.file_label.config(text=f"File: {os.path.basename(file_path)}")
            self.npc_data = npc_data.copy()
            
            messagebox.showinfo("Success", f"NPC saved successfully to {os.path.basename(file_path)}!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save NPC: {e}")
    
    def reload_npc(self):
        """Reload the current NPC file."""
        if self.current_npc_file and os.path.exists(self.current_npc_file):
            if self.has_unsaved_changes():
                if not messagebox.askyesno("Reload", "You have unsaved changes. Reload anyway?"):
                    return
            self.load_npc_file(self.current_npc_file)
        else:
            messagebox.showwarning("Warning", "No file to reload.")
    
    def clear_all(self):
        """Clear all form fields."""
        self.name_var.set('')
        self.occupation_var.set('')
        self.age_var.set('')
        self.gender_var.set('Unspecified')
        
        text_widgets = [
            self.appearance_text, self.persona_text, self.background_text,
            self.emotional_state_text, self.knowledge_text, self.goals_text,
            self.quirks_text, self.fears_text, self.relationships_text
        ]
        
        for widget in text_widgets:
            widget.delete('1.0', tk.END)
        
        self.mood_var.set('')
        self.location_var.set('')
        self.memory_file_var.set('')
        self.following_var.set(False)
    
    def validate_npc(self):
        """Validate the current NPC data."""
        issues = []
        
        # Required fields
        if not self.name_var.get().strip():
            issues.append("Name is required")
        
        if not self.persona_text.get('1.0', tk.END).strip():
            issues.append("Persona is required")
        
        if not self.background_text.get('1.0', tk.END).strip():
            issues.append("Background is required")
        
        # Validate JSON relationships
        relationships_text = self.relationships_text.get('1.0', tk.END).strip()
        if relationships_text:
            try:
                json.loads(relationships_text)
            except json.JSONDecodeError:
                issues.append("Relationships JSON is invalid")
        
        # Check if location exists (if specified)
        location = self.location_var.get().strip()
        if location and location.startswith('world/'):
            # Convert world path to actual directory
            actual_path = location.replace('world/', 'world_template/', 1)
            if not os.path.exists(actual_path):
                issues.append(f"Location path does not exist: {actual_path}")
        
        if issues:
            issue_text = "\n• ".join([""] + issues)
            messagebox.showwarning("Validation Issues", f"Found {len(issues)} issues:{issue_text}")
        else:
            messagebox.showinfo("Validation Passed", "NPC data is valid! ✅")
    
    def has_unsaved_changes(self):
        """Check if there are unsaved changes."""
        if not self.current_npc_file:
            # New NPC - check if any fields are filled
            return (self.name_var.get().strip() or 
                   self.persona_text.get('1.0', tk.END).strip() or 
                   self.background_text.get('1.0', tk.END).strip())
        
        # Compare current data with saved data
        # This is a simplified check - in practice, you'd want to compare all fields
        return self.name_var.get() != self.npc_data.get('name', '')
    
    def generate_template(self):
        """Generate a template NPC based on chosen archetype."""
        archetype = simpledialog.askstring(
            "Choose Archetype", 
            "Enter NPC archetype (e.g., merchant, guard, sage, blacksmith, innkeeper):"
        )
        
        if not archetype:
            return
        
        templates = {
            "merchant": {
                "occupation": "traveling merchant",
                "persona": "I am a seasoned merchant who has traveled many roads and seen many wonders. I know the value of things both common and rare, and I take pride in fair dealing and quality goods.",
                "background": "I started as a humble trader's apprentice and worked my way up through determination and honest business practices.",
                "knowledge": ["Trade routes and market prices", "Identifying valuable items", "Current events from other towns"],
                "goals": ["Make an honest profit", "Build lasting customer relationships", "Discover new trading opportunities"],
                "quirks": ["Always weighs coins by feel", "Keeps detailed ledgers", "Never travels without protection"],
                "mood": "businesslike but friendly"
            },
            "guard": {
                "occupation": "town guard",
                "persona": "I am a dedicated guard sworn to protect this town and its people. I take my duty seriously and have little patience for troublemakers.",
                "background": "I joined the guard to serve my community and have worked my way up through the ranks through loyalty and competence.",
                "knowledge": ["Local laws and regulations", "Security protocols", "Suspicious activity patterns"],
                "goals": ["Maintain order and safety", "Protect innocent citizens", "Uphold the law fairly"],
                "quirks": ["Constantly scans for threats", "Keeps weapons well-maintained", "Speaks in clipped, official tones"],
                "mood": "alert and professional"
            },
            "sage": {
                "occupation": "scholar and advisor",
                "persona": "I am a keeper of knowledge and wisdom, dedicating my life to understanding the mysteries of our world and sharing that knowledge with those who seek it.",
                "background": "I have spent decades studying ancient texts and mysteries, accumulating vast knowledge through patient research and contemplation.",
                "knowledge": ["Ancient history and lore", "Magical theory and practice", "Philosophy and wisdom traditions"],
                "goals": ["Preserve knowledge for future generations", "Help seekers find wisdom", "Solve ancient mysteries"],
                "quirks": ["Quotes ancient texts", "Collects rare books", "Lost in thought frequently"],
                "mood": "contemplative and wise"
            }
        }
        
        template = templates.get(archetype.lower())
        if template:
            self.occupation_var.set(template["occupation"])
            self.persona_text.delete('1.0', tk.END)
            self.persona_text.insert('1.0', template["persona"])
            self.background_text.delete('1.0', tk.END)
            self.background_text.insert('1.0', template["background"])
            self.knowledge_text.delete('1.0', tk.END)
            self.knowledge_text.insert('1.0', '\n'.join(template["knowledge"]))
            self.goals_text.delete('1.0', tk.END)
            self.goals_text.insert('1.0', '\n'.join(template["goals"]))
            self.quirks_text.delete('1.0', tk.END)
            self.quirks_text.insert('1.0', '\n'.join(template["quirks"]))
            self.mood_var.set(template["mood"])
            messagebox.showinfo("Template Generated", f"Generated {archetype} template!")
        else:
            messagebox.showinfo("Custom Template", f"No built-in template for '{archetype}'. Please fill in manually.")
    
    def quick_fill(self):
        """Quick fill with random example data for testing."""
        import random
        
        names = ["Elena", "Marcus", "Thom", "Lyra", "Gareth", "Mira", "Dorian", "Sage"]
        occupations = ["blacksmith", "baker", "librarian", "guard", "merchant", "healer", "scout"]
        moods = ["cheerful", "serious", "cautious", "friendly", "grumpy", "wise", "energetic"]
        
        name = random.choice(names)
        occupation = random.choice(occupations)
        
        self.name_var.set(f"{name} the {occupation.title()}")
        self.occupation_var.set(occupation)
        self.mood_var.set(random.choice(moods))
        
        self.persona_text.delete('1.0', tk.END)
        self.persona_text.insert('1.0', f"I am {name}, a skilled {occupation} who takes pride in my work and serves the community.")
        
        self.background_text.delete('1.0', tk.END)
        self.background_text.insert('1.0', f"I learned the trade of {occupation} from my family and have been practicing for many years.")
        
        # Auto-generate memory file
        self.auto_generate_memory_file()
        
        messagebox.showinfo("Quick Fill", "Filled form with example data!")
    
    def load_template(self):
        """Load a template from another NPC file."""
        template_file = filedialog.askopenfilename(
            title="Load Template from NPC File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir="world_template"
        )
        
        if template_file:
            if messagebox.askyesno("Load Template", "This will overwrite current data. Continue?"):
                self.load_npc_file(template_file)
                # Clear the current file reference since this is just a template
                self.current_npc_file = None
                self.file_label.config(text="New NPC (from template)")
    
    def add_quick_relationship(self, rel_type):
        """Add a quick relationship entry."""
        current_text = self.relationships_text.get('1.0', tk.END).strip()
        
        try:
            if current_text:
                relationships = json.loads(current_text)
            else:
                relationships = {}
        except json.JSONDecodeError:
            relationships = {}
        
        if rel_type == "player":
            relationships["player"] = "curious stranger to evaluate"
        elif rel_type == "family":
            relationships["family"] = "beloved relatives"
        
        self.relationships_text.delete('1.0', tk.END)
        self.relationships_text.insert('1.0', json.dumps(relationships, indent=2))
    
    def format_relationships_json(self):
        """Format the relationships JSON for better readability."""
        try:
            current_text = self.relationships_text.get('1.0', tk.END).strip()
            if current_text:
                relationships = json.loads(current_text)
                formatted = json.dumps(relationships, indent=2)
                self.relationships_text.delete('1.0', tk.END)
                self.relationships_text.insert('1.0', formatted)
        except json.JSONDecodeError:
            messagebox.showerror("JSON Error", "Invalid JSON format. Cannot format.")
    
    def browse_location(self):
        """Browse for location directory."""
        location_dir = filedialog.askdirectory(
            title="Select NPC Location",
            initialdir="world_template"
        )
        
        if location_dir:
            # Convert to relative world path
            if "world_template" in location_dir:
                rel_path = location_dir.split("world_template")[1].lstrip(os.sep)
                world_path = f"world/{rel_path.replace(os.sep, '/')}" if rel_path else "world"
                self.location_var.set(world_path)
            else:
                self.location_var.set(location_dir)
    
    def auto_generate_memory_file(self):
        """Auto-generate memory file name based on NPC name."""
        npc_name = self.name_var.get().strip()
        if npc_name:
            safe_name = "".join(c for c in npc_name.lower() if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            self.memory_file_var.set(f"memory_{safe_name}.csv")


def main():
    root = tk.Tk()
    app = NPCEditorStandalone(root)
    
    # Check if an NPC file was passed as a command line argument
    if len(sys.argv) > 1:
        npc_file = sys.argv[1]
        if os.path.exists(npc_file):
            app.load_npc_file(npc_file)
        else:
            messagebox.showwarning("File Not Found", f"NPC file not found: {npc_file}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
