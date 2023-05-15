from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi import Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.card.models import cards_table
from src.card.schemas import Card
from src.database import get_async_session


async def get_inserted_card(request: Request,
                            session: AsyncSession = Depends(get_async_session)) -> Card:
    card_number = request.cookies.get('inserted_card')
    if card_number is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card isn't inserted"
        )
    card_pin = request.cookies.get('card_pin')
    if card_pin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Enter PIN"
        )
    query = select(cards_table).where(cards_table.c.number == card_number)
    card = await session.execute(query)
    card = card.first()
    if not card or card.pin != card_pin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect number or PIN"
        )
    return Card(**{'pin': card.pin, 'number': card.number, 'cvv': card.cvv,
                   'date': card.date, 'account_id': card.account_id})
