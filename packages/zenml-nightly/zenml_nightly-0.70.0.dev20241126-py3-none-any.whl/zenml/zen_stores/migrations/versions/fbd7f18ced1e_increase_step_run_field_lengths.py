"""Increase step run field lengths [fbd7f18ced1e].

Revision ID: fbd7f18ced1e
Revises: 979eff8fc4b1
Create Date: 2023-04-24 14:21:58.080294

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "fbd7f18ced1e"
down_revision = "979eff8fc4b1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("step_run", schema=None) as batch_op:
        batch_op.alter_column(
            "parameters",
            existing_type=sa.TEXT(),
            type_=sa.String(length=16777215).with_variant(
                mysql.MEDIUMTEXT, "mysql"
            ),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "step_configuration",
            existing_type=sa.TEXT(),
            type_=sa.String(length=16777215).with_variant(
                mysql.MEDIUMTEXT, "mysql"
            ),
            existing_nullable=False,
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("step_run", schema=None) as batch_op:
        batch_op.alter_column(
            "step_configuration",
            existing_type=sa.String(length=16777215).with_variant(
                mysql.MEDIUMTEXT, "mysql"
            ),
            type_=sa.TEXT(),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "parameters",
            existing_type=sa.String(length=16777215).with_variant(
                mysql.MEDIUMTEXT, "mysql"
            ),
            type_=sa.TEXT(),
            existing_nullable=False,
        )

    # ### end Alembic commands ###
