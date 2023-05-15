from pydantic import BaseModel, Field
from pydantic.schema import date


class CardCreate(BaseModel):
    pin: str = Field(regex=r'^\d{4}$')


class Card(BaseModel):
    pin: str
    number: str
    cvv: str
    date: date
    account_id: int
