from langchain_core.tools import tool

@tool
def retrieve_scientist_context(query: str) -> str:
    """Search the knowledge base for information about science, scientists,
    and the nature of reality. Use this when you need specific facts you are
    unsure about, rather than guessing."""

    return f"[stubbed knowledge base] placeholder context for query: {query!r}"

tools=[retrieve_scientist_context]