"""Add user table

Revision ID: ea20b018b927
Revises: 9600f9e87958
Create Date: 2022-04-15 00:24:01.381926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea20b018b927'
down_revision = '9600f9e87958'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                             sa.Column('email', sa.String(), nullable=False),
                             sa.Column('password', sa.String(), nullable=False),
                             sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                             sa.PrimaryKeyConstraint('id'),
                             sa.UniqueConstraint('email'))

pass


def downgrade():
    op.drop_table('users') 
    pass
