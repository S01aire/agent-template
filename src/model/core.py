from enum import Enum
from typing import List, Dict, Any

from pydantic import BaseModel, Field, TypeAdapter

class Channel(Enum):
    DEFAULT = "默认"
    REDBOOK = "小红书"
    WEBSITE = "网页"
    GZH = "微信公众号"

