<<<<<<< HEAD
"""Detection engine: baseline drift plus signature rules."""

import logging

from baseline.manager import baseline_exists, load_baseline, save_baseline
from database.repositories.incident_repository import get_open_incidents, resolve_incident
from detector.compare import compare
from detector.drift import detect_drift
from detector.incident import create_incident
from detector.rule_loader import load_rules

logger = logging.getLogger(__name__)


def _rule_matches(rule: dict, process: dict) -> str | None:
    """Return the evidence string if ``process`` matches ``rule``, else ``None``."""
    field = rule["field"].lower()
    if field not in ("command", "name"):
        return None

    value = process.get(field, "")
    return value if rule["contains"].lower() in value.lower() else None


def detect(telemetry: dict) -> list[dict]:
    """Analyse one heartbeat and return any newly created incidents.

    The first heartbeat of a host only stores a baseline. Afterwards every
    heartbeat is compared against the previous one, signature rules are
    applied to running processes, and incidents whose trigger has gone away
    are resolved.
    """
    hostname = telemetry["system"]["hostname"]

    if not baseline_exists(hostname):
        logger.info("Creating baseline for %s", hostname)
        save_baseline(hostname, telemetry)
        return []

    incidents = detect_drift(hostname, compare(telemetry, load_baseline(hostname)))

    # rule id -> evidence strings that matched in this heartbeat
    active: dict[str, set[str]] = {}

    rules = load_rules()
    for process in telemetry.get("processes", []):
        for rule in rules:
            evidence = _rule_matches(rule, process)
            if evidence is None:
                continue

            active.setdefault(rule["id"], set()).add(evidence)
            logger.debug("Rule %s matched: %s", rule["id"], evidence)

            incident = create_incident(rule, hostname, evidence)
            if incident:
                incidents.append(incident)

    # Resolve signature incidents whose trigger is no longer running.
    # Drift incidents are resolved by detect_drift instead.
    for open_incident in get_open_incidents(hostname):
        rule_id = open_incident["rule_id"]
        if rule_id.startswith("DRIFT-"):
            continue
        if open_incident["evidence"] not in active.get(rule_id, set()):
            resolve_incident(hostname, rule_id)

    save_baseline(hostname, telemetry)
=======
from database.repositories.incident_repository import (
    get_all_open_incidents,
    resolve_incident,
)

from baseline.manager import (
    baseline_exists,
    load_baseline,
    save_baseline,
)

from detector.compare import compare
from detector.drift import detect_drift
from detector.rule_loader import load_rules
from detector.incident import create_incident


def detect(telemetry):

    hostname = telemetry["system"]["hostname"]

    incidents = []

    if not baseline_exists(hostname):

        print(f"[+] Creating baseline for {hostname}")

        save_baseline(hostname, telemetry)

        return []

    baseline = load_baseline(hostname)

    findings = compare(telemetry, baseline)

    incidents.extend(
        detect_drift(hostname, findings)
    )

    rules = load_rules()

    matched = {}

    processes = telemetry.get("processes", [])

    for process in processes:

        command = process.get("command", "")

        name = process.get("name", "")

        for rule in rules:

            field = rule["field"].lower()

            pattern = rule["contains"].lower()

            matched_now = False

            evidence = ""

            if field == "command":

                if pattern in command.lower():

                    matched_now = True
                    evidence = command

            elif field == "name":

                if pattern in name.lower():

                    matched_now = True
                    evidence = name

            if matched_now:

                matched.setdefault(rule["id"], set()).add(evidence)
                print("=" * 60)
                print("Rule:", rule["id"])
                print("Pattern:", pattern)
                print("Command:", command)
                print("Matched:", pattern in command.lower())

                incident = create_incident(
                    rule,
                    hostname,
                    evidence,
                )

                if incident:
                    incidents.append(incident)

    open_incidents = get_all_open_incidents(hostname)

    for incident in open_incidents:

        if incident.rule_id.startswith("DRIFT-"):
            continue

        active = matched.get(incident.rule_id, set())

        if incident.evidence not in active:

            resolve_incident(
                hostname,
                incident.rule_id,
            )

    save_baseline(hostname, telemetry)

>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
    return incidents
