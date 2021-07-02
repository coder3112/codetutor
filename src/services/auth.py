"""
Authentication business logic
"""
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from piccolo.apps.user.tables import BaseUser
from pydantic.networks import EmailStr

from src.config.settings import settings
from src.exceptions import credentials_exception
from src.models.user_profile import Role
from src.schemas.profile import ProfileIn
from src.schemas.user import UserIn, UserOut

from .profile import create_profile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    current_user: Optional[BaseUser] = (
        await BaseUser.select().where(BaseUser.username == username).first().run()
    )
    if current_user is None:
        raise credentials_exception
    return UserOut(**current_user)


async def login(username: str, password: str) -> Optional[Tuple[str, UserOut]]:
    user_id: Optional[int] = await BaseUser.login(username=username, password=password)
    if not user_id:
        return None
    data: Dict = {"sub": username}
    # TODO: Use expiry time
    access_jwt: str = create_access_token(data)
    user = await get_current_user(access_jwt)
    return access_jwt, user


async def register(user: UserIn):
    username: str = user.username
    email: EmailStr = user.email
    password: str = user.password
    first_name: Optional[str] = user.first_name
    last_name: Optional[str] = user.last_name
    user_qs = await BaseUser.select().where(BaseUser.username == username).run()
    if len(user_qs) > 0:
        return {"error": "Username already registered", "created": False}
    user_qs = await BaseUser.select().where(BaseUser.email == email).run()
    if len(user_qs) > 0:
        return {"error": "Email already registered", "created": False}
    created_user_list = await BaseUser.insert(
        BaseUser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            active=True,
        )
    ).run()
    created_user_id = (created_user_list[0]).get("id")
    profile = {
        "role": Role.student,
        "user_id": created_user_id,
    }
    await create_profile(ProfileIn(**profile))
    created_user: BaseUser = (
        await BaseUser.select(exclude_secrets=True)
        .where(BaseUser.id == created_user_id)
        .first()
        .run()
    )
    return {"user": created_user, "created": True}


async def change_password(new_pass, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    current_user: Optional[BaseUser] = (
        await BaseUser.select().where(BaseUser.username == username).first().run()
    )
    if current_user is None:
        raise credentials_exception

    current_user.password = new_pass
