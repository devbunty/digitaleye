<<<<<<< HEAD
from sqlalchemy import Column

from database.db import session_scope
from database.models import Process
from database.timeutils import utc_now


def save_processes(telemetry: dict) -> None:
    hostname = telemetry["system"]["hostname"]
    collected = utc_now()

    with session_scope() as session:
        session.add_all(
            Process(
                hostname=hostname,
                collection_time=collected,
                pid=proc.get("pid", 0),
                name=proc.get("name", ""),
                user=proc.get("user", ""),
                cpu_percent=proc.get("cpu_percent", 0),
                memory_percent=proc.get("memory_percent", 0),
                command=proc.get("command", ""),
            )
            for proc in telemetry.get("processes", [])
        )


def _search(column: Column, keyword: str | None = None, limit: int | None = None) -> list[dict]:
    with session_scope() as session:
        query = session.query(Process)
        if keyword is not None:
            query = query.filter(column.ilike(f"%{keyword}%"))
        query = query.order_by(Process.collection_time.desc())
        if limit:
            query = query.limit(limit)
        return [row.to_dict() for row in query.all()]


def get_all_processes(limit: int = 100) -> list[dict]:
    return _search(Process.name, limit=limit)


def search_process(name: str) -> list[dict]:
    """Processes whose name contains ``name`` (case-insensitive)."""
    return _search(Process.name, name)


def search_command(keyword: str) -> list[dict]:
    """Processes whose command line contains ``keyword`` (case-insensitive)."""
    return _search(Process.command, keyword)
=======
from datetime import datetime, UTC

from database.db import SessionLocal
from database.models import Process


def save_processes(telemetry):

    session = SessionLocal()

    try:

        hostname = telemetry["system"]["hostname"]

        collected = datetime.now(UTC)

        for proc in telemetry.get("processes", []):

            process = Process(

                hostname=hostname,

                collection_time=collected,

                pid=proc.get("pid", 0),

                name=proc.get("name", ""),

                user=proc.get("user", ""),

                cpu_percent=proc.get("cpu_percent", 0),

                memory_percent=proc.get("memory_percent", 0),

                command=proc.get("command", "")

            )

            session.add(process)

        session.commit()

    finally:

        session.close()
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
