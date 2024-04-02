from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.rule import is_type
from nonebot.permission import SUPERUSER
from nonebot.adapters import Message
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot import logger
from nonebot.adapters import Event, Bot
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="test",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)
# messageRule = is_type(Event)
test = on_command("test", block=True, priority=100)

@test.handle()
async def handle_function(args: Message = CommandArg()):
    print('接收到消息：' + args.extract_plain_text())