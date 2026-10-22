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
