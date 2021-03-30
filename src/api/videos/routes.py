from datetime import date

import aiofiles
from fastapi import APIRouter, BackgroundTasks, Body, Depends, File, UploadFile

from src.exceptions import CoursesException
from src.models.course import CourseModel
from src.services.courses import create_course
from src.utils.auth import is_instructor
from src.utils.video import check_transcoding, upload_video
from src.utils.video_parser import VideoJSONParser

from .schemas import CourseCreateResponse, CourseForm

router = APIRouter()


@router.post("/upload/video", status_code=201)
async def upload_new_video(
    background_tasks: BackgroundTasks,
    # form_data: VideoUploadForm = Body(...),
    name: str,
    description: str,
    course: int,
    section: int,
    video: UploadFile = File(...),
):
    # Using following link for video.read and f.write
    # https://stackoverflow.com/questions/63580229/how-to-save-uploadfile-in-fastapi
    # Basically, UploadFile is a wrapper around TemporaryFile
    # so you can use aiofiles and .read and .write methods in it.

    async with aiofiles.open(video.filename, "wb") as f:
        content = await video.read()
        await f.write(content)

    response = await upload_video(
        description=description, file_name=video.filename, name=name
    )
    background_tasks.add_task(check_transcoding, response[0])
    link = response[1]
    name = response[2]
    description = response[3]
    original_json = (
        await CourseModel.select(CourseModel.videos)
        .where(CourseModel.id == course)
        .first()
        .run()
    )
    video_parser = VideoJSONParser(f"{original_json['videos']}")
    new_json = video_parser.add_video(section, name, link, description)
    await CourseModel.update({CourseModel.videos: new_json}).run()
    return {"course_videos_json": new_json}


@router.post("/create/course", status_code=201, response_model=CourseCreateResponse)
async def create_new_course(form: CourseForm = Body(...), user=Depends(is_instructor)):
    title = form.title
    videos = "{}"
    modified_at = date.today()
    response = await create_course(title, user.username, videos, modified_at)
    if not response.get("created"):
        raise CoursesException(400, response.get("error"))
    return {"created": True, "course": form, "instructor": user}
