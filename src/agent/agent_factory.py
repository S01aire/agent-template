

from src.agent.base import BaseAgent
from src.model.config import (
    LLMConfig,
    AgentConfig,
)
from src.agent.client import LLMClient
from src.model.tool import ToolName

def get_main_agent() -> BaseAgent:
    llm_config = LLMConfig()
    llm = LLMClient(llm_config)
    system_prompt = """
[ROLE]
该系统是为了给用户搜集信息，你是该系统的入口智能体，负责与用户沟通。

[TASK]
你需要明确和完善用户需求，使用 "ask_human" 工具向用户追问，但不要过于频繁地追问用户；
你可以将任务下发给其他子智能体，比如你可以将任务交给一个负责搜索网络的子智能体。

[CONSTRAINT]
不要编造信息。
"""
    tools = [ToolName.ask_human, ToolName.get_time, ToolName.task_create, ToolName.task_update, ToolName.task_get, ToolName.task_list, ToolName.web_search]
    agent_config = AgentConfig(system_prompt=system_prompt, tools=tools)
    agent = BaseAgent(agent_config, llm)

    return agent

def get_websearch_agent() -> BaseAgent:
    llm_config = LLMConfig()
    llm = LLMClient(llm_config)
    tools = [ToolName.web_search, ToolName.get_time]
    agent_config = AgentConfig(tools=tools)
    agent = BaseAgent(agent_config, llm)

    return agent