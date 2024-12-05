"""Create Run Metadata Table [ec0d785ca296].

Revision ID: ec0d785ca296
Revises: 72722dee4686
Create Date: 2022-12-16 11:34:17.005750

"""

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "ec0d785ca296"
down_revision = "72722dee4686"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table("pipeline_run", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("enable_artifact_metadata", sa.Boolean(), nullable=True)
        )

    with op.batch_alter_table("step_run", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("enable_artifact_metadata", sa.Boolean(), nullable=True)
        )

    op.create_table(
        "run_metadata",
        sa.Column(
            "pipeline_run_id", sqlmodel.sql.sqltypes.GUID(), nullable=True
        ),
        sa.Column("step_run_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("artifact_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column(
            "stack_component_id", sqlmodel.sql.sqltypes.GUID(), nullable=True
        ),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column(
            "workspace_id", sqlmodel.sql.sqltypes.GUID(), nullable=False
        ),
        sa.Column("value", sa.TEXT(), nullable=False),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("key", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pipeline_run_id"],
            ["pipeline_run.id"],
            name="fk_run_metadata_pipeline_run_id_pipeline_run",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspace.id"],
            name="fk_run_metadata_workspace_id_workspace",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["stack_component_id"],
            ["stack_component.id"],
            name="fk_run_metadata_stack_component_id_stack_component",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["step_run_id"],
            ["step_run.id"],
            name="fk_run_metadata_step_run_id_step_run",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["artifact_id"],
            ["artifact.id"],
            name="fk_run_metadata_artifact_id_artifact",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name="fk_run_metadata_user_id_user",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("step_run", schema=None) as batch_op:
        batch_op.drop_column("enable_artifact_metadata")

    with op.batch_alter_table("pipeline_run", schema=None) as batch_op:
        batch_op.drop_column("enable_artifact_metadata")

    op.drop_table("run_metadata")
    # ### end Alembic commands ###
