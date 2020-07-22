import asyncio
import os
import re

import discord
import datetime

from lib.utils import is_empty


ROYAL_EMBLEM_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Imperial_Seal_of_Japan.svg/500px-Imperial_Seal_of_Japan.svg.png"
NAME_REGEX_IN = re.compile(r"(.*?)が.*に入りました")
NAME_REGEX_OUT = re.compile(r"(.*?)が.*から抜けました")
ROYAL_ROOM_ID = 727133544773845013
LAWLESS_CHANNEL_ID = 690909527461199922
PRISON_CHANNEL_ID = 724591472061579295
ROYAL_QUALIFICATION_ROLE_ID = int(os.getenv("ROYAL_ROLE"))

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
        self.royal_family_ids = [royal_user.id for royal_user in self.royal_family]

    async def on_message(self, message: discord.Message):
        if not message.embeds:
            return
        embed = message.embeds[0]
        if includes(embed.thumbnail.url, self.royal_family_ids):
            if "皇室" not in embed.title:
                return
            if embed.description == "何かが始まる予感がする。":
                parsed_display_name = re.findall(NAME_REGEX_IN, embed.title)[0]
                await message.channel.send(embed=embed_factory(parsed_display_name, self.user.id, self.user.avatar, True))
            elif embed.description == "あいつは良い奴だったよ...":
                parsed_display_name = re.findall(NAME_REGEX_OUT, embed.title)[0]
                await message.channel.send(embed=embed_factory(parsed_display_name, self.user.id, self.user.avatar, False))
            else:
                return
            await message.delete(delay=None)

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel != self.royal_room:
            return
        if member not in self.royal_family:
            await self.execution(member)

    async def execution(self, member):
        await member.move_to(self.prison_channel, reason="皇宮警察だ！！！")
        if not is_empty(self.voice_clients):
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


def embed_factory(member_name: str, my_id: int, my_avatar: str, is_in: bool) -> discord.Embed:
    message_in_or_out = "還幸" if is_in else "行幸"
    embed = discord.Embed(
        title="†卍 {} 卍† ".format(message_in_or_out),
        description="{} が{}なさいました。".format(member_name, message_in_or_out),
        color=0xffd800)
    embed.set_author(
        name="皇宮警察からのお知らせ",
        icon_url="https://cdn.discordapp.com/avatars/{}/{}.png".format(my_id, my_avatar))
    embed.set_thumbnail(url=ROYAL_EMBLEM_URL)
    return embed


if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")

    client = MainClient(TOKEN)
    client.run()
