<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
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
<<<<<<< HEAD
=======
=======
from detector.incident import create_incident
from database.repositories.incident_repository import (
    get_open_drift_incidents,
    resolve_drift_incident,
)

# Common Linux services that legitimately start/stop/update on their own
# and aren't meaningful signals of compromise on their own. New services
# outside this list still get flagged normally.
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
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


<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
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
<<<<<<< HEAD
=======
=======
def detect_drift(hostname, findings):

    incidents = []

    mapping = {
        "processes": ("New Process Detected", "Medium"),
        "ports": ("New Listening Port", "High"),
        "services": ("New Service", "High"),
        "users": ("New User Account", "High"),
    }

    for category, values in findings.items():

        title, severity = mapping[category]

        # ----------------------------
        # Create incidents
        # ----------------------------

        for item in values.get("added", []):

            if category == "services" and str(item) in BENIGN_SERVICES:
                continue

            rule = {
                "id": f"DRIFT-{category.upper()}",
                "title": title,
                "severity": severity,
                "mitre": "Behavioral",
                "category": category,
            }

            incident = create_incident(
                rule,
                hostname,
                str(item),
            )

            if incident:
                incidents.append(incident)

        # ----------------------------
        # Resolve incidents
        # ----------------------------

        for item in values.get("removed", []):

            resolve_drift_incident(
                hostname,
                f"DRIFT-{category.upper()}",
                str(item),
            )
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd

    return incidents
