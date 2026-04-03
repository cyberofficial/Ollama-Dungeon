"""
Network module with connection pooling for Ollama API.
Optimizes repeated API calls by reusing HTTP connections.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import OLLAMA_BASE_URL


class OllamaClient:
    """Singleton client with connection pooling for Ollama API."""
    
    _instance: 'OllamaClient | None' = None
    _session: 'requests.Session | None' = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._session = requests.Session()
            # Configure connection pooling
            adapter = HTTPAdapter(
                pool_connections=10,
                pool_maxsize=20,
                max_retries=Retry(total=3, backoff_factor=0.1)
            )
            cls._session.mount('http://', adapter)
            cls._session.mount('https://', adapter)
        return cls._instance
    
    @property
    def session(self):
        """Get the requests session."""
        return self._session
    
    def post(self, endpoint: str, **kwargs):
        """Make a POST request to Ollama API."""
        url = f"{OLLAMA_BASE_URL}{endpoint}"
        assert self._session is not None, "Session not initialized"
        return self._session.post(url, **kwargs)
    
    def get(self, endpoint: str, **kwargs):
        """Make a GET request to Ollama API."""
        url = f"{OLLAMA_BASE_URL}{endpoint}"
        assert self._session is not None, "Session not initialized"
        return self._session.get(url, **kwargs)
    
    def close(self):
        """Close the session."""
        if self._session:
            self._session.close()


# Global singleton instance
ollama_client = OllamaClient()