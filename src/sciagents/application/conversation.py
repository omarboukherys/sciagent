from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_groq import ChatGroq

from sciagents.config import settings
from sciagents.domain.prompts import SCIENTIST_CHARACTER_CARD

def get_chain():
    """Build the prompt | model | parser chain for a scientist conversation."""

    model = ChatGroq(
        model=settings.GROQ_LLM_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.7
    )

    prompt=ChatPromptTemplate.from_messages(
        [
            ("system", SCIENTIST_CHARACTER_CARD.prompt),
            ("user", "{{question}}")
        ],
        template_format="jinja2"
    )
    parser=StrOutputParser()

    return prompt | model | parser