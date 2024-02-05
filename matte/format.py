from dataclasses import fields

from aiogram import html
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup
from feedparser import FeedParserDict

from matte.db.models import Source
from matte.db.models import User
from matte.utils import SettingsUpdate
from matte.utils import SummarizePost
from matte.utils import UserSettings


class TextBuilder:
    def __init__(self, sample_post: FeedParserDict) -> None:
        self.sample_post = sample_post

    @property
    def yes(self) -> str:
        return "🟢"

    @property
    def no(self) -> str:
        return "🔴"

    @property
    def welcome(self) -> str:
        return (
            f"🔘 Welcome to Matte!\n\n"
            "Start by providing me any links to RSS feeds. "
            "Go ahead and just send me a message with link (one at a time)."
        )

    @property
    def invalid_url(self) -> str:
        return "Please provide a valid URL to an RSS feed"

    @property
    def invalid_feed(self) -> str:
        return "Target resource is not a valid feed"

    @property
    def unable_to_get_feed(self) -> str:
        return "I'm currently unable to get a feed from this source, please try again later"

    @property
    def summarization_unavailable(self) -> str:
        return "Summarization is unavailable for this post"

    def subscribed(self, feed: FeedParserDict) -> str:
        return (
            "Successfully subscribed to "
            f"{html.link(html.bold(feed.title), feed.link)}!"
        )

    @property
    def unsubscribed(self) -> str:
        return "Successfully unsubscribed from a feed!"

    @property
    def last_update(self) -> str:
        return "Last update in this feed:"

    @property
    def no_last_update(self) -> str:
        return "There are no recent updates in this feed at the moment, but I'll send you any once they appear!"

    @property
    def settings_list(self) -> str:
        return "Here's the list of settings:"

    @property
    def sample_post_preview(self) -> str:
        return "Posts will appear like this:"

    def settings_markup(self, settings: dict[str, bool]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        for field in fields(UserSettings):
            keyboard.button(
                text=self.setting(field.metadata["description"], settings[field.name]),
                callback_data=SettingsUpdate(field_name=field.name).pack(),
            )

        keyboard.adjust(1)
        return keyboard.as_markup()

    def post(self, entry: FeedParserDict, feed_name: str, user: User) -> str:
        result = ""

        if user.settings["feed_name"]:
            result += html.bold(feed_name) + "\n"

        if user.settings["post_name"]:
            if user.settings["post_link_in_post_name"]:
                result += html.bold(html.link(entry.title, entry.link)) + "\n"
            else:
                result += html.bold(entry.title) + "\n"

        if not user.settings["post_name"] or not user.settings["post_link_in_post_name"]:
            result += html.link(entry.link, entry.link)

        return result.rstrip()

    def post_summary_markup(self, url: str) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Summarize post", callback_data=SummarizePost(link=url).pack())
        return keyboard.as_markup()

    def add_summary(self, text: str, summary: str) -> str:
        return f"{text}\n\nSummary:\n{summary}"

    def source_list(self, sources: list[Source]) -> str:
        if not sources:
            return "You have no subscriptions at the moment. Send me a link to subscribe to a feed!"

        result = "Your subscriptions:\n"

        for index, source in enumerate(sources, start=1):
            result += f"{index}. {html.link(html.bold(source.name), source.home_link)} — {html.code(source.link)}\n"

        result += "Send the link again to unsubscribe from a feed."
        return result

    def setting(self, name: str, value: bool) -> str:
        return f"{self.yes if value else self.no} {name}"

    def setting_updated(self, name: str, value: bool) -> str:
        result = "Enabled " if value else "Disabled "

        for field in fields(UserSettings):
            if field.name == name:
                result += html.bold(field.metadata["description"])

        return result.rstrip()
