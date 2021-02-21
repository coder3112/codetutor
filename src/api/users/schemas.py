from pydantic import BaseModel

from schemas.user import UserOut


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
