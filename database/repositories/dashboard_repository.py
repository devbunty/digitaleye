<<<<<<< HEAD
from sqlalchemy import func

from database.db import session_scope
from database.models import Host, Incident
from database.repositories.incident_repository import OPEN
from database.repositories.mitre_repository import count_open_techniques
from database.repositories.telemetry_repository import latest_telemetry_by_host
from database.timeutils import to_iso

SEVERITIES = ("Critical", "High", "Medium", "Low")

# How much each open incident of a given severity lowers the health score.
HEALTH_PENALTY = {"Critical": 18, "High": 10, "Medium": 4, "Low": 1}
# How much each open incident adds to the threat score.
THREAT_WEIGHT = {"Critical": 10, "High": 5, "Medium": 2, "Low": 1}


def _open_counts_by_severity(session) -> dict[str, int]:
    rows = (
        session.query(Incident.severity, func.count(Incident.id))
        .filter(Incident.status == OPEN)
        .group_by(Incident.severity)
        .all()
    )
    return dict(rows)


def get_host_resource_inventory() -> list[dict]:
    """Hosts that have reported telemetry, with their latest CPU/memory."""
    with session_scope() as session:
        hosts = session.query(Host).order_by(Host.hostname).all()
        latest = latest_telemetry_by_host(session)

        return [
            {
                "hostname": host.hostname,
                "ip": host.ip,
                "os": host.os,
                "cpu": round(latest[host.hostname].cpu_usage or 0, 1),
                "memory": round(latest[host.hostname].memory_usage or 0, 1),
                "last_seen": to_iso(host.last_seen),
                "status": host.status,
            }
            for host in hosts
            if host.hostname in latest
        ]


def get_dashboard_summary() -> dict:
    """Fleet KPIs based on the latest telemetry sample of each host.

    Averaging the whole telemetry history mixes in stale samples and breaks
    as soon as several hosts report, so we always reduce to latest-per-host.
    """
    with session_scope() as session:
        hosts = session.query(Host).all()
        latest = list(latest_telemetry_by_host(session).values())
        open_by_severity = _open_counts_by_severity(session)

    if latest:
        avg_cpu = sum(t.cpu_usage or 0 for t in latest) / len(latest)
        avg_memory = sum(t.memory_usage or 0 for t in latest) / len(latest)
        last_sync = max(t.collection_time for t in latest)
    else:
        avg_cpu = avg_memory = 0
        last_sync = None

    total_hosts = len(hosts)
    online_hosts = sum(1 for host in hosts if host.is_online)

    # Security health is incident-driven; resource pressure only counts once
    # hosts are genuinely saturated.
    health = 100.0
    for severity, penalty in HEALTH_PENALTY.items():
        health -= open_by_severity.get(severity, 0) * penalty
    health -= max(0.0, (avg_cpu + avg_memory) / 2 - 70) * 0.4

    return {
        "total_hosts": total_hosts,
        "online_hosts": online_hosts,
        "offline_hosts": max(total_hosts - online_hosts, 0),
        "critical_alerts": open_by_severity.get("Critical", 0),
        "open_incidents": sum(open_by_severity.values()),
        "average_cpu": round(avg_cpu, 2),
        "average_memory": round(avg_memory, 2),
        "security_health": round(max(0.0, min(100.0, health)), 1),
        "last_sync": to_iso(last_sync),
    }


