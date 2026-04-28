from pathlib import Path
import json
from typing import List, Dict

from src.model.task import TaskStatus, Task

from src.log.logging_config import setup_logger


logger = setup_logger("task_tool")

class TaskManager:
    def __init__(self, tasks_dir: Path=Path("src/message_box/tasks/")):
        self.dir = tasks_dir
        self.dir.mkdir(exist_ok=True)
        self._next_id = self._max_id() + 1

    def _max_id(self) -> int:
        ids = [int(f.stem.split("_")[1]) for f in self.dir.glob("task_*.json")]
        return max(ids) if ids else 0
    
    def _load(self, task_id: int) -> Task:
        path = self.dir / f"task_{task_id}.json"
        if not path.exists():
            logger.error(f"Task {task_id} 没有找到")
        return Task.model_validate_json(path.read_text(encoding="utf-8"))
    
    def _save(self, task: Task):
        path = self.dir / f"task_{task.id}.json"
        path.write_text(task.model_dump_json(indent=2, ensure_ascii=False), encoding="utf-8")

    def create(self, subject: str, description: str = "") -> str:
        task = Task(
            id=self._next_id,
            subject=subject,
            description=description,
            status=TaskStatus.pending,
            blocked_by=[],
            owner="",
        )
        self._save(task)
        self._next_id += 1
        return task.model_dump_json(indent=2, ensure_ascii=False)
    
    def get(self, task_id: int) -> str:
        return self._load(task_id).model_dump_json(indent=2, ensure_ascii=False)
    
    def update(
            self,
            task_id: int,
            status: TaskStatus,
            add_blocked_by: list = None,
            remove_blocked_by: list = None
    ) -> str:
        task = self._load(task_id)

        if status:
            task.status = status
            if status == TaskStatus.completed:
                self._clear_dependency(task_id)

        if add_blocked_by:
            task.blocked_by = list(set(task.blocked_by + add_blocked_by))

        if remove_blocked_by:
            task.blocked_by = [x for x in task.blocked_by if x not in remove_blocked_by]

        self._save(task)

        return task.model_dump_json(indent=2, ensure_ascii=False)
    
    def _clear_dependency(self, completed_id: int):
        for f in self.dir.glob("task_*.json"):
            task: Task = Task.model_validate_json(f.read_text(encoding="utf-8"))
            if completed_id in task.blocked_by:
                task.blocked_by.remove(completed_id)
                self._save(task)

    def list_all(self) -> str:
        tasks: List[Task] = []

        files = sorted(
            self.dir.glob("task_*.json"),
            key=lambda f: int(f.stem.split("_")[1])
        )

        for f in files:
            tasks.append(Task.model_validate_json(f.read_text()))
        if not tasks:
            return "没有任务"
        
        lines = []
        for t in tasks:
            marker = {"pending": "[ ]", "in_progress": "[>]", "completed": "[x]"}.get(t.status, "[?]")
            blocked = f"(blocked by: {t.blocked_by})" if t.blocked_by else ""
            lines.append(f"{marker} #{t.id}: {t.subject} {blocked}")
            
        return "\n".join(lines)
    


from src.model.tool import BaseTool
from src.tool.registry import register_tool

task_manager = TaskManager()

@register_tool
class TaskCreateTool(BaseTool):
    name = "task_create"
    description = "创建一个新任务"
    input_schema = {
        "type": "object",
        "properties":{
            "subject": {"type": "string"},
            "description": {"type": "string"}
        },
        "required": ["subject"]
    }

    def execute(self, subject: str, description: str = ""):
        try:
            output = task_manager.create(subject, description)
            return self.success_response(output)
        except Exception as e:
            return self.fail_response(f"subject: {subject} 任务创建失败: {e}")
        
@register_tool
class TaskUpdateTool(BaseTool):
    name = "task_update"
    description = "更新一个任务的状态或依赖"
    input_schema = {
        "type": "object",
        "properties":{
            "task_id": {"type": "integer"},
            "status": {"type": "string", "enum": ["pending", "in_progress", "completed"]},
            "addBlockedBy": {"type": "array", "items": {"type": "integer"}}, 
            "removeBlockedBy": {"type": "array", "items": {"type": "integer"}}
        },
        "required": ["task_id"]
    }

    def execute(
            self, 
            task_id: int, 
            status: str = None, 
            addBlockedBy: List[int] = None, 
            removeBlockedBy: List[int] = None
        ):
        try: 
            output = task_manager.update(task_id=task_id, status=status, add_blocked_by=addBlockedBy, remove_blocked_by=removeBlockedBy)
            return self.success_response(output)
        except Exception as e:
            return self.fail_response(f"task_id: {task_id} 任务更新失败: {e}")

@register_tool
class TaskGetTool(BaseTool):
    name = "task_get"
    description =  "根据任务id，获取该任务的完整信息"
    input_schema = {
        "type": "object", 
        "properties": {"task_id": {"type": "integer"}}, 
        "required": ["task_id"]
    }

    def execute(self, task_id: int):
        try:
            output = task_manager.get(task_id=task_id)
            return self.success_response(output)
        except Exception as e:
            return self.fail_response(f"task_id: {task_id} 任务信息获取失败: {e}")
        
@register_tool
class TaskListTool(BaseTool):
    name = "task_list"
    description = "列出所有任务及其状态概要"
    input_schema = {
        "type": "object", 
        "properties": {}
    }

    def execute(self):
        try:
            output = task_manager.list_all()
            return self.success_response(output)
        except Exception as e:
            return self.fail_response("列出所有任务失败: {e}")
