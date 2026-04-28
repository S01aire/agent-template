"""
import subprocess
from pathlib import Path

from datetime import datetime
WORKDIR = Path.cwd()

def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=WORKDIR,
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
    
def get_current_time() -> str:
    return datetime.now().isoformat()
"""

import subprocess
from pathlib import Path

from src.model.tool import BaseTool
from src.tool.registry import register_tool


WORKDIR = Path.cwd()

@register_tool
class BashTool(BaseTool):
    name = "bash"
    description = "运行命令行"
    input_schema = {
        "type": "object", 
        "properties": {"command": {"type": "string"}}, 
        "required": ["command"]
    }

    def execute(self, command: str):
        dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
        if any(d in command for d in dangerous):
            return self.fail_response("Dangerous command blocked")
        try:
            r = subprocess.run(
                command,
                shell=True,
                cwd=WORKDIR,
                capture_output=True,
                text=True,
                timeout=120,
            )
            out = (r.stdout + r.stderr).strip()
            return self.success_response(out[:50000] if out else "(no output)")
        except subprocess.TimeoutExpired:
            return self.fail_response("Timeout (120s)")


