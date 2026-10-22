from flask import Blueprint, jsonify, request

from database.repositories.analytics_repository import get_analytics

bp = Blueprint("analytics", __name__)


@bp.get("/analytics")
def analytics():
    hostname = request.args.get("hostname") or None
    hours = request.args.get("hours", 72, type=int)
    return jsonify(get_analytics(hostname=hostname, hours=hours))
