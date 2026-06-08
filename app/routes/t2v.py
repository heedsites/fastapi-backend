from fastapi import APIRouter

from app.models.t2v import (
    VideoRequest,
    VideoResponse
)

from app.controllers.t2v import (
    generate_video_controller
)

router = APIRouter(
    tags=["Text-to-Video"]
)


@router.post(
    "/generate-video",
    response_model=VideoResponse
)
async def generate_video(
    request: VideoRequest
):

    return await generate_video_controller(
        request
    )