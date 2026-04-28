from typing import Literal, Union

from pydantic import BaseModel, Field


class SendRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class ResumeRequest(BaseModel):
    session_id: str = Field(min_length=1)
    tool_use_id: str = Field(min_length=1)
    answer: str = Field(min_length=1)


class FinalResponse(BaseModel):
    type: Literal["final"]
    answer: str


class AwaitHumanResponse(BaseModel):
    type: Literal["await_human"]
    question: str
    tool_use_id: str


ChatResponse = Union[FinalResponse, AwaitHumanResponse]
