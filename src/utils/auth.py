from src.models.blacklistjwt import BlackListedJWTModel
from typing import Optional, Tuple

from fastapi import Request
from fastapi.param_functions import Depends

from src.exceptions import (
    CredentialsException,
    admin_exception,
    credentials_exception,
    jwt_exception,
)
from src.models.user_profile import UserProfileModel
from src.services.auth import get_current_user


def get_authorization_scheme_param(authorization_header_value: str) -> Tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


async def jwt_required(request: Request) -> Optional[str]:
    authorization: str = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise jwt_exception
    jwts_blacklisted = (
        await BlackListedJWTModel.select().where(BlackListedJWTModel.jwt == param).run()
    )
    if jwts_blacklisted:
        raise credentials_exception
    try:
        user = await get_current_user(param)
        if not user:
            raise credentials_exception
        return param
    except CredentialsException:
        raise credentials_exception


async def is_admin(request: Request) -> Optional[str]:
    authorization: str = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise jwt_exception
    try:
        user = await get_current_user(param)
        if not user:
            raise credentials_exception
        if not user.admin:
            raise admin_exception
        return param
    except CredentialsException:
        raise credentials_exception


async def is_instructor(jwt=Depends(jwt_required)):
    user = await get_current_user(jwt)
    profile = (
        await UserProfileModel.select()
        .where(UserProfileModel.user_id == user.id)
        .first()
        .run()
    )
    print(profile)
    if profile.get("role") != "instructor":
        raise credentials_exception
    return user
