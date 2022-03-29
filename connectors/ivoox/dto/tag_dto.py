from pydantic import BaseModel


class Tag(BaseModel):
    """
    DTO for ivoox Tag
    """

    id: int
    name: str
