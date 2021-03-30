from fastapi import APIRouter, Depends

from src.models.user_profile import UserProfileModel
from src.schemas.profile import ProfileOut
from src.services.auth import get_current_user
from src.utils.auth import jwt_required

from .schemas import ProfileReturnModel

router = APIRouter()


@router.get("/profile", response_model=ProfileReturnModel)
async def get_user_profile(token: str = Depends(jwt_required)):
    """
    - Returns the profile of current users as well as the user himself.
    - Uses jwt of request, so profile obtained is always logged in user's
    """
    user = await get_current_user(token)
    user_id = user.id
    profile = (
        await UserProfileModel.select()
        .where(UserProfileModel.user_id == user_id)
        .first()
        .run()
    )
    profile_returned = ProfileOut(**profile)
    response_body = {"profile": profile_returned, "user": user}
    return response_body


@router.patch("/create/profile/instructor")
async def create_instructor_profile(token: str = Depends(jwt_required)):
    """
    - Makes a student profile an **instructor**
    - This means that now a user can be a student as well as create courses
    """
    user = await get_current_user(token)
    user_id = user.id
    profile: UserProfileModel = (
        await UserProfileModel.objects()
        .where(UserProfileModel.user_id == user_id)
        .first()
        .run()
    )
    profile.role = "instructor"
    await profile.save().run()
    return {"updated": True, "profile": profile}
