"""empty message

Revision ID: 45a519fbdd87
Revises: fcedd337efa3
Create Date: 2023-09-10 17:13:12.350488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45a519fbdd87'
down_revision = 'fcedd337efa3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('round_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'round_id')
    # ### end Alembic commands ###
