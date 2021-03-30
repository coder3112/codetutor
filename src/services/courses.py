from datetime import date

from src.models.course import CourseModel
from src.schemas.courses import CourseIn


async def create_course(title: str, instructor: int, videos: str, modified_at: date):

    qs = await CourseModel.select().where(CourseModel.title == title).run()
    if len(qs) > 0:
        return {
            "created": False,
            "error": "Could not create Course because a course with such a name already exists.",
        }

    courses = await CourseModel.insert(
        CourseModel(
            title=title,
            instructor=instructor,
            videos=videos,
            modified_at=modified_at,
        )
    )
    course_id = courses[0].get("id")
    course = await CourseModel.select().where(CourseModel.id == course_id).first().run()
    return {"created": True, "course": CourseIn(**course)}
