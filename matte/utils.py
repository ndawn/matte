import zlib
from base64 import b64decode
from base64 import b64encode
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from time import mktime

import feedparser
from aiogram.filters.callback_data import CallbackData
from aiohttp.client import ClientSession


@dataclass
class UserSettings:
    feed_name: bool = field(metadata={"description": "Display a feed title"})
    post_name: bool = field(metadata={"description": "Display a post title"})
    post_link_in_post_name: bool = field(metadata={"description": "Embed a post link into post name"})
    show_preview: bool = field(metadata={"description": "Show page preview"})


class SummarizePost(CallbackData, prefix="s"):
    link: str


class SettingsUpdate(CallbackData, prefix="settings_update"):
    field_name: str


async def get_feed(url: str) -> feedparser.FeedParserDict:
    async with ClientSession() as session:
        async with session.get(url) as response:
            return feedparser.parse(await response.text(), response_headers=response.headers)


def compress_link(url: str) -> str:
    return b64encode(zlib.compress(url.encode("utf-8"))).decode("utf-8")


def decompress_link(url: str) -> str:
    return b64decode(zlib.decompress(url.encode("utf-8"))).decode("utf-8")


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
