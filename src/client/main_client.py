from typing import Optional

import discord

from config import DISCORD_TOKEN, DISCORD_INTENTS, BOT_EXCEPTION_IDS, MESSAGE_CHANNEL_ID
from src.client.global_client import GlobalClient
from src.handler.message import MessageHandler
from src.handler.voice import VoiceHandler
from src.service.embed.embed_factory import EmbedFactory
from src.service.embed.exception import ExceptionEmbedFactory
from src.service.voice.execution import Execution


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

        client: discord.Client = super(MainClient, self)
        GlobalClient.static_init(client)
        self.MESSAGE_CHANNEL = self.get_channel(MESSAGE_CHANNEL_ID)

    async def on_message(self, message: discord.Message):
        if message.author.bot and message.author.id not in BOT_EXCEPTION_IDS:
            return

        try:
            await MessageHandler(message).handle()
        except Exception as e:
            embed = ExceptionEmbedFactory().make(e)
            await self.MESSAGE_CHANNEL.send(embed=embed)
            raise e

        if message.content.startswith("!debug-join"):
            ch: discord.VoiceChannel = self.get_channel(743171615755468941)
            await ch.connect(reconnect=False)

        if message.content.startswith("!debug-embed"):
            emb = EmbedFactory().make(message.author, False)
            await message.channel.send(embed=emb)

        if message.content.startswith("!debug-execute"):
            exc: Execution = Execution(message.author)
            if await exc.is_triggered():
                await exc.execute()

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
