import discord

from config import DISCORD_TOKEN, DISCORD_INTENTS
from src.service.embed.embed_factory import EmbedFactory
from src.service.data.royal_family_judge import ImperialHouseholdAgencyLibrary
from src.handler.message import MessageHandler
from src.handler.voice import VoiceHandler


class MainClient(discord.Client):
    def __init__(self) -> None:
        super(MainClient, self).__init__(intents=DISCORD_INTENTS)

    def launch(self) -> None:
        self.run(DISCORD_TOKEN)

    async def on_ready(self) -> None:
        number_of_servers: int = len(self.guilds)
        if number_of_servers != 1:
            raise RuntimeError("Error: This bot can run in only one server."
                               "But You are trying to run in {} server(s).".format(number_of_servers))

        guild = self.guilds[0]

        EmbedFactory.static_init(self.user)
        ImperialHouseholdAgencyLibrary.static_init(guild)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        await MessageHandler(message).handle()

    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState
    ):
        if member.bot:
            return

        await VoiceHandler(member, before, after).handle()
