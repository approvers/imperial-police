import os
import re
from typing import List

from discord import Intents

DISCORD_TOKEN = os.environ["IMPERIAL_POLICE_TOKEN"]
DISCORD_INTENTS: Intents = Intents.all()

ROYAL_ROOM_ID: int = int(os.environ["IMPERIAL_POLICE_ROYAL_ROOM_ID"])
ROYAL_QUALIFICATION_ROLE_ID: int = int(os.environ["IMPERIAL_POLICE_ROYAL_QUALIFICATION_ID"])
PRISON_CHANNEL_ID: int = int(os.environ["IMPERIAL_POLICE_PRISON_CHANNEL_ID"])
MESSAGE_CHANNEL_ID: int = int(os.environ["IMPERIAL_POLICE_MESSAGE_CHANNEL_ID"])

NATIONAL_ANTHEM = "ast/snd/broken_national_anthem.wav"
ROYAL_EMBLEM_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Imperial_Seal_of_Japan.svg/500px-Imperial_Seal_of_Japan.svg.png"

VCDIFF_REGEXES: List[re.Pattern] = [
    re.compile(r"(.*?)が.*に入りました"),
    re.compile(r"(.*?)が.*から抜けました")
]
