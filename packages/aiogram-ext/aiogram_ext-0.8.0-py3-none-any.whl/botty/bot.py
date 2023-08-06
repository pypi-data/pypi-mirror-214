from typing import TypeVar

import aiogram

from .deps import User

T = TypeVar("T")


class Bot(aiogram.Bot):
    def __init__(self, token: str, loop=None):
        super().__init__(token, loop, parse_mode="html", disable_web_page_preview=True)

    @property
    def url(self) -> str:
        me: User | None = getattr(self, "_me")
        if not me:
            raise RuntimeError("Bot has not `me` yet.")
        return f"https://t.me/{me.username}"

    def get_start_url(self, data: str = "0", *, group: bool = False) -> str:
        param = "startgroup" if group else "start"
        return f"{self.url}?{param}={data}"

    @property
    def start_url(self):
        return self.get_start_url()

    @property
    def startgroup_url(self):
        return self.get_start_url(group=True)
