"""empty message

Revision ID: 953e0e57ee54
Revises: 33517d06e1b9
Create Date: 2021-07-30 13:51:43.429129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '953e0e57ee54'
down_revision = '33517d06e1b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('batches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    op.add_column('stock_items', sa.Column('batch_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'stock_items', 'batches', ['batch_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stock_items', type_='foreignkey')
    op.drop_column('stock_items', 'batch_id')
    op.drop_table('batches')
    # ### end Alembic commands ###
