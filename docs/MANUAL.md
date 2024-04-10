# Rocket.Chat Adapter 使用指南

> 本文默认你使用 nb init 创建了一个空的 bootstrap 项目。

## 创建 Rocket.Chat 机器人

[如何创建一个 Rocket.Chat 机器人账户 (官方教程)](https://developer.rocket.chat/bots/creating-your-own-bot-from-scratch) 

> 注意：本项目 ( 基于 `rocket-python` ) 不支持调用 REST API 时进行 2FA 身份验证, 因此在启动之前请确保机器人账户已关闭 2FA 身份验证！

## 安装适配器

### 使用 nb-cli 安装 (推荐)

```shell
nb adapter install nonebot-adapter-rocketchat
```

### 使用 pip 进行安装

```shell
pip install nonebot-adapter-rocketchat
```

## 配置 nonebot

### 配置驱动器

NoneBot 默认选择的驱动器为 FastAPI，它是一个服务端类型驱 (ReverseDriver), 而 Rocket.Chat 适配器至少需要一个 HTTP 客户端驱动器类型驱动器和一个 WebSocket 客户端驱动器 (ForwardDriver), 所以你需要额外安装其他驱动器。

`HTTPX` 和 `websockets` 是推荐的客户端类型驱动器，你可以使用 nb-cli 进行安装。

```shell
nb driver install httpx
nb driver install websockets
```

### 配置环境变量 `.env`

```toml
# 填写在 `配置驱动器` 一节提到的驱动器
DRIVER=~fastapi+~httpx+~websockets

# Bot username
RC_USERNAME="yourbot.name"
# Bot password
RC_PASSWORD="password"
# RocketChat server url
RC_SERVER_HTTP="http://localhost:3000"
RC_SERVER_WSS="ws://localhost:3000/websocket"
# Proxy server (Optional)
[RC_PROXIES]
http = "http://127.0.0.1:7890"
https = "https://127.0.0.1:7890"
```

## 加载适配器

### 使用 pyproject.toml

> 如果您先前使用 `nb-cli` 安装适配器, 则该适配器将自动注册到配置文件

```toml
[tool.nonebot]
adapters = [
    { name = "RocketChat", module_name = "nonebot.adapters.rocketchat" }
]
```

### 使用 bot.py

```python
import nonebot
from nonebot.adapters.rocketchat import Adapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(Adapter)
```

## 示例

### 在插件监听中调用 REST API

- [nonebot 插件编写教程 (官方)](https://nonebot.dev/docs/tutorial/create-plugin)
- [REST API Endpoints](https://developer.rocket.chat/reference/api/rest-api/endpoints)

```python
# with plugin listener
@listener.handle()
async def handle_function(bot: Bot, event: RoomMessageEvent, msgArgs: Message = CommandArg()):
  bot.get_rest_api().send_message(f'检索到 {len(hits)} 条用户记录（仅展示一条示例记录）', event.rid, attachments=[{
            "color": "#00FF00",
            "text": "[App 用户直接点击即可下载]",
            # "ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "title": "下载全部检索结果 (15 分钟内有效)",
            "title_link": get_url,
            "title_link_download": True,
            "fields": fields
        }])
```