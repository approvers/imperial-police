import asyncio
import os

import discord


ROYAL_ROOM_ID = 727133544773845013
LAWLESS_CHANNEL_ID = 690909527461199922
PRISON_CHANNEL_ID = 724591472061579295
ROYAL_QUALIFICATION_ROLE_ID = 727046372456661012

NATIONAL_ANTHEM = "ast/snd/broken_national_anthem.wav"


class MainClient(discord.Client):
    def __init__(self, token) -> None:
        super().__init__()
        self.token: str = token
        self.guild: discord.Guild = None
        self.royal_family: list[discord.Member] = []
        self.royal_family_ids: list[int] = []
        self.royal_qualification: discord.Role = None
        self.royal_room: discord.VoiceChannel = None
        self.prison_channel: discord.VoiceChannel = None
        self.lawless_channel: discord.TextChannel = None
        self.is_voice_connected: bool = False

    def run(self) -> None:
        super().run(self.token)

    async def on_ready(self) -> None:
        self.guild = self.guilds[0]
        self.royal_qualification = self.guild.get_role(ROYAL_QUALIFICATION_ROLE_ID)
        self.royal_room = self.guild.get_channel(ROYAL_ROOM_ID)
        self.prison_channel = self.get_channel(PRISON_CHANNEL_ID)
        self.lawless_channel = self.get_channel(LAWLESS_CHANNEL_ID)
        self.royal_family = self.royal_qualification.members
        self.royal_family_ids = map(lambda x: x.id, self.royal_family)

    async def on_message(self, message: discord.Message):
        if not message.embeds:
            return
        if includes(message.embeds[0].thumbnail.url, self.royal_family_ids):
            await message.channel.send("卍 還幸 卍")
            await message.delete(delay=None)

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id == self.user.id:
            if before.channel is not None and after.channel is not None:
                return
            if after.channel is not None:
                self.is_voice_connected = True
            if before.channel is not None:
                self.is_voice_connected = False

        if after.channel != self.royal_room:
            return
        if member not in self.royal_family:
            await self.execution(member)

    async def execution(self, member):
        await member.move_to(self.prison_channel, reason="皇宮警察だ！！！")
        if self.is_voice_connected:
            return
        try:
            voice_client = await self.prison_channel.connect(reconnect=False)
            voice_client.play(discord.FFmpegPCMAudio(source=NATIONAL_ANTHEM))
            await asyncio.sleep(67)
            await voice_client.disconnect(force=True)
        except Exception as caught_exception:
            await self.lawless_channel.send(caught_exception)


def includes(query: str, search_from: list):
    for test_case in search_from:
        if str(test_case) in str(query):
            return True
    return False


if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")

    client = MainClient(TOKEN)
    client.run()
