import fitz
from docx import Document
from pathlib import Path
import os


class DocumentReader:

    @staticmethod
    def read_pdf(file_path):
        document = fitz.open(file_path)
        text = []

        for page in document:
            content = page.get_text("text")
            if content.strip():
                text.append(content)

        document.close()
        return "\n".join(text)


    @staticmethod
    def read_docx(file_path):
        document = Document(file_path)

        text = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(text)


    @staticmethod
    def read_txt(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


    @staticmethod
    def extract_text(file_path):
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return DocumentReader.read_pdf(file_path)

        if extension == ".docx":
            return DocumentReader.read_docx(file_path)

        if extension == ".txt":
            return DocumentReader.read_txt(file_path)

        raise ValueError(f"Unsupported file format: {extension}")