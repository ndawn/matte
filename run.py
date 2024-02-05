import asyncio
import os
from argparse import ArgumentParser
from contextlib import suppress

import feedparser
from aiogram import Bot
from aiogram.enums import ParseMode
from loguru import logger
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import create_async_engine

from matte.dispatcher import dispatcher
from matte.middleware import ContextMiddleware
from matte.config import Config


parser = ArgumentParser()
parser.add_argument("config_path")


async def main() -> None:
    args = parser.parse_args()

    config_path = os.path.join(os.path.abspath(os.curdir), args.config_path)
    config = Config.load(config_path)

    bot = Bot(config.bot_token, parse_mode=ParseMode.HTML)

    engine = create_async_engine(config.db_url, echo=config.db_echo)
    context_middleware = ContextMiddleware(engine)
    dispatcher.update.outer_middleware(context_middleware)

    dispatcher.workflow_data["config"] = config
    dispatcher.workflow_data["openai"] = AsyncOpenAI(api_key=config.openai_api_key)

    with open("sample.xml") as sample_post_file:
        dispatcher.workflow_data["sample_post"] = feedparser.parse(sample_post_file.read())

    logger.info("Starting bot...")

    with suppress(asyncio.CancelledError):
        await dispatcher.start_polling(bot)

    logger.info("Stopping bot...")


if __name__ == "__main__":
    asyncio.run(main())
