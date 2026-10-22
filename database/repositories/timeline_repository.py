from database.db import session_scope
from database.models import Incident, Telemetry
from database.timeutils import to_iso


def get_host_timeline(hostname: str) -> dict:
    """Telemetry samples and incidents for one host, newest first."""
    with session_scope() as session:
        telemetry = (
            session.query(Telemetry)
            .filter(Telemetry.hostname == hostname)
            .order_by(Telemetry.collection_time.desc())
            .all()
        )
        incidents = (
            session.query(Incident)
            .filter(Incident.hostname == hostname)
            .order_by(Incident.timestamp.desc())
            .all()
        )

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
