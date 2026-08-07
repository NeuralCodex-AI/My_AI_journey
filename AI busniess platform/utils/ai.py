from google import genai

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


class AI:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )


    def generate(
        self,
        prompt
    ):

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text


    def stream(
        self,
        prompt
    ):

        response = self.client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=prompt
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text