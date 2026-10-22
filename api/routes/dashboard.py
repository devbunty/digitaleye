from flask import Blueprint, jsonify

from database.repositories.dashboard_repository import (
    get_dashboard_summary,
    get_host_resource_inventory,
    get_live_threat_feed,
    get_threat_intelligence,
)
from database.repositories.incident_repository import get_recent_incidents
from database.repositories.mitre_repository import get_top_mitre_techniques

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.get("/summary")
def summary():
    return jsonify(get_dashboard_summary())


@bp.get("/incidents")
def incidents():
    return jsonify(get_recent_incidents(limit=10))


@bp.get("/resources")
def resources():
    return jsonify(get_host_resource_inventory())


@bp.get("/threat-feed")
def threat_feed():
    return jsonify(get_live_threat_feed())


@bp.get("/threat-intelligence")
def threat_intelligence():
    return jsonify(get_threat_intelligence())


@bp.get("/top-mitre")
def top_mitre():
    return jsonify(get_top_mitre_techniques(limit=5))
