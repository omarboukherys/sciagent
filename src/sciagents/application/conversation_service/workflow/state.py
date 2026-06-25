from langgraph.graph import MessagesState

class ScientistState(MessagesState):
    """The state that flows through the graph (the shared 'clipboard').

    Inherits `messages` (with the add_messages reducer) from MessagesState,
    and adds the scientist-specific fields the nodes need.
    """

    scientist_name: str
    scientist_perspective: str
    scientist_style: str
    scientist_context: str
    summary: str