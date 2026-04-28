"""
from tavily import TavilyClient

from src.models.config import WebSearchConfig
from src.log.logging_config import setup_logger
    
class WebSearcher:
    def __init__(self):
        config = WebSearchConfig()
        self.client = TavilyClient(api_key=config.api_key)

def run_websearch(query: str):
    logger = setup_logger("websearch")
    websearcher = WebSearcher()
    try:
        response = websearcher.client.search(query=query, max_results=5)
        return response
    except Exception as e:
        logger.error(f"网络搜索失败:{e}")
        return "网络搜索失败"
"""

from src.model.tool import BaseTool
from src.client.websearch import WebSearcher
from src.tool.registry import register_tool


@register_tool
class WebSearchTool(BaseTool):
    name = "web_search"
    description = "搜索互联网信息"
    input_schema = {
        "type": "object",
        "properties": {"query": {"type": "string", "description": "需要搜索的信息"}},
        "required": ["query"]
    }

    def execute(self, query: str):
        try: 
            web_searcher = WebSearcher()
            response = web_searcher.client.search(query=query, max_results=5)
            return self.success_response(response)
        except Exception as e:
            return self.fail_response(e)
