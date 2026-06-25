from langgraph.graph import END

from sciagents.application.conversation_service.workflow.state import ScientistState
from sciagents.config import settings

def should_summarize_conversation(state: ScientistState) -> str :
    """After the scientist answers, decide whether to summarize or end."""

    messages=state['messages']

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"
    
    return END