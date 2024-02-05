from dataclasses import asdict
from datetime import datetime
from uuid import uuid4

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from matte.config import Config
from matte.db.models import PostUrl
from matte.db.models import Source
from matte.db.models import User


class DatabaseService:
    def __init__(self, session: AsyncSession, config: Config) -> None:
        self.session = session
        self.config = config

    async def get_user(self, user_id: int) -> User:
        cursor = await self.session.execute(select(User).where(User.id == user_id))
        return cursor.unique().scalar_one()

    async def create_user(self, user_id: int, chat_id: int) -> User:
        user = User(
            id=user_id,
            chat_id=chat_id,
            settings={field: value for field, value in asdict(self.config.default_user_settings).items()},
            sources=[],
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_or_create_user(self, user_id: int, chat_id: int) -> User:
        try:
            return await self.get_user(user_id)
        except NoResultFound:
            return await self.create_user(user_id, chat_id)

    async def delete_user(self, user_id: int) -> None:
        await self.session.execute(delete(User).where(User.id == user_id))

    async def get_source_by_id(self, source_id: int) -> Source:
        cursor = await self.session.execute(select(Source).where(Source.id == source_id))
        return cursor.scalar_one()

    async def get_user_source_by_link(self, user: User, source_link: str) -> Source:
        cursor = await self.session.execute(
            select(Source).where((Source.link == source_link) & (Source.user_id == user.id))
        )
        return cursor.unique().scalar_one()

    async def list_sources(self, user: User | None = None) -> list[Source]:
        select_statement = select(Source)
        filters = Source.is_disabled == False

        if user is not None:
            filters &= Source.user_id == user.id

        select_statement = select_statement.where(filters)
        cursor = await self.session.execute(select_statement)
        return list(cursor.unique().scalars().all())

    async def create_source(
        self,
        name: str,
        link: str,
        home_link: str,
        user: User,
        last_updated: datetime | None = None,
    ) -> Source:
        source = Source(
            name=name,
            link=link,
            home_link=home_link,
            user=user,
            last_updated=last_updated or datetime.now(),
        )
        self.session.add(source)
        await self.session.flush()
        return source

    async def delete_source(self, source_id: int) -> None:
        await self.session.execute(delete(Source).where(Source.id == source_id))

    async def get_url(self, url_id: str) -> str:
        cursor = await self.session.execute(select(PostUrl).where(PostUrl.id == url_id))
        result = cursor.scalar_one()
        return result.url

    async def create_url(self, url: str) -> str:
        entity = PostUrl(id=str(uuid4()), url=url)
        self.session.add(entity)
        await self.session.flush()
        return entity.id

    async def delete_url(self, url_id: str) -> None:
        await self.session.execute(delete(PostUrl).where(PostUrl.id == url_id))
