from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Response, Request
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from random import randint
from starlette import status

from src.auth.models import accounts_table
from src.auth.schemas import SystemUser
from src.card.dependencies import get_inserted_card
from src.database import get_async_session
from src.dependencies import get_current_user
from src.card.schemas import CardCreate, Card
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
        'number': str(last_id + 1).zfill(8),
        'cvv': ''.join(str(randint(0, 9)) for i in range(3)),
        'account_id': user.id,
        'date': datetime.today()
    }

    stmt = insert(cards_table).values(card)
    await session.execute(stmt)
    await session.commit()

    return card


@router.post('/insert', summary="Cards insertion")
async def insert_card(card_number: str,
                      response: Response,
                      request: Request,
                      session: AsyncSession = Depends(get_async_session)):
    if request.cookies.get('inserted_card') is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card is already inserted"
        )
    query = select(cards_table).where(cards_table.c.number == card_number)
    card = await session.execute(query)
    card = card.first()
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect number or pin"
        )
    response.set_cookie(key="inserted_card", value=card_number)
    return {'message': f'card {card_number} was inserted'}


@router.post('/extract', summary="Cards extraction")
async def extract_card(response: Response,
                       request: Request):
    card_number = request.cookies.get('inserted_card')
    if card_number is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card isn't inserted"
        )
    response.delete_cookie("inserted_card")
    return {'message': f'card {card_number} was extracted'}


@router.post('/input_pin', summary="Cards insertion")
async def input_pin(card_pin: str, request: Request, response: Response):
    card_number = request.cookies.get('inserted_card')
    if card_number is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card isn't inserted"
        )
    response.set_cookie(key="card_pin", value=card_pin)
    return {'message': 'pin entered'}


@router.get('/balance', summary='View card balance')
async def get_balance(card: Card = Depends(get_inserted_card),
                      session: AsyncSession = Depends(get_async_session)):
    query = select(accounts_table.c.balance).where(accounts_table.c.id == card.account_id)
    balance = await session.execute(query)
    balance = balance.first()
    return {'balance': balance[0]}


@router.post('/increase', summary='Increase card balance')
async def increase_balance(money: int,
                           card: Card = Depends(get_inserted_card),
                           session: AsyncSession = Depends(get_async_session)):
    if money <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Money should be > 0"
        )

    query = select(accounts_table.c.balance).where(accounts_table.c.id == card.account_id)
    balance = await session.execute(query)
    balance = balance.first()

    stmt = update(accounts_table).where(accounts_table.c.id == card.account_id).values(balance=balance[0] + money)
    await session.execute(stmt)
    await session.commit()

    return {'message': 'good'}


@router.post('/decrease', summary='Decrease card balance')
async def decrease_balance(money: int,
                           card: Card = Depends(get_inserted_card),
                           session: AsyncSession = Depends(get_async_session)):
    if money <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Money should be > 0"
        )

    query = select(accounts_table.c.balance).where(accounts_table.c.id == card.account_id)
    balance = await session.execute(query)
    balance = balance.first()

    if balance[0] - money < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough money on card!"
        )

    stmt = update(accounts_table).where(accounts_table.c.id == card.account_id).values(balance=balance[0] - money)
    await session.execute(stmt)
    await session.commit()

    return {'message': 'good'}
