from enum import Enum
from typing import List, Dict, Any, Optional, Union, ClassVar
from abc import ABC, abstractmethod
import json

from pydantic import BaseModel, Field, ConfigDict

from src.log.logging_config import setup_logger


logger = setup_logger("tool")

class ToolName(str, Enum):
    bash = "bash"
    web_search = "web_search"
    get_time = "get_time"
    ask_human = "ask_human"
    gen_requirement = "gen_requirement"
    task_create = "task_create"
    task_update = "task_update"
    task_get = "task_get"
    task_list = "task_list"



class ToolResult(BaseModel):
    ok: bool
    output: Any = Field(default=None)
    error: Optional[Any] = None


class BaseTool(ABC, BaseModel):
    name: ClassVar[str]
    description: ClassVar[str]
    input_schema: ClassVar[Optional[dict]] = None

    def __call__(self, **kwargs) -> Any:
        return self.execute(**kwargs)
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """
        使用给定参数执行工具
        """

    def to_dict(self) -> Dict:
        """
        将工具转换为可以用于anthropic函数调用的形式
        """

        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }
    
    def success_response(self, data: Union[Dict[str, Any], str]) -> ToolResult:
        if isinstance(data, str):
            text = data
        else:
            text = json.dumps(data, indent=2)

        logger.info(f"工具{self.__class__.__name__}调用成功")
        return ToolResult(ok=True, output=text)
    
    def fail_response(self, msg: str) -> ToolResult:
        logger.error(f"工具{self.__class__.__name__}调用失败: {msg}")
        return ToolResult(ok=False, error=msg)
    


class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self.tools:
            logger.error(f"未知工具: {name}")
        return self.tools[name]
    
    def get_toollist(self, names: List[str]):
        return [self.tools[name] for name in names]
    
    def to_dict(self, names: List[str]) -> List[dict]:
        return [self.tools[name].to_dict() for name in names]


class ToolExecutor:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, tool_name: str, args: dict) -> ToolResult:
        tool = self.registry.get(tool_name)
        return tool.execute(**args)
        










