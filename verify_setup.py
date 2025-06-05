#!/usr/bin/env python3
"""
Verification script to check all components of Ollama Dungeon
"""

import json
import os
import sys
import requests
from typing import Dict, Any

def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists and report status."""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_json_valid(filepath: str) -> bool:
    """Check if JSON file is valid."""
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        print(f"   ✅ Valid JSON format")
        return True
    except Exception as e:
        print(f"   ❌ Invalid JSON: {e}")
        return False

def check_ollama_connection() -> bool:
    """Check Ollama server connection."""
    try:
        response = requests.get('http://localhost:11434/api/version', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server: Connected")
            return True
        else:
            print(f"❌ Ollama server: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama server: {e}")
        return False

def check_models_available() -> Dict[str, bool]:
    """Check if required models are available."""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            available_models = [m['name'] for m in response.json().get('models', [])]
            
            required_models = ['qwen3:8b', 'qwen3:4b']
            results = {}
            
            for model in required_models:
                available = model in available_models
                status = "✅" if available else "❌"
                print(f"{status} Model {model}: {'Available' if available else 'Not found'}")
                results[model] = available
            
            return results
        else:
            print(f"❌ Model check failed: HTTP {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ Model check failed: {e}")
        return {}

def check_world_structure() -> bool:
    """Check world directory structure."""
    print("\n🌍 World Structure Check:")
    
    # Check for world_template (required) and world (optional, will be created from template)
    template_dirs = [
        "world_template",
        "world_template/town",
        "world_template/town/tavern",
        "world_template/town/market",
        "world_template/forest",
        "world_template/forest/cave"
    ]
    
    all_good = True
    print("Checking world template (required):")
    for directory in template_dirs:
        exists = os.path.exists(directory)
        status = "✅" if exists else "❌"
        print(f"{status} Directory: {directory}")
        if not exists:
            all_good = False
    
    # Check if world exists (optional)
    world_exists = os.path.exists("world")
    world_status = "✅" if world_exists else "ℹ️"
    world_note = "Exists" if world_exists else "Will be created from template"
    print(f"\nWorld directory status:")
    print(f"{world_status} world: {world_note}")
    
    return all_good

def check_configuration_files() -> bool:
    """Check configuration files."""
    print("\n⚙️ Configuration Files Check:")
    
    config_files = [
        ("config.py", "Main configuration"),
        ("token_management.py", "Token management"),
        ("game_engine.py", "Game engine"),
        ("cli.py", "Command line interface"),
        ("main.py", "Main entry point"),
        ("requirements.txt", "Python dependencies")
    ]
    
    all_good = True
    for filepath, description in config_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    return all_good

def check_world_files() -> bool:
    """Check world JSON files."""
    print("\n🗺️ World Files Check:")
    
    # Check template files (required)
    template_files = [
        ("world_template/town/room.json", "Town square room (template)"),
        ("world_template/town/tavern/room.json", "Tavern room (template)"),
        ("world_template/town/market/room.json", "Market room (template)"),
        ("world_template/forest/room.json", "Forest room (template)"),
        ("world_template/forest/cave/room.json", "Cave room (template)")
    ]
    
    all_good = True
    print("Checking template files (required):")
    for filepath, description in template_files:
        if check_file_exists(filepath, description):
            if not check_json_valid(filepath):
                all_good = False
        else:
            all_good = False
    
    # Check world files (optional, will be created from template)
    world_files = [
        ("world/town/room.json", "Town square room"),
        ("world/town/tavern/room.json", "Tavern room"),
        ("world/town/market/room.json", "Market room"),
        ("world/forest/room.json", "Forest room"),
        ("world/forest/cave/room.json", "Cave room")
    ]
    
    print("\nChecking world files (optional):")
    world_files_exist = True
    for filepath, description in world_files:
        exists = os.path.exists(filepath)
        status = "✅" if exists else "ℹ️"
        note = "Exists" if exists else "Will be created from template"
        print(f"{status} {description}: {note}")
        if exists and not check_json_valid(filepath):
            world_files_exist = False
    
    return all_good

def check_agents() -> bool:
    """Check agent files."""
    print("\n🤖 Agent Files Check:")
    
    # Check template agent files (required)
    template_agent_files = [
        ("world_template/town/tavern/agent_alice.json", "Alice (tavern keeper) - template"),
        ("world_template/town/tavern/agent_bob.json", "Bob (scout) - template"),
        ("world_template/forest/cave/agent_grix.json", "Grix (goblin scout) - template")
    ]
    
    all_good = True
    print("Checking template agent files (required):")
    for filepath, description in template_agent_files:
        if check_file_exists(filepath, description):
            if check_json_valid(filepath):
                # Check agent-specific structure
                try:
                    with open(filepath, 'r') as f:
                        agent_data = json.load(f)
                    
                    required_fields = ['name', 'persona', 'location', 'memory_file', 'mood']
                    missing_fields = [field for field in required_fields if field not in agent_data]
                    
                    if missing_fields:
                        print(f"   ❌ Missing fields: {', '.join(missing_fields)}")
                        all_good = False
                    else:
                        print(f"   ✅ Agent structure valid")
                except Exception as e:
                    print(f"   ❌ Error reading agent data: {e}")
                    all_good = False
            else:
                all_good = False
        else:
            all_good = False
    
    # Check world agent files (optional)
    world_agent_files = [
        ("world/town/tavern/agent_alice.json", "Alice (tavern keeper)"),
        ("world/town/tavern/agent_bob.json", "Bob (scout)"),
        ("world/forest/cave/agent_grix.json", "Grix (goblin scout)")
    ]
    
    print("\nChecking world agent files (optional):")
    for filepath, description in world_agent_files:
        exists = os.path.exists(filepath)
        status = "✅" if exists else "ℹ️"
        note = "Exists" if exists else "Will be created from template"
        print(f"{status} {description}: {note}")
    
    return all_good

def check_items() -> bool:
    """Check item files."""
    print("\n🎒 Item Files Check:")
    
    # Check template item files (required)
    template_item_files = [
        ("world_template/town/tavern/rusty_dagger.json", "Rusty dagger (template)"),
        ("world_template/town/market/health_potion.json", "Health potion (template)")
    ]
    
    all_good = True
    print("Checking template item files (required):")
    for filepath, description in template_item_files:
        if check_file_exists(filepath, description):
            if not check_json_valid(filepath):
                all_good = False
        else:
            all_good = False
    
    # Check world item files (optional)
    world_item_files = [
        ("world/town/tavern/rusty_dagger.json", "Rusty dagger"),
        ("world/town/market/health_potion.json", "Health potion")
    ]
    
    print("\nChecking world item files (optional):")
    for filepath, description in world_item_files:
        exists = os.path.exists(filepath)
        status = "✅" if exists else "ℹ️"
        note = "Exists" if exists else "Will be created from template"
        print(f"{status} {description}: {note}")
    
    return all_good

def main():
    """Main verification function."""
    print("🔍 Ollama Dungeon - System Verification")
    print("=" * 50)
    
    # Check Ollama connectivity
    print("\n🔌 Ollama Connection Check:")
    ollama_ok = check_ollama_connection()
    
    if ollama_ok:
        models_ok = check_models_available()
    else:
        models_ok = {}
    
    # Check file structure
    config_ok = check_configuration_files()
    world_structure_ok = check_world_structure()
    world_files_ok = check_world_files()
    agents_ok = check_agents()
    items_ok = check_items()
      # Summary
    print("\n" + "=" * 50)
    print("📋 Summary:")
    
    checks = [
        ("Ollama Connection", ollama_ok),
        ("Required Models", all(models_ok.values()) if models_ok else False),
        ("Configuration Files", config_ok),
        ("World Template Structure", world_structure_ok),
        ("World Template Files", world_files_ok),
        ("Template Agent Files", agents_ok),
        ("Template Item Files", items_ok)
    ]
    
    all_passed = True
    for check_name, status in checks:
        icon = "✅" if status else "❌"
        print(f"{icon} {check_name}")
        if not status:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Your Ollama Dungeon is ready to run.")
        print("\nTo start the game:")
        print("   python main.py")
    else:
        print("⚠️ Some issues found. Please fix them before running the game.")
        
        if not ollama_ok:
            print("\n💡 To fix Ollama issues:")
            print("   1. Start Ollama server: ollama serve")
            print("   2. Pull required models:")
            print("      ollama pull qwen3:8b")
            print("      ollama pull qwen3:4b")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
