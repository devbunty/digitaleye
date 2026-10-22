<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
"""Per-host baselines, stored as the last accepted telemetry snapshot."""

import json
from pathlib import Path

import config


def _path(hostname: str) -> Path:
    # Hostnames come from agents over the network and end up in a file name,
    # so never let one point outside the baseline directory.
    if not hostname or Path(hostname).name != hostname or hostname in (".", ".."):
        raise ValueError(f"Unsafe hostname: {hostname!r}")
    return config.BASELINE_DIR / f"{hostname}.json"


def baseline_exists(hostname: str) -> bool:
    return _path(hostname).exists()


def load_baseline(hostname: str) -> dict:
    with open(_path(hostname), "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_baseline(hostname: str, telemetry: dict) -> None:
    config.BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    with open(_path(hostname), "w", encoding="utf-8") as handle:
        json.dump(telemetry, handle, indent=4)
<<<<<<< HEAD
=======
=======
import json
from pathlib import Path

BASELINE_DIR = Path("baseline/data")
BASELINE_DIR.mkdir(parents=True, exist_ok=True)


def get_file(hostname):
    return BASELINE_DIR / f"{hostname}.json"


def baseline_exists(hostname):
    return get_file(hostname).exists()


def load_baseline(hostname):

    with open(get_file(hostname), "r") as f:
        return json.load(f)


def save_baseline(hostname, telemetry):

    with open(get_file(hostname), "w") as f:
        json.dump(telemetry, f, indent=4)
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
