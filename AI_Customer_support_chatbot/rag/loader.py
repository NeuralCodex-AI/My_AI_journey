import os
from langchain_community.document_loaders import TextLoader
class DocumentLoader:
    def __init__(self, knowledge_base_path):
        self.knowledge_base_path = knowledge_base_path
    def load_documents(self):
        documents = []
        for file in os.listdir(self.knowledge_base_path):
            if file.endswith(".txt"):
                file_path = os.path.join(self.knowledge_base_path, file)
                loader = TextLoader(file_path, encoding="utf-8")
                documents.extend(loader.load())
        return documents