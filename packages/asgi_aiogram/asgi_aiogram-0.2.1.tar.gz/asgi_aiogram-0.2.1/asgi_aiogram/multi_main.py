from asyncio import create_task
from logging import getLogger
from typing import Any

from aiogram import Dispatcher
from aiogram.types import Update

from asgi_aiogram.aliases import Receiver, Sender
from asgi_aiogram.asgi import read_body
from asgi_aiogram.responses import ok, error, not_found
from asgi_aiogram.strategy import BaseStrategy
from asgi_aiogram.types import ScopeType


class MultiStrategyASGIAiogram:
    def __init__(self,
        strategy_map: dict[BaseStrategy, Dispatcher],
        handle_as_tasks: bool = True,
        handle_signals: bool = True,
        **kwargs: Any
    ):
        self.strategy_map = strategy_map
        self.handle_as_tasks = handle_as_tasks
        self.handle_signals = handle_signals
        self.kwargs_map = {}
        for dispatcher in strategy_map.values():
            self.kwargs_map[dispatcher] = {
                "dispatcher": dispatcher,
                **dispatcher.workflow_data,
                **kwargs,
            }
            self.kwargs_map[dispatcher].pop("bot", None)

        self.logger = getLogger("asgi_aiogram")
        self.task_list = set()
        self.resolve_chance = {}

    def resolve_dispatcher(self, path: str) -> BaseStrategy | None:
        if path not in self.resolve_chance:
            for strategy in self.strategy_map:
                if strategy.verify_path(path=path):
                    self.resolve_chance[path] = strategy
                    return strategy
            return None
        return self.resolve_chance[path]



    async def post(self, scope: ScopeType, receive: Receiver, send: Sender):
        strategy = self.resolve_dispatcher(path=scope["path"])
        if strategy is None:
            self.logger.warning("unknown path: %s", scope['path'])
            await not_found(send=send)
            return
        dispatcher = self.strategy_map[strategy]

        bot = await strategy.resolve_bot(scope=scope)
        if bot is None:
            self.logger.warning("unknown bot for: %s", scope['path'])
            await not_found(send=send)
            return
        try:
            cor = dispatcher.feed_update(
                bot=bot,
                update=Update.model_validate_json(await read_body(receive)),
                **self.kwargs_map[dispatcher],
            )
            if self.handle_as_tasks:
                handle_update_task = create_task(cor)
                self.task_list.add(handle_update_task)
                handle_update_task.add_done_callback(self.task_list.discard)
            else:
                await cor
                # if isinstance(response, TelegramMethod):
                #     form = bot.session.build_form_data(bot, response)
                #     form.add_field(
                #         name="method",
                #         value=response.__api_method__
                #     )
                #     await answer(send, form)
            await ok(send=send)
            return
        except Exception as e:
            self.logger.error(e)
            await error(send=send)
        return

    async def get(self, scope: ScopeType, receive: Receiver, send: Sender):
        pass

    async def lifespan(self, scope: ScopeType, receive: Receiver, send: Sender):
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                try:
                    for strategy, dispatcher in self.strategy_map.items():
                        await dispatcher.emit_startup(
                            **self.kwargs_map[dispatcher],
                            bots=strategy.bots,
                            bot=strategy.bot,
                            scope=scope,
                            strategy=strategy,
                        )
                        await strategy.startup()
                except Exception as e:
                    self.logger.error(e)
                    await send({'type': 'lifespan.startup.failed'})
                else:
                    await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                try:
                    for strategy, dispatcher in self.strategy_map.items():
                        await dispatcher.emit_shutdown(
                            **self.kwargs_map[dispatcher],
                            bots=strategy.bots,
                            bot=strategy.bot,
                            scope=scope,
                            strategy=strategy,
                        )
                        await strategy.shutdown()
                except Exception as e:
                    self.logger.error(e)
                    await send({'type': 'lifespan.shutdown.failed'})
                    return
                else:
                    await send({'type': 'lifespan.shutdown.complete'})
                    return

            else:
                self.logger.warning("unknown lifespan type: %s", message['type'])

    async def http(self, scope: ScopeType, receive: Receiver, send: Sender):
        if scope["method"] == "POST":
            return await self.post(scope=scope, receive=receive, send=send)
        if scope["method"] == "GET":
            return await self.get(scope=scope, receive=receive, send=send)
        self.logger.info("unsupported method: %s", scope['type'])



    async def __call__(self, scope: ScopeType, receive: Receiver, send: Sender):
        if scope['type'] == 'http':
            return await self.http(scope=scope, receive=receive, send=send)
        if scope['type'] == 'lifespan':
            return await self.lifespan(scope=scope, receive=receive, send=send)
        self.logger.warning("unsupported event type:", scope['type'])