import asyncio
from dataclasses import dataclass

from .deps import Message, TelegramAPIError, RetryAfter
from .html import bold


def schedule_broadcast(post: Message, chat_ids: list[int]):
    return Broadcast(post).schedule(chat_ids)


class Broadcast:
    INTERVAL = 0.1

    def __init__(self, post: Message):
        self._post = post
        self._summary = Summary()
        self._chat_ids = []

    def schedule(self, chat_ids: list[int]):
        self._chat_ids = chat_ids
        asyncio.create_task(self._broadcast())

    async def _broadcast(self):
        for i in self._chat_ids:
            await self._try_copy_post(i)
        await self._send_summary()

    async def _try_copy_post(self, chat_id: int):
        try:
            await self._post.copy_to(chat_id)
        except RetryAfter as e:
            self._summary.floods += 1
            await asyncio.sleep(e.timeout)
        except TelegramAPIError:
            self._summary.errors += 1
        else:
            self._summary.delivered += 1
        finally:
            await asyncio.sleep(self.INTERVAL)

    def _send_summary(self):
        return self._post.answer(self._summary.text)


@dataclass
class Summary:
    delivered: int = 0
    floods: int = 0
    errors: int = 0

    @property
    def text(self) -> str:
        return summary_text.format(
            delivered_count=self.delivered,
            floods_count=self.floods,
            errors_count=self.errors,
        )


summary_text = f"""
{bold("Рассылка окончена")}

Сообщений доставлено: {{delivered_count}}
Ошибок флуда: {{floods_count}}
Другие ошибки: {{errors_count}}
"""
