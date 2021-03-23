from typing import Optional

import discord

from config import ROYAL_EMBLEM_URL
from src.utils.discd import get_user_icon_url
from src.client.global_client import GlobalClient


class EmbedFactory:
    MY_AVATAR_URL: Optional[str] = None
    BASE_EMBED: Optional[discord.Embed] = None

    def __init__(self) -> None:
        EmbedFactory.static_check()

    @classmethod
    def static_check(cls):
        if cls.MY_AVATAR_URL is None:
            cls.MY_AVATAR_URL = get_user_icon_url(GlobalClient.client.user)
        if cls.BASE_EMBED is None:
            cls.BASE_EMBED = cls._make_base_embed()

    def make(self, member: discord.Member, is_join: bool) -> discord.Embed:
        embed: discord.Embed = EmbedFactory.BASE_EMBED

        customize_message: str
        if is_join:
            customize_message = "還幸"
        else:
            customize_message = "行幸"

        embed.title = "†卍 {} 卍†".format(customize_message)
        embed.description = "{} が{}なさいました。".format(member.display_name, customize_message)

        return embed

    @staticmethod
    def _make_base_embed() -> discord.Embed:
        embed = discord.Embed(
            color=0xffd800
        )
        embed.set_author(
            name="皇宮警察からのお知らせ",
            icon_url=EmbedFactory.MY_AVATAR_URL
        )
        embed.set_thumbnail(url=ROYAL_EMBLEM_URL)

        return embed
