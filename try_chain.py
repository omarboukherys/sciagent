from sciagents.application.conversation import get_chain
from sciagents.domain.scientist_factory import ScientistFactory

scientist=ScientistFactory.get_scientist("einstein")

chain=get_chain()

answer =chain.invoke(
    {
        "name":scientist.name,
        "perspective": scientist.perspective,
        "style": scientist.style,
        "question":"Do you think the universe is fundamentally random ?"
    }
)

print(answer)