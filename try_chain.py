import asyncio

from langchain_core.messages import HumanMessage

from sciagents.application.conversation_service.workflow.graph import create_workflow_graph
from sciagents.domain.scientist_factory import ScientistFactory


async def main():
    scientist = ScientistFactory.get_scientist("curie")
    graph = create_workflow_graph().compile()

    initial_state = {
        "messages": [HumanMessage(content="What specific elements did Marie Curie discover? Look it up to be precise.")],
        "scientist_name": scientist.name,
        "scientist_perspective": scientist.perspective,
        "scientist_style": scientist.style,
        "scientist_context": "",
        "summary": "",
    }

    final_state = await graph.ainvoke(initial_state)

    print("---- FINAL REPLY ----")
    print(final_state["messages"][-1].content)


asyncio.run(main())