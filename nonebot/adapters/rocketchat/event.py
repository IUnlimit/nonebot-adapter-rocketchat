from typing import TYPE_CHECKING, Dict, List, Optional
from typing_extensions import override

from pydantic import BaseModel
from nonebot.adapters import Event as BaseEvent
from nonebot.compat import model_dump

from .message import Message
from .model import Block, File, Mention, Paragraph, User, Url

if TYPE_CHECKING:
    from .bot import Bot

class Event(BaseEvent):
    
    # The unique identifier for the message.
    _id: str

    # 自定义字段
    # 机器人自身 Id, 生成时传入
    self_id: Optional[str] = None
    to_me: bool = False 

    @override
    def get_type(self) -> str:
        raise NotImplementedError

    # 返回事件的名称，用于日志打印
    @override
    def get_event_name(self) -> str:
        raise NotImplementedError

    # 返回事件的描述，用于日志打印，请注意转义 loguru tag
    @override
    def get_event_description(self) -> str:
        return str(model_dump(self, exclude_none=True))

    # 获取事件消息的方法，根据事件具体实现，如果事件非消息类型事件，则抛出异常
    @override
    def get_message(self) -> Message:
        raise NotImplementedError

    @override
    def get_plaintext(self) -> str:
        raise NotImplementedError

    # 获取用户 ID 的方法，根据事件具体实现，如果事件没有用户 ID，则抛出异常
    @override
    def get_user_id(self) -> str:
        raise NotImplementedError

    # 获取事件会话 ID 的方法，根据事件具体实现，如果事件没有相关 ID，则抛出异常
    @override
    def get_session_id(self) -> str:
        raise NotImplementedError

    # 判断事件是否和机器人有关
    @override
    def is_tome(self) -> bool:
        return self.to_me


