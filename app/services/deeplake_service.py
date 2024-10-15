import os
from typing import List

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.schema import Document

from ..types.datastore import DatastoreService

class DeepLakeService(DatastoreService):

    def __init__(self, dataset_name):

        dataset_base_url = os.getenv('DEEPLAKE_BASE_URL')

        if not dataset_base_url:
            raise ValueError("Unable to find deeplake dataset base path!")

        if not dataset_name:
            raise ValueError("A valid dataset name is required!")
        
        self.db = DeepLake(
            dataset_path=f"{dataset_base_url}/{dataset_name}",
            embedding_function=OpenAIEmbeddings(
                model='text-embedding-ada-002'
            )
        )
    
    def get_retriever(self):
        return self.db.as_retriever()

    def add_docs(self, docs: List[Document]):
        self.db.add_documents(docs)
