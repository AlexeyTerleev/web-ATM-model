from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from pydantic import ValidationError
from src.config import ALGORITHM, JWT_SECRET_KEY
from src.auth.schemas import SystemUser, TokenPayload
from src.database import get_async_session
from src.auth.models import accounts_table


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="./auth/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth),
                           session: AsyncSession = Depends(get_async_session)) -> SystemUser:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    query = select(accounts_table).where(accounts_table.c.login == token_data.sub)
    user = await session.execute(query)
    user = user.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return SystemUser(**{'id': user.id, 'login': user.login, 'password': user.hashed_password})
