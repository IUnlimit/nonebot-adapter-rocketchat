from typing_extensions import override

from pydantic import BaseModel
from nonebot.adapters import Event as BaseEvent
from nonebot.compat import model_dump

from .message import Message

# from .event import (

# )

class Event(BaseEvent):
    
    time: int

    @override
    def get_type(self) -> str:
        raise NotImplementedError

    # 返回事件的名称，用于日志打印
    @override
    def get_event_name(self) -> str:
        return self.__class__.__name__

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
        return False


# Message
class MessageEvent(Event):
    """消息事件"""
    message_id: str
    user_id: str
    msg: str
    message: Message

    @override
    def get_type(self) -> str:
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
        return self.user_id


# Meta
class MetaEvent(Event):
    @override
    def get_type(self) -> str:
        return "meta_event"

# 一个聊天对应一个心跳事件，暂不考虑实现
#{
#     "_id": "ZCCTjvDkst5ti7fAD",
#     "rid": "2CyBSwMLfhpm9uR4ktG6AhvCpKEoiQpn4r",
#     "u": {
#         "_id": "tG6AhvCpKEoiQpn4r",
#         "username": "iunlimit.bot"
#     },
#     "_updatedAt": "2024-04-01T16:25:39.455Z",
#     "alert": true,
#     "fname": "Poz Chou",
#     "groupMentions": 0,
#     "name": "illtamer",
#     "open": true,
#     "t": "d",
#     "unread": 2,
#     "userMentions": 0
# }
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