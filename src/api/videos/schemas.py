from pydantic import BaseModel

from src.schemas.user import UserOut


class VideoUploadForm(BaseModel):
    name: str
    description: str
    course: int
    section: int


class CourseForm(BaseModel):
    title: str


class CourseCreateResponse(BaseModel):
    created: bool
    course: CourseForm
    instructor: UserOut
