from typing import List, Dict
from pathlib import Path

from src.model.user import Requirement


def gen_requirement(task: str, location: str, time: str, topic: List[str]) -> Requirement:
    path = Path("src/message_box/requirement.md")
    req = Requirement(
        task=task,
        location=location,
        time=time,
        topic=topic.copy()
    )

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        md = f"""
# Requirement

- task: {req.task}
- location: {req.location or "None"}
- time: {req.time or "None"}
- topic: {", ".join(req.topic) if req.topic else "None"}
"""
    
        path.write_text(md, encoding="utf-8")

        return "生成Requirement成功"
    
    except Exception as e:
        return "生成Requirement失败"
