from typing import Optional, Tuple

from fastapi import Request

from src.exceptions import (
    CredentialsException,
    admin_exception,
    credentials_exception,
    jwt_exception,
)
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
    try:
        user = await get_current_user(param)
        if not user:
            raise credentials_exception
        return None
    except CredentialsException:
        raise credentials_exception
    return param


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
        return None
    except CredentialsException:
        raise credentials_exception
    return param
