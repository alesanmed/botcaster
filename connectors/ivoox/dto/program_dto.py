from typing import List, Optional

from pydantic import BaseModel

from .program_embeds_dto import ProgramEmbeds
from .program_skills_dto import ProgramSkills
from .program_tag_dto import ProgramTag


class Program(BaseModel):
    """
    DTO object for modeling the data in ivoox programs
    """

    id: int
    userId: int
    channelId: int
    name: str
    description: str
    image: str
    imageHeader: Optional[str]
    numAudios: int
    lastUploadDate: str
    commentPolicy: str
    hasFans: bool
    hasBrand: bool
    hasAffiliateProgram: bool
    url: str
    shortUrl: str
    genderId: int
    categoryId: int
    subcategoryId: int
    languageId: int
    collaboration: int
    explicit: int
    hideFeeds: int
    hideRanking: int
    hideListens: int
    hideLikes: int
    rssUrl: str
    feedId: Optional[int]
    publicEmail: Optional[str]
    iTunesCategory: Optional[int]
    numAudiosFeed: int
    exclusive: Optional[bool]
    iTunesType: str
    skills: ProgramSkills
    tags: List[ProgramTag]
    embeds: ProgramEmbeds
