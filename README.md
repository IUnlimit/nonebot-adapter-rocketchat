<p align="center"> 
  <img  src="https://github.com/IUnlimit/nonebot-adapter-rocketchat/blob/main/docs/images/logo.png?raw=true" width="200" height="200" alt="nonebot-adapter-rocketchat" />
</p>

<h1 align="center">
  NoneBot-Adapter-RocketChat
</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/IUnlimit/nonebot-adapter-rocketchat?label=version">
  <a alt="License" href="https://www.gnu.org/licenses/agpl-3.0.en.html"><image src="https://img.shields.io/badge/license-AGPLv3-4EB1BA.svg"></image></a>
</p>

## Usage

[How to create a RocketChat bot account](https://developer.rocket.chat/bots/creating-your-own-bot-from-scratch) 

> Notice: This project (as well as `rocketchat_API`) does not support 2FA authentication. Please make sure that the robot account has turned off 2FA authentication before starting !

```toml
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

### REST API

[REST API Endpoints](https://developer.rocket.chat/reference/api/rest-api/endpoints)

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

## Support

- [subscriptions](https://developer.rocket.chat/reference/api/realtime-api/subscriptions)
  - [ ] stream-notify-all
  - [ ] stream-notify-logged
  - [ ] stream-notify-room-users
  - [ ] stream-notify-room
  - [x] stream-room-messages
  - [ ] stream-notify-user

## Thanks

- [rocket-python](https://github.com/Pipoline/rocket-python)
- [RealTime API](https://github.com/hynek-urban/rocketchat-async)