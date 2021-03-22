from typing import Optional

import discord


class VoiceHandler:
    def __init__(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        self.is_join: Optional[bool]

        self.member: discord.Member = member
        self.before: discord.VoiceState = before
        self.after: discord.VoiceState = after

        if before.channel is None and after.channel is not None:
            self.is_join = True
        elif before.channel is not None and after.channel is None:
            self.is_join = False
        else:
            self.is_join = None

    async def handle(self):
        if self.is_join is None:
            return
