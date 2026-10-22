<<<<<<< HEAD
from database.db import session_scope
from database.models import Incident

OPEN = "Open"
RESOLVED = "Resolved"


def save_incident(hostname, rule_id, title, severity, mitre, category, evidence) -> int:
    """Insert a new open incident and return its database id."""
    with session_scope() as session:
        incident = Incident(
            hostname=hostname,
            rule_id=rule_id,
            title=title,
            severity=severity,
            mitre=mitre,
            category=category,
            evidence=evidence,
            status=OPEN,
        )
        session.add(incident)
        session.flush()
        return incident.id


def has_open_incident(hostname: str, rule_id: str) -> bool:
    with session_scope() as session:
        return (
            session.query(Incident.id)
            .filter(
                Incident.hostname == hostname,
                Incident.rule_id == rule_id,
                Incident.status == OPEN,
            )
            .first()
            is not None
        )


def get_open_incidents(hostname: str) -> list[dict]:
    with session_scope() as session:
        rows = (
            session.query(Incident)
            .filter(Incident.hostname == hostname, Incident.status == OPEN)
            .all()
        )
        return [row.to_dict() for row in rows]


def _resolve_first(hostname: str, rule_id: str, evidence: str | None = None) -> None:
    with session_scope() as session:
        query = session.query(Incident).filter(
            Incident.hostname == hostname,
            Incident.rule_id == rule_id,
            Incident.status == OPEN,
        )
        if evidence is not None:
            query = query.filter(Incident.evidence == evidence)

        incident = query.first()
        if incident:
            incident.status = RESOLVED


def resolve_incident(hostname: str, rule_id: str) -> None:
    """Mark the open incident for ``rule_id`` on ``hostname`` as resolved."""
    _resolve_first(hostname, rule_id)


def resolve_drift_incident(hostname: str, rule_id: str, evidence: str) -> None:
    """Resolve a drift incident once the drifted item disappears again."""
    _resolve_first(hostname, rule_id, evidence)


def get_recent_incidents(limit: int = 200, status=None, hostname=None) -> list[dict]:
    """Incidents across the fleet (or one host), most recent first."""
    with session_scope() as session:
        query = session.query(Incident)
        if status:
            query = query.filter(Incident.status == status)
        if hostname:
            query = query.filter(Incident.hostname == hostname)

        rows = query.order_by(Incident.timestamp.desc()).limit(limit).all()
        return [row.to_dict() for row in rows]


def get_incident_by_id(incident_id: int) -> dict | None:
    with session_scope() as session:
        row = session.get(Incident, incident_id)
        return row.to_dict() if row else None
=======
from sqlalchemy import func

from database.db import SessionLocal
from database.models import Incident


def save_incident(
    hostname,
    rule_id,
    title,
    severity,
    mitre,
    category,
    evidence,
):

    session = SessionLocal()

    incident = Incident(
        hostname=hostname,
        rule_id=rule_id,
        title=title,
        severity=severity,
        mitre=mitre,
        category=category,
        evidence=evidence,
        status="Open",
    )

    session.add(incident)
    session.commit()
    session.refresh(incident)

    incident_id = incident.id

    session.close()

    return incident_id


def get_open_incident(hostname, rule_id):

    session = SessionLocal()

    incident = (
        session.query(Incident)
        .filter(
            Incident.hostname == hostname,
            Incident.rule_id == rule_id,
            Incident.status == "Open",
        )
        .first()
    )

    session.close()

    return incident


def resolve_incident(hostname, rule_id):

    session = SessionLocal()

    incident = (
        session.query(Incident)
        .filter(
            Incident.hostname == hostname,
            Incident.rule_id == rule_id,
            Incident.status == "Open",
        )
        .first()
    )

    if incident:
        incident.status = "Resolved"
        session.commit()

    session.close()


def get_all_open_incidents(hostname):

    session = SessionLocal()

    incidents = (
        session.query(Incident)
        .filter(
            Incident.hostname == hostname,
            Incident.status == "Open",
        )
        .all()
    )

    session.close()

    return incidents


def get_open_drift_incidents(hostname):

    session = SessionLocal()

    incidents = (
        session.query(Incident)
        .filter(
            Incident.hostname == hostname,
            Incident.status == "Open",
            Incident.rule_id.like("DRIFT-%")
        )
        .all()
    )

    session.close()

    return incidents


def resolve_drift_incident(hostname, rule_id, evidence):

    session = SessionLocal()

    incident = (
        session.query(Incident)
        .filter(
            Incident.hostname == hostname,
            Incident.rule_id == rule_id,
            Incident.status == "Open",
            Incident.evidence == evidence
        )
        .first()
    )

    if incident:
        incident.status = "Resolved"
        session.commit()

    session.close()


def get_top_mitre():

    session = SessionLocal()

    rows = (
        session.query(
            Incident.mitre,
            func.count(Incident.id).label("count")
        )
        .filter(Incident.status == "Open")
        .group_by(Incident.mitre)
        .order_by(func.count(Incident.id).desc())
        .limit(5)
        .all()
    )

    session.close()

    return [
        {
            "mitre": row.mitre,
            "count": row.count
        }
        for row in rows
    ]


def get_recent_incidents(limit=200, status=None, hostname=None):
    """Return recent incidents across the fleet (or one host), most recent first.

    Used by the /incidents and /dashboard/incidents API routes.
    """

    session = SessionLocal()

    query = session.query(Incident)

    if status:
        query = query.filter(Incident.status == status)

    if hostname:
        query = query.filter(Incident.hostname == hostname)

    rows = (
        query
        .order_by(Incident.timestamp.desc())
        .limit(limit)
        .all()
    )

    result = [
        {
            "id": row.id,
            "timestamp": row.timestamp.isoformat() if row.timestamp else None,
            "hostname": row.hostname,
            "rule_id": row.rule_id,
            "title": row.title,
            "severity": row.severity,
            "mitre": row.mitre,
            "category": row.category,
            "evidence": row.evidence,
            "status": row.status,
        }
        for row in rows
    ]

    session.close()

    return result


def get_incident_by_id(incident_id):

    session = SessionLocal()

    row = session.query(Incident).filter(Incident.id == incident_id).first()

    session.close()

    if not row:
        return None

    return {
        "id": row.id,
        "timestamp": row.timestamp.isoformat() if row.timestamp else None,
        "hostname": row.hostname,
        "rule_id": row.rule_id,
        "title": row.title,
        "severity": row.severity,
        "mitre": row.mitre,
        "category": row.category,
        "evidence": row.evidence,
        "status": row.status,
    }
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
