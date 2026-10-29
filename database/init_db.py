"""Create the Digital Eye database tables.

Safe to run repeatedly: existing tables are left untouched.
"""

import config
from database.db import engine
from database.models import Base


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("=" * 50)
    print(f" {config.APP_NAME} database ready: {config.DB_PATH.name}")
    print("=" * 50)
