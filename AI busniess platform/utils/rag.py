import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from utils.pdf_reader import DocumentReader
from config import GEMINI_API_KEY


os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY


class RAG:

    def __init__(self):

        self.embedding = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )


    def create_vector_store(self, file_path, save_path):

        text = DocumentReader.extract_text(file_path)

        chunks = self.splitter.split_documents(
            [Document(page_content=text)]
        )

        vector_store = FAISS.from_documents(
            chunks,
            self.embedding
        )

        vector_store.save_local(save_path)

        return vector_store


    def load_vector_store(self, save_path):

        return FAISS.load_local(
            save_path,
            self.embedding,
            allow_dangerous_deserialization=True
        )


    def similarity_search(
        self,
        vector_store,
        question,
        k=4
    ):

        return vector_store.similarity_search(
            question,
            k=k
        )


    def ask(
        self,
        vector_store,
        question
    ):

        docs = self.similarity_search(
            vector_store,
            question
        )

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        prompt = f"""
You are an AI Business Assistant.

Answer ONLY using the provided context.

Context:

{context}

Question:

{question}

If the answer is not available in the context,
reply:

"I could not find this information in the uploaded document."
"""

        response = self.llm.invoke(prompt)

        return response.content


    def create_and_chat(
        self,
        file_path,
        save_path,
        question
    ):

        vector_store = self.create_vector_store(
            file_path,
            save_path
        )

        return self.ask(
            vector_store,
            question
        )