from typing import Any
from typing import Awaitable
from typing import Callable

from aiogram import BaseMiddleware
from aiogram.enums import UpdateType
from aiogram.types import Update
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine

from matte.db.service import DatabaseService
from matte.format import TextBuilder


class ContextMiddleware(BaseMiddleware):
    def __init__(self, engine: AsyncEngine) -> None:
        self.session_class = async_sessionmaker(engine)

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        async with self.session_class() as session:
            data["db"] = DatabaseService(session, data["config"])

            if event.event_type == UpdateType.CALLBACK_QUERY:
                user_id = event.callback_query.from_user.id
                chat_id = event.callback_query.message.chat.id
            else:
                user_id = event.message.from_user.id
                chat_id = event.message.chat.id

            data["user"] = await data["db"].get_or_create_user(user_id, chat_id)
            data["text"] = TextBuilder(sample_post=data["sample_post"], user=data["user"])

            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
