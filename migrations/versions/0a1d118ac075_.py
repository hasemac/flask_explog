"""empty message

Revision ID: 0a1d118ac075
Revises: 053fdf129b7e
Create Date: 2022-03-16 19:28:05.941404

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0a1d118ac075'
down_revision = '053fdf129b7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rfpc',
    sa.Column('shot', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('created', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('system', sa.Text(), nullable=True),
    sa.Column('order', sa.Text(), nullable=True),
    sa.Column('start_time', sa.Text(), nullable=True),
    sa.Column('end_time', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('shot')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rfpc')
    # ### end Alembic commands ###
