"""upgrade legacy prototype schema to v2

Revision ID: 0002_upgrade_legacy
Revises: 0001_baseline
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "0002_upgrade_legacy"
down_revision = "0001_baseline"
branch_labels = None
depends_on = None


def _columns(table):
    return {c["name"] for c in inspect(op.get_bind()).get_columns(table)}


def upgrade():
    insp = inspect(op.get_bind())
    tables = set(insp.get_table_names())
    if "managers" in tables:
        cols = _columns("managers")
        if "keycloak_username" not in cols:
            op.add_column("managers", sa.Column("keycloak_username", sa.String(128), nullable=True))
            op.create_index("ix_managers_keycloak_username", "managers", ["keycloak_username"], unique=True)
        if "keycloak_user_id" in cols:
            # column existed in prototype; keep it.
            pass
    if "workflows" in tables and "version" not in _columns("workflows"):
        op.add_column("workflows", sa.Column("version", sa.Integer(), nullable=False, server_default="1"))
    if "interactions" in tables:
        cols = _columns("interactions")
        if "source" not in cols:
            op.add_column("interactions", sa.Column("source", sa.String(32), nullable=True))
            op.create_index("ix_interactions_source", "interactions", ["source"], unique=False)
        if "external_id" not in cols:
            op.add_column("interactions", sa.Column("external_id", sa.String(255), nullable=True))
            op.create_index("ix_interactions_external_id", "interactions", ["external_id"], unique=False)
        if "external_updated_at" not in cols:
            op.add_column("interactions", sa.Column("external_updated_at", sa.DateTime(), nullable=True))
        # PostgreSQL allows multiple NULLs in a unique constraint, which is exactly
        # what we need for manually-created interactions without external IDs.
        constraints = {x.get("name") for x in inspect(op.get_bind()).get_unique_constraints("interactions")}
        if "uq_interaction_source_external" not in constraints:
            op.create_unique_constraint("uq_interaction_source_external", "interactions", ["source", "external_id"])


def downgrade():
    # This migration is intentionally conservative: a downgrade must not silently
    # discard integration identifiers or user mappings from a live CRM database.
    pass
