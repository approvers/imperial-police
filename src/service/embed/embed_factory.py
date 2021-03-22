from typing import Union, Optional
import logging

import discord

from config import ROYAL_EMBLEM_URL


class EmbedFactory:
    _MY_AVATAR_URL: str = None
    _BASE_EMBED: Optional[discord.Embed]

    def __init__(self) -> None:
        pass

    def make(self, member: discord.Member, is_join: bool) -> discord.Embed:
        embed: discord.Embed = EmbedFactory._BASE_EMBED

        customize_message: str
        if is_join:
            customize_message = "還幸"
        else:
            customize_message = "行幸"

        embed.title = "†卍 {} 卍† ".format(customize_message)
        embed.description = "{} が{}なさいました。".format(member.display_name, customize_message)

        return embed

    @classmethod
    def static_init(cls, my_client_user: discord.ClientUser):
        cls._MY_AVATAR_URL: str = EmbedFactory._get_user_icon_url(my_client_user)
        cls._BASE_EMBED: discord.Embed = cls._make_base_embed

    @staticmethod
    def _make_base_embed(self, member: discord.Member) -> discord.Embed:
        embed = discord.Embed(
            color=0xffd800
        )
        embed.set_author(
            name="皇宮警察からのお知らせ",
            icon_url=EmbedFactory._MY_AVATAR_URL
        )
        embed.set_thumbnail(url=ROYAL_EMBLEM_URL)

        return embed

    @staticmethod
    def _check_if_my_avatar_is_set() -> bool:
        if EmbedFactory._MY_AVATAR_URL is None or EmbedFactory == "":
            logging.warning(
                "MY_AVATAR_URL is not specified. Make sure you have called 'EmbedFactory.set_my_avatar_url'."
            )

    @staticmethod
    def _get_user_icon_url(user: Union[discord.Member, discord.ClientUser]) -> str:
        return "https://cdn.discordapp.com/avatars/{}/{}.png".format(user.id, user.avatar)
