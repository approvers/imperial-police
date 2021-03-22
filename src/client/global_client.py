from typing import List, Optional

import discord

from src.utils.discd import *


class GlobalClient:
    client: Optional[discord.Client] = None
    guild: Optional[discord.Guild] = None

    @classmethod
    def static_init(cls, client: discord.Client):
        cls.client = client
        cls.guild = client.guilds[0]
