"""add foreign key to posts table

Revision ID: 8f7f3ef023d7
Revises: a692ec37d7dd
Create Date: 2022-08-02 13:43:08.233664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f7f3ef023d7'
down_revision = 'a692ec37d7dd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", 
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', column_name="posts_id")
    pass
