from enum import Enum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, TypeAdapter


class EventType(str, Enum):
    await_human = "await_human"
    final = "final"

class AwaitHumanPayload(BaseModel):
    question: str
    tool_use_id: str

class FinalPayload(BaseModel):
    answer: str

class AwaitHumanEvent(BaseModel):
    type: Literal[EventType.await_human]
    message: str
    payload: AwaitHumanPayload

class FinalEvent(BaseModel):
    type: Literal[EventType.final]
    message: str
    payload: FinalPayload

Event = Annotated[
    Union[AwaitHumanEvent, FinalEvent],
    Field(discriminator="type"),
]

def make_await_human(question: str, tool_use_id: str) -> Event:
    payload = AwaitHumanPayload(question=question, tool_use_id=tool_use_id)
    return AwaitHumanEvent(type=EventType.await_human, message="", payload=payload)

def make_final(answer: str):
    payload = FinalPayload(answer=answer)
    return FinalEvent(type=EventType.final, message="", payload=payload)