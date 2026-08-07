from utils.ai import AI

from utils.prompts import (
    BLOG_PROMPT,
    SOCIAL_PROMPT,
    MARKETING_PROMPT
)


class ContentAI:

    def __init__(self):

        self.ai = AI()


    def blog(
        self,
        topic
    ):

        prompt = BLOG_PROMPT.format(
            topic=topic
        )

        return self.ai.generate(prompt)


    def social_post(
        self,
        topic,
        platform
    ):

        prompt = SOCIAL_PROMPT.format(
            topic=topic,
            platform=platform
        )

        return self.ai.generate(prompt)


    def marketing_copy(
        self,
        product
    ):

        prompt = MARKETING_PROMPT.format(
            product=product
        )

        return self.ai.generate(prompt)


    def product_description(
        self,
        product
    ):

        prompt = f"""
Write a professional product description.

Product:

{product}
"""

        return self.ai.generate(prompt)


    def seo_content(
        self,
        topic
    ):

        prompt = f"""
Write SEO optimized content.

Topic:

{topic}
"""

        return self.ai.generate(prompt)