"""add dataset quality info

Revision ID: 569c9af54b7d
Revises: 462bb8753b76
Create Date: 2026-09-01 21:25:09.604387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '569c9af54b7d'
down_revision: Union[str, Sequence[str], None] = '462bb8753b76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "dataset_profiles",
        sa.Column(
            "quality_info",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'::json"),
        ),
    )

    op.alter_column(
        "dataset_profiles",
        "quality_info",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("dataset_profiles", "quality_info")
