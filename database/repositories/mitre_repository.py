from sqlalchemy import func

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
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
<<<<<<< HEAD
=======
=======
from database.db import SessionLocal
from database.models import Incident


DRIFT_MITRE_MAP = {
    "processes": ("T1057", "Process Discovery"),
    "ports": ("T1571", "Non-Standard Port"),
    "services": ("T1543", "Create or Modify System Process"),
    "users": ("T1136", "Create Account"),
}


def get_top_mitre_techniques(limit=5):
    """Return top MITRE techniques for dashboard widgets.

    Drift incidents store mitre='Behavioral', so when no mapped MITRE
    techniques exist we derive technique labels from incident categories.
    """

    session = SessionLocal()

    try:
        rows = (
            session.query(
                Incident.mitre,
                func.count(Incident.id).label("count"),
            )
            .filter(
                Incident.status == "Open",
                Incident.mitre != "Behavioral",
                Incident.mitre != "",
            )
            .group_by(Incident.mitre)
            .order_by(func.count(Incident.id).desc())
            .limit(limit)
            .all()
        )

        if rows:
            return [
                {
                    "mitre": mitre,
                    "count": count,
                    "label": mitre,
                }
                for mitre, count in rows
            ]

        category_rows = (
            session.query(
                Incident.category,
                func.count(Incident.id).label("count"),
            )
            .filter(Incident.status == "Open")
            .group_by(Incident.category)
            .order_by(func.count(Incident.id).desc())
            .limit(limit)
            .all()
        )

        result = []
        for category, count in category_rows:
            code, label = DRIFT_MITRE_MAP.get(
                category,
                ("T1485", category.replace("_", " ").title()),
            )
            result.append({
                "mitre": code,
                "count": count,
                "label": label,
            })

        if result:
            return result

        # Last resort: group open incidents by rule id
        rule_rows = (
            session.query(
                Incident.rule_id,
                func.count(Incident.id).label("count"),
            )
            .filter(Incident.status == "Open")
            .group_by(Incident.rule_id)
            .order_by(func.count(Incident.id).desc())
            .limit(limit)
            .all()
        )

>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
        return [
            {
                "mitre": rule_id,
                "count": count,
                "label": rule_id.replace("DRIFT-", "").replace("_", " ").title(),
            }
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
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
<<<<<<< HEAD
=======
=======
            for rule_id, count in rule_rows
        ]

    finally:
        session.close()


def count_open_techniques():
    session = SessionLocal()

    try:
        mapped = (
            session.query(func.count(func.distinct(Incident.mitre)))
            .filter(
                Incident.status == "Open",
                Incident.mitre != "Behavioral",
                Incident.mitre != "",
            )
            .scalar()
        ) or 0

>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
        if mapped:
            return mapped

        return (
            session.query(func.count(func.distinct(Incident.category)))
<<<<<<< HEAD
            .filter(Incident.status == OPEN)
            .scalar()
        ) or 0
=======
<<<<<<< HEAD
            .filter(Incident.status == OPEN)
            .scalar()
        ) or 0
=======
            .filter(Incident.status == "Open")
            .scalar()
        ) or 0

    finally:
        session.close()
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
