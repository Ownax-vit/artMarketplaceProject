"""init

Revision ID: e5a47271acff
Revises: 
Create Date: 2023-07-15 14:32:09.093769

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Table, MetaData

from src.config import settings
from src.auth.schemas import UserDB

# revision identifiers, used by Alembic.

revision = 'e5a47271acff'
down_revision = None
branch_labels = None
depends_on = None


admin_user = UserDB(login=settings.admin_login, email=settings.admin_email, is_admin=True)
admin_user.change_password(settings.admin_pass)
dict_admin = admin_user.model_dump()

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('url_image', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug_name', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.CheckConstraint('char_length(name) > 4', name='name_min_length'),
    sa.CheckConstraint('char_length(slug_name) > 4', name='slug_name_min_length'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug_name'),
    sa.UniqueConstraint('url_image')
    )
    op.create_table('users',
    sa.Column('login', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('salt', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.create_table('subcategories',
    sa.Column('category_id', sa.Uuid(), nullable=False),
    sa.Column('url_image', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug_name', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.CheckConstraint('char_length(name) > 4', name='name_min_length'),
    sa.CheckConstraint('char_length(slug_name) > 4', name='slug_name_min_length'),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug_name'),
    sa.UniqueConstraint('url_image')
    )
    op.create_table('products',
    sa.Column('subcategory_id', sa.Uuid(), nullable=False),
    sa.Column('url_image_small', sa.String(length=255), nullable=False),
    sa.Column('url_image_medium', sa.String(length=255), nullable=False),
    sa.Column('url_image_large', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug_name', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.CheckConstraint('char_length(name) > 4', name='name_min_length'),
    sa.CheckConstraint('char_length(slug_name) > 4', name='slug_name_min_length'),
    sa.ForeignKeyConstraint(['subcategory_id'], ['subcategories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug_name')
    )
    op.create_table('baskets',
    sa.Column('product_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('product_id', 'user_id')
    )
    # ### end Alembic commands ###

    # create admin user
    meta = MetaData()
    meta.reflect(bind=op.get_bind())
    table_tbl = Table("users", meta)
    op.bulk_insert(table_tbl, [
        dict_admin,
    ],)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('baskets')
    op.drop_table('products')
    op.drop_table('subcategories')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###
