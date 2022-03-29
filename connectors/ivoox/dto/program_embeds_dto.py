from pydantic import BaseModel


class ProgramEmbeds(BaseModel):
    """
    DTO for ivoox program embeds
    """

    current: str
    fans: str
    subscription: str
