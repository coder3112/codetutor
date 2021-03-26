from pydantic import BaseModel

from src.schemas.profile import ProfileOut
from src.schemas.user import UserOut


class ProfileReturnModel(BaseModel):
    profile: ProfileOut
    user: UserOut
