from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient

from sciagents.config import settings
from sciagents.application.rag.embeddings import get_embedding_model

def get_vector_store() -> MongoDBAtlasVectorSearch:
    """Connect to the mongoDB vector store."""

    client=MongoClient(settings.MONGO_URI)
    collection=client[settings.MONGO_DB_NAME]['scientist_chunks']

    return MongoDBAtlasVectorSearch(
        collection=collection,
        embedding=get_embedding_model(),
        index_name="vector_index",
        relevance_score_fn="cosine",
    )

def get_retriever(top_k: int = settings.RAG_TOP_K):
    """Return a retriever that fetches the top_k most relevant chunks."""

    return get_vector_store().as_retriever(search_kwargs={"k": top_k})