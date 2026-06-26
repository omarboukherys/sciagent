from langchain_text_splitters import RecursiveCharacterTextSplitter

from sciagents.config import settings


def get_splitter(chunk_size: int = settings.RAG_CHUNK_SIZE):
    """Split documents into overlapping chunks for embedding."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size * 0.15),
    )