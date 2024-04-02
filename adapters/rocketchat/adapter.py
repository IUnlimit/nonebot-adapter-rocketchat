import asyncio
import collections
from datetime import datetime, timezone
import inspect
import signal
import sys
import time
from typing import Any, Dict, Generator, List, Optional, Type
from typing_extensions import override

from nonebot import get_plugin_config
from nonebot.exception import WebSocketClosed
from nonebot.compat import type_validate_python
from nonebot.utils import DataclassEncoder, escape_tag
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    WebSocket,
    ForwardDriver,
    ReverseDriver,
    HTTPServerSetup,
    WebSocketServerSetup,
    HTTPClientMixin
)

from nonebot.adapters import Adapter as BaseAdapter

from adapters.rocketchat.collator import Collator

from . import event as eventpy
from .bot import Bot
from .event import Event, MessageEvent
from .config import Config
from .message import Message, MessageSegment
from rocketchat_API.rocketchat import RocketChat
from .log import success, info, debug, error

DEFAULT_MODELS: List[Type[Event]] = []
for model_name in dir(eventpy):
    model = getattr(eventpy, model_name)
    if not inspect.isclass(model) or not issubclass(model, Event):
        continue
    DEFAULT_MODELS.append(model)

class Adapter(BaseAdapter):
    # event_models = Collator(
    #     "RocketChat",
    #     DEFAULT_MODELS,
    #     (
    #         "post_type",
    #         ("message_type", "notice_type", "request_type", "meta_event_type"),
    #         "sub_type",
    #     ),
    # )

    # _result_store = ResultStore()

    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.adapter_config = get_plugin_config(Config)
        self.connection: RocketChat
        self.listener: Optional[asyncio.Task] = None
        self.last_processed_timestamp = self.get_current_utc_timestamp()
        self.setup()

    def setup(self) -> None:
        # 判断用户配置的Driver类型是否符合适配器要求，不符合时应抛出异常
        # if not isinstance(self.driver, HTTPClientMixin):
        #     raise RuntimeError(
        #         f"Current driver {self.config.driver} doesn't support websocket client connections!"
        #         f"{self.get_name()} Adapter need a WebSocket Client Driver to work."
        #     )
        # 在 NoneBot 启动和关闭时进行相关操作
        self.driver.on_startup(self.startup)
        self.driver.on_shutdown(self.shutdown)

    """定义启动时的操作，例如和平台建立连接"""
    # TODO 自动重连
    async def startup(self) -> None:
        self.connection = RocketChat(
            self.adapter_config.rc_username, 
            self.adapter_config.rc_password, 
            server_url=str(self.adapter_config.rc_server_url), 
            proxies=self.adapter_config.rc_proxies)
        bot_id = self.connection.me().json()["username"]
        bot = Bot(self, self_id=bot_id)
        success(f"<y>Bot {bot_id}</y> connected")
        self.bot_connect(bot)
        self.listener = asyncio.create_task(self._forward_http(bot))

    """消息转发监听"""
    async def _forward_http(self, bot: Bot):
        id_queue = collections.deque(maxlen=1 << 13) # 8192
        while True:
            try:
                response = self.connection.subscriptions_get().json()
                updates = response.get('update')
                if updates:
                    for result in updates:
                        try:
                            self._handle_forward_http(result, id_queue, bot)
                        except Exception as e:
                            print(f'Error: {e} in {result}')
            except Exception as e:
                print(f'Error: {e} occurred when init listener')
            await asyncio.sleep(self.adapter_config.rc_message_update_interval if self.adapter_config.rc_message_update_interval else 1)

    """解析消息"""
    def _handle_forward_http(self, result, id_queue: collections.deque, bot: Bot):
        chat_type = result['t']
        room_id = result['rid']

        # info(result) match any msg
        # private / direct
        if chat_type == "d":
            response = self.connection.im_history(room_id).json()
            messages = response.get('messages', [])
        # channel
        elif chat_type == "c":
            response = self.connection.channels_history(room_id).json()
            messages = response.get('messages', [])
        # private group
        elif chat_type == "p":
            response = self.connection.groups_history(room_id).json()
            messages = response.get('messages', [])
        else:
            return
        
        for message in messages:
            # info(f"Processing message: {message['msg']}")
            if message['_id'] in id_queue or message['u']['username'] == self.adapter_config.rc_username:
                continue
            id_queue.append(message['_id'])

            message_timestamp = message['ts']
            if self.last_processed_timestamp and message_timestamp <= self.last_processed_timestamp:
                continue
            
            # info(message)
            # if event := self.json_to_event(message, ):
            date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            timestamp = datetime.strptime(message_timestamp, date_format).timestamp()
            # TODO
            event = MessageEvent(
                time=int(timestamp), 
                message_id=message['_id'], 
                user_id=message['u']['_id'],
                msg=message['msg'],
                message=Message(message['msg']))
            asyncio.create_task(bot.handle_event(event))


    """定义关闭时的操作，例如停止任务、断开连接"""
    async def shutdown(self) -> None:
        if self.listener is not None and not self.listener.done():
            self.listener.cancel()

    @classmethod
    @override
    def get_name(cls) -> str:
        return "RockatChat"

    @override
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        ...

    # @classmethod
    # def json_to_event(cls, json: Any) -> Optional[Event]:
    #     """将 json 数据转换为 Event 对象。

    #     如果为 API 调用返回数据且提供了 Event 对应 Bot，则将数据存入 ResultStore。

    #     参数:
    #         json: json 数据
    #         self_id: 当前 Event 对应的 Bot

    #     返回:
    #         Event 对象，如果解析失败或为 API 调用返回数据，则返回 None
    #     """
    #     if not isinstance(json, dict):
    #         return None
        
    #     # 判断是否为 api 调用返回

    #     try:
    #         for model in cls.get_event_model(json):
    #             try:
    #                 event = type_validate_python(model, json)
    #                 break
    #             except Exception as e:
    #                 # TODO debug message
    #                 error("Event Parser Error", e)
    #         else:
    #             event = type_validate_python(Event, json)

    #         return event
    #     except Exception as e:
    #         error(
    #             "<r><bg #f8bbd0>Failed to parse event. "
    #             f"Raw: {escape_tag(str(json))}</bg #f8bbd0></r>",
    #             e,
    #         )

    # @classmethod
    # def get_event_model(
    #     cls, data: Dict[str, Any]
    # ) -> Generator[Type[Event], None, None]:
    #     """根据事件获取对应 `Event Model` 及 `FallBack Event Model` 列表。"""
    #     yield from cls.event_models.get_model(data)

    @staticmethod
    def get_current_utc_timestamp():
        """Get the current UTC timestamp in the same format as the messages."""
        return datetime.now(timezone.utc).isoformat()

    def quit(self, signum, frame):
        sys.exit()