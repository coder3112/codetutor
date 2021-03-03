from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from piccolo.apps.user.tables import BaseUser
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.fastapi.endpoints import FastAPIKwargs, FastAPIWrapper

from src.exceptions import credentials_exception
from src.schemas.user import UserIn
from src.services.auth import login, register

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


@router.post("/register")
async def register_endpoint(form_data: UserIn):
    result = await register(form_data)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
