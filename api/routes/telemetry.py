"""Agent heartbeat ingestion and process hunting."""

import json
import re

from flask import Blueprint, jsonify, request

import config
from database.repositories.host_repository import update_host
from database.repositories.process_repository import (
    get_all_processes,
    save_processes,
    search_command,
    search_process,
)
from database.repositories.telemetry_repository import save_telemetry
from database.repositories.timeline_repository import get_host_timeline
from database.timeutils import utc_now
from detector.engine import detect

bp = Blueprint("telemetry", __name__)

SYSTEM_FIELDS = ("hostname", "ip_address", "os", "kernel")
SAFE_HOSTNAME = re.compile(r"^[A-Za-z0-9._-]{1,100}$")


@bp.get("/")
def home():
    return {
        "application": config.APP_NAME,
        "status": "Running",
        "version": config.APP_VERSION,
        "endpoints": [
            "/heartbeat",
            "/processes",
            "/hunt/process/<name>",
            "/hunt/command/<keyword>",
            "/dashboard/summary",
            "/dashboard/incidents",
            "/dashboard/resources",
            "/analytics",
            "/hosts",
            "/hosts/demo",
            "/timeline/<hostname>",
        ],
    }


def _validate_heartbeat(payload) -> str | None:
    """Return an error message if the heartbeat is malformed, else ``None``."""
    if not isinstance(payload, dict) or not isinstance(payload.get("system"), dict):
        return "JSON body with a 'system' object is required"

    system = payload["system"]
    missing = [field for field in SYSTEM_FIELDS if field not in system]
    if missing:
        return f"'system' is missing: {', '.join(missing)}"

    if not SAFE_HOSTNAME.match(str(system["hostname"])):
        return "'hostname' may only contain letters, digits, '.', '_' and '-'"

    return None


@bp.post("/heartbeat")
def heartbeat():
    telemetry = request.get_json(silent=True)

    error = _validate_heartbeat(telemetry)
    if error:
        return jsonify({"error": error}), 400

    hostname = telemetry["system"]["hostname"]

    update_host(telemetry["system"])
    save_telemetry(telemetry)
    save_processes(telemetry)

    stamp = utc_now().strftime("%Y%m%d_%H%M%S")
    log_file = config.TELEMETRY_LOG_DIR / f"{hostname}_{stamp}.json"
    log_file.write_text(json.dumps(telemetry, indent=4), encoding="utf-8")

    incidents = detect(telemetry)

    return jsonify({"status": "received", "incidents": len(incidents)})


@bp.get("/processes")
def processes():
    return jsonify(get_all_processes())


@bp.get("/hunt/process/<name>")
def hunt_process(name):
    return jsonify(search_process(name))


@bp.get("/hunt/command/<keyword>")
def hunt_command(keyword):
    return jsonify(search_command(keyword))


@bp.get("/timeline/<hostname>")
def timeline(hostname):
    return jsonify(get_host_timeline(hostname))
