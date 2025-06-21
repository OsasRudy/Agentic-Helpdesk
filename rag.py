import os
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_mistralai import ChatMistralAI
from langchain.chains import RetrievalQA
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up RAG system
embedding = OpenAIEmbeddings()
qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"))
vector_store = QdrantVectorStore.from_client(
    client=qdrant_client,
    collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
    embeddings=embedding
)
llm = ChatMistralAI(model_name="mistral-tiny", mistral_api_key=os.getenv("MISTRAL_API_KEY"))
qa = RetrievalQA.from_chain_type(
    llm,
    retriever=vector_store.as_retriever(),
    chain_type="stuff"
)

def retrieve_info(query):
    try:
        # Use the RAG system to retrieve relevant information
        retrieved_info = qa.retrieve(query)
        return retrieved_info
    except Exception as e:
        print("RAG error:", e)
        return ""