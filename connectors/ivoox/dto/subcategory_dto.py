from pydantic import BaseModel


class Subcategory(BaseModel):
    """DTO for Subcategory object"""

    id: int
    name: str
