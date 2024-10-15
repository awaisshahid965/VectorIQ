from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from app.services.deeplake_service import DeepLakeService

QDRANT_API_KEY = '2E_O1iz58WeZoLOFEJicu6xn8anDoTpYox8aZl1QI4gxfGI-IiUKZQ'
QDRANT_CLUSTER_URL = 'https://8b1c9908-150b-407b-8711-9f926256f19c.europe-west3-0.gcp.cloud.qdrant.io:6333'

# qdrant_client = QdrantClient(
#     url=QDRANT_CLUSTER_URL,
#     api_key=QDRANT_API_KEY
# )

# vectorstore = QdrantVectorStore(
#     client=qdrant_client
    
# )

# loading env vars
load_dotenv()

deeplake_service = DeepLakeService(
    dataset_name="stealth"
)


model = ChatOpenAI(
    model='gpt-4o-mini',
)

qa_chain = RetrievalQA.from_llm(model, retriever=deeplake_service.get_retriever())

def main():
    response = qa_chain.run("What is stealth?")
    print(response)



# if __name__ == '__main__':
#     main()
