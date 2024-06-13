"""commit message

Revision ID: a374a9e45026
Revises: 8139079c3164
Create Date: 2024-06-13 20:57:53.334551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a374a9e45026'
down_revision: Union[str, None] = '8139079c3164'
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
    op.add_column('relationship', sa.Column('accepted', sa.Boolean(), nullable=False))
    op.add_column('secondary_user', sa.Column('email', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'secondary_user', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'secondary_user', type_='unique')
    op.drop_column('secondary_user', 'email')
    op.drop_column('relationship', 'accepted')
    op.alter_column('calendar_entry', 'symptom_unit',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('calendar_entry', 'symptom_value',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('calendar_entry', 'symptom_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###