from typing import List, Optional

from pydantic import BaseModel

from .tag_dto import Tag


class EpisodeEmbeds(BaseModel):
    """DTO containing embeds of episode"""

    current: str
    adaptable: str
    html5: str
    mini: str
    wordpress: str


class EpisodeResponse(BaseModel):
    """DTO containing episode"""

    id: int
    url: str
    image: str
    title: str
    description: str
    programId: int
    subcategoryId: int
    uploadDate: str
    type: str
    status: str
    visible: bool
    listens: int
    likes: int
    comments: int
    shortUrl: str
    mediaUrl: str
    genderId: int
    languageId: int
    iTunesType: str
    iTunesSeasson: Optional[str]
    iTunesEpisode: Optional[str]
    premiereRelease: Optional[str]
    embeds: EpisodeEmbeds
    duration: Optional[int]
    tags: List[Tag]
