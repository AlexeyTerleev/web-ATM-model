from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str


class UserAuth(BaseModel):
    login: str
    password: str


class UserOut(BaseModel):
    id: int
    login: str


class SystemUser(UserOut):
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


