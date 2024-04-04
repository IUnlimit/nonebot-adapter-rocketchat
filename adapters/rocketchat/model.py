# Models
from typing import Dict, List, Optional, Union
from pydantic import BaseModel

# u 事件触发者
class Sender(BaseModel):
    # _id
    _id: str
    # username
    username: str
    # name
    name: str

class File(BaseModel):
    # _id
    _id: str
    # storage name
    name: str
    # file type - image/jpeg
    type: str

# url 
class Url(BaseModel):
    url: str
    meta: Dict
    ignoreParse: bool

# block
class Block(BaseModel):
    type: str
    blockId: str
    callId: Optional[str] = None
    appId: Optional[str] = None

# mentions @消息
class Mention(BaseModel):
    # _id
    _id: str
    # username @对象的 username
    username: str
    # name @对象的 name
    name: str
    type: str

# md 消息
class Markdown(BaseModel):
    # 消息类型 LINK PLAIN_TEXT
    type: str
    value: Union[str, Dict]
    # EMOJI
    shortCode: Optional[str] = None

# md 消息段落
class Paragraph(BaseModel):
    value: List[Markdown]