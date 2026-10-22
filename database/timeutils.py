"""Timestamp helpers.

SQLite hands back naive datetimes even for ``DateTime(timezone=True)``
columns. Everything we store is UTC, so naive values are treated as UTC.
"""

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Current time as a timezone-aware UTC datetime."""
    return datetime.now(UTC)


def as_aware_utc(value: datetime | None) -> datetime | None:
    """Return ``value`` as an aware UTC datetime (naive input is assumed UTC)."""
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def as_naive_utc(value: datetime | None) -> datetime | None:
    """Return ``value`` as a naive UTC datetime, handy for comparisons."""
    aware = as_aware_utc(value)
    return aware.replace(tzinfo=None) if aware else None


def to_iso(value: datetime | None) -> str | None:
    """ISO-8601 string with an explicit UTC offset, or ``None``.

    The explicit offset matters: browsers parse an offset-less timestamp as
    *local* time, which makes every "x minutes ago" label wrong.
    """
    aware = as_aware_utc(value)
    return aware.isoformat() if aware else None
