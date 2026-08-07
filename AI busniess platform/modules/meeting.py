from utils.ai import AI
from utils.mongo import MongoDB
from utils.helper import current_time
from utils.prompts import MEETING_PROMPT


class MeetingAI:

    def __init__(self):

        self.ai = AI()
        self.db = MongoDB()
        self.collection = "meeting_notes"


    def summarize(
        self,
        transcript,
        user_email
    ):

        prompt = f"""
{MEETING_PROMPT}

Transcript:

{transcript}
"""

        result = self.ai.generate(prompt)

        self.db.insert_one(
            self.collection,
            {
                "email": user_email,
                "transcript": transcript,
                "summary": result,
                "created_at": current_time()
            }
        )

        return result


    def history(
        self,
        user_email
    ):

        return self.db.find(
            self.collection,
            {
                "email": user_email
            }
        )


    def delete_history(
        self,
        user_email
    ):

        self.db.delete_many(
            self.collection,
            {
                "email": user_email
            }
        )