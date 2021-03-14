from typing import List

from pydantic import BaseModel

from src.models.user_profile import Role
from src.schemas.user import UserOut


class ProfileIn(BaseModel):
    """
    Schema for Profile being input into the database
    """

    role: Role = Role.student
    user: int
    courses_bought: List = []
    courses_completed: List = []


class ProfileOut(BaseModel):
    """
    Schema for Profile being output.
    """

    id: int
    role: Role = Role.student
    user: UserOut
    courses_bought: List = []
    courses_completed: List = []
