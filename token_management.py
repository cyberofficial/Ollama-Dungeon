import json
import requests
import tiktoken
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging
from config import MODELS, TOKEN_SETTINGS, OLLAMA_BASE_URL
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TokenManager:
    """Manages token counting and context compression."""
    
    def __init__(self):
        # Use cl100k_base encoding (GPT-4 style) as approximation for token counting
        # This won't be 100% accurate for Qwen models but will be close enough
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except:
            # Fallback: rough approximation
            self.encoding = None
            logger.warning("tiktoken not available, using rough token estimation")
          # Initialize dynamic token limits for each agent
        self.agent_token_limits = {}  # agent_name -> current_token_limit
        
        # Track model state per agent to avoid unnecessary reloads
        self.model_states = {}  # (agent_name, model) -> {'num_ctx': int, 'last_used': datetime}
        self.agent_model_state = {}  # agent_name -> {'model': str, 'num_ctx': int, 'last_used': timestamp}
    
    def get_current_token_limit(self, agent_name: str) -> int:
        """Get the current token limit for an agent."""
        if agent_name not in self.agent_token_limits:
            self.agent_token_limits[agent_name] = TOKEN_SETTINGS['starting_tokens']
        return self.agent_token_limits[agent_name]
    
    def check_and_increase_token_limit(self, agent_name: str, current_tokens: int) -> Tuple[bool, int]:
        """
        Check if token limit should be increased and increase it if needed.
        Returns (was_increased, new_limit)
        """
        current_limit = self.get_current_token_limit(agent_name)
        threshold = int(current_limit * TOKEN_SETTINGS['token_increase_threshold'])
        
        if current_tokens >= threshold:
            # Calculate new limit
            old_limit = current_limit
            new_limit = current_limit + TOKEN_SETTINGS['increase_tokens_by']
            
            # Don't exceed compression threshold
            max_allowed = TOKEN_SETTINGS['compression_threshold']
            if new_limit > max_allowed:
                new_limit = max_allowed
              # Only increase if we actually can
            if new_limit > current_limit:
                self.agent_token_limits[agent_name] = new_limit
                
                # Only log if not suppressed
                if not TOKEN_SETTINGS.get('suppress_token_info', False):
                    logger.info(f"Increased token limit for {agent_name}: {current_limit} -> {new_limit}")
                
                # Record analytics
                token_analytics.record_token_expansion(agent_name, old_limit, new_limit)                
                return True, new_limit
        
        return False, current_limit
    
    def should_expand_tokens(self, agent_name: str, messages: List[Dict[str, str]]) -> Tuple[bool, str]:
        """
        Check if tokens should be expanded for an agent.
        Returns (should_expand, message_for_user)
        """
        current_tokens = self.count_message_tokens(messages)
        was_increased, new_limit = self.check_and_increase_token_limit(agent_name, current_tokens)
        
        if was_increased:
            # Only show message if not suppressed
            if not TOKEN_SETTINGS.get('suppress_token_info', False):
                return True, f"🔄 Increased token limit for {agent_name} to {new_limit} tokens to accommodate conversation length."
            else:
                return True, ""  # Expansion happened but message suppressed
        
        return False, ""
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self.encoding:
            return len(self.encoding.encode(text))
        else:
            # Rough approximation: ~4 characters per token
            return len(text) // 4
    
    def count_message_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count tokens in a list of messages."""
        total = 0
        for message in messages:            # Add some overhead for message structure
            total += self.count_tokens(message.get('content', '')) + 10
        return total
    
    def should_compress(self, messages: List[Dict[str, str]], agent_name: str = "default") -> bool:
        """Check if context should be compressed."""
        if not TOKEN_SETTINGS['enable_auto_compression']:
            return False
        
        token_count = self.count_message_tokens(messages)
        
        # First check if we can expand tokens instead of compressing
        was_expanded, _ = self.check_and_increase_token_limit(agent_name, token_count)
        if was_expanded:
            # We expanded, so don't compress yet
            return False
        
        # If we can't expand anymore, check if we should compress
        return token_count >= TOKEN_SETTINGS['compression_threshold']
    
    def compress_context(self, messages: List[Dict[str, str]], agent_name: str) -> List[Dict[str, str]]:
        """Compress context by summarizing older messages."""
        if len(messages) <= 2:  # Keep system prompt and at least one exchange
            return messages
        
        try:
            # Keep the system prompt (first message)
            system_prompt = messages[0] if messages and messages[0]['role'] == 'system' else None
            
            # Determine how many recent messages to keep based on urgency
            current_tokens = self.count_message_tokens(messages)
            if current_tokens >= TOKEN_SETTINGS.get('emergency_compression_threshold', 38000):
                # Emergency mode: Keep only last 3 messages
                recent_messages = messages[-3:]
                logger.warning(f"Emergency compression for {agent_name}: keeping only last 3 messages")
            else:
                # Normal mode: Keep last 5 messages
                recent_messages = messages[-5:]
            
            # Get messages to summarize (everything except system and recent)
            start_idx = 1 if system_prompt else 0
            end_idx = len(messages) - len(recent_messages)
            messages_to_summarize = messages[start_idx:end_idx] if end_idx > start_idx else []
            
            if not messages_to_summarize:
                return messages  # Nothing to compress
            
            # Create summary using the summary model
            summary = self._create_summary(messages_to_summarize, agent_name)
            
            # Build new context
            new_messages = []
            
            if system_prompt:
                new_messages.append(system_prompt)
            
            # Add summary as a system message
            new_messages.append({
                "role": "system",
                "content": f"[CONVERSATION SUMMARY] Previous interactions with {agent_name}: {summary}"
            })
              # Add recent messages
            new_messages.extend(recent_messages)
            
            compression_ratio = len(messages) / len(new_messages)
            # Only log compression if not suppressed
            if not TOKEN_SETTINGS.get('suppress_token_info', False):
                logger.info(f"Compressed context for {agent_name}: {len(messages)} -> {len(new_messages)} messages (ratio: {compression_ratio:.1f}x)")
            return new_messages
            
        except Exception as e:
            logger.error(f"Failed to compress context for {agent_name}: {e}")
            # Fallback: just keep recent messages based on urgency
            current_tokens = self.count_message_tokens(messages)
            if current_tokens >= TOKEN_SETTINGS.get('emergency_compression_threshold', 38000):
                return messages[-5:] if len(messages) > 5 else messages
            else:
                return messages[-10:] if len(messages) > 10 else messages
    
    def _create_summary(self, messages: List[Dict[str, str]], agent_name: str) -> str:
        """Create a summary of messages using the summary model."""
        try:
            # Prepare text for summarization
            conversation_text = ""
            for msg in messages:
                role = msg['role']
                content = msg['content']
                if role == 'user':
                    conversation_text += f"Player: {content}\n"
                elif role == 'assistant':
                    conversation_text += f"{agent_name}: {content}\n"
            
            # Create summarization prompt
            summary_prompt = f"""Please create a concise summary of this conversation between the player and {agent_name}. 
