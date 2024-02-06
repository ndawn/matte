from dataclasses import fields

from aiogram import html
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup
from feedparser import FeedParserDict

from matte.db.models import Source
from matte.db.models import User
from matte.translations import languages
from matte.translations import translations
from matte.utils import SelectLanguage
from matte.utils import SettingsUpdate
from matte.utils import SummarizePost
from matte.utils import UserSettings


class TextBuilder:
    def __init__(self, sample_post: FeedParserDict, user: User) -> None:
        self.sample_post = sample_post
        self.user = user

    @property
    def yes(self) -> str:
        return "🟢"

    @property
    def no(self) -> str:
        return "🔴"

    @property
    def select_language(self) -> str:
        return translations[self.user.language]["select_language"]

    @property
    def select_language_prompt(self) -> str:
        return translations[self.user.language]["select_language_prompt"]

    @property
    def welcome(self) -> str:
        return translations[self.user.language]["welcome"]

    @property
    def invalid_url(self) -> str:
        return translations[self.user.language]["invalid_url"]

    @property
    def invalid_feed(self) -> str:
        return translations[self.user.language]["invalid_feed"]

    @property
    def unable_to_get_feed(self) -> str:
        return translations[self.user.language]["unable_to_get_feed"]

    @property
    def summarization_unavailable(self) -> str:
        return translations[self.user.language]["summarization_unavailable"]

    def subscribed(self, feed: FeedParserDict) -> str:
        return (
            f"{translations[self.user.language]['subscribed']} "
            f"{html.link(html.bold(feed.title), feed.link)}!"
        )

    @property
    def unsubscribed(self) -> str:
        return translations[self.user.language]["unsubscribed"]

    @property
    def last_update(self) -> str:
        return translations[self.user.language]["last_update"]

    @property
    def no_last_update(self) -> str:
        return translations[self.user.language]["no_last_update"]

    @property
    def settings_list(self) -> str:
        return translations[self.user.language]["settings_list"]

    @property
    def sample_post_preview(self) -> str:
        return translations[self.user.language]["sample_post_preview"]

    def settings_markup(self, settings: dict[str, bool]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        for field in fields(UserSettings):
            keyboard.button(
                text=self.setting(translations[self.user.language]["settings"][field.name], settings[field.name]),
                callback_data=SettingsUpdate(field_name=field.name).pack(),
            )

        keyboard.button(
            text=self.select_language,
            callback_data=SettingsUpdate(field_name="language").pack(),
        )

        keyboard.adjust(1)
        return keyboard.as_markup()

    def post(self, entry: FeedParserDict, feed_name: str) -> str:
        result = ""

        if self.user.settings["feed_name"]:
            result += html.bold(feed_name) + "\n"

        if self.user.settings["post_name"]:
            if self.user.settings["post_link_in_post_name"]:
                result += html.bold(html.link(entry.title, entry.link)) + "\n"
            else:
                result += html.bold(entry.title) + "\n"

        if not self.user.settings["post_name"] or not self.user.settings["post_link_in_post_name"]:
            result += html.link(entry.link, entry.link)

        return result.rstrip()

    def post_summary_markup(self, url: str) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(
            text=translations[self.user.language]["summarize_post"],
            callback_data=SummarizePost(link=url).pack(),
        )
        return keyboard.as_markup()

    @property
    def language_list_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        for language, display_name in languages.items():
            keyboard.button(
                text=display_name,
                callback_data=SelectLanguage(language=language).pack(),
            )

        keyboard.button(
            text=translations[self.user.language]["go_back"],
            callback_data=SelectLanguage(language="go_back").pack(),
        )

        keyboard.adjust(2)
        return keyboard.as_markup()

    def add_summary(self, text: str, summary: str) -> str:
        return f"{text}\n\n{translations[self.user.language]['summary']}:\n{summary}"

    def source_list(self, sources: list[Source]) -> str:
        if not sources:
            return translations[self.user.language]["no_subscriptions"]

        result = f"{translations[self.user.language]['your_subscriptions']}:\n"

        for index, source in enumerate(sources, start=1):
            result += f"{index}. {html.link(html.bold(source.name), source.home_link)} — {html.code(source.link)}\n"

        result += translations[self.user.language]["unsubscribe_prompt"]
        return result

    def setting(self, name: str, value: bool) -> str:
        return f"{self.yes if value else self.no} {name}"

    def setting_updated(self, name: str, value: bool) -> str:
        result = translations[self.user.language]["setting_enabled" if value else "setting_disabled"] + ":\n"
        result += html.bold(translations[self.user.language]["settings"].get(name, ""))
        return result.rstrip()
