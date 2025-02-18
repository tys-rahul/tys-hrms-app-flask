"""Create reimbursements table

Revision ID: e405576d4488
Revises: cc87d8e5f79c
Create Date: 2024-11-12 18:26:42.800480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e405576d4488'
down_revision = 'cc87d8e5f79c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reimbursements', schema=None) as batch_op:
        batch_op.alter_column(
            'user_id',
            existing_type=sa.VARCHAR(),
            type_=sa.Integer(),
            existing_nullable=False,
            postgresql_using='user_id::integer'  # Explicitly cast user_id to integer
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reimbursements', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)

    # ### end Alembic commands ###
