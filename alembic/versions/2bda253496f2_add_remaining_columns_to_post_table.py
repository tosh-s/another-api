"""add remaining columns to post table

Revision ID: 2bda253496f2
Revises: 8f7f3ef023d7
Create Date: 2022-08-02 22:10:08.172717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bda253496f2'
down_revision = '8f7f3ef023d7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.BOOLEAN(), nullable=False, server_default = 'TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable =False),)
    pass


def downgrade():
    op.drop_column('posts', column_name='published')
    op.drop_column('posts', column_name='published')
    pass
