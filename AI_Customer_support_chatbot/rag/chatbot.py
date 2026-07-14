from langchain_google_genai import ChatGoogleGenerativeAI

from rag.loader import DocumentLoader
from rag.splitter import DocumentSplitter
from rag.embeddings import EmbeddingManager
from rag.vector_store import VectorStoreManager
from rag.retriever import RetrieverManager
from rag.prompt import SYSTEM_PROMPT
from config import GOOGLE_API_KEY
class CustomerChatbot:

    def __init__(self):
        # Knowledge base location
        self.knowledge_path = "knowledge_base"
        # FAISS database location
        self.vector_path = "vector_db/faiss_index"
        # Create embedding model
        self.embedding_manager = EmbeddingManager()
        self.embeddings = (
            self.embedding_manager.get_embeddings()
        )
        # Create LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.3
        )
        self.retriever = None
    def build_database(self):
        print("Loading documents...")
        # Load files
        loader = DocumentLoader(
            self.knowledge_path
        )
        documents = loader.load_documents()
        print("Splitting documents...")
        # Split documents
        splitter = DocumentSplitter()
        chunks = splitter.split_documents(
            documents
        )
        print("Creating FAISS database...")
        # Create vector database
        vector_manager = VectorStoreManager(
            self.vector_path
        )
        vector_store = vector_manager.create_vector_store(
            chunks,
            self.embeddings
        )
        # Create retriever
        retriever_manager = RetrieverManager(
            vector_store
        )
        self.retriever = (
            retriever_manager.get_retriever()
        )
        print("Database created successfully!")
    def load_database(self):
        vector_manager = VectorStoreManager(
            self.vector_path
        )
        vector_store = vector_manager.load_vector_store(
            self.embeddings
        )
        retriever_manager = RetrieverManager(
            vector_store
        )
        self.retriever = (
            retriever_manager.get_retriever()
        )
    def ask(self, question):
        # Search relevant documents
        documents = self.retriever.invoke(
            question
        )
        context = ""
        for doc in documents:
            context += doc.page_content + "\n"
        # Create final prompt
        final_prompt = SYSTEM_PROMPT.format(
            context=context,
            question=question
        )
        # Send to Gemini
        response = self.llm.invoke(
            final_prompt
        )
        return response.content