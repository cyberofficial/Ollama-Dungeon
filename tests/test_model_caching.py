#!/usr/bin/env python3
"""
Test script for model reload optimization
"""

def test_model_caching():
    """Test the model caching logic."""
    print("=== Testing Model Reload Optimization ===")
    print()
    
    from token_management import token_manager
    from config import TOKEN_SETTINGS
    
    agent_name = "test_agent"
    model = "qwen3:4b"
    
    # First call - should reload (new agent)
    should_reload1 = token_manager.should_reload_model(agent_name, model, 1000)
    print(f"1️⃣ First call (new agent): should_reload = {should_reload1}")
    
    # Update model state
    token_manager.update_model_state(agent_name, model, 1000)
    print(f"   Updated model state: {token_manager.get_model_state_info(agent_name)}")
    
    # Second call with same parameters - should NOT reload
    should_reload2 = token_manager.should_reload_model(agent_name, model, 1000)
    print(f"2️⃣ Same parameters: should_reload = {should_reload2}")
    
    # Third call with different context size - should reload
    should_reload3 = token_manager.should_reload_model(agent_name, model, 1100)
    print(f"3️⃣ Different context size (1100): should_reload = {should_reload3}")
    
    # Update with new context size
    token_manager.update_model_state(agent_name, model, 1100)
    print(f"   Updated model state: {token_manager.get_model_state_info(agent_name)}")
    
    # Fourth call with same new parameters - should NOT reload
    should_reload4 = token_manager.should_reload_model(agent_name, model, 1100)
    print(f"4️⃣ Same new parameters: should_reload = {should_reload4}")
    
    # Fifth call with different model - should reload
    should_reload5 = token_manager.should_reload_model(agent_name, "different_model", 1100)
    print(f"5️⃣ Different model: should_reload = {should_reload5}")
    
    # Test reload_on_lower functionality
    print("\n=== Testing reload_on_lower Functionality ===")
    
    # Reset with high token count
    agent_name = "high_token_agent"
    token_manager.update_model_state(agent_name, model, 5000)
    print(f"   Set up agent with 5000 tokens: {token_manager.get_model_state_info(agent_name)}")
    
    # With reload_on_lower = False (default), lower token count should NOT reload
    should_reload6 = token_manager.should_reload_model(agent_name, model, 3000)
    print(f"6️⃣ Lower token count with reload_on_lower=False: should_reload = {should_reload6}")
    
    # Temporarily change reload_on_lower setting to True
    original_setting = TOKEN_SETTINGS.get('reload_on_lower', False)
    TOKEN_SETTINGS['reload_on_lower'] = True
    
    # With reload_on_lower = True, lower token count should trigger reload
    should_reload7 = token_manager.should_reload_model(agent_name, model, 3000)
    print(f"7️⃣ Lower token count with reload_on_lower=True: should_reload = {should_reload7}")
    
    # Reset the setting
    TOKEN_SETTINGS['reload_on_lower'] = original_setting
    
    print()
    expected_results = [True, False, True, False, True, False, True]
    actual_results = [should_reload1, should_reload2, should_reload3, should_reload4, should_reload5, should_reload6, should_reload7]
    
    if expected_results == actual_results:
        print("✅ Model caching optimization working correctly!")
        print("   - New agents trigger model reload")
        print("   - Same parameters don't trigger reload")
        print("   - Different models trigger reload")
        print("   - Higher token counts always trigger reload")
        print("   - Lower token counts only trigger reload when reload_on_lower=True")
    else:
        print("❌ Model caching test failed!")
        print(f"   Expected: {expected_results}")
        print(f"   Actual:   {actual_results}")
    
    print()
    print("💡 Benefits:")
    print("   - Faster response times for repeated calls")
    print("   - Reduced GPU/CPU usage")
    print("   - Better resource utilization")
    print("   - Only reloads when actually needed")

if __name__ == "__main__":
    test_model_caching()
