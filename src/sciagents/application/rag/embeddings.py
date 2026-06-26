from langchain_huggingface import HuggingFaceEmbeddings

from sciagents.config import settings


def get_embedding_model():
    """Return the local sentence-transformers embedding model."""
    return HuggingFaceEmbeddings(
        model_name=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
        model_kwargs={"device": settings.RAG_DEVICE},
        encode_kwargs={"normalize_embeddings": True},
    )