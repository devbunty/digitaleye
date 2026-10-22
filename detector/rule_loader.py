<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
import logging

import yaml

import config

logger = logging.getLogger(__name__)

REQUIRED_KEYS = {"id", "title", "severity", "mitre", "category", "field", "contains"}


def load_rules() -> list[dict]:
    """Load signature rules from ``rules/*.yaml``.

    A file may hold a list of rules or a mapping with a ``rules`` list. Files
    in any other shape, and rules missing required keys, are skipped. Rules
    are re-read on every call, so edits take effect without a restart.
    """
    rules = []

    for path in sorted(config.RULES_DIR.glob("*.yaml")):
        with open(path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)

        if isinstance(data, dict):
            data = data.get("rules", [])
        if not isinstance(data, list):
            continue

        for rule in data:
            missing = REQUIRED_KEYS - set(rule)
            if missing:
                logger.warning("Skipping rule in %s, missing: %s", path.name, sorted(missing))
                continue
            rules.append(rule)
<<<<<<< HEAD
=======
=======
import yaml
from pathlib import Path

RULE_DIR = Path("rules")


def load_rules():

    rules = []

    for file in RULE_DIR.glob("*.yaml"):

        with open(file, "r") as f:

            data = yaml.safe_load(f)

            if not data:
                continue

            # File contains a list of rules
            if isinstance(data, list):
                rules.extend(data)

            # File contains {"rules": [...]}
            elif isinstance(data, dict):
                rules.extend(data.get("rules", []))
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd

    return rules
