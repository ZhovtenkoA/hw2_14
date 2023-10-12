"""usermodel

Revision ID: d624c55cbf2e
Revises: 4c5659d1eb18
Create Date: 2023-10-12 12:55:54.525786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d624c55cbf2e"
down_revision: Union[str, None] = "4c5659d1eb18"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=250), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("avatar", sa.String(length=255), nullable=True),
        sa.Column("refresh_token", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.add_column("contacts", sa.Column("users_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        None, "contacts", "users", ["users_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "contacts", type_="foreignkey")
    op.drop_column("contacts", "users_id")
    op.drop_table("users")
    # ### end Alembic commands ###
