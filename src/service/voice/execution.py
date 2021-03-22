import asyncio
from abc import ABC
from typing import Optional

import discord

from config import EXECUTION_REASON, NATIONAL_ANTHEM, VC_STAY_LENGTH, PRISON_CHANNEL_ID, ROYAL_ROOM_ID
from src.service.voice.voice_abs import VoiceFunctionAbstract
from src.service.misc.royal_judge import RoyalJudge
from src.client.global_client import GlobalClient


class Execution(VoiceFunctionAbstract, ABC):
    IS_EXECUTING: bool = False
    PRISON_CHANNEL: Optional[discord.VoiceChannel] = None

    @classmethod
    def disconnected(cls):
        cls.IS_EXECUTING = False

    def __init__(self, member: discord.Member, after: discord.VoiceState, is_join: bool):
        Execution.static_check()

        self.member: discord.Member = member
        self.is_join: bool = is_join
        self.after: discord.VoiceState = after
        self._is_triggered: Optional[bool] = False

    @classmethod
    def static_check(cls):
        if cls.PRISON_CHANNEL is None:
            cls.PRISON_CHANNEL = GlobalClient.client.get_channel(PRISON_CHANNEL_ID)

    async def is_triggered(self) -> bool:
        self._is_triggered = False

        if self.member.voice is None:
            return self._is_triggered

        if self.after.channel.id != ROYAL_ROOM_ID:
            return self._is_triggered

        if RoyalJudge.is_royal_family_member_from_id(self.member.id):
            return self._is_triggered

        await self.member.move_to(Execution.PRISON_CHANNEL, reason=EXECUTION_REASON)

        number_of_clients: int = len(GlobalClient.client.voice_clients)
        if number_of_clients > 1:
            raise RuntimeError("Error: Too many voice clients detected."
                               "Expected only one, but got {}".format(number_of_clients))

        if number_of_clients == 0 and not Execution.IS_EXECUTING:
            self._is_triggered = True
            return self._is_triggered

        if number_of_clients == 1 and not Execution.IS_EXECUTING:
            try:
                client: discord.VoiceClient = GlobalClient.client.voice_clients[0]
                await client.disconnect(force=True)

            except Exception as e:
                Execution.IS_EXECUTING = False
                raise e

            self._is_triggered = True
            return self._is_triggered

        if Execution.IS_EXECUTING:
            return self._is_triggered

    async def execute(self):
        if not self._is_triggered:
            return

        try:
            voice_client: discord.VoiceClient = await Execution.PRISON_CHANNEL.connect(reconnect=False)
            voice_client.play(discord.FFmpegPCMAudio(source=NATIONAL_ANTHEM))
            Execution.IS_EXECUTING = True

        except Exception as e:
            Execution.IS_EXECUTING = False
            raise e

        await asyncio.sleep(VC_STAY_LENGTH)
        await voice_client.disconnect(force=True)
