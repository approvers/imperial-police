import discord

from src.handler.me_handler import MeHandler
from src.service.voice.royal_embed import RoyalEmbed
from src.service.voice.mover import Mover
from src.service.voice.play_sound import PlaySound


class VoiceHandler:
    def __init__(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        self.member: discord.Member = member
        self.before: discord.VoiceState = before
        self.after: discord.VoiceState = after

        self.is_join: bool

        if before.channel is None and after.channel is not None:
            self.is_join = True
        elif before.channel is not None and after.channel is None:
            self.is_join = False
        elif before.channel != after.channel:
            self.is_join = True
        else:
            self.is_join = None

    async def handle(self, is_me: bool = False):
        if is_me:
            my_handler: MeHandler = MeHandler(self.member, self.before, self.after)
            await my_handler.handle()

        royals: RoyalEmbed = RoyalEmbed(self.before, self.after, self.member, self.is_join)
        mover: Mover = Mover(self.member, self.after, self.is_join)
        sound: PlaySound = PlaySound(self.member, self.after, self.is_join)

        royals_trigger: bool = royals.is_triggered()
        mover_trigger: bool = mover.is_triggered()
        sound_trigger: bool = await sound.is_triggered()

        if royals_trigger:
            await royals.execute()

        if mover_trigger:
            await mover.execute()

        if sound_trigger:
            await sound.execute()
