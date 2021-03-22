import discord

from src.service.message.questions import ManyQuestions
from src.service.message.vcdiff_cleaner import VCDiffCleaner


class MessageHandler:
    def __init__(self, message):
        self.message: discord.Message = message

    async def handle(self):
        questions: ManyQuestions = ManyQuestions(self.message)
        vcdiff_cleaner: VCDiffCleaner = VCDiffCleaner(self.message)

        if questions.is_triggered():
            await questions.execute()

        if vcdiff_cleaner.is_triggered():
            await vcdiff_cleaner.execute()
