"""empty message

Revision ID: be5094a33db4
Revises: 
Create Date: 2022-03-25 21:27:07.221357

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'be5094a33db4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rfpc',
    sa.Column('shot', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('created', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('sys', sa.Text(), nullable=True),
    sa.Column('order_value', sa.Text(), nullable=True),
    sa.Column('start_time', sa.Text(), nullable=True),
    sa.Column('end_time', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('shot')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rfpc')
    # ### end Alembic commands ###