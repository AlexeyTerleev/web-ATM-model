from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from random import randint

from src.auth.schemas import SystemUser
from src.database import get_async_session
from src.dependencies import get_current_user
from src.card.schemas import CardCreate
from src.card.models import cards_table

router = APIRouter(
    prefix="/card",
    tags=["Operations with card"],
)


@router.post("/register", summary="Create new card")
async def create_user(data: CardCreate,
                      user: SystemUser = Depends(get_current_user),
                      session: AsyncSession = Depends(get_async_session)):

    query = select(cards_table.c.id).order_by(cards_table.c.id.desc()).limit(1)
    last_id = await session.execute(query)
    last_id = last_id.first()
    if last_id is None:
        last_id = 0
    else:
        last_id = last_id[0]
    card = {
        'pin': data.pin,
        'number': str(last_id+1).zfill(8),
        'cvv': ''.join(str(randint(0, 9)) for i in range(3)),
        'account_id': user.id,
        'date': datetime.today()
    }

    stmt = insert(cards_table).values(card)
    await session.execute(stmt)
    await session.commit()

    return card
