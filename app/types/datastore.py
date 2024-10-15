from abc import ABC, abstractmethod
# from typing import List

# from langchain.schema import Document

class DatastoreService(ABC):
    
    @abstractmethod
    def add_docs(self, docs):
        """Method to add documents to the datastore."""
        pass

    @abstractmethod
    def get_retriever(self):
        """Method to return a retriever for embeddings."""
        pass
