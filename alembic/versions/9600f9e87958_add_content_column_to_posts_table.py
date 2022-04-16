"""add content column to posts table

Revision ID: 9600f9e87958
Revises: aca72e12a2a1
Create Date: 2022-04-14 20:30:26.980033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9600f9e87958'
down_revision = 'aca72e12a2a1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
