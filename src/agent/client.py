from typing import List, Dict

from anthropic import Anthropic

from src.model.config import (
    LLMConfig,
)


class LLMClient:
    def __init__(self, config: LLMConfig):
        self.client = Anthropic(api_key=config.api_key, base_url=config.base_url)

class ClientManager:
    _instance = None
    _llm_client: LLMClient

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClientManager, cls).__new__(cls)
        return cls._instance

    def init_client(self):
        _llm_config = LLMConfig()
        self._llm_client = LLMClient(_llm_config)

    def get_llm_client(self):
        return self._llm_client



        



