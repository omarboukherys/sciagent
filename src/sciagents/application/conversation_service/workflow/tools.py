from langchain_core.tools import tool
from sciagents.application.rag.retrievers import get_retriever

@tool
def retrieve_scientist_context(query: str) -> str:
    """Search the knowledge base for information about science, scientists,
    and the nature of reality. Use this when you need specific facts you are
    unsure about, rather than guessing."""

    retriever = get_retriever()
    docs = retriever.invoke(query)
    return "\n\n".join(doc.page_content for doc in docs)

tools=[retrieve_scientist_context]