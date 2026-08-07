from utils.ai import AI

from utils.prompts import (
    CODE_EXPLAIN_PROMPT,
    BUG_PROMPT,
    CODE_GENERATION_PROMPT
)


class CodingAI:

    def __init__(self):

        self.ai = AI()


    def explain(
        self,
        code
    ):

        prompt = CODE_EXPLAIN_PROMPT.format(
            code=code
        )

        return self.ai.generate(prompt)


    def debug(
        self,
        code
    ):

        prompt = BUG_PROMPT.format(
            code=code
        )

        return self.ai.generate(prompt)


    def generate(
        self,
        requirement
    ):

        prompt = CODE_GENERATION_PROMPT.format(
            requirement=requirement
        )

        return self.ai.generate(prompt)


    def optimize(
        self,
        code
    ):

        prompt = f"""
Optimize the following code.

Code:

{code}
"""

        return self.ai.generate(prompt)


    def convert(
        self,
        code,
        language
    ):

        prompt = f"""
Convert the following code to {language}.

Code:

{code}
"""

        return self.ai.generate(prompt)


    def documentation(
        self,
        code
    ):

        prompt = f"""
Write complete documentation for the following code.

Code:

{code}
"""

        return self.ai.generate(prompt)


    def complexity(
        self,
        code
    ):

        prompt = f"""
Analyze the time and space complexity of the following code.

Code:

{code}
"""

        return self.ai.generate(prompt)


    def review(
        self,
        code
    ):

        prompt = f"""
Review the following code and suggest improvements.

Code:

{code}
"""

        return self.ai.generate(prompt)