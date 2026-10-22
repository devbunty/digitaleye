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
