import os
import uuid
import shutil
from datetime import datetime
from pathlib import Path

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"
VECTOR_DIR = "vector_db"

for folder in [UPLOAD_DIR, REPORT_DIR, VECTOR_DIR]:
    Path(folder).mkdir(parents=True, exist_ok=True)


def save_uploaded_file(uploaded_file):
    extension = Path(uploaded_file.name).suffix
    filename = f"{uuid.uuid4().hex}{extension}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as file:
        shutil.copyfileobj(uploaded_file, file)

    return filepath


def save_report_file(report_content, extension="txt"):
    """✅ Report ko file mein save karne ka function"""
    # Ensure reports folder exists
    Path(REPORT_DIR).mkdir(parents=True, exist_ok=True)
    
    filename = f"{uuid.uuid4().hex}.{extension}"
    filepath = os.path.join(REPORT_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(report_content)
    
    return filepath


def generate_filename(extension):
    return f"{uuid.uuid4().hex}.{extension}"


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(text):
    return " ".join(text.split())


def allowed_file(filename):
    allowed = {
        ".pdf",
        ".docx",
        ".txt",
        ".png",
        ".jpg",
        ".jpeg",
        ".mp3",
        ".wav"
    }
    return Path(filename).suffix.lower() in allowed


def response_format(title, content):
    return {
        "title": title,
        "content": content,
        "created_at": current_time()
    }