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

    return rules
