import asyncio
from typing import TypeVar, Awaitable

import aiogram
from aiogram.utils.executor import start_polling, Executor
from aiohttp.web import Application

from .bot import Bot
from .buttons import CallbackButton
from .config import APP_PORT
from .deps import State, MongoStorage
from .filters import (
    CallbackQueryButton,
    InlineQueryButton,
    MessageButton,
    StorageDataFilter,
)

T = TypeVar("T")


class Dispatcher(aiogram.Dispatcher):
    def __init__(self, bot: Bot, storage: MongoStorage, loop=None):
        super().__init__(bot, loop, storage)

    @staticmethod
    def _gen_payload(
        locals_: dict, exclude: list[str] = None, default_exclude=("self", "cls")
    ):
        kwargs = locals_.pop("kwargs", {})
        locals_.update(kwargs)

        if exclude is None:
            exclude = []
        return {
            key: value
            for key, value in locals_.items()
            if key not in exclude + list(default_exclude)
            and value is not None
            and not key.startswith("_")
        }

    def _setup_filters(self):
        filters_factory = self.filters_factory
        filters_factory.bind(
            StorageDataFilter,
            exclude_event_handlers=[
                self.errors_handlers,
                self.poll_handlers,
                self.poll_answer_handlers,
            ],
        )
        filters_factory.bind(
            CallbackQueryButton, event_handlers=[self.callback_query_handlers]
        )
        filters_factory.bind(
            InlineQueryButton, event_handlers=[self.inline_query_handlers]
        )
        filters_factory.bind(
            MessageButton,
            event_handlers=[
                self.message_handlers,
                self.edited_message_handlers,
            ],
        )

        super()._setup_filters()

    def command(self, command: str):
        return CommandHandler(self, command)

    def start(self, state: str | State | None = "*"):
        return self.command("start").state(state)

    def button(self, button: CallbackButton | list[CallbackButton]):
        return ButtonHandler(self, button)

    def text(self, text: str = None):
        return TextHandler(self, text)

    def contact(self):
        return ContactHandler(self)

    def document(self):
        return DocumentHandler(self)

    def photo(self):
        return PhotoHandler(self)

    def message(self, content_types: str | list[str] = "any"):
        return MessageHandler(self, content_types)

    def sticker(self):
        return self.message("sticker")

    def error(self, exc: Exception = Exception):
        return self.errors_handler(exception=exc)

    @property
    def CONTACT(self):  # noqa
        return self.contact()

    @property
    def DOCUMENT(self):  # noqa
        return self.document()

    @property
    def PHOTO(self):  # noqa
        return self.photo()

    @property
    def TEXT(self):  # noqa
        return self.text()

    @property
    def START(self):  # noqa
        return self.start()

    @property
    def MESSAGE(self):  # noqa
        return self.message()

    @property
    def ERROR(self):  # noqa
        return self.error()

    def run(self, *tasks: Awaitable):
        async def on_startup(_):
            for task in tasks:
                await task

        start_polling(self, on_startup=on_startup)

    def run_server(
        self,
        app_url: str,
        app: Application = None,
        path: str = "/bot",
        port: int = APP_PORT,
    ):
        executor = Executor(self)
        executor.set_webhook(path, web_app=app)
        self._set_webhook(app_url + path)
        executor.run_app(port=port)

    def _set_webhook(self, url: str):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.bot.set_webhook(url))


class Handler:
    def __init__(self, dp: Dispatcher):
        self._dp = dp
        self._state = None
        self._chat_id = None
        self._user_id = None
        self._extra = {}

    def state(self, value: str | State | None = "*"):
        self._state = value
        return self

    def chat_id(self, value: int):
        self._chat_id = value
        return self

    def user_id(self, value: int | list[int]):
        self._user_id = value
        return self

    def extra(self, **kwargs):
        self._extra = kwargs
        return self

    def __call__(self, callback):
        raise NotImplementedError


class MessageHandler(Handler):
    def __init__(self, dp: Dispatcher, content_types: str | list[str] = "any"):
        super().__init__(dp)
        self._command = None
        self._text = None
        self._content_types = content_types
        self._is_forwarded = None
        self._is_reply = None

    @property
    def forwarded(self):
        self._is_forwarded = True
        return self

    @property
    def has_reply(self):
        self._is_reply = True
        return self

    def __call__(self, callback):
        deco = self._dp.message_handler(
            content_types=self._content_types,
            button=self._text,
            commands=self._command,
            state=self._state,
            chat_id=self._chat_id,
            user_id=self._user_id,
            is_forwarded=self._is_forwarded,
            is_reply=self._is_reply,
            **self._extra,
        )
        return deco(callback)


class TextHandler(MessageHandler):
    def __init__(self, dp: Dispatcher, text: str = None):
        super().__init__(dp, "text")
        self._text = text


class CommandHandler(TextHandler):
    def __init__(self, dp: Dispatcher, command: str):
        super().__init__(dp)
        self._command = command


class ContactHandler(MessageHandler):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp, "contact")


class PhotoHandler(MessageHandler):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp, "photo")


class DocumentHandler(MessageHandler):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp, "document")


class ButtonHandler(Handler):
    def __init__(self, dp: Dispatcher, button: CallbackButton | list[CallbackButton]):
        super().__init__(dp)
        self._button = button

    def __call__(self, callback):
        deco = self._dp.callback_query_handler(
            button=self._button,
            state=self._state,
            chat_id=self._chat_id,
            user_id=self._user_id,
            **self._extra,
        )
        return deco(callback)
