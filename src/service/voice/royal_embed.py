from abc import ABC
from typing import Optional

import discord

from config import MESSAGE_CHANNEL_ID, ROYAL_ROOM_ID
from src.service.voice.voice_abs import VoiceFunctionAbstract
from src.service.embed.embed_factory import EmbedFactory
from src.service.misc.royal_judge import RoyalJudge
from src.client.global_client import GlobalClient


class RoyalEmbed(VoiceFunctionAbstract, ABC):
    MESSAGE_CHANNEL: Optional[discord.TextChannel] = None

    def __init__(
            self,
            before: discord.VoiceState,
            after: discord.VoiceState,
            member: discord.Member,
            is_join: Optional[bool]
    ):
        RoyalEmbed.static_check()

        self._is_triggered = False
        self.before: discord.VoiceState = before
        self.after: discord.VoiceState = after
        self.member: discord.Member = member
        self.is_join: Optional[bool] = is_join

    @classmethod
    def static_check(cls):
        if cls.MESSAGE_CHANNEL is None:
            cls.MESSAGE_CHANNEL = GlobalClient.client.get_channel(MESSAGE_CHANNEL_ID)

    def is_triggered(self) -> bool:
        self._is_triggered = False

        if not RoyalJudge.is_royal_family_member_from_id(self.member.id):
            return self._is_triggered

        if self.is_join is None:
            return self._is_triggered

        if self.after.channel is None:
            if self.before.channel.id == ROYAL_ROOM_ID:
                self._is_triggered = True
                return self._is_triggered
        else:
            if self.after.channel.id == ROYAL_ROOM_ID:
                self._is_triggered = True
                return self._is_triggered

    async def execute(self):
        embed: discord.Embed = EmbedFactory().make(self.member, self.is_join)
        await RoyalEmbed.MESSAGE_CHANNEL.send(embed=embed)
