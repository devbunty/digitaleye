<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
from sqlalchemy import and_, func

from database.db import session_scope
from database.models import Telemetry
from database.timeutils import utc_now


def save_telemetry(telemetry: dict) -> None:
    system = telemetry.get("system", {})

    with session_scope() as session:
        session.add(
            Telemetry(
                hostname=system.get("hostname", "unknown"),
                collection_time=utc_now(),
                cpu_usage=system.get("cpu_usage", 0.0),
                memory_usage=system.get("memory_usage", 0.0),
                process_count=len(telemetry.get("processes", [])),
            )
        )


def latest_telemetry_by_host(session) -> dict[str, Telemetry]:
    """Newest telemetry sample for every host, keyed by hostname."""
    newest = (
        session.query(
            Telemetry.hostname,
            func.max(Telemetry.collection_time).label("latest_time"),
        )
        .group_by(Telemetry.hostname)
        .subquery()
    )

    rows = (
        session.query(Telemetry)
        .join(
            newest,
            and_(
                Telemetry.hostname == newest.c.hostname,
                Telemetry.collection_time == newest.c.latest_time,
            ),
        )
        .all()
    )
    return {row.hostname: row for row in rows}
<<<<<<< HEAD
=======
=======
from datetime import datetime, UTC

from database.db import SessionLocal
from database.models import Telemetry


def save_telemetry(telemetry):

    session = SessionLocal()

    try:

        system = telemetry.get("system", {})
        processes = telemetry.get("processes", [])

        record = Telemetry(

            hostname=system.get("hostname", "unknown"),

            collection_time=datetime.now(UTC),

            cpu_usage=system.get("cpu_usage", 0.0),

            memory_usage=system.get("memory_usage", 0.0),

            process_count=len(processes)

        )

        session.add(record)

        session.commit()

    finally:

        session.close()
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
