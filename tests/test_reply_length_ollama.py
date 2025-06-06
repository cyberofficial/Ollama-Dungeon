#!/usr/bin/env python3
"""
Test script to verify agent reply length configuration works with actual Ollama API calls.
This test creates temporary agents and tests their response lengths with real AI.
"""

import sys
import os
import json
import tempfile
import shutil
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import AGENT_SETTINGS, MODELS, OLLAMA_BASE_URL
from game_engine import Agent, WorldController

def check_ollama_available():
    """Check if Ollama is running and the model is available."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            model_names = [model['name'] for model in models.get('models', [])]
            if MODELS['main'] in model_names:
                return True, f"✅ Ollama is running and {MODELS['main']} is available"
            else:
                return False, f"❌ Model {MODELS['main']} not found. Available: {model_names}"
        else:
            return False, f"❌ Ollama API returned status {response.status_code}"
    except Exception as e:
        return False, f"❌ Cannot connect to Ollama: {e}"

def create_test_agent(name, reply_length, temp_dir):
    """Create a temporary agent file for testing."""
    agent_data = {
        "name": name,
        "persona": "A helpful test character",
        "mood": "friendly",
        "background": "You are a test character created to verify response lengths.",
        "appearance": "A friendly test character",
        "occupation": "Tester",
        "emotional_state": "Curious and helpful",
        "knowledge": ["Testing", "Conversations"],
        "goals": ["Help with testing", "Provide clear responses"],
        "fears": ["Confusing responses", "Technical failures"],
        "quirks": ["Always mentions being a test character"],
        "relationships": {},
        "location": temp_dir,
        "memory_file": f"memory_{name.lower()}.csv"
    }
    
    agent_file = os.path.join(temp_dir, f"{name.lower()}.json")
    with open(agent_file, 'w') as f:
        json.dump(agent_data, f, indent=2)
    
    return agent_file

def create_test_room(temp_dir):
    """Create a temporary room file for testing."""
    room_data = {
        "name": "Test Room",
        "description": "A simple test room for verifying agent responses.",
        "exits": {},
        "items": []
    }
    
    room_file = os.path.join(temp_dir, "room.json")
    with open(room_file, 'w') as f:
        json.dump(room_data, f, indent=2)
    
    return room_file

def count_sentences(text):
    """Count sentences in text (rough approximation)."""
    import re
    # Split by sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text.strip())
    # Filter out empty strings
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)

def test_reply_lengths_with_ollama():
    """Test different reply length settings with actual Ollama API calls."""
    
    print("🧪 Testing Agent Reply Lengths with Ollama API")
    print("=" * 60)
    
    # Check if Ollama is available
    ollama_ok, message = check_ollama_available()
    print(message)
    if not ollama_ok:
        print("\n❌ Cannot run test without Ollama. Please start Ollama and ensure the model is loaded.")
        return
    
    # Create temporary directory for test files
    temp_dir = tempfile.mkdtemp()
    print(f"📁 Using temporary directory: {temp_dir}")
    
    try:
        # Create test room
        room_file = create_test_room(temp_dir)
        
        # Test each reply length setting
        length_settings = ['brief', 'medium', 'detailed', 'verbose']
        test_prompt = "Hello! Can you tell me about yourself and what you like to do?"
        
        results = {}
        
        for length_setting in length_settings:
            print(f"\n🔧 Testing '{length_setting}' setting...")
            
            # Temporarily change the config
            original_setting = AGENT_SETTINGS.get('reply_length', 'medium')
            AGENT_SETTINGS['reply_length'] = length_setting
            
            try:
                # Create test agent
                agent_name = f"TestAgent_{length_setting.title()}"
                agent_file = create_test_agent(agent_name, length_setting, temp_dir)
                  # Create a minimal world controller
                class MockWorldController:
                    def __init__(self, location):
                        self.player_location = location
                    
                    def get_current_room(self):
                        return {
                            "name": "Test Room",
                            "description": "A simple test room for verifying agent responses.",
                            "exits": {}
                        }
                    
                    def get_agents_in_room(self):
                        return []
                    
                    def get_items_in_room(self):
                        return []
                
                world_controller = MockWorldController(temp_dir)
                
                agent = Agent(agent_file, world_controller)
                
                # Generate response
                print(f"   Asking: '{test_prompt}'")
                room_context = f"You are in a test room. The room is simple and designed for testing."
                
                response = agent.generate_response(test_prompt, room_context)
                sentence_count = count_sentences(response)
                word_count = len(response.split())
                
                results[length_setting] = {
                    'response': response,
                    'sentences': sentence_count,
                    'words': word_count
                }
                
                print(f"   📊 Response: {sentence_count} sentences, {word_count} words")
                print(f"   💬 Response: {response[:100]}{'...' if len(response) > 100 else ''}")
                
            except Exception as e:
                print(f"   ❌ Error testing {length_setting}: {e}")
                results[length_setting] = {'error': str(e)}
            
            finally:
                # Restore original setting
                AGENT_SETTINGS['reply_length'] = original_setting
        
        # Analyze results
        print(f"\n📈 Results Analysis:")
        print("=" * 40)
        
        for setting in length_settings:
            if setting in results and 'error' not in results[setting]:
                data = results[setting]
                print(f"{setting:8}: {data['sentences']:2} sentences, {data['words']:3} words")
            else:
                print(f"{setting:8}: ERROR")
        
        # Check if lengths are generally increasing
        valid_results = [(k, v) for k, v in results.items() if 'error' not in v]
        if len(valid_results) >= 2:
            print(f"\n✅ Length Progression Check:")
            for i, (setting, data) in enumerate(valid_results):
                if i > 0:
                    prev_setting, prev_data = valid_results[i-1]
                    if data['sentences'] >= prev_data['sentences']:
                        print(f"   ✅ {setting} ({data['sentences']}) >= {prev_setting} ({prev_data['sentences']})")
                    else:
                        print(f"   ⚠️  {setting} ({data['sentences']}) < {prev_setting} ({prev_data['sentences']}) - may vary due to AI randomness")
        
        print(f"\n🎯 Expected Ranges:")
        print(f"   brief:    1-2 sentences")
        print(f"   medium:   1-3 sentences")
        print(f"   detailed: 3-5 sentences")
        print(f"   verbose:  5+ sentences")
        
        print(f"\n📝 Full Responses:")
        print("=" * 40)
        for setting, data in results.items():
            if 'error' not in data:
                print(f"\n{setting.upper()}:")
                print(f"   {data['response']}")
        
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        print(f"\n🧹 Cleaned up temporary files")
    
    print(f"\n🎉 Ollama API test completed!")
    print(f"💡 Note: AI responses can vary due to randomness, but should generally follow length guidelines.")

if __name__ == "__main__":
    test_reply_lengths_with_ollama()
