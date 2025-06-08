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
    """Check if recommended models are available (informational only)."""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            available_models = [m['name'] for m in response.json().get('models', [])]
            
            recommended_models = ['qwen3:8b', 'qwen3:4b']
            results = {}
            
            print("Recommended models (you can use any compatible models):")
            for model in recommended_models:
                available = model in available_models
                status = "✅" if available else "ℹ️"
                print(f"{status} Model {model}: {'Available' if available else 'Not installed (optional)'}")
                results[model] = available
            
            # Check if any recommended models are missing
            missing_recommended = [model for model, available in results.items() if not available]
            
            if missing_recommended:
                print(f"\nℹ️ Some recommended models not found. Are you using different models?")
                print("   You can use any compatible Ollama model for this game.")
                
                # Privacy-respecting model scan option
                try:
                    user_input = input("\n   Would you like to check available models? (y/N): ").strip().lower()
                    if user_input in ['y', 'yes']:
                        if available_models:
                            print(f"\n   ✅ {len(available_models)} model(s) found and available for use.")
                        else:
                            print("\n   ℹ️ No models found. Install models with: ollama pull <model_name>")
                    else:
                        print("   ℹ️ Skipping model scan (privacy respected).")
                except (EOFError, KeyboardInterrupt):
                    print("   ℹ️ Skipping model scan.")
            else:
                # Show count only if all recommended models are available
                if available_models:
                    print(f"\n   ✅ {len(available_models)} total model(s) available.")
            
            return results
        else:
            print(f"ℹ️ Model check failed: HTTP {response.status_code}")
            return {}
    except Exception as e:
        print(f"ℹ️ Model check failed: {e}")
        return {}

def check_world_structure() -> bool:
    """Check world directory structure."""
    print("\n🌍 World Structure Check:")
    
    # Check for world_template (required) and world (optional, will be created from template)
    template_dirs = [
        "world_template",
        "world_template/crystal_caves",
        "world_template/crystal_caves/mining_tunnels",
        "world_template/sky_gardens",
        "world_template/sky_gardens/meditation_grove",
        "world_template/sunspire_city",
        "world_template/sunspire_city/merchant_quarter",
        "world_template/sunspire_city/scholar_district",
        "world_template/whispering_dunes",
        "world_template/whispering_dunes/ancient_ruins",
        "world_template/whispering_dunes/nomad_camp"
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
        ("npc_editor.py", "NPC editor"),
        ("world_editor.py", "World editor"),
        ("editor_launcher.py", "Editor launcher"),
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
        ("world_template/crystal_caves/room.json", "Crystal Caves room (template)"),
        ("world_template/crystal_caves/mining_tunnels/room.json", "Mining Tunnels room (template)"),
        ("world_template/sky_gardens/room.json", "Sky Gardens room (template)"),
        ("world_template/sky_gardens/meditation_grove/room.json", "Meditation Grove room (template)"),
        ("world_template/sunspire_city/room.json", "Sunspire City room (template)"),
        ("world_template/sunspire_city/merchant_quarter/room.json", "Merchant Quarter room (template)"),
        ("world_template/sunspire_city/scholar_district/room.json", "Scholar District room (template)"),
        ("world_template/whispering_dunes/room.json", "Whispering Dunes room (template)"),
        ("world_template/whispering_dunes/ancient_ruins/room.json", "Ancient Ruins room (template)"),
        ("world_template/whispering_dunes/nomad_camp/room.json", "Nomad Camp room (template)")
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
        ("world/crystal_caves/room.json", "Crystal Caves room"),
        ("world/crystal_caves/mining_tunnels/room.json", "Mining Tunnels room"),
        ("world/sky_gardens/room.json", "Sky Gardens room"),
        ("world/sky_gardens/meditation_grove/room.json", "Meditation Grove room"),
        ("world/sunspire_city/room.json", "Sunspire City room"),
        ("world/sunspire_city/merchant_quarter/room.json", "Merchant Quarter room"),
        ("world/sunspire_city/scholar_district/room.json", "Scholar District room"),
        ("world/whispering_dunes/room.json", "Whispering Dunes room"),
        ("world/whispering_dunes/ancient_ruins/room.json", "Ancient Ruins room"),
        ("world/whispering_dunes/nomad_camp/room.json", "Nomad Camp room")
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
        ("world_template/crystal_caves/mining_tunnels/agent_kael.json", "Kael (miner) - template"),
        ("world_template/sky_gardens/meditation_grove/agent_lyra.json", "Lyra (druid) - template"),
        ("world_template/sunspire_city/merchant_quarter/agent_zahra.json", "Zahra (merchant) - template"),
        ("world_template/sunspire_city/scholar_district/agent_qasim.json", "Qasim (scholar) - template")
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
        ("world/crystal_caves/mining_tunnels/agent_kael.json", "Kael (miner)"),
        ("world/sky_gardens/meditation_grove/agent_lyra.json", "Lyra (druid)"),
        ("world/sunspire_city/merchant_quarter/agent_zahra.json", "Zahra (merchant)"),
        ("world/sunspire_city/scholar_district/agent_qasim.json", "Qasim (scholar)")
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
        ("world_template/crystal_caves/mining_tunnels/crystal_pickaxe.json", "Crystal Pickaxe (template)"),
        ("world_template/sky_gardens/meditation_grove/celestial_dew.json", "Celestial Dew (template)"),
        ("world_template/sunspire_city/merchant_quarter/sunfire_crystal.json", "Sunfire Crystal (template)"),
        ("world_template/sunspire_city/scholar_district/scroll_desert_navigation.json", "Desert Navigation Scroll (template)")
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
        ("world/crystal_caves/mining_tunnels/crystal_pickaxe.json", "Crystal Pickaxe"),
        ("world/sky_gardens/meditation_grove/celestial_dew.json", "Celestial Dew"),
        ("world/sunspire_city/merchant_quarter/sunfire_crystal.json", "Sunfire Crystal"),
        ("world/sunspire_city/scholar_district/scroll_desert_navigation.json", "Desert Navigation Scroll")
    ]
    
    print("\nChecking world item files (optional):")
    for filepath, description in world_item_files:
        exists = os.path.exists(filepath)
        status = "✅" if exists else "ℹ️"
        note = "Exists" if exists else "Will be created from template"
        print(f"{status} {description}: {note}")
    
    return all_good

