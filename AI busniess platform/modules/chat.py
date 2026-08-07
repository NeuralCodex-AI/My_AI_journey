from utils.ai import AI
from utils.mongo import MongoDB
from utils.helper import current_time


class Chat:

    def __init__(self):

        self.ai = AI()
        self.db = MongoDB()
        self.collection = "chat_history"


    def ask(
        self,
        user_email,
        message
    ):

        answer = self.ai.generate(
            message
        )

        self.save_chat(
            user_email,
            message,
            answer
        )

        return answer


    def stream(
        self,
        user_email,
        message
    ):

        response = ""

        for chunk in self.ai.stream(
            message
        ):

            response += chunk
            yield chunk

        self.save_chat(
            user_email,
            message,
            response
        )


    def save_chat(
        self,
        user_email,
        user_message,
        ai_message
    ):

        self.db.insert_one(
            self.collection,
            {
                "email": user_email,
                "user": user_message,
                "assistant": ai_message,
                "created_at": current_time()
            }
        )


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


    def clear_history(
        self,
        user_email
    ):

        self.db.delete_many(
            self.collection,
            {
                "email": user_email
            }
        )