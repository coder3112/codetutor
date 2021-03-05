from typing import List, Optional, Union

from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import UUID4


class UserOut(BaseModel):
    id: Union[int, UUID4]
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    active: bool
    admin: bool


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]


class UserListOut(BaseModel):
    __root__: List[UserOut]
