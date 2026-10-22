"""Turn baseline differences into incidents."""

from database.repositories.incident_repository import resolve_drift_incident
from database.mitre import BEHAVIORAL
from detector.incident import create_incident

# category -> (incident title, severity)
DRIFT_RULES = {
    "processes": ("New Process Detected", "Medium"),
    "ports": ("New Listening Port", "High"),
    "services": ("New Service", "High"),
    "users": ("New User Account", "High"),
}

# Common Linux services that start, stop and update on their own. They are not
# a meaningful sign of compromise by themselves; any other new service is
# still flagged.
BENIGN_SERVICES = {
    "fwupd.service",
    "fwupd-refresh.service",
    "packagekit.service",
    "man-db.service",
    "apt-daily.service",
    "apt-daily-upgrade.service",
    "snapd.service",
    "systemd-tmpfiles-clean.service",
    "logrotate.service",
    "motd-news.service",
}


def detect_drift(hostname: str, findings: dict) -> list[dict]:
    """Open an incident for each added item and resolve those that went away."""
    incidents = []

    for category, values in findings.items():
        title, severity = DRIFT_RULES[category]
        rule = {
            "id": f"DRIFT-{category.upper()}",
            "title": title,
            "severity": severity,
            "mitre": BEHAVIORAL,
            "category": category,
        }

        for item in values.get("added", []):
            if category == "services" and item in BENIGN_SERVICES:
                continue
            incident = create_incident(rule, hostname, str(item))
            if incident:
                incidents.append(incident)

        for item in values.get("removed", []):
            resolve_drift_incident(hostname, rule["id"], str(item))

    return incidents
