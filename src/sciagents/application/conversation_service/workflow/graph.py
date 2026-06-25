from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from sciagents.application.conversation_service.workflow.state import ScientistState
from sciagents.application.conversation_service.workflow.tools import tools
from sciagents.application.conversation_service.workflow.nodes import (
    conversation_node,
    summarize_context_node,
    summarize_conversation_node,
)
from sciagents.application.conversation_service.workflow.edges import (
    should_summarize_conversation,
)


def create_workflow_graph():
    graph_builder = StateGraph(ScientistState)

    # 1. Register the nodes
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("retrieve_context", ToolNode(tools))
    graph_builder.add_node("summarize_context_node", summarize_context_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)

    # 2. Wire the edges
    graph_builder.add_edge(START, "conversation_node")

    graph_builder.add_conditional_edges(
        "conversation_node",
        tools_condition,
        {
            "tools": "retrieve_context",
            END: END,
        },
    )

    graph_builder.add_edge("retrieve_context", "summarize_context_node")
    graph_builder.add_edge("summarize_context_node", "conversation_node")

    graph_builder.add_conditional_edges(
        "conversation_node",
        should_summarize_conversation,
        {
            "summarize_conversation_node": "summarize_conversation_node",
            END: END,
        },
    )

    graph_builder.add_edge("summarize_conversation_node", END)

    return graph_builder