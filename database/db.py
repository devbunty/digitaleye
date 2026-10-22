"""Database engine and session management."""

import logging
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import config

logger = logging.getLogger(__name__)


def _adopt_legacy_database() -> None:
    """Rename the pre-rebrand ``osvf.db`` so existing data keeps working."""
    if config.DB_PATH.exists() or not config.LEGACY_DB_PATH.exists():
        return
    config.LEGACY_DB_PATH.rename(config.DB_PATH)
    logger.info("Renamed %s to %s", config.LEGACY_DB_PATH.name, config.DB_PATH.name)


_adopt_legacy_database()

engine = create_engine(f"sqlite:///{config.DB_PATH}", echo=False, future=True)

# expire_on_commit=False keeps loaded rows readable after the session closes,
# which is how the repositories hand data back to their callers.
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Yield a session that commits on success, rolls back on error, always closes."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
