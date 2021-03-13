from enum import Enum

from piccolo import columns
from piccolo.table import Table
from piccolo.columns.reference import LazyTableReference


class Role(str, Enum):
    instructor = "instructor"
    student = "student"


class UserProfileModel(Table, tablename="profiles"):
    """
    It's fields are:
        - Role
        - User(OnetoOne)
        - Courses Bought(ManytoMany)
        - Courses Completed(ManytoMany)
    """

    role = columns.Varchar()
    user = columns.ForeignKey(
        references=LazyTableReference(
            "BaseUser", module_path="piccolo.apps.user.tables"
        )
    )

    courses_bought = columns.ForeignKey(
        references=LazyTableReference("CourseModel", module_path="src.models.course")
    )

    courses_completed = columns.ForeignKey(
        references=LazyTableReference("CourseModel", module_path="src.models.course")
    )

    def get_role(self) -> Role:
        if self.role == "instructor":
            return Role.instructor
        return Role.student

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def email(self) -> str:
        return self.user.email
