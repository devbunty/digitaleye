import json
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
import logging
from datetime import datetime

import config
from database.repositories.incident_repository import has_open_incident, save_incident
from database.timeutils import utc_now

logger = logging.getLogger(__name__)


def create_incident(rule: dict, hostname: str, evidence: str) -> dict | None:
    """Record an incident unless one is already open for this rule and host.

    Returns the incident, or ``None`` when it would have been a duplicate.
    The incident is stored in the database and also written as a JSON file
    under ``incidents/`` for easy export.
    """
    if has_open_incident(hostname, rule["id"]):
        return None

    incident = {
        "timestamp": utc_now().isoformat(),
        "hostname": hostname,
        "rule_id": rule["id"],
        "title": rule["title"],
        "severity": rule["severity"],
        "mitre": rule["mitre"],
        "category": rule["category"],
        "evidence": evidence,
    }

    db_id = save_incident(
        hostname,
        rule["id"],
        rule["title"],
        rule["severity"],
        rule["mitre"],
        rule["category"],
        evidence,
    )

    config.INCIDENT_DIR.mkdir(exist_ok=True)
    path = config.INCIDENT_DIR / f"{rule['id']}_{int(datetime.now().timestamp())}.json"
    path.write_text(json.dumps(incident, indent=4), encoding="utf-8")

    logger.warning(
        "Incident #%s created: rule=%s host=%s evidence=%s",
        db_id,
        rule["id"],
        hostname,
        evidence,
    )
<<<<<<< HEAD
=======
=======
from pathlib import Path
from datetime import datetime, UTC

from database.repositories.incident_repository import (
    save_incident,
    get_open_incident,
)

INCIDENT_DIR = Path("incidents")
INCIDENT_DIR.mkdir(exist_ok=True)


def create_incident(rule, hostname, evidence):

    # ---------------------------------
    # Don't create duplicate open alerts
    # ---------------------------------

    existing = get_open_incident(
        hostname,
        rule["id"]
    )

    if existing:
        return None

    incident = {

        "timestamp": datetime.now(UTC).isoformat(),

        "hostname": hostname,

        "rule_id": rule["id"],

        "title": rule["title"],

        "severity": rule["severity"],

        "mitre": rule["mitre"],

        "category": rule["category"],

        "evidence": evidence

    }

    db_id = save_incident(

        hostname,

        rule["id"],

        rule["title"],

        rule["severity"],

        rule["mitre"],

        rule["category"],

        evidence

    )

    filename = INCIDENT_DIR / (
        f"{rule['id']}_{int(datetime.now().timestamp())}.json"
    )

    with open(filename, "w") as f:
        json.dump(incident, f, indent=4)

    print()
    print("=" * 60)
    print(" INCIDENT CREATED")
    print("=" * 60)
    print(f"Database ID : {db_id}")
    print(f"Rule        : {rule['id']}")
    print(f"Hostname    : {hostname}")
    print(f"Evidence    : {evidence}")
    print()

>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
    return incident
