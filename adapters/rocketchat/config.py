from typing import Optional
from pydantic import Field, BaseModel


class Config(BaseModel):
    rc_username: Optional[str] = Field(default=None)
    rc_password: Optional[str] = Field(default=None)
    rc_server_http: Optional[str] = Field(default=None)
    rc_server_wss: Optional[str] = Field(default=None)
    rc_proxies: Optional[dict] = Field(default=None)
    rc_message_update_interval: Optional[float] = Field(default=None)
