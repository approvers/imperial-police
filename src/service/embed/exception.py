from typing import Union, Optional
import logging

import discord

from config import ERROR_CROSS_URL
from src.utils.discd import get_user_icon_url
from src.client.global_client import GlobalClient


class ExceptionEmbedFactory:
    MY_AVATAR_URL: Optional[str] = None

    def __init__(self) -> None:
        ExceptionEmbedFactory.static_check()

    @classmethod
    def static_check(cls):
        if cls.MY_AVATAR_URL is None:
            cls.MY_AVATAR_URL = get_user_icon_url(GlobalClient.client.user)

    def make(self, caught_error: Exception) -> discord.Embed:
        embed: discord.Embed = discord.Embed(
            title="例外が発生あそばされました",
            color=0xed2102
        )

        embed.set_author(name="皇宮警察からのお知らせ", icon_url=ExceptionEmbedFactory.MY_AVATAR_URL)
        embed.set_thumbnail(url=ERROR_CROSS_URL)

        embed.add_field(name="例外の内容", value="```\n{}\n```".format(caught_error))

        return embed
