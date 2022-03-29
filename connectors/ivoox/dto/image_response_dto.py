from pydantic import BaseModel


class ImageResponse(BaseModel):
    """DTO holding the response data when image is uploaded"""

    mimetype: str
    checksum: str
    size: int
    path: str
    url: str
