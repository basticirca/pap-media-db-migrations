"""added preset table

Revision ID: 003_45a51fef73ca
Revises: 002_88971660dfff
Create Date: 2017-11-16 23:15:48.613000

"""
from alembic import op
import sqlalchemy as db


# revision identifiers, used by Alembic.
revision = '003_45a51fef73ca'
down_revision = '002_88971660dfff'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('preset',
      db.Column('id', db.Integer(), nullable=False),
      db.Column('json', db.String(length=4096), nullable=False),
      db.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('preset')