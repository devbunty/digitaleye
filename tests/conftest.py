"""Test fixtures: every test gets its own database and working directories."""

import os
import tempfile
from pathlib import Path

# The engine is created on import, so point it at a throw-away file first.
_DB_DIR = tempfile.mkdtemp(prefix="digitaleye-tests-")
os.environ["DIGITALEYE_DB"] = str(Path(_DB_DIR) / "test.db")

import pytest  # noqa: E402

import config  # noqa: E402
from api import create_app  # noqa: E402
from database.db import engine  # noqa: E402
from database.models import Base  # noqa: E402


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "BASELINE_DIR", tmp_path / "baseline")
    monkeypatch.setattr(config, "INCIDENT_DIR", tmp_path / "incidents")
    monkeypatch.setattr(config, "TELEMETRY_LOG_DIR", tmp_path / "telemetry")

    Base.metadata.drop_all(engine)
    app = create_app()
    app.testing = True
    return app.test_client()


def make_heartbeat(hostname="web-01", processes=(), services=(), cpu=12.5, memory=40.0):
    """Build a heartbeat payload shaped like what an agent sends."""
    return {
        "system": {
            "hostname": hostname,
            "ip_address": "10.0.0.5",
            "os": "Ubuntu 22.04 LTS",
            "kernel": "6.8.0",
            "cpu_usage": cpu,
            "memory_usage": memory,
        },
        "processes": [
            {"pid": i, "name": name, "user": "root", "command": command}
            for i, (name, command) in enumerate(processes, start=100)
        ],
        "services": [{"service": name} for name in services],
        "ports": [],
        "users": [{"user": "root"}],
    }
