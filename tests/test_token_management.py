#!/usr/bin/env python3
"""
Token Management Tests for Ollama Dungeon
Tests token counting, context compression, memory management, and emergency scenarios.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from token_management import TokenManager, ContextManager, token_manager, context_manager
from token_management import estimate_tokens_remaining, get_token_usage_warning, monitor_token_usage_across_agents
from config import TOKEN_SETTINGS

class TestTokenManager(unittest.TestCase):
    """Test token management functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.token_manager = TokenManager()
    
    def test_token_counting_basic(self):
        """Test basic token counting functionality."""
        test_texts = [
            ("Hello world", 2),
            ("This is a longer sentence with more words.", 8),
            ("", 0),
            ("Single", 1)
        ]
        
        for text, expected_min in test_texts:
            tokens = self.token_manager.count_tokens(text)
            self.assertGreaterEqual(tokens, expected_min, f"Token count for '{text}' should be at least {expected_min}")
    
    def test_message_token_counting(self):
        """Test token counting for message lists."""
        messages = [
            {"role": "user", "content": "Hello there!"},
            {"role": "assistant", "content": "Hello! How can I help you today?"},
            {"role": "user", "content": "Tell me about the weather."}
        ]
        
        total_tokens = self.token_manager.count_message_tokens(messages)
        
        # Should be greater than 0 and reasonable
        self.assertGreater(total_tokens, 0)
        self.assertLess(total_tokens, 1000)  # Shouldn't be extremely high for short messages
        
        # Test empty messages
        empty_tokens = self.token_manager.count_message_tokens([])
        self.assertEqual(empty_tokens, 0)
    
    def test_compression_threshold_check(self):
        """Test compression threshold detection."""
        # Test with small message list (should not compress)
        small_messages = [
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Hello"}
        ]
        
        should_compress = self.token_manager.should_compress(small_messages)
        self.assertFalse(should_compress)
        
        # Test with large message list (should compress)
        large_messages = []
        for i in range(100):
            large_messages.append({"role": "user", "content": f"This is a very long message {i} " * 50})
            large_messages.append({"role": "assistant", "content": f"This is a very long response {i} " * 50})
        
        should_compress_large = self.token_manager.should_compress(large_messages)
        self.assertTrue(should_compress_large)
    
    @patch('requests.post')
    def test_context_compression(self, mock_post):
        """Test context compression functionality."""
        # Mock the API response for summarization
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {"content": "This is a summary of the previous conversation where the user and assistant discussed various topics."}
        }
        mock_post.return_value = mock_response
        
        # Create large message list
        large_messages = []
        for i in range(50):
            large_messages.append({"role": "user", "content": f"User message {i} with content " * 20})
            large_messages.append({"role": "assistant", "content": f"Assistant response {i} with content " * 20})
        
        # Test compression
        compressed = self.token_manager.compress_context(large_messages, "test_agent")
        
        # Should have fewer messages after compression
        self.assertLess(len(compressed), len(large_messages))
        
        # Should contain a summary message
        summary_found = any("summary" in msg.get("content", "").lower() for msg in compressed)
        self.assertTrue(summary_found)
    
    @patch('requests.post')
    def test_compression_failure_handling(self, mock_post):
        """Test handling of compression failures."""
        # Mock API failure
        mock_post.side_effect = Exception("API Error")
        
        messages = [
            {"role": "user", "content": "Test message"},
            {"role": "assistant", "content": "Test response"}
        ]
        
        # Should not raise exception, should return original or subset
        result = self.token_manager.compress_context(messages, "test_agent")
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 0)
    
    def test_compression_with_auto_disabled(self):
        """Test behavior when auto-compression is disabled."""
        # Temporarily disable auto-compression
        original_setting = TOKEN_SETTINGS['enable_auto_compression']
        TOKEN_SETTINGS['enable_auto_compression'] = False
        
        try:
            large_messages = []
            for i in range(100):
                large_messages.append({"role": "user", "content": f"Message {i} " * 50})
            
            should_compress = self.token_manager.should_compress(large_messages)
            self.assertFalse(should_compress)
        
        finally:
            TOKEN_SETTINGS['enable_auto_compression'] = original_setting
    
    def test_emergency_compression_scenario(self):
        """Test emergency compression when regular compression fails."""
        # Create extremely large message list
        huge_messages = []
        for i in range(200):
            huge_messages.append({"role": "user", "content": f"Huge message {i} " * 100})
            huge_messages.append({"role": "assistant", "content": f"Huge response {i} " * 100})
        
        token_count = self.token_manager.count_message_tokens(huge_messages)
        
        # Should exceed emergency threshold
        self.assertGreater(token_count, TOKEN_SETTINGS['emergency_compression_threshold'])


