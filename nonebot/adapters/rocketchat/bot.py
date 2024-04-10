from typing import TYPE_CHECKING, Union, Any
from typing_extensions import override

from nonebot.compat import type_validate_python
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from rocketchat.api import RocketChatAPI

from .log import error
from .event import Event, MessageEvent, RoomMessageEvent
from .message import Message, MessageSegment
if TYPE_CHECKING:
    from .adapter import Adapter

class Bot(BaseBot):
    """
    nonebot_adapter_rocketchat 协议 Bot 适配。
    """

    @override
    def __init__(self, adapter, self_id: str, **kwargs: Any):
        super().__init__(adapter, self_id)
        self.adapter = adapter
        # 一些有关 Bot 的信息也可以在此定义和存储

    # 根据需要，对事件进行某些预处理
    """事件中所有对消息的处理仅局限于 message 对象, 原 md 与 attachments 不进行改动"""
    async def handle_event(self, eventJson: Any):
        # exclude self event
        if eventJson["u"] and eventJson["u"]["username"] == self.self_id:
            return
        
        try:
            event: Event = type_validate_python(RoomMessageEvent, eventJson)
        except Exception as e:
            error(f"Error occurred when parse event: {eventJson}", e)
            return

        # TODO 在此反序列化 message
        event.self_id = self.self_id

        # 检查事件是否和机器人有关操作，去除事件消息首尾的 @bot
        # 检查事件是否有回复消息，调用平台 API 获取原始消息的消息内容
        if isinstance(event, RoomMessageEvent):
            event.room_type = self.adapter.room_types[event.rid]
            self._parse_message(event)
            assert event.message is not None

            # ensure message not empty
            self._strip(event)
            if len(event.message) == 0:
                event.message.append(MessageSegment.text(""))
            self._check_at_me(event)

        # 调用 handle_event 让 NoneBot 对事件进行处理
        await handle_event(self, event)

    @override
    async def send(
        self,
        event: Event,
        message: Union[str, Message, MessageSegment],
        **kwargs,
    ) -> Any:
        # 根据平台实现 Bot 回复事件的方法
        rest_api: RocketChatAPI = self.adapter.rest_api
        if isinstance(event, RoomMessageEvent) != True:
            raise Exception("Unsupport")
        room_event: RoomMessageEvent = event
        # 将消息处理为平台所需的格式后，调用发送消息接口进行发送，例如：
        # data = message_to_platform_data(message)
        rest_api.send_message(str(message), room_event.rid)

    # 获取 RocketChat RESTFul API 调用对象
    def get_rest_api(self) -> RocketChatAPI:
        return self.adapter.rest_api

    def _parse_message(self, event: MessageEvent):
        """返回消息对象 TODO
        单独解析 self.md 可能会错过如 附件(图片)消息 一类的,消息存储于
        self.attachments 中的消息,后续完善相关解析
        // 如 attachments.description -> msg, attachments.descriptionMd -> md
        """
        if not event.md:
            event.message = Message().append(MessageSegment.text(""))
        else:
            event.message = Message().extend(Message._construct(event.md))

    def _strip(self, event: MessageEvent):
        """去除首尾部连续的空消息段
        ['', @, '', 'a', '', 'b', ''] -> [@, 'a', '', 'b']
        """
        if not event.message:
            return

        del_indexs = []
        for index, seg in enumerate(event.message):
            if seg.is_text():
                if len(str(seg).strip()) == 0:
                    del_indexs.append(index)
                else:
                    break
        # 从后往前删,确保索引不变
        del_indexs.sort(reverse=True)
        for i in del_indexs:
            del event.message[i]

        del_indexs = []
        for index, seg in enumerate(reversed(event.message)):
            if seg.is_text():
                if len(str(seg).strip()) == 0:
                    del_indexs.append(index)          
                else:
                    break
        # 已 reverse, 算长度直接删
        length = len(event.message)
        for i in del_indexs:
            del event.message[length-1-i]

    def _check_at_me(self, event: RoomMessageEvent):
        """检查消息中否存在 @机器人，去除相邻消息的空字符串, 删除@并赋值 `event.to_me`"""
        # direct room
        if event.room_type == "d":
            event.to_me = True
        elif event.mentions and len(event.mentions) != 0:
            # @bot
            for metion in event.mentions:
                if metion.username == self.self_id:
                    event.to_me = True
            
            assert event.message is not None
            first_at = event.message[0]
            if first_at.type == "MENTION_USER" and first_at.data["value"]["value"] == self.self_id:
                # 确保消息主体不为空
                if len(event.message) == 1 and event.to_me:
                    event.message.append(MessageSegment.text(""))
                # strip left
                next_msg = event.message[1]
                if next_msg.type == "PLAIN_TEXT":
                    next_msg.data["value"] = str(next_msg.data["value"]).lstrip()
                event.message.pop(0)
            
            latest_at = event.message[-1]
            if latest_at.type == "MENTION_USER" and latest_at.data["value"]["value"] == self.self_id:
                # 确保消息主体不为空
                if len(event.message) == 1 and event.to_me:
                    event.message.insert(0, MessageSegment.text(""))
                # strip right
                next_msg = event.message[-2]
                if next_msg.type == "PLAIN_TEXT":
                    next_msg.data["value"] = str(next_msg.data["value"]).rstrip()
                event.message.pop()