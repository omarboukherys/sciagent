from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

from sciagents.config import settings
from sciagents.domain.prompts import SCIENTIST_CHARACTER_CARD
from sciagents.application.conversation_service.workflow.tools import tools


def get_chat_model(model_name: str = settings.GROQ_LLM_MODEL, temperature: float = 0.7):
    """Create a ChatGroq model instance."""
    return ChatGroq(
        model=model_name,
        api_key=settings.GROQ_API_KEY,
        temperature=temperature,
    )


def get_scientist_response_chain():
    """The in-character conversation chain, with the retrieval tool bound."""
    model = get_chat_model()
    model_with_tools = model.bind_tools(tools)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SCIENTIST_CHARACTER_CARD.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ],
        template_format="jinja2",
    )

    return prompt | model_with_tools


def get_conversation_summary_chain():
    """A cheap chain that summarizes a long conversation."""
    model = get_chat_model(
        model_name=settings.GROQ_LLM_MODEL_CONTEXT_SUMMARY,
        temperature=0.0,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="messages"),
            (
                "user",
                "Summarize the conversation so far between the user and "
                "{{ scientist_name }}, capturing the key points. Keep it concise.",
            ),
        ],
        template_format="jinja2",
    )

    return prompt | model


def get_context_summary_chain():
    """Compress retrieved context with the cheap model."""
    model = get_chat_model(
        model_name=settings.GROQ_LLM_MODEL_CONTEXT_SUMMARY,
        temperature=0.0,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                "Condense the following retrieved information into the key facts "
                "useful for answering the user. Be concise:\n\n{{ context }}",
            ),
        ],
        template_format="jinja2",
    )

    return prompt | model