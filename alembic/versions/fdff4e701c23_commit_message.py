"""commit message

Revision ID: fdff4e701c23
Revises: b5d70b7036d0
Create Date: 2024-06-14 02:54:49.414528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdff4e701c23'
down_revision: Union[str, None] = 'b5d70b7036d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pill_consumption',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('primary_id', sa.UUID(), nullable=False),
    sa.Column('calender_entry_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('time', sa.Date(), nullable=False),
    sa.Column('dosage', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['calender_entry_id'], ['calendar_entry.id'], ),
    sa.ForeignKeyConstraint(['primary_id'], ['primary_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('calendar_entry', 'symptom_name',
               existing_type=sa.VARCHAR(),
               nullable='False')
    op.alter_column('calendar_entry', 'symptom_value',
               existing_type=sa.VARCHAR(),
               nullable='False')
    op.alter_column('calendar_entry', 'symptom_unit',
               existing_type=sa.VARCHAR(),
               nullable='True')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('calendar_entry', 'symptom_unit',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('calendar_entry', 'symptom_value',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('calendar_entry', 'symptom_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_table('pill_consumption')
    # ### end Alembic commands ###
