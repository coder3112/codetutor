import datetime
from typing import List

from pydantic.main import BaseModel


class CourseIn(BaseModel):
    title: str
    instructor: int
    videos: List
    modified_at: datetime.date


class CourseForm(BaseModel):
    title: str
