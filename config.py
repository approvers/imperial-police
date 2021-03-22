import os
import re
from typing import List

from discord import Intents
from pydub import AudioSegment

DISCORD_TOKEN = os.environ["IMPERIAL_POLICE_TOKEN"]
DISCORD_INTENTS: Intents = Intents.all()

ROYAL_ROOM_ID: int = int(os.environ["IMPERIAL_POLICE_ROYAL_ROOM_ID"])
ROYAL_QUALIFICATION_ROLE_ID: int = int(os.environ["IMPERIAL_POLICE_ROYAL_QUALIFICATION_ID"])
PRISON_CHANNEL_ID: int = int(os.environ["IMPERIAL_POLICE_PRISON_CHANNEL_ID"])
MESSAGE_CHANNEL_ID: int = int(os.environ["IMPERIAL_POLICE_MESSAGE_CHANNEL_ID"])
BOT_EXCEPTION_IDS: List[int] = [int(i) for i in os.environ["IMPERIAL_POLICE_BOT_EXCEPTION_IDS"].split("@")]

NATIONAL_ANTHEM: str = "ast/snd/broken_national_anthem.wav"
VC_STAY_LENGTH: int = AudioSegment.from_file(NATIONAL_ANTHEM, "wav").duration_seconds
ROYAL_EMBLEM_URL: str = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Imperial_Seal_of_Japan.svg/500px-Imperial_Seal_of_Japan.svg.png"
ERROR_CROSS_URL: str = "https://illust8.com/wp-content/uploads/2018/08/mark_batsu_illust_898.png"
EXECUTION_REASON: str = "皇宮警察だ！！！"

VCDIFF_REGEXES: List[re.Pattern] = [
    re.compile(r"(.*?)が.*に入りました"),
    re.compile(r"(.*?)が.*から抜けました")
]
