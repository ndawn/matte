import asyncio
from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime

import feedparser
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter
from aiogram.utils.keyboard import InlineKeyboardMarkup
from contextlib import suppress
from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine

from matte.config import Config
from matte.db.service import DatabaseService
from matte.format import TextBuilder
from matte.utils import get_feed
from matte.utils import get_publication_date


class FeedPoller:
    def __init__(self, bot: Bot, db_engine: AsyncEngine, config: Config) -> None:
        self.bot = bot
        self.session_class = async_sessionmaker(db_engine)
        self.config = config

    async def send_with_retry(self, chat_id: int, text: str, reply_markup: InlineKeyboardMarkup | None) -> None:
        try:
            await self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except TelegramRetryAfter as exception:
            await asyncio.sleep(exception.retry_after)
            await self.send_with_retry(chat_id, text, reply_markup)

    async def poll(self) -> None:
        while True:
            logger.debug(f"Sleeping for {self.config.poll_interval} seconds")
            await asyncio.sleep(self.config.poll_interval)

            logger.debug("Starting feed polling...")

            async with self.session_class() as session:
                try:
                    service = DatabaseService(session, self.config)
                    sources = await service.list_sources()

                    source_map = defaultdict(list)
                    per_user_updates = defaultdict(list)
                    user_map = {}

                    for source in sources:
                        source_map[source.link].append(source)

                        if source.user.id not in user_map:
                            user_map[source.user.id] = source.user

                    feed_map = list(source_map.keys())
                    feed_map = {
                        key: value
                        for key, value in zip(feed_map, await asyncio.gather(*(get_feed(url) for url in feed_map)))
                    }

                    for source_link, sources in source_map.items():
                        for source in sources:
                            new_updates = sorted(
                                filter(
                                    lambda entry_: self.is_later(entry_, source.last_updated),
                                    feed_map[source_link].entries,
                                ),
                                key=get_publication_date,
                                reverse=True,
                            )

                            per_user_updates[source.user_id].extend(
                                map(lambda entry_: (feed_map[source_link].feed, entry_), new_updates)
                            )

                            if new_updates:
                                source.last_updated = get_publication_date(new_updates[0])

                    for user_id, updates in per_user_updates.items():
                        try:
                            text = TextBuilder(sample_post=sample_post, user=user_map[user_id])

                            for update in sorted(updates, key=lambda update_: get_publication_date(update_[1])):
                                url_id = None

                                if self.config.summarization_enabled:
                                    url_id = await service.create_url(update[1].link)

                                await self.send_with_retry(
                                    chat_id=user_map[user_id].chat_id,
                                    text=text.post(entry=update[1], feed_name=update[0].title),
                                    reply_markup=(
                                        text.post_summary_markup(url_id)
                                        if url_id is not None else None
                                    ),
                                )
                        except Exception as exception:
                            logger.error("Encountered an exception while processing update")
                            logger.exception(exception)

                    await session.commit()
                except Exception as exception:
                    logger.error("Caught an exception while polling feeds:")
                    logger.exception(exception)

    @staticmethod
    def is_later(entry: feedparser.FeedParserDict, date: datetime) -> bool:
        entry_date = get_publication_date(entry)
        return entry_date is not None and entry_date > date


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("config_path")
    args = parser.parse_args()

    app_config = Config.load(args.config_path)

    with open(app_config.sample_post_path) as sample_post_file:
        sample_post = feedparser.parse(sample_post_file.read())

    bot_instance = Bot(app_config.bot_token, parse_mode=ParseMode.HTML)
    engine = create_async_engine(app_config.db_url, echo=app_config.db_echo)
    poller = FeedPoller(bot_instance, engine, app_config)

    with suppress(asyncio.CancelledError):
        asyncio.run(poller.poll())
