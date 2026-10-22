<<<<<<< HEAD
from database.db import session_scope
from database.models import Host
from database.repositories.host_repository import host_to_dict
from database.repositories.telemetry_repository import latest_telemetry_by_host


def get_asset_summary() -> dict:
    with session_scope() as session:
        hosts = session.query(Host).all()

    online = sum(1 for host in hosts if host.is_online)
    operating_systems = [(host.os or "").lower() for host in hosts]

    return {
        "total_hosts": len(hosts),
        "online": online,
        "offline": len(hosts) - online,
        "linux": sum(1 for os in operating_systems if "linux" in os or "ubuntu" in os),
        "windows": sum(1 for os in operating_systems if "windows" in os),
    }


def get_all_assets() -> list[dict]:
    """Every host with its status and latest resource usage."""
    with session_scope() as session:
        hosts = session.query(Host).order_by(Host.hostname).all()
        latest = latest_telemetry_by_host(session)

        assets = []
        for host in hosts:
            sample = latest.get(host.hostname)
            assets.append(
                {
                    **host_to_dict(host),
                    "cpu": sample.cpu_usage if sample else 0,
                    "memory": sample.memory_usage if sample else 0,
                    "processes": sample.process_count if sample else 0,
                }
            )
        return assets
=======
from datetime import datetime, UTC

from database.db import SessionLocal
from database.models import Host, Telemetry


ONLINE_THRESHOLD_SECONDS = 120


def is_online(last_seen, is_demo=False):
    # Demo hosts aren't backed by a real agent, so nothing ever refreshes
    # their last_seen after creation — a pure time-since-last-seen check
    # would flip them to "Offline" within minutes even though they're
    # meant to represent an active fleet member. Treat them as always on.
    if is_demo:
        return True

    if not last_seen:
        return False

    if last_seen.tzinfo:
        last_seen = last_seen.replace(tzinfo=None)

    return (datetime.utcnow() - last_seen).total_seconds() <= ONLINE_THRESHOLD_SECONDS

def get_asset_summary():

    session = SessionLocal()

    try:

        hosts = session.query(Host).all()

        total_hosts = len(hosts)

        linux = 0
        windows = 0
        online = 0

        for host in hosts:

            if "linux" in host.os.lower() or "ubuntu" in host.os.lower():
                linux += 1

            if "windows" in host.os.lower():
                windows += 1

            if is_online(host.last_seen, host.is_demo):
                online += 1

        return {

            "total_hosts": total_hosts,

            "online": online,

            "offline": total_hosts - online,

            "linux": linux,

            "windows": windows,

        }

    finally:

        session.close()


def get_assets():

    session = SessionLocal()

    try:

        inventory = []

        hosts = session.query(Host).all()

        for host in hosts:

            latest = (
                session.query(Telemetry)
                .filter(
                    Telemetry.hostname == host.hostname
                )
                .order_by(
                    Telemetry.collection_time.desc()
                )
                .first()
            )

            inventory.append({

                "hostname": host.hostname,

                "ip": host.ip,

                "os": host.os,

                "kernel": host.kernel,

                "last_seen": (
                    host.last_seen.isoformat()
                    if host.last_seen
                    else None
                ),

                "status": (
                    "Online"
                    if is_online(host.last_seen, host.is_demo)
                    else "Offline"
                ),

                "cpu": (
                    latest.cpu_usage
                    if latest
                    else 0
                ),

                "memory": (
                    latest.memory_usage
                    if latest
                    else 0
                ),

            })

        return inventory

    finally:

        session.close()

def get_all_assets():

    session = SessionLocal()

    try:

        hosts = session.query(Host).order_by(Host.hostname).all()

        assets = []

        for host in hosts:

            latest = (
                session.query(Telemetry)
                .filter(Telemetry.hostname == host.hostname)
                .order_by(Telemetry.collection_time.desc())
                .first()
            )

            assets.append({

                "hostname": host.hostname,

                "ip": host.ip,

                "os": host.os,

                "kernel": host.kernel,

                "status": "Online" if is_online(host.last_seen, host.is_demo) else "Offline",

                "first_seen": host.first_seen.isoformat(),

                "last_seen": host.last_seen.isoformat(),

                "cpu": latest.cpu_usage if latest else 0,

                "memory": latest.memory_usage if latest else 0,

                "processes": latest.process_count if latest else 0,

                "is_demo": bool(host.is_demo),

            })

        return assets

    finally:

        session.close()
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
