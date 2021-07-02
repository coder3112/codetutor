from fastapi import APIRouter, Depends

from src.models.user_profile import UserProfileModel
from src.schemas.profile import ProfileOut
from src.services.auth import get_current_user
from src.utils.auth import jwt_required
from src.services.profile import get_profile as get_profile_db

from .schemas import ProfileReturnModel

router = APIRouter()


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


@router.get('/profile')
async def get_profile(jwt=Depends(jwt_required)):
    user = await get_current_user(jwt)
    username = user.username
    profile = await get_profile_db(username)
    return ProfileOut(**profile)
