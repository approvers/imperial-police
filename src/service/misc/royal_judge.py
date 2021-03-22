from typing import List, Optional

import discord

from config import ROYAL_ROOM_ID, ROYAL_QUALIFICATION_ROLE_ID
from src.client.global_client import GlobalClient


class RoyalJudge:
    ROYAL_ROOM: Optional[discord.VoiceChannel] = None
    ROYAL_QUALIFICATION_ROLE: Optional[discord.Role] = None

    @classmethod
    def static_checker(cls):
        if cls.ROYAL_ROOM is None:
            cls.ROYAL_ROOM = GlobalClient.client.get_channel(ROYAL_ROOM_ID)
        if cls.ROYAL_QUALIFICATION_ROLE is None:
            cls.ROYAL_QUALIFICATION_ROLE = GlobalClient.guild.get_role(ROYAL_QUALIFICATION_ROLE_ID)

    @classmethod
    def get_royal_role(cls) -> discord.Role:
        cls.static_checker()

        return cls.ROYAL_QUALIFICATION_ROLE

    @classmethod
    def get_royal_room(cls) -> discord.VoiceChannel:
        cls.static_checker()

        return cls.ROYAL_ROOM

    @classmethod
    def get_royal_member_id_list(cls) -> List[int]:
        cls.static_checker()

        return [m.id for m in cls.ROYAL_QUALIFICATION_ROLE.members]

    @classmethod
    def is_royal_family_member_from_id(cls, member_id: int) -> bool:
        cls.static_checker()

        return member_id in cls.get_royal_member_id_list()

    @classmethod
    def is_royal_family_member(cls, member: discord.Member) -> bool:
        cls.static_checker()

        return cls.is_royal_family_member_from_id(member.id)
