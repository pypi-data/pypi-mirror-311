from typing import Sequence

from aiogram import Bot

from asgi_aiogram.strategy.base import BaseStrategy
from asgi_aiogram.types import ScopeType


class SingleStrategy(BaseStrategy):
    def __init__(self, path: str, bot: Bot):
        self._path = path
        self._bot = bot

    def verify_path(self, path: str) -> bool:
        return self._path == path

    async def resolve_bot(self, scope: ScopeType) -> Bot | None:
        return self._bot

    async def shutdown(self):
        await self._bot.session.close()

    @property
    def bots(self) -> Sequence[Bot]:
        return [self._bot]

    @property
    def bot(self) -> Bot | None:
        return self._bot