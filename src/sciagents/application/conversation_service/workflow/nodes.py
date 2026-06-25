from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig

from sciagents.application.conversation_service.workflow.chains import (
    get_scientist_response_chain,
    get_conversation_summary_chain,
    get_context_summary_chain,
)
from sciagents.application.conversation_service.workflow.state import ScientistState
from sciagents.config import settings


async def conversation_node(state: ScientistState, config: RunnableConfig):
    """The in-character scientist turn. May answer, or emit a tool call."""
    chain = get_scientist_response_chain()
    response = await chain.ainvoke(
        {
            "messages": state["messages"],
            "scientist_name": state["scientist_name"],
            "scientist_perspective": state["scientist_perspective"],
            "scientist_style": state["scientist_style"],
            "scientist_context": state.get("scientist_context", ""),
            "summary": state.get("summary", ""),
        },
        config,
    )

    return {"messages": response}


async def summarize_context_node(state: ScientistState):
    """Compress the just-retrieved tool output in place, to save tokens."""
    chain = get_context_summary_chain()
    last_message = state["messages"][-1]
    response = await chain.ainvoke({"context": last_message.content})
    last_message.content = response.content
    return {}


async def summarize_conversation_node(state: ScientistState):
    """When the chat gets long, write a summary and drop the old messages."""
    chain = get_conversation_summary_chain()
    response = await chain.ainvoke(
        {
            "messages": state["messages"],
            "scientist_name": state["scientist_name"],
        }
    )

    delete_messages = [
        RemoveMessage(id=m.id)
        for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
    ]

    return {"summary": response.content, "messages": delete_messages}