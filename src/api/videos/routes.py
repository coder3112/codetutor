from datetime import date

from fastapi import APIRouter, Body, File, UploadFile
from fastapi.param_functions import Depends

from src.models.course import CourseModel
from src.schemas.courses import CourseForm
from src.utils.auth import is_instructor
from src.utils.video import upload_video
from src.utils.video_parser import VideoJSONParser

from .schemas import VideoUploadForm

router = APIRouter()


@router.post("/upload/video", status_code=201)
async def upload_new_video(form_data: VideoUploadForm, video: UploadFile = File(...)):
    response = await upload_video(
        description=form_data.description, file_name=video.filename, name=form_data.name
    )
    link = response[1]
    name = response[2]
    description = response[3]
    original_json = CourseModel.select(CourseModel.videos).where(
        CourseModel.id == form_data.course
    )
    video_parser = VideoJSONParser(original_json)
    new_json = video_parser.add_video(form_data.section, name, link, description)
    await CourseModel.update({CourseModel.videos: new_json}).run()
    return {"course_videos_json": new_json}


@router.post("/create/course", status_code=201)
async def create_new_course(form: CourseForm = Body(...), user = Depends(is_instructor)):
    title = form.title
    videos = '{}'
    modified_at = date.today()

    await CourseModel.insert(
        CourseModel(
            title=title, instructor=user.username, videos=videos, modified_at=modified_at
        )
    )
    return {"created": True, "course": form.dict(), "instructor": user}
