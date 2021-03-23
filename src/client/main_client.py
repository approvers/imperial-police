from typing import Optional

import discord

from config import DISCORD_TOKEN, DISCORD_INTENTS, BOT_EXCEPTION_IDS, MESSAGE_CHANNEL_ID
from src.client.global_client import GlobalClient
from src.service.embed.exception import ExceptionEmbedFactory
from src.handler.message import MessageHandler
from src.handler.voice import VoiceHandler


class MainClient(discord.Client):
    def __init__(self) -> None:
        super(MainClient, self).__init__(intents=DISCORD_INTENTS)

        self.MESSAGE_CHANNEL: Optional[discord.TextChannel] = None

    def launch(self) -> None:
        self.run(DISCORD_TOKEN)

    async def on_ready(self) -> None:
        number_of_guilds: int = len(self.guilds)
        if number_of_guilds != 1:
            raise RuntimeError("Error: This bot can run in only one server."
                               "But You are trying to run in {} server(s).".format(number_of_guilds))

        self.MESSAGE_CHANNEL = self.get_channel(MESSAGE_CHANNEL_ID)

        client: discord.Client = super(MainClient, self)
        GlobalClient.static_init(client)

        me_as_member: discord.Member = GlobalClient.guild.get_member(self.user.id)
        my_voice_state: discord.VoiceState = me_as_member.voice

        if my_voice_state is None:
            return

        if my_voice_state.channel is not None:
            await me_as_member.move_to(None)

    async def on_message(self, message: discord.Message):
        if message.author.bot and message.author.id not in BOT_EXCEPTION_IDS:
            return

        try:
            await MessageHandler(message).handle()
        except Exception as e:
            embed = ExceptionEmbedFactory().make(e)
            await self.MESSAGE_CHANNEL.send(embed=embed)
            raise e

    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState
    ):
        if member.id == self.user.id:
            await VoiceHandler(member, before, after).handle(is_me=True)
            return

        if member.bot:
            return

        try:
            await VoiceHandler(member, before, after).handle()
        except Exception as e:
            embed = ExceptionEmbedFactory().make(e)
            await self.MESSAGE_CHANNEL.send(embed=embed)
            raise e
