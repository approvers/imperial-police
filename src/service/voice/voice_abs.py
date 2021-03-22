import discord

import abc


class VoiceFunctionAbstract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        pass

    @abc.abstractmethod
    def is_triggered(self) -> bool:
        pass

    @abc.abstractmethod
    async def execute(self, **kwargs):
        pass
