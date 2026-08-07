import os
from utils.helper import save_uploaded_file, current_time, save_report_file
from utils.rag import RAG
from utils.mongo import MongoDB
from utils.pdf_reader import DocumentReader


class DocumentAI:

    def __init__(self):
        self.rag = RAG()
        self.db = MongoDB()
        self.collection = "document_reports"


    def upload_document(self, uploaded_file):
        return save_uploaded_file(uploaded_file)


    def create_index(self, file_path):
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        vector_path = "vector_db/document"
        self.rag.create_vector_store(file_path, vector_path)
        return vector_path


    def generate_report(self, file_path, user_email):
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: File not found - {file_path}"
        
        # Read document text
        text = DocumentReader.extract_text(file_path)
        
        # Generate summary
        summary = self.rag.llm.invoke(f"Summarize this document: {text}")
        
        # Generate key points
        key_points = self.rag.llm.invoke(f"Extract key points from this document: {text}")
        
        # Create report
        report = f"""
# Document Report

## Summary
{summary.content}

## Key Points
{key_points.content}

---
Generated: {current_time()}
        """
        
        # Save report to file
        report_file_path = save_report_file(report, "txt")
        
        # Save to database
        self.db.insert_one(self.collection, {
            "email": user_email,
            "file_path": file_path,
            "report": report,
            "report_file": report_file_path,
            "created_at": current_time()
        })
        
        return report


    def ask(self, file_path, question):
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: File not found - {file_path}"
        
        try:
            # Create index
            vector_path = self.create_index(file_path)
            
            # Load vector store
            vector = self.rag.load_vector_store(vector_path)
            
            # Ask question
            answer = self.rag.ask(vector, question)
            
            if "could not find" in answer.lower():
                return "Answer not found in document."
            
            return answer
            
        except Exception as e:
            return f"Error: {str(e)}"


    def get_report_history(self, user_email):
        return self.db.find(self.collection, {"email": user_email})