import datetime

from pydantic.main import BaseModel


class CourseIn(BaseModel):
    title: str
    instructor: str
    videos: str
    modified_at: datetime.date
