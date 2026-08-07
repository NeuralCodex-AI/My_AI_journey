import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MONGODB_URI = os.getenv("MONGODB_URI")

DATABASE_NAME = "AI_Business_Assistant"

VECTOR_DB_PATH = "vector_db"

UPLOAD_FOLDER = "uploads"

REPORT_FOLDER = "reports"

ALLOWED_FILES = {
    ".pdf",
    ".docx",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg",
    ".mp3",
    ".wav"
}

GEMINI_MODEL = "gemini-2.5-flash"

EMBEDDING_MODEL = "models/text-embedding-004"