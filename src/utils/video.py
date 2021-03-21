from typing import Optional

import vimeo

from src.config.settings import settings

client = vimeo.VimeoClient(
    token=f"{settings.vimeo_token}",
    key=f"{settings.vimeo_client_id}",
    secret=f"{settings.vimeo_client_secret}",
)


async def check_transcoding(uri: str):
    response = client.get(uri + "?fields=transcode.status").json()
    while True:
        if response["transcode"]["status"] == "complete":
            return "complete"
        if response["transcode"]["status"] == "in_progress":
            continue
        return "error"


async def upload_video(
    file_name: str,
    description: str,
    name: Optional[str] = None,
) -> str:
    if not name:
        name = file_name
    uri = client.upload(
        file_name,
        data={
            "name": name,
            "description": description,
        },
    )
    response = client.get(uri + "?fields=link").json()
    video_link: str = response["link"]
    return video_link
