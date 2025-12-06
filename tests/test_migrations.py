"""Integration tests for Alembic migrations."""
import os
from unittest.mock import patch
from alembic import command
from alembic.config import Config

def test_migrations_stairway():
    """Verifies that the database schema allows full upgrades and downgrades.

    Executes a 'Stairway' test strategy to ensure migration scripts are 
    structurally sound and reversible. We use a file-based SQLite database
    to persist state between the upgrade/downgrade commands, ensuring
    we don't accidentally touch the production DB.
    """
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