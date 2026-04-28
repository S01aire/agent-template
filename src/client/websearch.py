from tavily import TavilyClient

from src.model.config import WebSearchConfig
    
class WebSearcher:
    def __init__(self):
        config = WebSearchConfig()
        self.client = TavilyClient(api_key=config.api_key)