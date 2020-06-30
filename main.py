import asyncio
import os

import discord


ROYAL_ROOM_ID = 727133544773845013
PRISON_CHANNEL_ID = 724591472061579295
ROYAL_FAMILY_IDS = [554985192549515264]

NATIONAL_ANTHEM = "ast/snd/broken_national_anthem.wav"


class MainClient(discord.Client):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.prison_channel = None
        self.is_executing = False

    def run(self) -> None:
        super().run(self.token)

    async def on_ready(self):
        self.prison_channel = self.get_channel(PRISON_CHANNEL_ID)

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel is None:
            return
        if after.channel.id != ROYAL_ROOM_ID:
            return
        if member.id not in ROYAL_FAMILY_IDS:
            await member.move_to(self.prison_channel, reason="皇宮警察だ！！！")
            await self.execution()

    async def execution(self):
        if self.is_executing:
            return

        self.is_executing = True

        voice_client = await self.prison_channel.connect(reconnect=False)
        voice_client.play(discord.FFmpegPCMAudio(source=NATIONAL_ANTHEM))
        await asyncio.sleep(70)
        await voice_client.disconnect(force=True)

        self.is_executing = False


if __name__ == "__main__":
    TOKEN = "NzI3NTExMzQ2MjU3NzIzNDYz.Xvs6KA.LzUGRnk57OgqImXk6vCNFcgc_H0"

    client = MainClient(TOKEN)
    client.run()
