"""added preset table

Revision ID: 003_7fe022eacc36
Revises: 002_88971660dfff
Create Date: 2017-11-16 23:47:20.895000

"""
from alembic import op
import sqlalchemy as db


# revision identifiers, used by Alembic.
revision = '003_7fe022eacc36'
down_revision = '002_88971660dfff'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('preset',
      db.Column('id', db.Integer(), nullable=False),
      db.Column('name', db.String(length=256), nullable=False),
      db.Column('json', db.String(length=4096), nullable=False),
      db.PrimaryKeyConstraint('id'),
      db.UniqueConstraint('name')
    )


def downgrade():
    op.drop_table('preset')
