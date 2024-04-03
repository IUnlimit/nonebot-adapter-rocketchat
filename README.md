<p align="center"> 
  <img  src="./docs/images/logo.png" width="200" height="200" alt="nonebot-adapter-rocketchat" />
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
# Message update interval (Unit: seconds)
RC_MESSAGE_UPDATE_INTERVAL=0.5
```

## Thanks

- [rocketchat_API](https://github.com/jadolg/rocketchat_API)
- [RealTime API](https://github.com/hynek-urban/rocketchat-async)