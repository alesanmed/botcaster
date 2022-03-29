from pydantic import BaseModel


class ProgramSkills(BaseModel):
    """
    DTO for ivoox program skills
    """

    overTwoHours: bool
    scheduledPublish: bool
    hideStats: bool
    visibility: bool
    feedToITunes: bool
    hideAudios: bool
    selectRssLength: bool
    revenueShare: bool
    advancedStats: bool
