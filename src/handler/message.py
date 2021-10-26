import discord

from src.service.message.questions import ManyQuestions
from src.service.message.vcdiff_cleaner import VCDiffCleaner


class MessageHandler:
    def __init__(self, message):
        self.message: discord.Message = message

    async def handle(self):
        # TODO: ここがデータ渡しであることをわすれている
        questions: ManyQuestions = ManyQuestions(self.message)
        vcdiff_cleaner: VCDiffCleaner = VCDiffCleaner(self.message)

        questions_trigger: bool = questions.is_triggered()
        vcdiff_cleaner_trigger: bool = vcdiff_cleaner.is_triggered()

        if questions_trigger:
            await questions.execute()

        if vcdiff_cleaner_trigger:
            await vcdiff_cleaner.execute()
