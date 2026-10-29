"""Hosts and the asset inventory."""

from flask import Blueprint, jsonify, request

from database.repositories.assets_repository import get_all_assets, get_asset_summary
from database.repositories.host_repository import create_demo_host, delete_demo_host, list_hosts

bp = Blueprint("hosts", __name__)


def _clean(value) -> str | None:
    return (value or "").strip() or None


@bp.get("/hosts")
def hosts_list():
    return jsonify(list_hosts())


@bp.post("/hosts/demo")
def hosts_create_demo():
    payload = request.get_json(silent=True) or {}

    hostname = _clean(payload.get("hostname"))
    if not hostname:
        return jsonify({"error": "hostname is required"}), 400

    try:
        host = create_demo_host(
            hostname=hostname,
            ip=_clean(payload.get("ip")),
            os_name=_clean(payload.get("os")),
            kernel=_clean(payload.get("kernel")),
        )
    except ValueError as err:
        return jsonify({"error": str(err)}), 409

    return jsonify(host), 201


@bp.delete("/hosts/<hostname>")
def hosts_delete_demo(hostname):
    try:
        delete_demo_host(hostname)
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
    except PermissionError as err:
        return jsonify({"error": str(err)}), 403

    return jsonify({"status": "deleted", "hostname": hostname})


@bp.get("/assets")
def assets():
    return jsonify(get_all_assets())


@bp.get("/assets/hosts")
def assets_hosts():
    return jsonify(get_all_assets())


@bp.get("/assets/summary")
def assets_summary():
    return jsonify(get_asset_summary())
