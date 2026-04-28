
from src.agent.base import BaseAgent
from src.cli.renderer import render_system

def handle_command(command: str, agent: BaseAgent) -> bool:
    if command == "/exit":
        render_system("再见。")
        return False
    
    render_system(f"未知命令：{command}")
    return True