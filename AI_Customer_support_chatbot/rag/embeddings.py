from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GOOGLE_API_KEY
class EmbeddingManager:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY
        )
    def get_embeddings(self):
        return self.embeddings