class TestContextManager(unittest.TestCase):
    """Test shared context management functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.context_manager = ContextManager()
    
    def test_add_shared_context(self):
        """Test adding shared context for locations."""
        location = "test_tavern"
        context = "The player entered looking worried."
        source = "player"
        
        self.context_manager.add_shared_context(location, context, source)
        
        # Check that context was added
        self.assertIn(location, self.context_manager.shared_contexts)
        self.assertEqual(len(self.context_manager.shared_contexts[location]), 1)
        
        # Check context entry details
        entry = self.context_manager.shared_contexts[location][0]
        self.assertEqual(entry['content'], context)
        self.assertEqual(entry['source'], source)
        self.assertIn('timestamp', entry)
        self.assertIn('tokens', entry)
        self.assertGreater(entry['tokens'], 0)
    
    def test_get_shared_context(self):
        """Test retrieving shared context."""
        location = "test_location"
        
        # Add multiple contexts
        contexts = [
            "Player entered the room",
            "Agent looked around nervously", 
            "A loud noise came from outside"
        ]
        
        for i, context in enumerate(contexts):
            self.context_manager.add_shared_context(location, context, f"source_{i}")
        
        # Get shared context
        shared = self.context_manager.get_shared_context(location)
        
        self.assertIsInstance(shared, str)
        self.assertGreater(len(shared), 0)
        
        # Should contain some of the added contexts
        found_contexts = sum(1 for ctx in contexts if ctx in shared)
        self.assertGreater(found_contexts, 0)
    
    def test_get_shared_context_with_token_limit(self):
        """Test shared context retrieval with token limits."""
        location = "test_location"
        
        # Add many large contexts
        for i in range(20):
            large_context = f"This is a very long context message {i} " * 50
            self.context_manager.add_shared_context(location, large_context, "test")
        
        # Get context with small token limit
        shared = self.context_manager.get_shared_context(location, max_tokens=100)
        
        # Should be limited
        token_count = self.context_manager.token_manager.count_tokens(shared)
        self.assertLessEqual(token_count, 200)  # Some tolerance for formatting
    
    def test_context_trimming(self):
        """Test automatic context trimming."""
        location = "test_location"
        
        # Add more than the limit (10)
        for i in range(15):
            self.context_manager.add_shared_context(location, f"Context {i}", "test")        
        # Should be trimmed to 10
        contexts = self.context_manager.shared_contexts[location]
        self.assertLessEqual(len(contexts), 10)
        
        # Should keep the most recent ones
        self.assertIn("Context 14", contexts[-1]['content'])
    
    def test_context_stats(self):
        """Test context statistics."""
        location = "test_location"
        
        # Add some contexts
        for i in range(5):
            self.context_manager.add_shared_context(location, f"Context {i}", f"source_{i}")
        
        stats = self.context_manager.get_context_stats(location)
        
        self.assertIn('count', stats)
        self.assertIn('total_tokens', stats)
        self.assertIn('recent_sources', stats)
        self.assertEqual(stats['count'], 5)
        self.assertGreater(stats['total_tokens'], 0)
        self.assertEqual(len(stats['recent_sources']), 3)  # Only last 3 sources
    
    def test_empty_location_context(self):
        """Test handling of empty location contexts."""
        empty_shared = self.context_manager.get_shared_context("nonexistent_location")
        self.assertEqual(empty_shared, "")
        
        empty_stats = self.context_manager.get_context_stats("nonexistent_location")
        self.assertEqual(empty_stats['count'], 0)
        self.assertEqual(empty_stats['total_tokens'], 0)


class TestTokenUtilities(unittest.TestCase):
    """Test token utility functions."""
    
    def test_estimate_tokens_remaining(self):
        """Test token remaining estimation."""
        current_tokens = 1000
        remaining = estimate_tokens_remaining(current_tokens)
        
        expected_remaining = TOKEN_SETTINGS['compression_threshold'] - current_tokens
        self.assertEqual(remaining, max(0, expected_remaining))
          # Test with tokens over threshold
        high_tokens = TOKEN_SETTINGS['compression_threshold'] + 1000
        remaining_high = estimate_tokens_remaining(high_tokens)
        self.assertEqual(remaining_high, 0)
    
    def test_token_usage_warnings(self):
        """Test token usage warning messages."""
        # Test no warning for low usage
        low_tokens = 1000
        warning = get_token_usage_warning(low_tokens)
        self.assertIsNone(warning)
        
        # Test warning for approaching threshold
        approaching_tokens = int(TOKEN_SETTINGS['compression_threshold'] * 0.8)
        warning = get_token_usage_warning(approaching_tokens)
        self.assertIsNotNone(warning)
        if warning:
            self.assertIn("large", warning.lower())
        
        # Test warning for at threshold
        threshold_tokens = TOKEN_SETTINGS['compression_threshold']
        warning = get_token_usage_warning(threshold_tokens)
        self.assertIsNotNone(warning)
        if warning:
            self.assertIn("compression", warning.lower())
        
        # Test critical warning
        critical_tokens = int(TOKEN_SETTINGS['max_context_tokens'] * 0.95)
        warning = get_token_usage_warning(critical_tokens)
        self.assertIsNotNone(warning)
        if warning:
            self.assertIn("critical", warning.lower())
    
    def test_token_warnings_disabled(self):
        """Test behavior when token warnings are disabled."""
        original_setting = TOKEN_SETTINGS.get('show_token_warnings', True)
        TOKEN_SETTINGS['show_token_warnings'] = False
        
        try:
            high_tokens = TOKEN_SETTINGS['compression_threshold'] * 2
            warning = get_token_usage_warning(high_tokens)
            self.assertIsNone(warning)
        
        finally:
            TOKEN_SETTINGS['show_token_warnings'] = original_setting
    
    def test_monitor_token_usage_across_agents(self):
        """Test monitoring token usage across multiple agents."""
        # Mock agents with different token usage
        mock_agents = []
        
        for i in range(3):
            agent = Mock()
            agent.context_messages = [
                {"role": "user", "content": f"Message {j} " * (10 * (i + 1))} 
                for j in range(10 * (i + 1))
            ]
            agent.data = {'name': f'Agent_{i}'}
            mock_agents.append(agent)
        
        # Mock token counting
        with patch.object(token_manager, 'count_message_tokens') as mock_count:
            # Return different token counts for different agents
            mock_count.side_effect = lambda msgs: len(msgs) * 50
            
            stats = monitor_token_usage_across_agents(mock_agents)
            
            self.assertIn('total_tokens', stats)
            self.assertIn('agent_count', stats)
            self.assertIn('agent_stats', stats)
            self.assertIn('high_usage_agents', stats)
            self.assertIn('compression_needed', stats)
            
            self.assertEqual(stats['agent_count'], 3)
            self.assertGreater(stats['total_tokens'], 0)


class TestTokenIntegration(unittest.TestCase):
    """Integration tests for token management systems."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.token_manager = TokenManager()
        self.context_manager = ContextManager()
    
    def test_full_token_lifecycle(self):
        """Test complete token management lifecycle."""
        # Simulate a conversation that grows over time
        messages = []
        location = "test_room"
        
        # Phase 1: Normal conversation
        for i in range(10):
            user_msg = f"User message {i} with some content"
            assistant_msg = f"Assistant response {i} with helpful information"
            
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
            
            # Add to shared context
            self.context_manager.add_shared_context(location, user_msg, "player")
        
        # Check initial state
        token_count = self.token_manager.count_message_tokens(messages)
        should_compress = self.token_manager.should_compress(messages)
        
        self.assertGreater(token_count, 0)
        # Should not need compression yet
        self.assertFalse(should_compress)
        
        # Phase 2: Conversation grows large
        for i in range(10, 100):
            long_msg = f"This is a much longer user message {i} " * 30
            long_response = f"This is a detailed assistant response {i} " * 30
            
            messages.append({"role": "user", "content": long_msg})
            messages.append({"role": "assistant", "content": long_response})
        
        # Should now need compression
        large_token_count = self.token_manager.count_message_tokens(messages)
        should_compress_now = self.token_manager.should_compress(messages)
        
        self.assertGreater(large_token_count, token_count)
        self.assertTrue(should_compress_now)
        
        # Phase 3: Test warning system
        warning = get_token_usage_warning(large_token_count)
        self.assertIsNotNone(warning)
        
        # Phase 4: Test shared context retrieval under load
        shared_context = self.context_manager.get_shared_context(location, max_tokens=500)
        shared_tokens = self.token_manager.count_tokens(shared_context)
        self.assertLessEqual(shared_tokens, 600)  # Some tolerance
    
    @patch('requests.post')
    def test_compression_under_load(self, mock_post):
        """Test compression behavior under high load."""
        # Mock summarization API
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {"content": "Summary of conversation covering multiple topics."}
        }
        mock_post.return_value = mock_response
        
        # Create very large conversation
        massive_messages = []
        for i in range(200):
            massive_messages.append({
                "role": "user", 
                "content": f"Extremely long user message {i} " * 100
            })
            massive_messages.append({
                "role": "assistant", 
                "content": f"Extremely long assistant response {i} " * 100
            })
        
        # Test compression
        original_count = len(massive_messages)
        compressed = self.token_manager.compress_context(massive_messages, "stress_test_agent")
        
        # Should be significantly reduced
        self.assertLess(len(compressed), original_count * 0.5)
        
        # Should still have some context
        self.assertGreater(len(compressed), 2)
        
        # Should have summary
        has_summary = any("summary" in msg.get("content", "").lower() for msg in compressed)
        self.assertTrue(has_summary)


if __name__ == '__main__':
    unittest.main()
