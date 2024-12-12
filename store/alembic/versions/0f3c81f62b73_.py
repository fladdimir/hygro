"""empty message

Revision ID: 0f3c81f62b73
Revises: 
Create Date: 2024-11-23 12:57:36.528292

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0f3c81f62b73"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "measurement",
        sa.Column("sensor_id", sa.String(), nullable=False),
        sa.Column("tsp", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "measurement_type",
            sa.Enum("HUMIDITY", "TEMPERATURE", name="measurementtype"),
            nullable=False,
        ),
        sa.Column("value", sa.Numeric(precision=6, scale=3), nullable=False),
        # do not create pk:
        # sa.PrimaryKeyConstraint('sensor_id', 'tsp', 'measurement_type')
    )
    # setup timescaledb hypertable:
    op.execute("SELECT create_hypertable('measurement', by_range('tsp'));")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("measurement")
    # drop measurementtype enum type
    op.execute('DROP TYPE public."measurementtype"')
    # ### end Alembic commands ###
