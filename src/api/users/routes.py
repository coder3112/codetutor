from src.models.blacklistjwt import BlackListedJWTModel
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from piccolo.apps.user.tables import BaseUser
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.exceptions import credentials_exception
from src.schemas.user import UserIn, UserListOut
from src.services.auth import get_current_user, login, register
from src.utils.auth import is_admin, jwt_required

from .schemas import RegisterReturnResponse, TokenSchema

router = APIRouter()


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    - Login endpoint of the API
    - It requires you to send a ```application/x-www-form-urlencoded``` with the following: <br>
     - Required
        - ```username```
        - ```password```
     - Optional
        |Parameter|Default|
        |----------|------|
        |```grant_type```|password|
        |```scope```|Empty String|
        |```client_id```|Empty String|
        |```client_secret```|Empty String|
    """
    result = await login(username=form_data.username, password=form_data.password)
    try:
        jwt = result[0]
        user = result[1]
    except (TypeError, IndexError):
        raise credentials_exception
    token = {"access_token": jwt, "user": user, "token_type": "bearer"}
    return token


@router.post("/register", status_code=201, response_model=RegisterReturnResponse)
async def register_endpoint(form_data: UserIn = Body(...)):
    """
    - Register endpoint for the API.
    - It needs you to send a **JSON payload** of the form:
    ```
    {
    "username": "string",
    "email": "user@example.com",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
    }
    ```
    """
    result = await register(form_data)
    if result.get("created"):
        return result
    raise HTTPException(
        detail=f"Could not register user because {result.get('error')}",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@router.get("/users")
async def return_all_users(request=Depends(is_admin)):
    """
    - Returns a **list of users registered**
    - You must be an admin to access this endpoint
    """
    users = await BaseUser.select().run()
    users_serialized = UserListOut.parse_obj(users)
    return {"users": users_serialized}


@router.delete("/delete/user")
async def delete_user(jwt: str = Depends(jwt_required)):
    """
    - **Delete** a user account
    - Uses logged in user as the user
    """
    user = await get_current_user(jwt)  # Get user
    deleted_user = (
        await BaseUser.delete().where(BaseUser.id == user.id).run()
    )  # Delete user.
    return RedirectResponse("/logout")


@router.post("/logout")
async def logout_user(jwt: str = Depends(jwt_required)):
    """
    - Logs out user
    - uses given JWT
    """
    # Add jwt to blacklist
    await BlackListedJWTModel.insert(BlackListedJWTModel(jwt=jwt)).run()
    return {"logged_out": True}
