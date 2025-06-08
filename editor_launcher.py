#!/usr/bin/env python3
"""
Ollama-Dungeon Editor Launcher
Main launcher for the World Editor and NPC Editor tools
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from pathlib import Path

class EditorLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama-Dungeon Editor Suite")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Ollama-Dungeon Editor Suite",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Choose an editor to launch:",
            font=("Arial", 10)
        )
        desc_label.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)
        
        # World Editor button
        world_btn = ttk.Button(
            buttons_frame,
            text="🌍 World Editor",
            command=self.launch_world_editor,
            width=20
        )
        world_btn.pack(pady=5)
          # NPC Editor button
        npc_btn = ttk.Button(
            buttons_frame,
            text="👤 NPC Editor",
            command=self.launch_npc_editor,
            width=20
        )
        npc_btn.pack(pady=5)
          # Documentation button
        docs_btn = ttk.Button(
            buttons_frame,
            text="🌐 View Integration Guide",
            command=self.open_integration_guide,
            width=20
        )
        docs_btn.pack(pady=5)
          # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="About", padding="10")
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        info_text = """World Editor: Create and edit game worlds, rooms, and items
NPC Editor: Design and manage NPCs/Agents with personalities
Integration Guide: Learn how to use both editors together
        
Both editors work together - you can edit NPCs directly 
from the World Editor's interface. See the Integration Guide 
for detailed workflow examples and tips."""
        
        info_label = ttk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        info_label.pack()
        
        # Status frame
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready to launch editors",
            font=("Arial", 8),
            foreground="green"
        )
        self.status_label.pack()
    
    def launch_world_editor(self):
        """Launch the World Editor"""
        try:
            self.status_label.config(text="Launching World Editor...", foreground="blue")
            self.root.update()
            
            # Check if world_editor.py exists
            if not os.path.exists("world_editor.py"):
                messagebox.showerror(
                    "Error", 
                    "world_editor.py not found in current directory"
                )
                self.status_label.config(text="Error: world_editor.py not found", foreground="red")
                return
            
            # Launch the world editor
            subprocess.Popen([sys.executable, "world_editor.py"])
            self.status_label.config(text="World Editor launched", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch World Editor:\n{e}")
            self.status_label.config(text="Error launching World Editor", foreground="red")
    
    def launch_npc_editor(self):
        """Launch the NPC Editor"""
        try:
            self.status_label.config(text="Launching NPC Editor...", foreground="blue")
            self.root.update()
            
            # Check if npc_editor.py exists
            if not os.path.exists("npc_editor.py"):
                messagebox.showerror(
                    "Error", 
                    "npc_editor.py not found in current directory"
                )
                self.status_label.config(text="Error: npc_editor.py not found", foreground="red")
                return
              # Launch the NPC editor
            subprocess.Popen([sys.executable, "npc_editor.py"])
            self.status_label.config(text="NPC Editor launched", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch NPC Editor:\n{e}")
            self.status_label.config(text="Error launching NPC Editor", foreground="red")
    
    def open_integration_guide(self):
        """Open the Editor Integration Guide from GitHub"""
        guide_url = "https://github.com/cyberofficial/Ollama-Dungeon/blob/main/Guides/09-editor-integration.md"
        
        try:
            # Open the GitHub guide in the default web browser
            import webbrowser
            webbrowser.open(guide_url)
            self.status_label.config(text="Integration guide opened in browser", foreground="green")
            
        except Exception as e:
            # Fallback: show the URL to copy
            messagebox.showinfo(
                "Integration Guide",
                f"Please open the integration guide in your browser:\n\n{guide_url}"
            )
            self.status_label.config(text="Guide URL provided", foreground="green")

def main():
    """Main function"""
    root = tk.Tk()
    app = EditorLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
