from typing import Optional

import discord

from config import PRISON_CHANNEL_ID
from src.utils.discd import unmute
from src.client.global_client import GlobalClient
from src.service.voice.execution import Execution


class MyHandler:
    PRISON_CHANNEL: Optional[discord.VoiceChannel] = None

    def __init__(self, me: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        MyHandler.static_checker()

        self.me: discord.Member = me
        self.before: discord.VoiceState = before
        self.after: discord.VoiceState = after

    @classmethod
    def static_checker(cls):
        if cls.PRISON_CHANNEL is None:
            cls.PRISON_CHANNEL = GlobalClient.client.get_channel(PRISON_CHANNEL_ID)

    async def handle(self):
        if self.after.mute:
            await unmute(self.me)

        if self.after.channel is None:
            Execution.disconnected()
            return

        if self.after.channel.id == PRISON_CHANNEL_ID:
            return
        else:
            await self.me.move_to(MyHandler.PRISON_CHANNEL)
