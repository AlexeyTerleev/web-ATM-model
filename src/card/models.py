import sqlalchemy
from sqlalchemy import MetaData, Identity, Integer, String, DATE

from src.auth.models import accounts_table

metadata = MetaData()

cards_table = sqlalchemy.Table(
    "card",
    metadata,
    sqlalchemy.Column("id", Integer, Identity(start=1, cycle=True), primary_key=True),

    sqlalchemy.Column("pin", String(4)),
    sqlalchemy.Column("number", String(8)),
    sqlalchemy.Column("cvv", String(3)),
    sqlalchemy.Column("date", DATE),

    sqlalchemy.Column("account_id", sqlalchemy.ForeignKey(accounts_table.c.id)),
)