Focus on key events, decisions, and important information that should be remembered.

Conversation:
{conversation_text}

Summary (2-3 sentences):"""

            # Call Ollama with summary model
            response = requests.post(f'{OLLAMA_BASE_URL}/api/generate',
                json={
                    'model': MODELS['summary'],
                    'prompt': summary_prompt,
                    'stream': False,
                    'options': {
                        'num_ctx': 8000,  # Smaller context for summary model
                        'temperature': 0.3  # Lower temperature for more consistent summaries
                    }
                    })
            
            if response.status_code == 200:
                summary = response.json()['response'].strip()
                # Strip thinking tokens from summary
                from game_engine import strip_thinking_tokens
                summary = strip_thinking_tokens(summary)
                return summary
            else:
                logger.error(f"Summary API call failed: {response.status_code}")
                return f"Had a conversation with the player involving {len(messages)} exchanges."                
        except Exception as e:
            logger.error(f"Error creating summary: {e}")
            return f"Had a conversation with the player involving {len(messages)} exchanges."
            
    def should_reload_model(self, agent_name: str, model: str, num_ctx: int) -> bool:
        """Check if the model needs to be reloaded for this agent."""
        if agent_name not in self.agent_model_state:
            return True
        
        current_state = self.agent_model_state[agent_name]
        
        # Check if model changed
        if current_state['model'] != model:
            return True
        
        # Check if context size changed
        if current_state['num_ctx'] != num_ctx:
            # If reload_on_lower is False and new context size is smaller, don't reload
            if TOKEN_SETTINGS.get('reload_on_lower', False) == False and num_ctx < current_state['num_ctx']:
                return False
            return True
        
        return False
    
    def update_model_state(self, agent_name: str, model: str, num_ctx: int):
        """Update the tracked model state for an agent."""
        self.agent_model_state[agent_name] = {
            'model': model,
            'num_ctx': num_ctx,
            'last_used': datetime.now().isoformat()
        }
    
    def get_model_state_info(self, agent_name: str) -> str:
        """Get human-readable model state info for debugging."""
        if agent_name not in self.agent_model_state:
            return f"No model state tracked for {agent_name}"
        
        state = self.agent_model_state[agent_name]
        return f"Model: {state['model']}, Context: {state['num_ctx']}, Last used: {state['last_used']}"


class ContextManager:
    """Manages shared context between agents."""
    
    def __init__(self):
        self.shared_contexts: Dict[str, List[Dict[str, Any]]] = {}
        self.token_manager = TokenManager()
    
    def add_shared_context(self, location: str, context: str, source: str = "player"):
        """Add shared context for a location."""
        if location not in self.shared_contexts:
            self.shared_contexts[location] = []
        
        context_entry = {
            'content': context,
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'tokens': self.token_manager.count_tokens(context)
        }
        
        self.shared_contexts[location].append(context_entry)
        
        # Limit shared context to prevent token overflow
        self._trim_shared_context(location)
    
    def get_shared_context(self, location: str, max_tokens: int = 1000) -> str:
        """Get shared context for a location, limited by tokens."""
        if location not in self.shared_contexts:
            return ""
        
        contexts = self.shared_contexts[location]
        if not contexts:
            return ""
        
        # Get recent contexts within token limit
        result_contexts = []
        total_tokens = 0
        
        for context in reversed(contexts):  # Start with most recent
            if total_tokens + context['tokens'] > max_tokens:
                break
            result_contexts.insert(0, context)  # Insert at beginning to maintain order
            total_tokens += context['tokens']
        
        if not result_contexts:
            return ""
        
        # Format contexts
        formatted = []
        for ctx in result_contexts:
            source_info = f"({ctx['source']})" if ctx['source'] != 'player' else ""
            formatted.append(f"{ctx['content']} {source_info}")
        
        return " ".join(formatted)
    
    def _trim_shared_context(self, location: str):
        """Trim shared context to keep it manageable."""
        if location not in self.shared_contexts:
            return
        
        contexts = self.shared_contexts[location]
        
        # Keep only last 10 contexts
        if len(contexts) > 10:
            self.shared_contexts[location] = contexts[-10:]
    
    def get_context_stats(self, location: str) -> Dict[str, Any]:
        """Get statistics about shared context."""
        if location not in self.shared_contexts:
            return {'count': 0, 'total_tokens': 0}
        
        contexts = self.shared_contexts[location]
        total_tokens = sum(ctx['tokens'] for ctx in contexts)
        
        return {
            'count': len(contexts),
            'total_tokens': total_tokens,
            'recent_sources': [ctx['source'] for ctx in contexts[-3:]]
        }


class TokenAnalytics:
    """Track and analyze token usage over time for NPCs and system."""
    
    def __init__(self, analytics_file: str = "token_analytics.json"):
        self.analytics_file = analytics_file
        self.session_data = {}
        self.load_analytics()
    
    def _get_default_stats(self):
        """Get default stats dictionary."""
        return {
            'total_tokens_used': 0,
            'api_calls': 0,
            'expansions': 0,
            'compressions': 0,
            'peak_tokens': 0,
            'first_seen': None,
            'last_active': None,
            'conversation_turns': 0
        }
    
    def _ensure_agent_stats(self, agent_name: str):
        """Ensure agent has stats entry."""
        if agent_name not in self.session_data:
            self.session_data[agent_name] = self._get_default_stats()
    
    def load_analytics(self):
        """Load existing analytics data."""
        if os.path.exists(self.analytics_file):
            try:
                with open(self.analytics_file, 'r') as f:
                    self.session_data = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load token analytics: {e}")
    
    def save_analytics(self):
        """Save analytics data to file."""
        try:
            with open(self.analytics_file, 'w') as f:                json.dump(self.session_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save token analytics: {e}")
    
    def record_api_call(self, agent_name: str, tokens_used: int):
        """Record an API call with token usage."""
        self._ensure_agent_stats(agent_name)
        now = datetime.now().isoformat()
        stats = self.session_data[agent_name]
        
        stats['total_tokens_used'] += tokens_used
        stats['api_calls'] += 1
        stats['conversation_turns'] += 1
        stats['peak_tokens'] = max(stats['peak_tokens'], tokens_used)
        stats['last_active'] = now
        
        if not stats['first_seen']:
            stats['first_seen'] = now
        
        # Auto-save every 10 API calls to prevent data loss
        if stats['api_calls'] % 10 == 0:
            self.save_analytics()
    
    def record_token_expansion(self, agent_name: str, old_limit: int, new_limit: int):
        """Record a token limit expansion."""
        self._ensure_agent_stats(agent_name)
        self.session_data[agent_name]['expansions'] += 1
        
    def record_compression(self, agent_name: str, tokens_before: int, tokens_after: int):
        """Record a context compression."""
        self._ensure_agent_stats(agent_name)
        stats = self.session_data[agent_name]
        stats['compressions'] += 1
    
    def get_agent_analytics(self, agent_name: str) -> Dict[str, Any]:
        """Get analytics for a specific agent."""
        self._ensure_agent_stats(agent_name)
        stats = dict(self.session_data[agent_name])
        
        # Calculate derived metrics
        if stats['api_calls'] > 0:
            stats['avg_tokens_per_call'] = stats['total_tokens_used'] // stats['api_calls']
        else:
            stats['avg_tokens_per_call'] = 0
            
        return stats
    
    def get_top_token_users(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top token using agents."""
        agents = []
        for agent_name, stats in self.session_data.items():
            agents.append({
                'name': agent_name,
                'total_tokens': stats['total_tokens_used'],
                'api_calls': stats['api_calls'],
                'expansions': stats['expansions'],
                'compressions': stats['compressions']
            })
        
        return sorted(agents, key=lambda x: x['total_tokens'], reverse=True)[:limit]
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get system-wide token usage summary."""
        total_tokens = sum(stats['total_tokens_used'] for stats in self.session_data.values())
        total_calls = sum(stats['api_calls'] for stats in self.session_data.values())
        total_expansions = sum(stats['expansions'] for stats in self.session_data.values())
        total_compressions = sum(stats['compressions'] for stats in self.session_data.values())
        
        return {
            'total_agents_tracked': len(self.session_data),
            'total_tokens_used': total_tokens,
            'total_api_calls': total_calls,
            'total_expansions': total_expansions,
            'total_compressions': total_compressions,
            'avg_tokens_per_call': total_tokens // total_calls if total_calls > 0 else 0
        }


# Global instances
token_manager = TokenManager()
context_manager = ContextManager()
token_analytics = TokenAnalytics()


def estimate_tokens_remaining(current_tokens: int) -> int:
    """Estimate how many tokens are remaining before compression."""
    return max(0, TOKEN_SETTINGS['compression_threshold'] - current_tokens)


def get_token_usage_warning(current_tokens: int) -> Optional[str]:
    """Get a warning message if approaching token limits."""
    if not TOKEN_SETTINGS.get('show_token_warnings', True):
        return None
    
    threshold = TOKEN_SETTINGS['compression_threshold']
    max_tokens = TOKEN_SETTINGS['max_context_tokens']
    
    if current_tokens >= max_tokens * 0.95:
        return "⚠️ CRITICAL: Very close to token limit! Context will be heavily compressed."
    elif current_tokens >= threshold:
        return "⚠️ WARNING: Approaching token limit. Context compression will occur soon."
    elif current_tokens >= threshold * 0.8:
        return "ℹ️ INFO: Context is getting large. Consider using /compress command."
    
    return None


def monitor_token_usage_across_agents(agents_list) -> Dict[str, Any]:
    """Monitor token usage across multiple agents and return summary stats."""
    total_tokens = 0
    agent_stats = []
    high_usage_agents = []
    
    for agent in agents_list:
        tokens = token_manager.count_message_tokens(agent.context_messages)
        total_tokens += tokens
        
        status = "✅ Normal"
        if tokens > TOKEN_SETTINGS['compression_threshold']:
            status = "🔴 High"
            high_usage_agents.append(agent.data['name'])
        elif tokens > TOKEN_SETTINGS['compression_threshold'] * 0.8:
            status = "🟡 Medium"
        
        agent_stats.append({
            'name': agent.data['name'],
            'tokens': tokens,
            'status': status
        })
    
    return {
        'total_tokens': total_tokens,
        'agent_count': len(agents_list),
        'agent_stats': agent_stats,
        'high_usage_agents': high_usage_agents,
        'compression_needed': len(high_usage_agents) > 0
    }
