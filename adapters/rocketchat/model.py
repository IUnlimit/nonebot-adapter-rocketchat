# Models
from typing import Dict, List, Optional, Union
from pydantic import BaseModel

# u 用户
"""https://developer.rocket.chat/reference/api/schema-definition/user"""
class User(BaseModel):
    # The unique identifier for the user.
    _id: str
    # The date and time when the user was created.
    createdAt: Optional[Dict] = None
    # An array of role IDs associated with the user. Eg "user", "admin", “livechat-agent”
    roles: Optional[List[str]] = None
    # The type of user. E.g. “user”, “app” or “bot”
    type: Optional[str] = None
    # Indicates whether the user is active or not.
    active: Optional[bool] = None
    # The username of the user.
    username: Optional[str] = None
    # The nickname of the user.
    nickname: Optional[str] = None
    # The name of the user.
    name: Optional[str] = None
    # Additional services associated with the user.
    services: Optional[Dict] = None
    # An array of email objects associated with the user.
    emails: Optional[List] = None
    # The status of the user.
    status: Optional[str] = None
    # The status connection of the user.
    statusConnection: Optional[str] = None
    # The date and time of the user's last login.
    lastLogin: Optional[Dict] = None
    # The biography or description of the user.
    bio: Optional[str] = None
    # The origin of the user's avatar.
    avatarOrigin: Optional[str] = None
    # The ETag of the user's avatar.
    avatarETag: Optional[str] = None
    # The URL of the user's avatar.
    avatarUrl: Optional[str] = None
    # The UTC offset of the user's timezone.
    utcOffset: Optional[int] = None
    # The language preference of the user.
    language: Optional[str] = None
    # The default status of the user.
    statusDefault: Optional[str] = None
    # The custom status text of the user.
    statusText: Optional[str] = None
    # OAuth information associated with the user.
    oauth: Optional[Dict] = None
    # The date and time when the user object was last updated.
    _updatedAt: Optional[Dict] = None
    # End-to-end encryption information associated with the user.
    e2e: Optional[Dict] = None
    # Indicates whether the user needs to change their password.
    requirePasswordChange: Optional[bool] = None
    # Additional custom fields associated with the user.
    customFields: Optional[Dict] = None
    # User-specific settings.
    settings: Optional[Dict] = None
    # The ID of the user's default room.
    defaultRoom: Optional[str] = None
    # Indicates whether the user is an LDAP user.
    ldap: Optional[bool] = None
    # The extension associated with the user.
    extension: Optional[str] = None
    # The token for inviting the user.
    inviteToken: Optional[str] = None
    # Indicates whether the user can view all information.
    canViewAllInfo: Optional[bool] = None
    # The phone number associated with the user.
    phone: Optional[str] = None
    # The reason associated with the user.
    reason: Optional[str] = None
    # Indicates whether the user is a federated user.
    federated: Optional[bool] = None
    # Federation information associated with the user.
    federation: Optional[Dict] = None
    # Banner information associated with the user.
    banners: Optional[Dict] = None
    # An array of import IDs associated with the user.
    importIds: Optional[List[str]] = None

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
    value: Optional[Union[str, Dict]] = None
    # EMOJI
    shortCode: Optional[str] = None
    # unicode EMOJI
    unicode: Optional[str] = None

# md 消息段落
class Paragraph(BaseModel):
    value: List[Markdown]