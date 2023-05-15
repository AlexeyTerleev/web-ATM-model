from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from src.config import JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY, \
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_token(key: str, subject: Union[str, Any], expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow()
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, key, ALGORITHM)
    return encoded_jwt


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return create_token(JWT_SECRET_KEY, subject, expires_delta)


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return create_token(JWT_REFRESH_SECRET_KEY, subject, expires_delta)