from pydantic import BaseModel, Field

class Scientist(BaseModel):
    """A scientist agent with a name, a perspective on reality, and a talking style."""

    id: str =Field(description="Unique identifier, example: einstein")
    name: str = Field(description="The name of the scientist like Albert Einstein")
    perspective: str = Field(description="The scientist's stance on the nature of reality.")
    style: str = Field(description="How the scientist talks")