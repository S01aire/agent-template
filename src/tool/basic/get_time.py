

from datetime import datetime

from src.model.tool import BaseTool
from src.tool.registry import register_tool


@register_tool
class GetTimeTool(BaseTool):
    name = "get_time"
    description = "获取当前时间"
    input_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }

    def execute(self):
        current_time = datetime.now().isoformat()
        return self.success_response(current_time)