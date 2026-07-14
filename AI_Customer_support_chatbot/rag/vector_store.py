from langchain_community.vectorstores import FAISS
class VectorStoreManager:
    def __init__(self, path):
        self.path = path
    def create_vector_store(self, chunks, embeddings):
        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )
        vector_store.save_local(
            self.path
        )
        return vector_store
    def load_vector_store(self, embeddings):
        vector_store = FAISS.load_local(
            self.path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vector_store