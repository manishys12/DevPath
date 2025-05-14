"""Add custom roadmap fields

Revision ID: custom_roadmap_fields
Revises: 
Create Date: 2023-11-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'custom_roadmap_fields'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to the roadmap table
    op.add_column('roadmap', sa.Column('is_custom', sa.Boolean(), nullable=True, server_default='0'))
    op.add_column('roadmap', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.add_column('roadmap', sa.Column('is_public', sa.Boolean(), nullable=True, server_default='1'))
    op.add_column('roadmap', sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()))
    op.add_column('roadmap', sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now()))
    
    # Create foreign key for creator_id
    op.create_foreign_key('fk_roadmap_creator', 'roadmap', 'user', ['creator_id'], ['id'])


def downgrade():
    # Drop foreign key first
    op.drop_constraint('fk_roadmap_creator', 'roadmap', type_='foreignkey')
    
    # Drop columns
    op.drop_column('roadmap', 'updated_at')
    op.drop_column('roadmap', 'created_at')
    op.drop_column('roadmap', 'is_public')
    op.drop_column('roadmap', 'creator_id')
    op.drop_column('roadmap', 'is_custom')
