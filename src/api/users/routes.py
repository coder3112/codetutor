from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo.apps.user.tables import BaseUser
from piccolo_api.fastapi.endpoints import FastAPIWrapper, FastAPIKwargs
from fastapi import APIRouter

router = APIRouter()


def add_piccolo_user_crud(fastapi_app):
    FastAPIWrapper(
        root_url="/users/",
        fastapi_app=fastapi_app,
        piccolo_crud=PiccoloCRUD(BaseUser),
        fastapi_kwargs=FastAPIKwargs({"tags": ["Auth"]}),
    )
