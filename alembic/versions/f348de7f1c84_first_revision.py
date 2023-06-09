"""First revision

Revision ID: f348de7f1c84
Revises: 
Create Date: 2023-04-30 16:55:46.415517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f348de7f1c84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, cycle=True), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('balance', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, cycle=True), nullable=False),
    sa.Column('pin', sa.String(length=4), nullable=True),
    sa.Column('number', sa.String(length=8), nullable=True),
    sa.Column('cvv', sa.String(length=3), nullable=True),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    op.drop_table('account')
    # ### end Alembic commands ###
