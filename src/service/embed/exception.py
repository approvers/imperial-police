from typing import Optional

import discord

from config import ERROR_CROSS_URL, MAINTAINER_DISCORD_ID
from src.exception.misunderstanding import MisunderstandingException
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
            title="お例外が発生あそばされました",
            color=0xed2102
        )

        embed.set_author(name="皇宮警察からのお知らせ", icon_url=ExceptionEmbedFactory.MY_AVATAR_URL)
        embed.set_thumbnail(url=ERROR_CROSS_URL)

        embed.add_field(name="例外の内容", value="```\n{}\n```".format(caught_error))

        if type(caught_error) is MisunderstandingException:
            embed.description = "この例外は <@!{}> が仕様を適当に推測して実装した箇所で、".format(MAINTAINER_DISCORD_ID) + \
                                "起こらないと思っていた事態が起こっていることを示しています。"

        return embed
