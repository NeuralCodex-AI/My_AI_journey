import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
st.set_page_config(
    page_title="AI PDF Chat Assistant",
    page_icon="",
    layout="wide"
)
with st.sidebar:
    st.title("AI PDF Assistant")
    uploaded_files=st.file_uploader(
        'upload_file',
        type=["pdf"],
        accept_multiple_files=True
    )
    st.divider()
    st.subheader("Quick_Action")
    summary_btn = st.button("Summarize PDF")
    quiz_btn = st.button("Generate Quiz")
    mcq_btn = st.button(" Generate MCQs")
    download_btn = st.button("Download Summary")
    clear_btn = st.button("Clear Chat")

st.title(" AI PDF Chat Assistant")
st.caption("Upload PDF files and chat with your documents.")
if "messages" not in st.session_state:
    st.session_state.messages = []

GEMINI_API_KEY="YOUR_API_KEY"

class PDFAssistant:

    def __init__(self):
        self.api_key=GEMINI_API_KEY
        self.vector_store = None
        self.summary = ""
        self.documents = None
        self.chunks = None

    def load_pdf(self, uploaded_files):
        self.documents = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name
            loader = PyPDFLoader(temp_path)
            docs = loader.load()
            self.documents.extend(docs)
        return self.documents

    def create_chunks(self):
        if self.documents is None:
            return
        splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
        )
        self.chunks = splitter.split_documents(self.documents)
        return self.chunks

    def create_vector_db(self):
        if self.chunks is None:
            return
        embedding_model = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=self.api_key
        )
        self.vector_store = FAISS.from_documents(
            self.chunks,
            embedding_model
        )
        return self.vector_store
    
    def ask_question(self, question):

        if self.vector_store is None:
            return "Please upload a PDF first."

        docs = self.vector_store.similarity_search(question, k=3)
        context = ""
        for doc in docs:
            context += doc.page_content + "\n\n"

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key
        )
        prompt = f"""
            Answer the question using the context below.
           Context:
           {context}
           Question:
          {question}"""
        response = llm.invoke(prompt)
        return response.content

    def summarize(self):
        if self.documents is None:
            return "Please upload a PDF first."
        context = ""
        for doc in self.documents:
            context += doc.page_content + "\n"
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key
        )
        prompt = f"""
            Summarize the following document in simple language.
            {context}"""
        response = llm.invoke(prompt)
        self.summary = response.content
        return self.summary

    def generate_quiz(self):
        if self.documents is None:
            return "Please upload a PDF first."
        context = ""
        for doc in self.documents:
            context += doc.page_content + "\n"
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key
        )
        prompt = f"""
            Generate 10 quiz questions from the following document.
            {context}"""

        response = llm.invoke(prompt)
        return response.content

    def generate_mcqs(self):
        if self.documents is None:
            return "Please upload a PDF first."
        context = ""
        for doc in self.documents:
            context += doc.page_content + "\n"
        llm = ChatGoogleGenerativeAI(
             model="gemini-2.5-flash",
            google_api_key=self.api_key
        )
        prompt = f"""
            Generate 10 MCQs from the document.
            Each MCQ must contain:
            A)
            B)
            C)
            D)
            Also provide the correct answer.
            {context}"""
        response = llm.invoke(prompt)
        return response.content

if "bot" not in st.session_state:
    st.session_state.bot = PDFAssistant()
bot = st.session_state.bot

if "vector_ready" not in st.session_state:
    st.session_state.vector_ready = False
if uploaded_files and not st.session_state.vector_ready:
    with st.spinner("Processing PDF..."):
        bot.load_pdf(uploaded_files)
        bot.create_chunks()
        bot.create_vector_db()
    st.session_state.vector_ready = True
    st.success("PDF Uploaded Successfully!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
user_input = st.chat_input(
    "Ask anything about your uploaded PDF..."
)
if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    response = bot.ask_question(user_input)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
    st.rerun()
if summary_btn:
    summary = bot.summarize()
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": f"Summary\n\n{summary}"
        }
    )
    st.rerun()
if quiz_btn:
    quiz = bot.generate_quiz()
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": f"Quiz\n\n{quiz}"
        }
    )
    st.rerun()
if mcq_btn:
    mcqs = bot.generate_mcqs()
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": f"MCQs\n\n{mcqs}"
        }
    )
    st.rerun()
if download_btn:
    if bot.summary:
        st.download_button(
            label="Download Summary",
            data=bot.summary,
            file_name="summary.txt",
            mime="text/plain"
        )
    else:
        st.warning("Generate Summary First.")
if clear_btn:
    st.session_state.messages = []
    st.session_state.bot = PDFAssistant()
    st.session_state.vector_ready = False
    st.rerun()