"""question field unique

Revision ID: 12e46efabb04
Revises: 78b2234a997a
Create Date: 2022-11-14 16:26:06.012791

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "12e46efabb04"
down_revision = "78b2234a997a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "quiz", ["question"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "quiz", type_="unique")
    # ### end Alembic commands ###
