import re
from abc import ABC
from typing import Optional, List

import discord

from config import VCDIFF_REGEXES
from src.service.message.message_abs import MessageFunctionAbstract
from src.service.data.royal_family_judge import ImperialHouseholdAgencyLibrary
from src.utils import utils


class VCDiffCleaner(MessageFunctionAbstract, ABC):
    def __init__(self, message: discord.Message):
        self.message: discord.Message = message
        self._is_triggered: Optional[bool] = False

    def is_triggered(self) -> bool:
        self._is_triggered = False

        if len(self.message.embeds) != 1:
            return self._is_triggered

        embed = self.message.embeds[0]

        royal_family_ids: List[int] = ImperialHouseholdAgencyLibrary.get_royal_member_id_list()
        if not utils.includes(embed.thumbnail.url, royal_family_ids):
            return self._is_triggered

        if ImperialHouseholdAgencyLibrary.get_royal_room_name() not in embed.title:
            return self._is_triggered

        for regex in VCDIFF_REGEXES:
            if re.search(regex, embed.title):
                self._is_triggered = True
                return self._is_triggered

    async def execute(self):
        await self.message.delete(delay=None)
