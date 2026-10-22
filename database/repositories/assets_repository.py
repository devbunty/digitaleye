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
