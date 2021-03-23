from typing import Union

import discord


async def unmute(member: discord.Member):
    await member.edit(mute=False)


def get_user_icon_url(user: Union[discord.Member, discord.ClientUser]) -> str:
    return "https://cdn.discordapp.com/avatars/{}/{}.png".format(user.id, user.avatar)
