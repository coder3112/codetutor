from pydantic import BaseModel


class VideoUploadForm(BaseModel):
    name: str
    description: str
    course: int
    section: int
