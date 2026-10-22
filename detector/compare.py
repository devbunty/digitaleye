<<<<<<< HEAD
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
=======
def compare_set(old_items, new_items, key):

    old = {str(item[key]) for item in old_items if key in item}

>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
    new = {str(item[key]) for item in new_items if key in item}

    return {
        "added": sorted(new - old),
        "removed": sorted(old - new),
<<<<<<< HEAD
        "active": sorted(new),
    }


def compare(current: dict, baseline: dict) -> dict:
    """Added/removed/active items per category (processes, ports, ...)."""
    return {
        category: compare_set(baseline.get(category, []), current.get(category, []), key)
        for category, key in CATEGORY_KEYS.items()
    }
=======
        "active": sorted(new)
    }


def compare(current, baseline):

    findings = {}

    findings["processes"] = compare_set(
        baseline.get("processes", []),
        current.get("processes", []),
        "command"
    )

    findings["ports"] = compare_set(
        baseline.get("ports", []),
        current.get("ports", []),
        "port"
    )

    findings["services"] = compare_set(
        baseline.get("services", []),
        current.get("services", []),
        "service"
    )

    findings["users"] = compare_set(
        baseline.get("users", []),
        current.get("users", []),
        "user"
    )

    return findings
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
