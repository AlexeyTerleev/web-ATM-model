import sqlalchemy

from src.database import metadata


accounts_table = sqlalchemy.Table(
    "account",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),

    sqlalchemy.Column("login", sqlalchemy.String(40)),
    sqlalchemy.Column("password", sqlalchemy.String(40)),
    sqlalchemy.Column("balance", sqlalchemy.Integer)
)

cards_table = sqlalchemy.Table(
    "card",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),

    sqlalchemy.Column("pin", sqlalchemy.String(4)),
    sqlalchemy.Column("number", sqlalchemy.String(8)),
    sqlalchemy.Column("cvv", sqlalchemy.String(3)),
    sqlalchemy.Column("date", sqlalchemy.DATE),

    sqlalchemy.Column("account_id", sqlalchemy.ForeignKey(accounts_table.c.id)),
)
