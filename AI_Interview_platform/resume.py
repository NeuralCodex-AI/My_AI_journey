from pypdf import PdfReader
from docx import Document
from rag import (
    create_vector_store,
    save_vector_store,
    analyze_resume
)
def extract_pdf_text(file_path):
    reader = PdfReader(
        file_path
    )
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
            text += "\n"
    return text
def extract_docx_text(file_path):
    document = Document(
        file_path
    )
    text = ""
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text
            text += "\n"
    return text
def extract_resume_text(file_path):
    if file_path.endswith(".pdf"):
        text = extract_pdf_text(
            file_path
        )
    elif file_path.endswith(".docx"):
        text = extract_docx_text(
            file_path
        )
    else:
        return "Unsupported file format"
    return text
def create_resume_vectorstore(
    file_path,
    save_path="vectorstore/resume"
):
    resume_text = extract_resume_text(
        file_path
    )
    if not resume_text.strip():
        return "Resume text could not be extracted"
    vectorstore = create_vector_store(
        resume_text,
        "resume"
    )
    save_vector_store(
        vectorstore,
        save_path
    )
    return vectorstore
def process_resume(
    file_path
):
    resume_text = extract_resume_text(
        file_path
    )
    if not resume_text.strip():
        return {
            "error": "Could not extract resume text"
        }
    resume_vectorstore = create_vector_store(
        resume_text,
        "resume"
    )
    analysis = analyze_resume(
        resume_vectorstore
    )
    return {
        "resume_text": resume_text,
        "analysis": analysis,
        "vectorstore": resume_vectorstore
    }