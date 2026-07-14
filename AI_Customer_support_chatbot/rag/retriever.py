class RetrieverManager:
    def __init__(self, vector_store):
        self.vector_store = vector_store
    def get_retriever(self):
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k":3
            }
        )
        return retriever