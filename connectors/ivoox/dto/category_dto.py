from typing import List

from pydantic import BaseModel

from connectors.ivoox.dto.subcategory_dto import Subcategory


class Category(BaseModel):
    """DTO object for Category model"""

    id: int
    name: str
    subcategories: List[Subcategory]
