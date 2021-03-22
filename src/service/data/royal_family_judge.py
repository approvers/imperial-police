from typing import Optional, List, Union

import discord

from config import ROYAL_QUALIFICATION_ROLE_ID, ROYAL_ROOM_ID


class ImperialHouseholdAgencyLibrary:
    _GUILD: Optional[discord.Guild]

    @classmethod
    def static_init(cls, guild: discord.Guild):
        cls._GUILD = guild

    @classmethod
    def is_initialized(cls):
        if cls._GUILD is None:
            raise RuntimeError("Error: You need to call 'RoyalFamilyJudge.static_init()' first.")

    @classmethod
    def get_royal_role(cls) -> discord.Role:
        return cls._GUILD.get_role(ROYAL_QUALIFICATION_ROLE_ID)

    @classmethod
    def get_royal_members(cls) -> List[discord.Member]:
        cls.is_initialized()

        return cls.get_royal_role().members

    @classmethod
    def get_royal_member_id_list(cls) -> List[int]:
        cls.is_initialized()

        return [m.id for m in cls.get_royal_role().members]

    @classmethod
    def is_royal_family_member(cls, member: discord.Member) -> bool:
        cls.is_initialized()

        return cls.is_royal_family_member_from_id(member.id)

    @classmethod
    def is_royal_family_member_from_id(cls, member_id: int) -> bool:
        cls.is_initialized()

        return member_id in cls.get_royal_member_id_list()

    @classmethod
    def get_royal_room_name(cls) -> str:
        channel: discord.TextChannel = cls._GUILD.get_channel(ROYAL_ROOM_ID)

        return channel.name
