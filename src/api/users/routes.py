from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from piccolo.apps.user.tables import BaseUser
from starlette.requests import Request

from src.exceptions import credentials_exception
from src.schemas.user import UserIn, UserListOut
from src.services.auth import login, register
from src.utils.auth import is_admin

from .schemas import TokenSchema

router = APIRouter()


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await login(username=form_data.username, password=form_data.password)
    try:
        jwt = result[0]
        user = result[1]
    except (TypeError, IndexError):
        raise credentials_exception
    token = {"access_token": jwt, "user": user, "token_type": "bearer"}
    return token


@router.post("/register", status_code=201)
async def register_endpoint(form_data: UserIn = Body(...)):
    result = await register(form_data)
    if result.get("created"):
        return result
    raise HTTPException(
        detail=f"Could not register user because {result.get('error')}",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@router.get("/users")
async def return_all_users(request: Request = Depends(is_admin)):
    users = await BaseUser.select()
    users_serialized = UserListOut.parse_obj(users)
    return {"users": users_serialized}
