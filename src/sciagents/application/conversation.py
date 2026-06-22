from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_groq import ChatGroq
from sciagents.config import settings

def get_chain():
    """Build the prompt | model | parser chain for a scientist conversation."""

    model=ChatGroq(
        model=settings.GROQ_LLM_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.7
    )

    prompt=ChatPromptTemplate(
        [
            (
                "system",
                "You are {name}, the famous scientist. {perspective} {style} "
                "Stay in character. Keep replies to a few sentences.",
            ),
            (
                "user",
                ("{question}")
            )
        ]
    )

    parser=StrOutputParser()

    return prompt | model | parser