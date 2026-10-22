<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
from database.db import session_scope
from database.models import Incident, Telemetry
from database.timeutils import to_iso


def get_host_timeline(hostname: str) -> dict:
    """Telemetry samples and incidents for one host, newest first."""
    with session_scope() as session:
<<<<<<< HEAD
=======
=======
from database.db import SessionLocal
from database.models import Telemetry, Incident


def get_host_timeline(hostname):

    session = SessionLocal()

    try:

>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
        telemetry = (
            session.query(Telemetry)
            .filter(Telemetry.hostname == hostname)
            .order_by(Telemetry.collection_time.desc())
            .all()
        )
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======

>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
        incidents = (
            session.query(Incident)
            .filter(Incident.hostname == hostname)
            .order_by(Incident.timestamp.desc())
            .all()
        )

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
        return {
            "hostname": hostname,
            "telemetry": [
                {
                    "time": to_iso(t.collection_time),
                    "cpu": t.cpu_usage,
                    "memory": t.memory_usage,
                    "processes": t.process_count,
                }
                for t in telemetry
            ],
            "incidents": [
                {
                    "time": to_iso(i.timestamp),
                    "rule": i.rule_id,
                    "title": i.title,
                    "severity": i.severity,
                    "evidence": i.evidence,
                }
                for i in incidents
            ],
        }
<<<<<<< HEAD
=======
=======
        return telemetry, incidents

    finally:

        session.close()
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
