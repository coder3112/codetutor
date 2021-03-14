from fastapi import APIRouter, Depends

from src.models.user_profile import UserProfileModel
from src.schemas.profile import ProfileOut
from src.services.auth import get_current_user
from src.utils.auth import jwt_required

router = APIRouter()


@router.get("/profile")
async def get_user_profile(token: str = Depends(jwt_required)):
    user = await get_current_user(token)
    user_id = user.id
    profile = (
        await UserProfileModel.select()
        .where(UserProfileModel.user_id == user_id)
        .first()
        .run()
    )
    response_body = {"profile": profile, "user": user}
    return ProfileOut(**response_body)
