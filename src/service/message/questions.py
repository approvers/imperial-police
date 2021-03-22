import random
from abc import ABC
from typing import Optional

import discord

from src.service.message.message_abs import MessageFunctionAbstract


class ManyQuestions(MessageFunctionAbstract, ABC):
    def __init__(self, message: discord.Message):
        self.message: discord.Message = message
        self._is_triggered: Optional[bool] = None

    def is_triggered(self) -> bool:
        if self.message.author.bot:
            return self._is_triggered
        if "???" in self.message.content:
            self._is_triggered = True
        else:
            self._is_triggered = False

        return self._is_triggered

    async def execute(self):
        if (self._is_triggered is None) or (not self._is_triggered):
            return

        length = int(random.randint(1, 30))
        content = ManyQuestions._create_questions_content(length)
        await self.message.channel.send(content)

    @staticmethod
    def _create_questions_content(length: int) -> str:
        result = ""

        for n in range(length):
            random_num = random.randint(0, 1)

            if random_num:
                result += "?"
            else:
                result += "？"

        return result
