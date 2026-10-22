from sqlalchemy import func

from database.db import session_scope
from database.mitre import BEHAVIORAL, technique_for_category
from database.models import Incident
from database.repositories.incident_repository import OPEN


def _open_counts(session, column, *extra_filters, limit: int):
    return (
        session.query(column, func.count(Incident.id))
        .filter(Incident.status == OPEN, *extra_filters)
        .group_by(column)
        .order_by(func.count(Incident.id).desc())
        .limit(limit)
        .all()
    )


def get_top_mitre_techniques(limit: int = 5) -> list[dict]:
    """Most common open techniques for the dashboard widget.

    Drift incidents carry ``mitre="Behavioral"``, so when no signature-rule
    techniques exist we fall back to their category, then to the rule id.
    """
    with session_scope() as session:
        mapped = _open_counts(
            session,
            Incident.mitre,
            Incident.mitre != BEHAVIORAL,
            Incident.mitre != "",
            limit=limit,
        )
        if mapped:
            return [{"mitre": mitre, "count": count, "label": mitre} for mitre, count in mapped]

        by_category = _open_counts(session, Incident.category, limit=limit)
        if by_category:
            result = []
            for category, count in by_category:
                code, label = technique_for_category(category)
                result.append({"mitre": code, "count": count, "label": label})
            return result

        by_rule = _open_counts(session, Incident.rule_id, limit=limit)
        return [
            {
                "mitre": rule_id,
                "count": count,
                "label": rule_id.replace("DRIFT-", "").replace("_", " ").title(),
            }
            for rule_id, count in by_rule
        ]


def count_open_techniques() -> int:
    with session_scope() as session:
        mapped = (
            session.query(func.count(func.distinct(Incident.mitre)))
            .filter(
                Incident.status == OPEN,
                Incident.mitre != BEHAVIORAL,
                Incident.mitre != "",
            )
            .scalar()
        )
        if mapped:
            return mapped

        return (
            session.query(func.count(func.distinct(Incident.category)))
            .filter(Incident.status == OPEN)
            .scalar()
        ) or 0