def check_memory_files() -> bool:
    """Check memory files for agents."""
    print("\n🧠 Memory Files Check:")
    
    # Check template memory files (required)
    template_memory_files = [
        ("world_template/crystal_caves/mining_tunnels/memory_kael.csv", "Kael's memory (template)"),
        ("world_template/sky_gardens/meditation_grove/memory_lyra.csv", "Lyra's memory (template)"),
        ("world_template/sunspire_city/merchant_quarter/memory_zahra.csv", "Zahra's memory (template)"),
        ("world_template/sunspire_city/scholar_district/memory_qasim.csv", "Qasim's memory (template)")
    ]
    
    all_good = True
    print("Checking template memory files (required):")
    for filepath, description in template_memory_files:
        if check_file_exists(filepath, description):            # Check if it's a valid CSV (basic check)
            try:
                with open(filepath, 'r') as f:
                    content = f.read().strip()
                    # For template files, they might be empty or have minimal content
                    if not content:
                        print(f"   ✅ Empty template memory file (will be populated during gameplay)")
                    elif 'timestamp' in content.lower() or 'memory' in content.lower() or content.count(',') > 0:
                        print(f"   ✅ Valid memory file format")
                    else:
                        print(f"   ✅ Template memory file ready")
            except Exception as e:
                print(f"   ❌ Error reading memory file: {e}")
                all_good = False
        else:
            all_good = False
    
    # Check world memory files (optional)
    world_memory_files = [
        ("world/crystal_caves/mining_tunnels/memory_kael.csv", "Kael's memory"),
        ("world/sky_gardens/meditation_grove/memory_lyra.csv", "Lyra's memory"),
        ("world/sunspire_city/merchant_quarter/memory_zahra.csv", "Zahra's memory"),
        ("world/sunspire_city/scholar_district/memory_qasim.csv", "Qasim's memory")
    ]
    
    print("\nChecking world memory files (optional):")
    for filepath, description in world_memory_files:
        exists = os.path.exists(filepath)
        status = "✅" if exists else "ℹ️"
        note = "Exists" if exists else "Will be created from template"
        print(f"{status} {description}: {note}")
    
    return all_good

def check_additional_directories() -> bool:
    """Check additional project directories."""
    print("\n📁 Additional Directories Check:")
    
    directories = [
        ("Guides", "Game guides and documentation", True),
        ("saves", "Save files directory", False),
        ("tests", "Test files directory", True)
    ]
    
    all_good = True
    for dir_path, description, required in directories:
        exists = os.path.exists(dir_path)
        if required:
            status = "✅" if exists else "❌"
            if not exists:
                all_good = False
        else:
            status = "✅" if exists else "ℹ️"
        
        note = "Exists" if exists else ("Required" if required else "Optional")
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
    additional_dirs_ok = check_additional_directories()
    world_structure_ok = check_world_structure()
    world_files_ok = check_world_files()
    agents_ok = check_agents()
    memory_files_ok = check_memory_files()
    items_ok = check_items()
      # Summary
    print("\n" + "=" * 50)
    print("📋 Summary:")
    
    checks = [
        ("Ollama Connection", ollama_ok),
        ("Configuration Files", config_ok),
        ("World Template Structure", world_structure_ok),
        ("World Template Files", world_files_ok),
        ("Template Agent Files", agents_ok),
        ("Template Item Files", items_ok),
        ("Agent Memory Files", memory_files_ok),
        ("Additional Directories", additional_dirs_ok)    ]
    
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
          # Show model information if available
        if models_ok:
            available_recommended = sum(1 for available in models_ok.values() if available)
            total_recommended = len(models_ok)
            if available_recommended > 0:
                print(f"\nℹ️ Recommended models available: {available_recommended}/{total_recommended}")
            else:
                print("\nℹ️ No recommended models found, but you can use any compatible Ollama model.")
                print("   Popular options: llama3, mistral, codellama, or any other model you prefer.")
    else:
        print("⚠️ Some issues found. Please fix them before running the game.")
        
        if not ollama_ok:
            print("\n💡 To fix Ollama issues:")
            print("   1. Start Ollama server: ollama serve")
            print("   2. Install any compatible model, for example:")
            print("      ollama pull llama3")
            print("      ollama pull qwen3:8b  # (optional, recommended)")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
