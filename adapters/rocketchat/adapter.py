import asyncio
import collections
import contextlib
from datetime import datetime, timezone
import hashlib
import inspect
import json
import signal
import sys
import time
from typing import Any, Dict, Generator, List, Optional, Type
from typing_extensions import override

from nonebot import get_plugin_config
from nonebot.exception import WebSocketClosed
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
    HTTPClientMixin,
    WebSocketClientMixin
)

from nonebot.adapters import Adapter as BaseAdapter

from . import event as eventpy
from .bot import Bot
from .event import Event, MessageEvent, RoomMessageEvent
from .config import Config
from .message import Message, MessageSegment
from rocketchat.api import RocketChatAPI
from .log import success, info, debug, error
from .realtime import RealTime

# TODO 多实例
class Adapter(BaseAdapter):

    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.adapter_config = get_plugin_config(Config)
        self.rest_api: RocketChatAPI
        self.listener: Optional[asyncio.Task] = None
        self.room_types = dict()
        # self.last_processed_timestamp = self.get_current_utc_timestamp()
        self.setup()

    def setup(self) -> None:
        # 判断用户配置的Driver类型是否符合适配器要求，不符合时应抛出异常
        if not isinstance(self.driver, WebSocketClientMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} doesn't support websocket client connections ! "
                f"{self.get_name()} Adapter need a WebSocket Client Driver to work."
            )
        # 在 NoneBot 启动和关闭时进行相关操作
        self.driver.on_startup(self.startup)
        self.driver.on_shutdown(self.shutdown)

    """定义启动时的操作，例如和平台建立连接"""
    async def startup(self) -> None:
        config = self.adapter_config
        self.rest_api = RocketChatAPI(settings={
            'username': config.rc_username,
            'password': config.rc_password,
            'domain': config.rc_server_http
        })
        bot_id = self.rest_api.get_my_info()["username"]
        self.listener = asyncio.create_task(self._forward_ws(bot_id))

    async def _forward_ws(self, rest_bot_id: str):
        while True:
            try:
                config = self.adapter_config
                realtime = RealTime()
                await realtime.start(config.rc_server_wss, config.rc_username, config.rc_password)

                bot = Bot(self, self_id=rest_bot_id)
                self.bot_connect(bot)
                success(f"<y>Bot {rest_bot_id}</y> connected")

                for channel_id, channel_type in await realtime.get_channels():
                    # 同类型(stream-room-messages) 注册归注册,只保留最后一个callback
                    await realtime.subscribe_to_channel_messages(
                        channel_id, 
                        channel_type, 
                        lambda event: asyncio.create_task(bot.handle_event(event)))
                    
                    info(f"Subscribe channel {channel_id} ({channel_type})")
                    self.room_types[channel_id] = channel_type
                    
                await realtime.run_forever()
            except (RealTime.ConnectionClosed, RealTime.ConnectCallFailed) as e:
                # 尝试重连
                error(
                    "<r><bg #f8bbd0>Error while setup websocket to "
                    f"{escape_tag(config.rc_server_wss)}. Trying to reconnect...</bg #f8bbd0></r>",
                    e,
                )
            except Exception as e:
                error(
                    "<r><bg #f8bbd0>Error while process data from "
                    f"websocket {self.adapter_config.rc_server_wss}. "
                    "Trying to reconnect...</bg #f8bbd0></r>",
                    e,
                )
            finally:
                # 这里要断开 Bot 连接
                if bot:
                    self.bot_disconnect(bot)
                    bot = None
            await asyncio.sleep(3)


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