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
                "id": row.id,
                "hostname": row.hostname,
                "rule_id": row.rule_id,
                "title": row.title,
                "severity": row.severity,
                "status": row.status,
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
