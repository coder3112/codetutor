from typing import List, Optional

from pydantic import BaseModel

from src.models.user_profile import Role


class ProfileIn(BaseModel):
    """
    Schema for Profile being input into the database
    """

    role: Role = Role.student
    user_id: int
    courses_bought: List = []
    courses_completed: List = []


class ProfileOut(BaseModel):
    """
    Schema for Profile being output.
    """

    id: int
    role: Role = Role.student
    user_id: int
    courses_bought: Optional[List] = []
    courses_completed: Optional[List] = []
