from utils.helper import save_uploaded_file
from utils.rag import RAG
from utils.mongo import MongoDB
from utils.prompts import RESUME_PROMPT
from utils.helper import current_time


class ResumeAI:

    def __init__(self):

        self.rag = RAG()
        self.db = MongoDB()
        self.collection = "resume_analysis"


    def analyze(
        self,
        uploaded_file,
        user_email
    ):

        file_path = save_uploaded_file(uploaded_file)

        vector_path = "vector_db/resume"

        self.rag.create_vector_store(
            file_path,
            vector_path
        )

        vector = self.rag.load_vector_store(
            vector_path
        )

        result = self.rag.ask(
            vector,
            RESUME_PROMPT
        )

        self.db.insert_one(
            self.collection,
            {
                "email": user_email,
                "file": file_path,
                "analysis": result,
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