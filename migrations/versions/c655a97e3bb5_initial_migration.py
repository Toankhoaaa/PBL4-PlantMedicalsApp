"""Initial migration

Revision ID: c655a97e3bb5
Revises: 
Create Date: 2024-11-04 14:49:14.875532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c655a97e3bb5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plants',
    sa.Column('plant_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('scientific_name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image_url', sa.String(length=200), nullable=True),
    sa.Column('family', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('plant_id')
    )
    op.create_table('regions',
    sa.Column('region_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('region_id')
    )
    op.create_table('chemical_components',
    sa.Column('component_id', sa.Integer(), nullable=False),
    sa.Column('plant_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('quantity', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['plant_id'], ['plants.plant_id'], ),
    sa.PrimaryKeyConstraint('component_id')
    )
    op.create_table('medicinal_uses',
    sa.Column('use_id', sa.Integer(), nullable=False),
    sa.Column('plant_id', sa.Integer(), nullable=False),
    sa.Column('application', sa.String(length=200), nullable=False),
    sa.Column('preparation_method', sa.Text(), nullable=True),
    sa.Column('dose', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['plant_id'], ['plants.plant_id'], ),
    sa.PrimaryKeyConstraint('use_id')
    )
    op.create_table('plant_regions',
    sa.Column('plant_id', sa.Integer(), nullable=False),
    sa.Column('region_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['plant_id'], ['plants.plant_id'], ),
    sa.ForeignKeyConstraint(['region_id'], ['regions.region_id'], ),
    sa.PrimaryKeyConstraint('plant_id', 'region_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('plant_regions')
    op.drop_table('medicinal_uses')
    op.drop_table('chemical_components')
    op.drop_table('regions')
    op.drop_table('plants')
    # ### end Alembic commands ###