from urllib.parse import urlparse

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.types import Message
from loguru import logger

from matte.db.models import User
from matte.db.service import DatabaseService
from matte.format import TextBuilder
from matte.utils import get_feed
from matte.utils import SettingsUpdate


dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def on_start_command(message: Message, text: TextBuilder) -> None:
    await message.answer(text.welcome)


@dispatcher.message(Command("list"))
async def get_source_list(message: Message, user: User, text: TextBuilder) -> None:
    await message.answer(text.source_list(user.sources), disable_web_page_preview=True)


@dispatcher.message(Command("settings"))
async def get_settings(message: Message, user: User, text: TextBuilder) -> None:
    await message.answer(text.settings_list, reply_markup=text.settings_markup(user.settings))


@dispatcher.callback_query(SettingsUpdate.filter())
async def update_settings(
    query: CallbackQuery,
    callback_data: SettingsUpdate,
    user: User,
    text: TextBuilder,
) -> None:
    new_value = user.toggle_setting(callback_data.field_name)

    await query.message.edit_text(text.setting_updated(callback_data.field_name, new_value))
    await query.message.answer(text.sample_post_preview)

    await query.message.answer(
        text.post(entry=text.sample_post.entries[0], feed_name=text.sample_post.feed.title, user=user),
        disable_web_page_preview=not user.settings["show_preview"],
    )

    await query.message.answer(text.settings_list, reply_markup=text.settings_markup(user.settings))


@dispatcher.message()
async def process_source_link(
    message: Message,
    db: DatabaseService,
    user: User,
    text: TextBuilder,
) -> None:
    try:
        link = urlparse(message.text)

        if not link.scheme or not link.netloc:
            await message.answer(text.invalid_url)
            return
    except ValueError:
        await message.answer(text.invalid_url)
        return

    feed = await get_feed(message.text)

    try:
        source = await db.get_user_source_by_link(user, message.text)
        await db.delete_source(source.id)
        await message.answer(text.unsubscribed)
        return
    except Exception as exception:
        logger.debug(exception)

    if not feed.feed or not hasattr(feed.feed, "title") or not hasattr(feed.feed, "link"):
        if feed.bozo:
            logger.debug(feed.bozo_exception)

        logger.debug(feed)
        await message.answer(text.invalid_feed)
        return

    await db.create_source(name=feed.feed.title, link=message.text, home_link=feed.feed.link, user=user)
    await message.answer(text.subscribed(feed.feed), disable_web_page_preview=True)

    if feed.entries:
        await message.answer(text.last_update)
        await message.answer(
            text.post(entry=feed.entries[0], feed_name=feed.feed.title, user=user),
            disable_web_page_preview=not user.settings["show_preview"],
        )
    else:
        await message.answer(text.no_last_update)