"""https://developer.rocket.chat/reference/api/schema-definition/message"""
# Message
class MessageEvent(Event):
    """消息事件"""

    # msg 文本化消息(非纯文字消息, 不一定有值)
    msg: str
    # The ID of the thread where the message belongs to.
    tmid: Optional[str] = None
    # Indicates whether the thread should be shown.
    tshow: Optional[bool] = None
    # A timestamp of when the message was created. (The date of creation on client)
    ts: Optional[Dict] = None
    # An array of user mentions within the message. Identifies (type: "type of the mention;
    #   either user or team", _id: "id of the user that is mentioned", username: "username 
    #   of the user that is mentioned", name: name of the user that is mentioned).
    mentions: Optional[List[Mention]] = None
    # Boolean that states whether or not this message should be grouped 
    #   together with other messages from the same user
    groupable: Optional[bool] = None
    # An array of channel where message belongs to
    channels: Optional[List[Dict]] = None
    # The user who sent the message (either the _id or username or name).
    u: User
    # If a uikit message, then the uikit will block components.
    blocks: Optional[List[Block]] = None
    # A way to display the message is "sent" from someone else other 
    #   than the user who sent the message
    alias: Optional[str] = None
    # The message's content in a markdown format.
    md: Optional[List[Paragraph]] = None
    # Indicates whether the message is hidden.
    _hidden: Optional[bool] = None
    # Indicates whether the message is imported.
    imported: Optional[bool] = None
    # An array of user IDs representing the  message replies.
    replies: Optional[List[str]] = None
    # The geographic location associated with the message.
    location: Optional[Dict] = None
    # A list of users that have the message starred (list of user Ids (_id)
    starred: Optional[List] = None
    # Indicates whether the message is pinned.
    pinned: Optional[bool] = None
    # The date and time when the message was pinned.
    pinnedAt: Optional[Dict] = None
    # Information about the user who pinned the message.
    pinnedBy: Optional[Dict] = None
    # Indicates whether the message is unread.
    unread: Optional[bool] = None
    # Indicates whether the message is temporary.
    temp: Optional[bool] = None
    # The direct room id (if belongs to a direct room).
    drid: Optional[str] = None
    # The date and time when the last thread message was sent.
    tlm: Optional[Dict] = None
    # The count of messages deleted in the thread.
    dcount: Optional[int] = None
    # The count of messages in the thread.
    tcount: Optional[int] = None
    # The type of the message.
    t: Optional[str] = None
    # The end-to-end encryption status of the message.
    e2e: Optional[str] = None
    # The acknowledgement status of an off-the-record message.
    otrAck: Optional[str] = None
    # An array of URLs contained within the message.
    urls: Optional[List[Url]]
    # An array of action links associated with the message.
    # (deprecated)
    actionLinks: Optional[List[Dict]] = None
    # The file property associated with the message.
    # (deprecated)
    file: Optional[File] = None
    # Information about a file upload associated with the message.
    fileUpload: Optional[Dict] = None
    # An array of file properties associated with the message.
    files: Optional[List[File]] = None
    # An array of attachment objects, available only when the message has at least one attachment.
    # https://developer.rocket.chat/reference/api/rest-api/endpoints/messaging/chat-endpoints/postmessage#attachments-detail
    attachments: Optional[List] = None
    # Object containing reaction information associated with the message.
    # {':airplane:': {'usernames': ['illtamer']}, ':ok_hand:': {'usernames': ['illtamer']}}}
    reactions: Optional[Dict] = None
    # Indicates whether the message is private.
    private: Optional[bool] = None
    # Indicates whether the message is sent by a bot.
    # (deprecated)
    bot: Optional[bool] = None
    # Indicates whether the message was sent by email.
    sentByEmail: Optional[bool] = None
    # The date and time when a WebRTC call ended.
    webRtcCallEndTs: Optional[Dict] = None
    # The role associated with the message.
    role: Optional[str] = None
    # A url to an image, that is accessible to anyone, to display 
    #   as the avatar instead of the message user's account avatar
    avatar: Optional[str] = None
    # The emoji associated with the user who sent the message.
    emoji: Optional[str] = None
    # An array of tokens extracted from the message content.
    tokens: Optional[List] = None
    # The HTML representation of the message.
    html: Optional[str] = None
    # A deprecated field used for messages sent by visitors
    # (deprecated)
    token: Optional[str] = None
    # Information about federation associated with the message.
    federation: Optional[Dict] = None
    # Additional data related to SLA (Service Level Agreements) change history messages.
    # (used for specific message types)
    slaData: Optional[Dict] = None
    # Additional data related to priority change history messages.
    # (used for specific message types)
    priorityData: Optional[Dict] = None
    
    # 一些未在文档声明但是存在的字段
    parseUrls: Optional[bool] = None
    _updatedAt: Optional[Dict] = None

    # 自定义字段
    message: Optional[Message] = None

    @override
    def get_type(self) -> str:
        """获取事件类型的方法，类型通常为 NoneBot 内置的四种类型。"""
        return "message"

    @override
    def get_plaintext(self) -> str:
        return self.msg

    @override
    def get_message(self) -> Message:
        # 返回事件消息对应的 NoneBot Message 对象
        if not self.message:
            raise AttributeError
        return self.message

    @override
    def get_user_id(self) -> str:
        return str(self.u._id)


class RoomMessageEvent(MessageEvent):

    # The unique id for the room. This will identify the room that the message belongs to. Example: 'GENERAL'
    rid: str

    # room type - d, p
    room_type: Optional[str] = None

    # 返回事件的名称，用于日志打印
    @override
    def get_event_name(self) -> str:
        """获取事件名称的方法。"""
        return "stream-room-messages"

    @override
    def get_session_id(self) -> str:
        """获取会话 id 的方法，用于判断当前事件属于哪一个会话，
        通常是用户 id、群组 id 组合。
        """
        return self.rid + self.u._id

    # 判断事件是否和机器人有关
    @override
    def is_tome(self) -> bool:
        if self.room_type == "d":
            return True
        return super().is_tome()


# Meta
# class MetaEvent(Event):
#     @override
#     def get_type(self) -> str:
#         return "meta_event"

# class HeartbeatEvent(MetaEvent):
    # """心跳事件"""


# Notice
# class JoinRoomEvent(Event):
#     """加入房间事件，通常为通知事件"""
#     user_id: str
#     room_id: str

#     @override
#     def get_type(self) -> str:
#         return "notice"


# Request
# class ApplyAddFriendEvent(Event):
    # """申请添加好友事件，通常为请求事件"""
    # user_id: str

    # @override
    # def get_type(self) -> str:
    #     return "request"