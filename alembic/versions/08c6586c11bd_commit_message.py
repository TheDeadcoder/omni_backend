"""commit message

Revision ID: 08c6586c11bd
Revises: 4462f23de8b8
Create Date: 2024-06-13 19:06:53.287014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08c6586c11bd'
down_revision: Union[str, None] = '4462f23de8b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('calendar_entry', 'symptom_name',
               existing_type=sa.VARCHAR(),
               nullable='False')
    op.alter_column('calendar_entry', 'symptom_value',
               existing_type=sa.VARCHAR(),
               nullable='False')
    op.alter_column('calendar_entry', 'symptom_unit',
               existing_type=sa.VARCHAR(),
               nullable='True')
    op.drop_constraint('primary_user_super_id_fkey', 'primary_user', type_='foreignkey')
    op.drop_column('primary_user', 'super_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('primary_user', sa.Column('super_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('primary_user_super_id_fkey', 'primary_user', 'primary_user', ['super_id'], ['id'])
    op.alter_column('calendar_entry', 'symptom_unit',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('calendar_entry', 'symptom_value',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('calendar_entry', 'symptom_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
