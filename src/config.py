import os
import json

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

class DocRegistry:
    def __init__(self):
        # Base hardcoded defaults
        self._docs = {
            "langchain": "https://docs.langchain.com",
            "llama-index": "https://docs.llamaindex.ai",
            "openai": "https://platform.openai.com/docs",
        }
        self._load_from_env()

    def _load_from_env(self):
        """
        Load extra docs from MCP_EXTRA_DOCS env var.
        Format: '{"name": "url", "name2": "url2"}'
        """
        extra = os.getenv("MCP_EXTRA_DOCS")
        if extra:
            try:
                self._docs.update(json.loads(extra))
            except json.JSONDecodeError:
                pass

    def register(self, name: str, url: str):
        self._docs[name.lower()] = url

    def get_url(self, name: str) -> str:
        return self._docs.get(name.lower())

    def list_supported(self):
        return list(self._docs.keys())

registry = DocRegistry()