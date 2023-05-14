from pydantic import BaseModel, Field


class CardCreate(BaseModel):
    pin: str = Field(regex=r'^\d{4}$')
