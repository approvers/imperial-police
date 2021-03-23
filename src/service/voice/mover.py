from typing import Optional
from abc import ABC

import discord

from config import PRISON_CHANNEL_ID, EXECUTION_REASON
from src.service.voice.voice_abs import VoiceFunctionAbstract
from src.service.misc.royal_judge import RoyalJudge
from src.client.global_client import GlobalClient


class Mover(VoiceFunctionAbstract, ABC):
    PRISON_CHANNEL: Optional[discord.VoiceChannel] = None

    @classmethod
    def static_check(cls):
        if cls.PRISON_CHANNEL is None:
            cls.PRISON_CHANNEL = GlobalClient.client.get_channel(PRISON_CHANNEL_ID)

    def __init__(self, member: discord.Member, after: discord.VoiceState, is_join: bool):
        Mover.static_check()

        self._is_triggered: bool = False

        self.member: discord.Member = member
        self.after: discord.VoiceState = after
        self.is_join: bool = is_join

    def is_triggered(self) -> bool:
        self._is_triggered = False

        if not self.is_join:
            return self._is_triggered

        if self.after.channel.id != RoyalJudge.get_royal_room().id:
            return self._is_triggered

        if RoyalJudge.is_royal_family_member_from_id(self.member.id):
            return self._is_triggered

        self._is_triggered = True
        return self._is_triggered

    async def execute(self):
        await self.member.move_to(Mover.PRISON_CHANNEL, reason=EXECUTION_REASON)
