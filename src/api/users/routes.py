from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from piccolo.apps.user.tables import BaseUser
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.fastapi.endpoints import FastAPIKwargs, FastAPIWrapper

from api.users.schemas import TokenSchema
from exceptions import credentials_exception
from services.auth import login

router = APIRouter()


def add_piccolo_user_crud(fastapi_app):
    FastAPIWrapper(
        root_url="/users/",
        fastapi_app=fastapi_app,
        piccolo_crud=PiccoloCRUD(BaseUser),
        fastapi_kwargs=FastAPIKwargs({"tags": ["Auth"]}),
    )


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt = await login(username=form_data.username, password=form_data.password)
    if not jwt:
        raise credentials_exception
    token = {"access_token": jwt, "token_type": "bearer"}
    return token
