from pydantic import BaseModel, Field


class VideoRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Prompt for generating AI video"
    )


class VideoResponse(BaseModel):
    status: str
    video: str | None = None
    message: str | None = None