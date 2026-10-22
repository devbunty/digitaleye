"""MITRE ATT&CK mapping for baseline-drift incidents.

Drift incidents are stored with ``mitre="Behavioral"`` because they come from
comparing against a baseline rather than from a signature rule. For display
we map their category to the closest ATT&CK technique.
"""

BEHAVIORAL = "Behavioral"

DRIFT_TECHNIQUES = {
    "processes": ("T1057", "Process Discovery"),
    "ports": ("T1571", "Non-Standard Port"),
    "services": ("T1543", "Create or Modify System Process"),
    "users": ("T1136", "Create Account"),
}


def technique_for_category(category: str | None) -> tuple[str, str]:
    """Return ``(code, label)`` for a drift category, with a generic fallback."""
    if category in DRIFT_TECHNIQUES:
        return DRIFT_TECHNIQUES[category]
    return "T1485", (category or "Unknown").replace("_", " ").title()
