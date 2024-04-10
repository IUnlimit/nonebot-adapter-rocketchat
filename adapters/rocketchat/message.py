from typing import List, Type, Union, Iterable
from typing_extensions import override, Self

from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment

from adapters.rocketchat.model import Paragraph


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
        return str(self.data["value"])

    @override
    def __add__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return Message(self) + (
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @override
    def __radd__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return (
            MessageSegment.text(other) if isinstance(other, str) else Message(other)
        ) + self

    # 判断该消息段是否为纯文本
    @override
    def is_text(self) -> bool:
        return self.type == "PLAIN_TEXT"

    # TODO builder 方法
    @classmethod
    def text(cls, text: str) -> Self:
        return cls("PLAIN_TEXT", {"value": text})


class Message(BaseMessage[MessageSegment]):

    # 返回适配器的 MessageSegment 类型本身
    @classmethod
    @override
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @override
    def __add__(
        self, other: Union[str, MessageSegment, Iterable[MessageSegment]]
    ) -> Self:
        return super().__add__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    # def to_rich_text(self, truncate: Optional[int] = 70) -> str:
    #     return "".join(seg.to_rich_text(truncate=truncate) for seg in self)

    @override
    def __radd__(
        self, other: Union[str, MessageSegment, Iterable[MessageSegment]]
    ) -> Self:
        return super().__radd__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @override
    def __iadd__(
        self, other: Union[str, MessageSegment, Iterable[MessageSegment]]
    ) -> Self:
        return super().__iadd__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )
    
    # 实现从json中构造消息数组，如无字符串嵌入格式可直接返回文本类型 MessageSegment
    @staticmethod
    @override
    def _construct(p_list: Union[List[Paragraph], str]) -> Iterable[MessageSegment]:
        if p_list is None:
            return []
        if isinstance(p_list, str):
            return [MessageSegment.text(p_list)]
        segments = []
        for para in p_list:
            for md in para.value:
                # {"type": "PLAIN_TEXT", "value": "你好 "}
                # {'type': 'EMOJI', 'unicode': '👍'}
                md_dict = md.__dict__
                # 删除值为 None 的键值对
                none_keys = [key for key, value in md_dict.items() if value is None]
                for key in none_keys:
                    del md_dict[key]
                
                md_type = md_dict["type"]
                del md_dict["type"]
                segments.append(MessageSegment(md_type, md_dict))
        return segments

    @override
    def extract_plain_text(self) -> str:
        return "".join(str(seg).strip() for seg in self if seg.is_text())
