from dataclasses import dataclass
from datetime import datetime
from time import mktime

import feedparser
from aiogram.filters.callback_data import CallbackData
from aiohttp.client import ClientSession


@dataclass
class UserSettings:
    feed_name: bool
    post_name: bool
    post_link_in_post_name: bool
    show_preview: bool


class SummarizePost(CallbackData, prefix="s", sep="|"):
    link: str


class SelectLanguage(CallbackData, prefix="lang"):
    language: str


class SettingsUpdate(CallbackData, prefix="settings_update"):
    field_name: str


async def get_feed(url: str) -> feedparser.FeedParserDict:
    async with ClientSession(trust_env=True) as session:
        async with session.get(url) as response:
            if response.content_length is not None and response.content_length > 1_000_000:  # yay, magic numbers
                raise RuntimeError("Content length is too big")

            text = b""

            while not response.content.is_eof():
                text += await response.content.read(4096)

                if len(text) > 1_000_000:
                    raise RuntimeError("Content length is too big")

            return feedparser.parse(text.decode("utf-8"), response_headers=response.headers)


def get_publication_date(entry: feedparser.FeedParserDict) -> datetime | None:
    if hasattr(entry, "published_parsed"):
        date = entry.published_parsed
    elif hasattr(entry, "updated_parsed"):
        date = entry.updated_parsed
    else:
        date = None

    if date is not None:
        date = datetime.fromtimestamp(mktime(date))

    return date
