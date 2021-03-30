import asyncio
from abc import ABC
from typing import Optional

import discord

from config import NATIONAL_ANTHEM, VC_STAY_LENGTH, PRISON_CHANNEL_ID
from src.service.voice.voice_abs import VoiceFunctionAbstract
from src.service.misc.royal_judge import RoyalJudge
from src.exception.misunderstanding import MisunderstandingException
from src.client.global_client import GlobalClient


class PlaySound(VoiceFunctionAbstract, ABC):
    IS_EXECUTING: bool = False
    PRISON_CHANNEL: Optional[discord.VoiceChannel] = None

    @classmethod
    async def disconnected(cls):
        cls.IS_EXECUTING = False

        number_of_voice_clients: int = len(GlobalClient.client.voice_clients)
        if number_of_voice_clients > 1:
            raise MisunderstandingException("The coder thought there can be only one or no voice client,"
                                            "but got {}.".format(number_of_voice_clients))

        if number_of_voice_clients == 1:
            await GlobalClient.client.voice_clients[0].disconnect()

    def __init__(self, member: discord.Member, after: discord.VoiceState, is_join: bool):
        PlaySound.static_check()

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

        if PlaySound.IS_EXECUTING:
            return self._is_triggered

        if not self.is_join and self.is_join is not None:
            return self._is_triggered

        if self.after.channel.id != RoyalJudge.get_royal_room().id:
            return self._is_triggered

        if RoyalJudge.is_royal_family_member_from_id(self.member.id):
            return self._is_triggered

        number_of_voice_clients: int = len(GlobalClient.client.voice_clients)
        if number_of_voice_clients > 1:
            raise MisunderstandingException("The coder thought there can be only one or no voice client,"
                                            "but got {}.".format(number_of_voice_clients))

        self._is_triggered = True
        return self._is_triggered

    async def execute(self):
        if not self._is_triggered:
            return

        voice_client: discord.VoiceClient = await PlaySound.PRISON_CHANNEL.connect(reconnect=False)
        voice_client.play(discord.FFmpegPCMAudio(NATIONAL_ANTHEM))
        PlaySound.IS_EXECUTING = True

        await asyncio.sleep(VC_STAY_LENGTH)
        await voice_client.disconnect(force=True)

    # async def do(self):
    #     """
    #     実際にPartyIchiyoを実行する
    #     """
    #     voice_client = await self.base_voice_channel.connect(reconnect=False)
    #     if self.music == 0:
    #         chosen_music = random.choice(list(PartyIchiyo.MUSICS_LIST.values()))
    #         voice_client.play(discord.FFmpegPCMAudio(chosen_music))
    #     else:
    #         chosen_music = PartyIchiyo.MUSICS_LIST[self.music]
    #         voice_client.play(discord.FFmpegPCMAudio(chosen_music))
    #     await self.kikisen_channel.send("パーティー Nigth")
    #     sleep_time = MP3(chosen_music).info.length
    #     await asyncio.sleep(sleep_time + 0.5)
    #     await voice_client.disconnect(force=True)
