from pydantic import BaseModel


class ProgramTag(BaseModel):
    """
    DTO for ivoox program tag
    """

    id: int
    name: str
