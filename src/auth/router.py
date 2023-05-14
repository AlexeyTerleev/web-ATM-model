from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from src.database import get_async_session
from src.auth.models import accounts_table
from src.auth.schemas import UserCreate, UserOut, TokenSchema

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup", summary="Create new user", response_model=UserOut)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(accounts_table).where(accounts_table.c.login == data.login)
    result = await session.execute(query)
    result = result.first()
    print(result)
    if result is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    user = {
        'login': data.login,
        'hashed_password': get_hashed_password(data.password),
        'balance': 0
    }

    stmt = insert(accounts_table).values(user)
    await session.execute(stmt)
    await session.commit()

    return user


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    query = select(accounts_table).where(accounts_table.c.login == form_data.username)
    user = await session.execute(query)
    user = user.first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.login),
        "refresh_token": create_refresh_token(user.login),
    }
