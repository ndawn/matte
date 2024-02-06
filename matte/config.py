import os
import tomllib
from dataclasses import dataclass
from typing import Self

from matte.utils import UserSettings


@dataclass
class Config:
    db_url: str
    db_echo: bool
    bot_token: str
    openai_api_key: str
    poll_interval: int
    sample_post_path: str
    default_language: str
    default_user_settings: UserSettings
    summarization_enabled: bool
    summarization_model: str
    summarization_prompt: str

    @classmethod
    def load(cls, path: str | os.PathLike) -> Self:
        with open(path, "rb") as config_file:
            raw_config = tomllib.load(config_file)
            default_user_settings = UserSettings(**raw_config.pop("default_user_settings"))
            return cls(**raw_config, default_user_settings=default_user_settings)
