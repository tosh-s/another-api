"""add remaining columns to posts table

Revision ID: fa949dddff13
Revises: 24646361361d
Create Date: 2022-07-26 17:10:41.548138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa949dddff13'
## notice the up revision and down revision codes available to update or rollback changes.
down_revision = '24646361361d'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
     pass


def downgrade():
    op.drop_column('posts','content')
    pass
