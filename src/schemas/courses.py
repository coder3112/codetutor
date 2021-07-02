import datetime

from typing import List
from pydantic.main import BaseModel


class CourseIn(BaseModel):
    title: str
    instructor: str
    videos: str
    modified_at: datetime.date


class CourseOut(BaseModel):
    title: str
    instructor: str
    videos: str


class CourseOutList(BaseModel):
    __root__: List[CourseOut]