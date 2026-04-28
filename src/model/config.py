import os
from typing import List, Dict

from pydantic import BaseModel, Field
from dotenv import load_dotenv

from src.model.tool import ToolName


load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

websearch_api_key = os.getenv("WEBSEARCH_API_KEY")

class LLMConfig(BaseModel):
    api_key: str = api_key
    base_url: str = base_url

class WebSearchConfig(BaseModel):
    api_key: str = websearch_api_key
    

class AgentConfig(BaseModel):
    name: str = Field(default="default")
    model_name: str = Field(default="glm-5")
    system_prompt: str = Field(default="")
    tools: List[ToolName] = Field(default=[])
    max_tokens: int = Field(default=8000)



class ConfigManager(BaseModel):
    llm: LLMConfig = Field(default_factory=LLMConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)