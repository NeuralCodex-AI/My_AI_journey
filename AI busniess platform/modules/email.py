from utils.ai import AI
from utils.prompts import (
    EMAIL_PROMPT,
    REPLY_PROMPT,
    GRAMMAR_PROMPT
)


class EmailAI:

    def __init__(self):

        self.ai = AI()


    def generate(
        self,
        purpose,
        details
    ):

        prompt = EMAIL_PROMPT.format(
            purpose=purpose,
            details=details
        )

        return self.ai.generate(
            prompt
        )


    def reply(
        self,
        email
    ):

        prompt = REPLY_PROMPT.format(
            email=email
        )

        return self.ai.generate(
            prompt
        )


    def grammar(
        self,
        text
    ):

        prompt = GRAMMAR_PROMPT.format(
            text=text
        )

        return self.ai.generate(
            prompt
        )