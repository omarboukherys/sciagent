from contextlib import contextmanager

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.mongodb import MongoDBSaver

from sciagents.config import settings
from sciagents.application.conversation_service.workflow.graph import create_workflow_graph
from sciagents.domain.scientist_factory import ScientistFactory

@contextmanager
def get_compiled_graph():
    """Open a mongo checkpointer and yield a comiled graph that perists state."""
    with MongoDBSaver.from_conn_string(settings.MONGO_URI, settings.MONGO_DB_NAME) as checkpointer:
        graph=create_workflow_graph().compile(checkpointer=checkpointer)

        yield graph

async def generate_response(scientist_id: str, message: str, thread_id: str) -> str:
    """Run one conversation turn, persisted under thread_id."""

    scientist=ScientistFactory.get_scientist(scientist_id)

    with get_compiled_graph() as graph:
        config={"configurable":{"thread_id": thread_id}}

        result=await graph.ainvoke(
            {
                "messages":[HumanMessage(content=message)],
                "scientist_name": scientist.name,
                "scientist_perspective": scientist.perspective,
                "scientist_style": scientist.style,
                "scientist_context": "",
                "summary": ""
            },
            config
        )

        return result['messages'][-1].content
    
async def stream_response(scientist_id: str, message: str, thread_id: str):
    """Yield the scientist's reply token by token as it is generated."""
    scientist=ScientistFactory.get_scientist(scientist_id)

    with get_compiled_graph() as graph:
        config={"configurable": {'thread_id': thread_id}}

        async for chunk, metadata in graph.astream(
            {
                "messages":[HumanMessage(content=message)],
                "scientist_name": scientist.name,
                "scientist_perspective": scientist.perspective,
                "scientist_style": scientist.style,
                "scientist_context":"",
                "summary":"",
            },
            config,
            stream_mode="messages"
        ):
            if chunk.content and metadata["langgraph_node"]=="conversation_node":
                yield chunk.content