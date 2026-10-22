"""Compare current telemetry with a stored baseline."""

# category -> key identifying an item within that category
CATEGORY_KEYS = {
    "processes": "command",
    "ports": "port",
    "services": "service",
    "users": "user",
}


def compare_set(old_items: list[dict], new_items: list[dict], key: str) -> dict:
    old = {str(item[key]) for item in old_items if key in item}
    new = {str(item[key]) for item in new_items if key in item}

    return {
        "added": sorted(new - old),
        "removed": sorted(old - new),
        "active": sorted(new),
    }


def compare(current: dict, baseline: dict) -> dict:
    """Added/removed/active items per category (processes, ports, ...)."""
    return {
        category: compare_set(baseline.get(category, []), current.get(category, []), key)
        for category, key in CATEGORY_KEYS.items()
    }
