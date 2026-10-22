from flask import Blueprint, jsonify, request

from database.repositories.incident_repository import get_incident_by_id, get_recent_incidents

bp = Blueprint("incidents", __name__)


@bp.get("/incidents")
def incidents_list():
    return jsonify(
        get_recent_incidents(
            limit=200,
            status=request.args.get("status"),
            hostname=request.args.get("hostname"),
        )
    )


@bp.get("/incidents/<int:incident_id>")
def incidents_detail(incident_id):
    incident = get_incident_by_id(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify(incident)
