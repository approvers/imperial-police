import discord

import abc


class MessageFunctionAbstract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, message: discord.Message):
        pass

    @abc.abstractmethod
    def is_triggered(self) -> bool:
        pass

    @abc.abstractmethod
    async def execute(self, **kwargs):
        pass
