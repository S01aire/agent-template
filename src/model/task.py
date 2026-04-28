from typing import List, Dict
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Task(BaseModel):
    id: int
    subject: str
    description: str = Field(default="")
    status: TaskStatus = Field(default=TaskStatus.pending)
    blocked_by: List[int] = Field(default_factory=list)
    owner: str = Field(default="")
