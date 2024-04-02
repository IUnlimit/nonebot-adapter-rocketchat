from typing import Type, Union, Mapping, Iterable
from typing_extensions import override

from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment["Message"]):

    # 返回适配器的 Message 类型本身
    @classmethod
    @override
    def get_message_class(cls) -> Type["Message"]:
        return Message

    # TODO
    # 返回该消息段的纯文本表现形式，通常在日志中展示
    @override
    def __str__(self) -> str:
        return self.data["value"]

    # 判断该消息段是否为纯文本
    @override
    def is_text(self) -> bool:
        return self.type == "text"


class Message(BaseMessage[MessageSegment]):

    # 返回适配器的 MessageSegment 类型本身
    @classmethod
    @override
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    # TODO
    # 实现从字符串中构造消息数组，如无字符串嵌入格式可直接返回文本类型 MessageSegment
    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:
        return [MessageSegment("text", {"value": msg})]
