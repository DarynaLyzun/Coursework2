"""Integration tests for Alembic migrations."""
from alembic import command
from alembic.config import Config

def test_migrations_stairway():
    """Verifies that the database schema allows full upgrades and downgrades.

    Executes a 'Stairway' test strategy to ensure migration scripts are 
    structurally sound and reversible. The process involves:
    1. Upgrading to 'head' (creating all tables).
    2. Downgrading to 'base' (dropping all tables).
    3. Upgrading to 'head' again (restoring the schema).
    """
    alembic_cfg = Config("alembic.ini")
    
    command.upgrade(alembic_cfg, "head")
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")