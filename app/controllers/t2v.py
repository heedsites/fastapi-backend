from app.models.t2v import (
    VideoRequest,
    VideoResponse
)

from app.services.t2v_service import (
    generate_scenes,
    create_video
)


async def generate_video_controller(
    request: VideoRequest
):

    try:

        scenes = generate_scenes(
            request.text
        )

        video_path = create_video(
            scenes
        )

        return VideoResponse(
            status="success",
            video=video_path
        )

    except Exception as error:

        return VideoResponse(
            status="error",
            message=str(error)
        )