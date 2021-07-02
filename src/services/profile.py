"""
Authentication business logic
"""
from piccolo.apps.user.tables import BaseUser

from src.models.user_profile import Role, UserProfileModel
from src.schemas.profile import ProfileIn, ProfileOut


async def create_profile(profile: ProfileIn):
    role: Role = profile.role
    user_id = profile.user_id

    user_qs = await BaseUser.select().where(BaseUser.id == user_id).run()
    if len(user_qs) <= 0:
        return {"error": "Such a user does not exist", "created": False}
    profile_user_qs = (
        await UserProfileModel.select()
        .where(UserProfileModel.user_id.id == user_id)
        .run()
    )
    if len(profile_user_qs) > 0:
        return {"error": "Profile with user exists", "created": False}
    created_profile_list = await UserProfileModel.insert(
        UserProfileModel(role=role, user_id=user_id)
    ).run()
    created_profile_id = created_profile_list[0].get("id")
    profile = (
        await UserProfileModel.select()
        .where(UserProfileModel.id == created_profile_id)
        .first()
        .run()
    )
    return {"profile": profile, "created": True}


async def get_profile(username: str):
    profile = (
            await UserProfileModel.select()
            .where(UserProfileModel.username == username)
            .first()
            .run()
            )
    return profile
