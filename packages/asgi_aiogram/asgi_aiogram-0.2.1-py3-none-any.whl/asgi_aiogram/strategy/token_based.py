from asyncio import gather
from typing import Any, Sequence

from aiogram import Bot

from asgi_aiogram.path_normalization import split_path_by_token_placeholder
from asgi_aiogram.strategy.base import BaseStrategy
from asgi_aiogram.types import ScopeType


class TokenBasedStrategy(BaseStrategy):
    def __init__(self, path: str, bot_settings: dict[str, Any]):
        self._path_prefix, self._slice, self._path_postfix = split_path_by_token_placeholder(path)
        self._bots: dict[str, Bot] = {}
        self._bot_settings = bot_settings

    def verify_path(self, path: str) -> bool:
        if not path.startswith(self._path_prefix):
            return False
        if not path.endswith(self._path_postfix):
            return False
        return True

    async def resolve_bot(self, scope: ScopeType) -> Bot | None:
        token = scope["path"][self._slice]
        if token not in self._bots:
            self._bots[token] = Bot(token=token, **self._bot_settings)
        return self._bots[token]

    async def shutdown(self):
        await gather(*(bot.session.close() for bot in self._bots.values()))

    @property
    def bots(self) -> Sequence[Bot]:
        return list(self._bots.values())