def get_live_threat_feed(limit: int = 10) -> list[dict]:
    """Newest open incidents, or the newest overall when nothing is open."""
    with session_scope() as session:
        query = session.query(Incident).order_by(Incident.timestamp.desc())
        rows = query.filter(Incident.status == OPEN).limit(limit).all()
        if not rows:
            rows = query.limit(limit).all()

        return [
            {
=======
from datetime import datetime

from sqlalchemy import func, and_

from database.models import Host
from database.models import Incident
from database.models import Telemetry
from database.db import SessionLocal


def get_host_resource_inventory():

    session = SessionLocal()

    try:

        latest = (

            session.query(

                Telemetry.hostname,

                func.max(
                    Telemetry.collection_time
                ).label("latest_time")

            )

            .group_by(Telemetry.hostname)

            .subquery()

        )

        rows = (

            session.query(

                Host.hostname,

                Host.ip,

                Host.os,

                Host.last_seen,

                Host.is_demo,

                Telemetry.cpu_usage,

                Telemetry.memory_usage

            )

            .join(

                latest,

                Host.hostname == latest.c.hostname

            )

            .join(

                Telemetry,

                and_(

                    Telemetry.hostname == latest.c.hostname,

                    Telemetry.collection_time == latest.c.latest_time

                )

            )

            .order_by(Host.hostname)

            .all()

        )

        inventory = []

        for row in rows:

            last_seen = row.last_seen
            online = bool(row.is_demo)
            if not online and last_seen is not None:
                seen = last_seen.replace(tzinfo=None) if last_seen.tzinfo else last_seen
                online = (datetime.utcnow() - seen).total_seconds() <= 120

            inventory.append({
                "hostname": row.hostname,
                "ip": row.ip,
                "os": row.os,
                "cpu": round(row.cpu_usage or 0, 1),
                "memory": round(row.memory_usage or 0, 1),
                "last_seen": last_seen.isoformat() if last_seen else None,
                "status": "Online" if online else "Offline",
            })

        return inventory

    finally:

        session.close()


def get_cpu_memory_history(limit=50):

    session = SessionLocal()

    try:

        rows = (
            session.query(Telemetry)
            .order_by(Telemetry.collection_time.desc())
            .limit(limit)
            .all()
        )

        rows.reverse()

        return rows

    finally:

        session.close()


def get_dashboard_summary():
    """Fleet KPIs using the latest telemetry sample per host.

    Averaging the entire telemetry history mixes old samples and breaks
    when more than one host is reporting — always reduce to latest/host.
    """

    session = SessionLocal()

    try:

        total_hosts = session.query(Host).count()

        latest_per_host = (
            session.query(
                Telemetry.hostname,
                func.max(Telemetry.collection_time).label("latest_time"),
            )
            .group_by(Telemetry.hostname)
            .subquery()
        )

        latest_rows = (
            session.query(Telemetry)
            .join(
                latest_per_host,
                and_(
                    Telemetry.hostname == latest_per_host.c.hostname,
                    Telemetry.collection_time == latest_per_host.c.latest_time,
                ),
            )
            .all()
        )

        if latest_rows:
            avg_cpu = sum(r.cpu_usage or 0 for r in latest_rows) / len(latest_rows)
            avg_memory = sum(r.memory_usage or 0 for r in latest_rows) / len(latest_rows)
            last_sync = max(r.collection_time for r in latest_rows)
        else:
            avg_cpu = 0
            avg_memory = 0
            last_sync = None

        critical_alerts = (
            session.query(Incident)
            .filter(
                Incident.severity == "Critical",
                Incident.status == "Open",
            )
            .count()
        )

        open_incidents = (
            session.query(Incident)
            .filter(Incident.status == "Open")
            .count()
        )

        high_open = (
            session.query(Incident)
            .filter(
                Incident.severity == "High",
                Incident.status == "Open",
            )
            .count()
        )

        medium_open = (
            session.query(Incident)
            .filter(
                Incident.severity == "Medium",
                Incident.status == "Open",
            )
            .count()
        )

        low_open = (
            session.query(Incident)
            .filter(
                Incident.severity == "Low",
                Incident.status == "Open",
            )
            .count()
        )

        online_hosts = 0
        now = datetime.utcnow()
        for host in session.query(Host).all():
            if host.is_demo:
                online_hosts += 1
                continue
            if host.last_seen is None:
                continue
            seen = host.last_seen
            if seen.tzinfo:
                seen = seen.replace(tzinfo=None)
            if (now - seen).total_seconds() <= 120:
                online_hosts += 1

        # Security health is incident-driven, not resource-driven
        health = 100.0
        health -= critical_alerts * 18
        health -= high_open * 10
        health -= medium_open * 4
        health -= low_open * 1
        # Mild resource pressure only when hosts are saturated
        pressure = max(0.0, ((avg_cpu + avg_memory) / 2) - 70)
        health -= pressure * 0.4

        return {
            "total_hosts": total_hosts,
            "online_hosts": online_hosts,
            "offline_hosts": max(total_hosts - online_hosts, 0),
            "critical_alerts": critical_alerts,
            "open_incidents": open_incidents,
            "average_cpu": round(avg_cpu, 2),
            "average_memory": round(avg_memory, 2),
            "security_health": round(max(0.0, min(100.0, health)), 1),
            "last_sync": last_sync.isoformat() if last_sync else None,
        }

    finally:

        session.close()


def get_live_threat_feed(limit=10):

    session = SessionLocal()

    try:
        # Prefer open threats; fall back to newest overall if none open
        rows = (
            session.query(Incident)
            .filter(Incident.status == "Open")
            .order_by(Incident.timestamp.desc())
            .limit(limit)
            .all()
        )

        if not rows:
            rows = (
                session.query(Incident)
                .order_by(Incident.timestamp.desc())
                .limit(limit)
                .all()
            )

        result = []

        for row in rows:
            result.append({
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
                "id": row.id,
                "hostname": row.hostname,
                "rule_id": row.rule_id,
                "title": row.title,
                "severity": row.severity,
                "status": row.status,
<<<<<<< HEAD
                "time": to_iso(row.timestamp),
            }
            for row in rows
        ]


def get_threat_intelligence() -> dict:
    """Open-incident counts per severity plus an overall threat level."""
    with session_scope() as session:
        counts = _open_counts_by_severity(session)
        affected_hosts = (
            session.query(func.count(func.distinct(Incident.hostname)))
            .filter(Incident.status == OPEN)
            .scalar()
        )

    score = sum(counts.get(sev, 0) * weight for sev, weight in THREAT_WEIGHT.items())

    if score > 50:
        level = "CRITICAL"
    elif score > 25:
        level = "HIGH"
    elif score > 10:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        **{sev.lower(): counts.get(sev, 0) for sev in SEVERITIES},
        "hosts": affected_hosts,
        "mitre": count_open_techniques(),
        "score": level,
    }
=======
                "time": row.timestamp.isoformat() if row.timestamp else None,
            })

        return result

    finally:
        session.close()
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
