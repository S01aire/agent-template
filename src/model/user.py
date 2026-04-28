from typing import List, Dict, Optional

from pydantic import BaseModel, Field

from src.model.core import Channel


class Requirement(BaseModel):
    task: str = Field(..., description="用户的需求")
    location: Optional[str] = Field(default=None, description="活动地点")
    time: Optional[str] = Field(default=None, description="活动时间")
    topic: List[str] = Field(default_factory=list, description="活动主题")


class Result(BaseModel):
    title: str = Field(..., description="活动名称")
    location: str = Field(..., description="活动地点")
    time: str = Field(..., description="活动时间")
    source_channel: Channel = Field(default=Channel.DEFAULT, description="搜集渠道")
    description: str = Field(..., description="活动描述")
