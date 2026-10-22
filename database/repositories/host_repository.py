import logging
import random
from datetime import timedelta

from database.db import session_scope
from database.models import Host, Incident, Process, Telemetry
from database.timeutils import to_iso, utc_now

logger = logging.getLogger(__name__)


def host_to_dict(host: Host) -> dict:
    return {
        "hostname": host.hostname,
        "ip": host.ip,
        "os": host.os,
        "kernel": host.kernel,
        "first_seen": to_iso(host.first_seen),
        "last_seen": to_iso(host.last_seen),
        "is_demo": bool(host.is_demo),
        "status": host.status,
    }


def list_hosts() -> list[dict]:
    with session_scope() as session:
        rows = session.query(Host).order_by(Host.hostname).all()
        return [host_to_dict(host) for host in rows]


def update_host(system: dict) -> None:
    """Register a host on first contact, refresh it on every heartbeat."""
    hostname = system["hostname"]
    now = utc_now()

    with session_scope() as session:
        host = session.query(Host).filter(Host.hostname == hostname).first()

        if host is None:
            host = Host(hostname=hostname, first_seen=now, is_demo=False)
            session.add(host)
            logger.info("New host registered: %s", hostname)
        else:
            logger.debug("Host updated: %s", hostname)

        host.ip = system["ip_address"]
        host.os = system["os"]
        host.kernel = system["kernel"]
        host.last_seen = now


# --- Demo hosts ----------------------------------------------------------------

DEMO_PROCESSES = [
    ("systemd", "root"),
    ("sshd", "root"),
    ("nginx", "www-data"),
    ("python3", "appuser"),
    ("cron", "root"),
    ("bash", "appuser"),
    ("node", "appuser"),
    ("postgres", "postgres"),
]

DEMO_INCIDENTS = [
    {
        "rule_id": "DRIFT-PROCESSES",
        "title": "New Process Detected",
        "severity": "Medium",
        "mitre": "Behavioral",
        "category": "processes",
    },
    {
        "rule_id": "DRIFT-SERVICES",
        "title": "New Service",
        "severity": "High",
        "mitre": "Behavioral",
        "category": "services",
    },
]

DEMO_OPERATING_SYSTEMS = ["Ubuntu 22.04 LTS", "Debian 12", "Windows Server 2022"]


def create_demo_host(hostname, ip=None, os_name=None, kernel=None) -> dict:
    """Create a host with no real agent behind it, seeded with sample data.

    The seeded telemetry, processes and incidents make every dashboard panel
    show something meaningful straight away. Only hosts created this way
    (``is_demo=True``) can later be removed through the API.
    """
    now = utc_now()

    with session_scope() as session:
        if session.query(Host).filter(Host.hostname == hostname).first():
            raise ValueError(f"Host '{hostname}' already exists")

        host = Host(
            hostname=hostname,
            ip=ip or f"10.50.0.{random.randint(2, 250)}",
            os=os_name or random.choice(DEMO_OPERATING_SYSTEMS),
            kernel=kernel or "6.8.0-demo-generic",
            first_seen=now,
            last_seen=now,
            is_demo=True,
        )
        session.add(host)

        # One telemetry sample every five minutes for the last hour.
        for i in range(12):
            session.add(
                Telemetry(
                    hostname=hostname,
                    collection_time=now - timedelta(minutes=5 * (11 - i)),
                    cpu_usage=round(random.uniform(8, 65), 1),
                    memory_usage=round(random.uniform(20, 75), 1),
                    process_count=random.randint(90, 210),
                )
            )

        for pid, (name, user) in enumerate(DEMO_PROCESSES, start=1000):
            session.add(
                Process(
                    hostname=hostname,
                    collection_time=now,
                    pid=pid,
                    name=name,
                    user=user,
                    cpu_percent=round(random.uniform(0, 12), 1),
                    memory_percent=round(random.uniform(0, 8), 1),
                    command=f"/usr/bin/{name}",
                )
            )

        # A couple of incidents of mixed status spread over the last few hours.
        for i, template in enumerate(DEMO_INCIDENTS):
            session.add(
                Incident(
                    hostname=hostname,
                    timestamp=now - timedelta(hours=i + 1),
                    evidence=f"demo-seeded evidence for {hostname}",
                    status="Resolved" if i % 2 else "Open",
                    **template,
                )
            )

        return {
            "hostname": hostname,
            "ip": host.ip,
            "os": host.os,
            "kernel": host.kernel,
            "is_demo": True,
        }


def delete_demo_host(hostname: str) -> None:
    """Remove a demo host and its seeded data.

    Raises ``ValueError`` if the host does not exist and ``PermissionError``
    if it is a real enrolled host, which can only be removed directly in the
    database, never through the API.
    """
    with session_scope() as session:
        host = session.query(Host).filter(Host.hostname == hostname).first()

        if not host:
            raise ValueError(f"Host '{hostname}' not found")

        if not host.is_demo:
            raise PermissionError(f"'{hostname}' is a live enrolled host: refusing to delete")

        for model in (Telemetry, Process, Incident):
            session.query(model).filter(model.hostname == hostname).delete()
        session.delete(host)
