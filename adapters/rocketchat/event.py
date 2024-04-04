from typing import TYPE_CHECKING, List, Optional
from typing_extensions import override

from pydantic import BaseModel
from nonebot.adapters import Event as BaseEvent
from nonebot.compat import model_dump

from .message import Message
from .model import Block, File, Mention, Paragraph, Sender, Url

if TYPE_CHECKING:
    from .bot import Bot

class Event(BaseEvent):
    
    # _id
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
        return NotImplementedError

    # 返回事件的描述，用于日志打印，请注意转义 loguru tag
    @override
    def get_event_description(self) -> str:
        return str(model_dump(self))

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


# Message
class MessageEvent(Event):
    """消息事件"""

    # msg 文本化消息(非纯文字消息, 不一定有值)
    msg: str
    # ts.$date
    # timestamp: int
    # u 事件触发者
    u: Sender
    # _updatedAt.$date
    # updated_at: int
    urls: List[Url]
    # mentions @消息列表
    mentions: List[Mention]
    channels: List

    # md 格式消息解析
    md: Optional[List[Paragraph]] = None
    # t 消息类型
    t: Optional[str] = None
    # attachments 附加消息内容 如回复的消息 / 带图片的消息
    attachments: Optional[List] = None
    # blocks 消息块
    blocks: Optional[List[Block]] = None
    # groupable
    groupable: Optional[bool] = None
    # file
    file: Optional[File] = None
    # files
    files: Optional[List[File]] = None

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
        return self.message

    @override
    def get_user_id(self) -> str:
        return str(self.u._id)


class RoomMessageEvent(MessageEvent):

    # rid room id
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