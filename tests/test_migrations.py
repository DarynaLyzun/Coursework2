"""Integration tests for database migrations."""

import os
from unittest.mock import patch

from alembic import command
from alembic.config import Config


def test_migrations_stairway():
    """Verifies that migrations can be upgraded and downgraded repeatedly."""
    test_db_url = "sqlite:///migration_test.db"

    with patch.dict(os.environ, {"DATABASE_URL": test_db_url}, clear=True):
        alembic_cfg = Config("alembic.ini")

        try:
            command.upgrade(alembic_cfg, "head")
            command.downgrade(alembic_cfg, "base")
            command.upgrade(alembic_cfg, "head")
        finally:
            if os.path.exists("migration_test.db"):
                os.remove("migration_test.db")