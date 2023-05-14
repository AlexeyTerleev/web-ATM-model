from sqlalchemy import Table, Column, Integer, String, MetaData, Identity

metadata = MetaData()

accounts_table = Table(
    "account",
    metadata,
    Column("id", Integer, Identity(start=1, cycle=True), primary_key=True),

    Column("login", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("balance", Integer, nullable=False)
)



