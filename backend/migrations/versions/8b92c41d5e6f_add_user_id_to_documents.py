"""add_user_id_to_documents

Revision ID: 8b92c41d5e6f
Revises: 794570c1769d
Create Date: 2026-11-22 12:44:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8b92c41d5e6f'
down_revision: Union[str, Sequence[str], None] = '794570c1769d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('documents', sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        op.f('fk_documents_user_id_users'),
        'documents',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.create_index(op.f('ix_documents_user_id'), 'documents', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_documents_user_id'), table_name='documents')
    op.drop_constraint(op.f('fk_documents_user_id_users'), 'documents', type_='foreignkey')
    op.drop_column('documents', 'user_id')
