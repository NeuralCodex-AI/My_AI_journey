from langchain_text_splitters import RecursiveCharacterTextSplitter
class DocumentSplitter:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
    def split_documents(self, documents):
        chunks = self.text_splitter.split_documents(documents)
        return chunks