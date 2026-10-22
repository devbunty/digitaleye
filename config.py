"""Central configuration for Digital Eye.

Every filesystem path and tunable lives here so the rest of the code never
depends on the current working directory. Override anything through the
environment, e.g. ``DIGITALEYE_PORT=8080 python run.py``.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

APP_NAME = "Digital Eye"
APP_SLUG = "digitaleye"
APP_VERSION = "1.0.0"

# --- Storage -----------------------------------------------------------------
DB_PATH = Path(os.environ.get("DIGITALEYE_DB", BASE_DIR / f"{APP_SLUG}.db"))
LEGACY_DB_PATH = BASE_DIR / "osvf.db"  # name used before the rebrand

BASELINE_DIR = BASE_DIR / "baseline" / "data"
INCIDENT_DIR = BASE_DIR / "incidents"
RULES_DIR = BASE_DIR / "rules"
TELEMETRY_LOG_DIR = BASE_DIR / "logs" / "telemetry"

# --- Server ------------------------------------------------------------------
HOST = os.environ.get("DIGITALEYE_HOST", "0.0.0.0")
PORT = int(os.environ.get("DIGITALEYE_PORT", "5000"))
# The Werkzeug debugger allows remote code execution, so it is opt-in.
DEBUG = os.environ.get("DIGITALEYE_DEBUG", "0") == "1"

# --- Behaviour ---------------------------------------------------------------
# A host that has not sent a heartbeat for this long is reported as Offline.
ONLINE_THRESHOLD_SECONDS = 120
