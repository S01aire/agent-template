from typing import List, Dict

from src.model.config import (
    AgentConfig
)
from src.model.tool import ToolName, ToolRegistry, ToolExecutor, ToolResult

from src.agent.client import LLMClient
from src.model.event import EventType, Event, make_await_human, make_final
from src.log.logging_config import setup_logger
from src.tool.registry import load_tools, TOOL_CLASSES

logger = setup_logger("agent_loop")

class BaseAgent:
    def __init__(self, config: AgentConfig, llm: LLMClient):
        self.name = config.name
        self.llm = llm
        self.model_name = config.model_name
        self.system_prompt = config.system_prompt
        self.tool_names:List[ToolName] = config.tools
        self.max_tokens=config.max_tokens

        self.registry = ToolRegistry()
        self.tool_executor = ToolExecutor(self.registry)
        self._init_tools()

        logger.info(f"创建agent:{self.name}")

    def _init_tools(self):
        load_tools()

        for tool_name in self.tool_names:
            tool_cls = TOOL_CLASSES.get(tool_name)
            if tool_cls is None:
                logger.error(f"工具未注册:{tool_name}")
                raise ValueError(f"工具未注册:{tool_name}")
            self.registry.register(tool_cls())



    def agent_loop(self, messages: list) -> Event:
        while True:
            response = self.llm.client.messages.create(
                model=self.model_name,
                system=self.system_prompt,
                messages=messages,
                tools=self.registry.to_dict([tool_name.value for tool_name in self.tool_names]),
                max_tokens=self.max_tokens,
            )
            
            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                texts = []
                for block in response.content:
                    if block.type == "text":
                        texts.append(block.text)

                final_anwser = "\n".join(texts) 
                event = make_final(answer=final_anwser)
                return event
            
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    logger.info(f"调用工具：{block.name}")

                    if block.name == "ask_human":
                        self._pending_messages = messages
                        event = make_await_human(
                            question=block.input["question"], 
                            tool_use_id=block.id,
                        )
                        return event

                    
                    try:
                        tool_result: ToolResult = self.tool_executor.execute(block.name, block.input)
                    except Exception as e:
                        raise RuntimeError(f"工具执行失败:{e}")
                    
                    if tool_result.ok:
                        output = tool_result.output
                    else:
                        output = tool_result.error

                    
                    logger.info(f"工具{block.name}调用结果：{output}")
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})
            messages.append({"role": "user", "content": results})

    def resume_with_human(self, tool_use_id: str, answer: str) -> Event:
        messages = self._pending_messages
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result", 
                "tool_use_id": tool_use_id, 
                "content": answer
            }]
        })
        self._pending_messages = None
        return self.agent_loop(messages)




        
