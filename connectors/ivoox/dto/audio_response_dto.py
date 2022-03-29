from pydantic import BaseModel


class AudioResponse(BaseModel):
    """DTO holding the data for a response when uploading an audio"""

    server: str
    ref: str
    req: str
    name: str
    type: str
    size: int
    error: int
    ext: str
