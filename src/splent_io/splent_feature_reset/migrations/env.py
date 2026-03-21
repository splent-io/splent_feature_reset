"""Alembic migration environment for splent_feature_reset."""

from splent_io.splent_feature_reset import models  # registers ResetToken with db.metadata  # noqa
from splent_framework.migrations.feature_env import run_feature_migrations

FEATURE_NAME = "splent_feature_reset"
FEATURE_TABLES = {"reset_token"}

run_feature_migrations(FEATURE_NAME, FEATURE_TABLES)
