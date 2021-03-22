from typing import Optional

import discord

from src.handler.my_handler import MyHandler
from src.service.voice.execution import Execution
from src.service.voice.royals import Royals


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

    async def handle(self, is_me: bool = False):
        if is_me:
            my_handler: MyHandler = MyHandler(self.member, self.before, self.after)
            await my_handler.handle()

        if self.is_join is None:
            return

        execution: Execution = Execution(self.member, self.after, self.is_join)
        royals: Royals = Royals(self.before, self.after, self.member, self.is_join)

        if await execution.is_triggered():
            await execution.execute()

        if royals.is_triggered():
            await royals.execute()
