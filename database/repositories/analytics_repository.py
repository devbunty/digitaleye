"""Aggregates behind the Analytics and Threat Intel pages."""

from collections import defaultdict
from datetime import datetime, timedelta

from database.db import session_scope
from database.mitre import BEHAVIORAL, technique_for_category
from database.models import Host, Incident, Telemetry
from database.repositories.incident_repository import OPEN, RESOLVED
from database.timeutils import as_naive_utc, to_iso, utc_now

SEVERITY_ORDER = ("Critical", "High", "Medium", "Low")
STATUS_ORDER = (OPEN, RESOLVED)
MAX_CHART_POINTS = 120
MAX_TELEMETRY_ROWS = 2000


# --- Small helpers -------------------------------------------------------------


def _now() -> datetime:
    return as_naive_utc(utc_now())


def _count_by(rows, key) -> list[dict]:
    """``[{"name", "count"}]`` sorted by count (desc), then name."""
    counts = defaultdict(int)
    for row in rows:
        counts[key(row) or "Unknown"] += 1
    return [
        {"name": name, "count": count}
        for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def _count_in_order(rows, key, order, default) -> list[dict]:
    """Counts for the values in ``order`` only, skipping empty buckets."""
    counts = defaultdict(int)
    for row in rows:
        counts[key(row) or default] += 1
    return [{"name": name, "count": counts[name]} for name in order if counts[name] > 0]


def _mitre_label(incident: Incident) -> str:
    """Technique label for an incident, mapping drift categories to ATT&CK."""
    if incident.mitre and incident.mitre != BEHAVIORAL:
        return incident.mitre
    code, name = technique_for_category(incident.category)
    return f"{code} – {name}"


def _bucket_width(hours: int) -> timedelta:
    """Readable bucket width for the selected window."""
    if hours <= 24:
        return timedelta(minutes=15)
    if hours <= 72:
        return timedelta(hours=1)
    return timedelta(hours=4)


def _downsample(items: list, limit: int = MAX_CHART_POINTS) -> list:
    step = max(1, len(items) // limit)
    return items[::step][-limit:]


def _load_incidents(session, hostname, cutoff) -> list[Incident]:
    query = session.query(Incident)
    if hostname:
        query = query.filter(Incident.hostname == hostname)

    # Filtered in Python so naive SQLite timestamps compare correctly.
    return [
        row
        for row in query.order_by(Incident.timestamp.asc()).all()
        if (ts := as_naive_utc(row.timestamp)) is not None and ts >= cutoff
    ]


def _load_telemetry(session, hostnames, cutoff, limit=None) -> list[Telemetry]:
    query = session.query(Telemetry)
    if hostnames:
        query = query.filter(Telemetry.hostname.in_(hostnames))

    if limit:
        # Newest rows first so the cap keeps the most recent samples.
        rows = query.order_by(Telemetry.collection_time.desc()).limit(limit).all()
        rows.reverse()
    else:
        rows = query.order_by(Telemetry.collection_time.asc()).all()

    return [
        row
        for row in rows
        if (ts := as_naive_utc(row.collection_time)) is not None and ts >= cutoff
    ]


# --- Incident aggregates -------------------------------------------------------


def _summarize(incidents: list[Incident], monitored_hosts: int) -> dict:
    by_severity = defaultdict(int)
    for incident in incidents:
        by_severity[incident.severity] += 1

    open_count = sum(1 for i in incidents if i.status == OPEN)

    return {
        "total_incidents": len(incidents),
        "open": open_count,
        "resolved": len(incidents) - open_count,
        "critical": by_severity["Critical"],
        "high": by_severity["High"],
        "medium": by_severity["Medium"],
        "low": by_severity["Low"],
        "affected_hosts": len({i.hostname for i in incidents}),
        "monitored_hosts": monitored_hosts,
    }


def _timeline(incidents, cutoff) -> list[dict]:
    """Hourly incident counts per severity across the whole window."""
    start = cutoff.replace(minute=0, second=0, microsecond=0)
    end = _now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    buckets = {}
    slot = start
    while slot <= end:
        key = slot.isoformat()
        buckets[key] = {
            "time": key,
            "label": slot.strftime("%m/%d %H:%M"),
            "total": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }
        slot += timedelta(hours=1)

    for incident in incidents:
        ts = as_naive_utc(incident.timestamp)
        bucket = buckets.get(ts.replace(minute=0, second=0, microsecond=0).isoformat())
        if bucket is None:
            continue
        bucket["total"] += 1
        severity = (incident.severity or "").lower()
        if severity in bucket:
            bucket[severity] += 1

    return list(buckets.values())


def _pivot_by_host(incidents, attr, host_names) -> list[dict]:
    """Rows ready for stacked bars: ``{name, <host_a>: n, <host_b>: m, ...}``."""
    grid = defaultdict(lambda: defaultdict(int))
    for incident in incidents:
        grid[getattr(incident, attr) or "Unknown"][incident.hostname] += 1

    rows = []
    for name, counts in sorted(grid.items(), key=lambda item: (-sum(item[1].values()), item[0])):
        rows.append({"name": name, **{host: counts.get(host, 0) for host in host_names}})
    return rows


def _timeline_by_host(incidents, cutoff, hours, host_names) -> list[dict]:
    """Incident counts per time bucket, split by host, so a spike can be
    traced to the machine that caused it."""
    width = _bucket_width(hours)
    end = _now() + width

    buckets = []
    slot = cutoff
    while slot <= end:
        buckets.append(
            {
                "time": slot.isoformat(),
                "label": slot.strftime("%m/%d %H:%M"),
                "total": 0,
                **{host: 0 for host in host_names},
            }
        )
        slot += width

    for incident in incidents:
        ts = as_naive_utc(incident.timestamp)
        index = min(max(int((ts - cutoff) / width), 0), len(buckets) - 1)
        buckets[index]["total"] += 1
        if incident.hostname in buckets[index]:
            buckets[index][incident.hostname] += 1

    return buckets


# --- Resource trends -------------------------------------------------------------


def _resource_trends(session, hostname, cutoff) -> list[dict]:
    """CPU/memory series for one host, or fleet averages per minute."""
    rows = _load_telemetry(session, [hostname] if hostname else None, cutoff, MAX_TELEMETRY_ROWS)

    if hostname:
        return [
            {
                "time": as_naive_utc(r.collection_time).isoformat(),
                "label": as_naive_utc(r.collection_time).strftime("%H:%M"),
                "cpu": round(r.cpu_usage or 0, 1),
                "memory": round(r.memory_usage or 0, 1),
                "processes": r.process_count or 0,
            }
            for r in _downsample(rows)
        ]

    per_minute = defaultdict(list)
    for row in rows:
        slot = as_naive_utc(row.collection_time).replace(second=0, microsecond=0)
        per_minute[slot].append(row)

    result = []
    for slot in _downsample(sorted(per_minute)):
        samples = per_minute[slot]
        count = len(samples)
        result.append(
            {
                "time": slot.isoformat(),
                "label": slot.strftime("%H:%M"),
                "cpu": round(sum(s.cpu_usage or 0 for s in samples) / count, 1),
                "memory": round(sum(s.memory_usage or 0 for s in samples) / count, 1),
                "processes": round(sum(s.process_count or 0 for s in samples) / count),
            }
        )
    return result


def _resource_trends_by_host(session, host_names, cutoff, hours) -> dict:
    """One CPU and one memory line per host on a shared time grid.

    Each row is ``{time, label, <host>: value}``; a host without a sample in
    a bucket gets ``None`` so charts leave a gap instead of a false zero.
    """
    width = _bucket_width(hours)
    grid = defaultdict(lambda: defaultdict(list))  # bucket start -> host -> samples

    for row in _load_telemetry(session, host_names, cutoff):
        index = int((as_naive_utc(row.collection_time) - cutoff) / width)
        grid[cutoff + index * width][row.hostname].append(row)

    label_format = "%m/%d %H:%M" if hours > 24 else "%H:%M"
    cpu_rows, memory_rows = [], []

    for slot in _downsample(sorted(grid)):
        cpu = {"time": slot.isoformat(), "label": slot.strftime(label_format)}
        memory = dict(cpu)

        for host in host_names:
            samples = grid[slot].get(host)
            cpu[host] = round(sum(s.cpu_usage or 0 for s in samples) / len(samples), 1) if samples else None
            memory[host] = round(sum(s.memory_usage or 0 for s in samples) / len(samples), 1) if samples else None

        cpu_rows.append(cpu)
        memory_rows.append(memory)

    return {"cpu": cpu_rows, "memory": memory_rows}


# --- Public API ------------------------------------------------------------------


def get_analytics(hostname: str | None = None, hours: int = 72) -> dict:
    """Fleet-wide (or single-host) analytics for the dashboard."""
    hours = max(1, int(hours))
    cutoff = _now() - timedelta(hours=hours)

    with session_scope() as session:
        incidents = _load_incidents(session, hostname, cutoff)

        host_query = session.query(Host).order_by(Host.hostname)
        if hostname:
            host_query = host_query.filter(Host.hostname == hostname)
        hosts = host_query.all()
        host_names = [host.hostname for host in hosts]

        mitre_counts = _count_by(incidents, _mitre_label)

        # Per-host breakdowns only make sense when comparing several hosts.
        compare_hosts = not hostname and len(host_names) > 1

        return {
            "scope": hostname or "fleet",
            "hours": hours,
            "generated_at": _now().isoformat(),
            "summary": _summarize(incidents, len(hosts)),
            "by_severity": _count_in_order(incidents, lambda i: i.severity, SEVERITY_ORDER, "Low"),
            "by_category": _count_by(incidents, lambda i: i.category),
            "by_status": _count_in_order(incidents, lambda i: i.status, STATUS_ORDER, OPEN),
            "by_host": _count_by(incidents, lambda i: i.hostname),
            "by_mitre": mitre_counts,
            "timeline": _timeline(incidents, cutoff),
            "resource_trends": _resource_trends(session, hostname, cutoff),
            "hosts": [
                {
                    "hostname": h.hostname,
                    "ip": h.ip,
                    "os": h.os,
                    "last_seen": to_iso(h.last_seen),
                }
                for h in hosts
            ],
            "host_names": host_names,
            # Null unless the fleet view compares more than one host.
            "by_category_by_host": _pivot_by_host(incidents, "category", host_names) if compare_hosts else None,
            "by_severity_by_host": _pivot_by_host(incidents, "severity", host_names) if compare_hosts else None,
            "timeline_by_host": _timeline_by_host(incidents, cutoff, hours, host_names) if compare_hosts else None,
            "resource_trends_by_host": (
                _resource_trends_by_host(session, host_names, cutoff, hours) if compare_hosts else None
            ),
        }
