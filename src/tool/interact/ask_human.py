
from src.model.tool import BaseTool
from src.tool.registry import register_tool

@register_tool
class AskHumanTool(BaseTool):
    name = "ask_human"
    description = "向用户追问澄清需求"
    input_schema = {
        "type": "object",
        "properties": {"question": {"type": "string"}},
        "required": ["question"],
    }

    def execute(self, question: str):
        #仅用于补全形式
        return self.success_response({"question": question})