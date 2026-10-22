<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
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
<<<<<<< HEAD
=======
=======
from collections import defaultdict
from datetime import datetime, timedelta, UTC

from database.db import SessionLocal
from database.models import Host, Incident, Telemetry


def _naive_utc_now():
    return datetime.now(UTC).replace(tzinfo=None)


def _as_naive(dt):
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.astimezone(UTC).replace(tzinfo=None)
    return dt


def _apply_host_filter(query, hostname):
    if hostname:
        return query.filter(Incident.hostname == hostname)
    return query


# Drift incidents (new process/port/service/user) are stored with
# mitre="Behavioral" since they come from baseline comparison rather than
# a specific signature rule. That's fine for storage, but it means naively
# filtering them out of the MITRE breakdown makes the chart look empty
# any time drift incidents are the only open incidents — which is the
# common case. Map them to the same technique labels the dashboard's
# top-MITRE widget already uses instead of discarding them.
DRIFT_MITRE_LABELS = {
    "processes": "T1057 – Process Discovery",
    "ports": "T1571 – Non-Standard Port",
    "services": "T1543 – Create/Modify System Process",
    "users": "T1136 – Create Account",
}


def _mitre_label(incident):
    if incident.mitre and incident.mitre != "Behavioral":
        return incident.mitre
    return DRIFT_MITRE_LABELS.get(
        incident.category,
        (incident.category or "Unknown").replace("_", " ").title(),
    )


def get_analytics(hostname=None, hours=72):
    """Fleet-aware analytics aggregates for the Analytics dashboard."""

    session = SessionLocal()

    try:
        hours = max(1, int(hours))
        cutoff = _naive_utc_now() - timedelta(hours=hours)

        query = session.query(Incident)
        query = _apply_host_filter(query, hostname)
        rows = query.order_by(Incident.timestamp.asc()).all()

        # Filter in Python so naive SQLite timestamps compare correctly
        incidents = []
        for row in rows:
            ts = _as_naive(row.timestamp)
            if ts is None or ts < cutoff:
                continue
            incidents.append(row)

        total = len(incidents)
        open_count = sum(1 for i in incidents if i.status == "Open")
        resolved = total - open_count
        critical = sum(1 for i in incidents if i.severity == "Critical")
        high = sum(1 for i in incidents if i.severity == "High")
        medium = sum(1 for i in incidents if i.severity == "Medium")
        low = sum(1 for i in incidents if i.severity == "Low")
        affected_hosts = len({i.hostname for i in incidents})

        by_severity = _ordered_severity(incidents)
        by_category = _count_map(incidents, "category")
        by_status = _ordered_status(incidents)
        by_host = _count_map(incidents, "hostname")
        mitre_counts = defaultdict(int)
        for i in incidents:
            mitre_counts[_mitre_label(i)] += 1
        by_mitre = [
            {"name": name, "count": count}
            for name, count in sorted(
                mitre_counts.items(), key=lambda x: (-x[1], x[0])
            )
        ]

        timeline = _build_timeline(incidents, cutoff, hours)

        host_query = session.query(Host)
        if hostname:
            host_query = host_query.filter(Host.hostname == hostname)
        hosts = host_query.order_by(Host.hostname).all()

        host_list = [
            {
                "hostname": h.hostname,
                "ip": h.ip,
                "os": h.os,
                "last_seen": h.last_seen.isoformat() if h.last_seen else None,
            }
            for h in hosts
        ]
        host_names = [h.hostname for h in hosts]

        resource_trends = _resource_trends(session, hostname, hours)

        # Per-host breakdowns — only meaningful (and only computed) when
        # looking at more than one host; a single-host view already gets
        # clean per-host data from the fields above.
        by_category_by_host = None
        by_severity_by_host = None
        timeline_by_host = None
        resource_trends_by_host = None

        if not hostname and len(host_names) > 1:
            by_category_by_host = _pivot_by_host(incidents, "category", host_names)
            by_severity_by_host = _pivot_by_host(incidents, "severity", host_names)
            timeline_by_host = _build_timeline_by_host(
                incidents, cutoff, hours, host_names
            )
            resource_trends_by_host = _resource_trends_by_host(
                session, host_names, hours
            )

        return {
            "scope": hostname or "fleet",
            "hours": hours,
            "generated_at": _naive_utc_now().isoformat(),
            "summary": {
                "total_incidents": total,
                "open": open_count,
                "resolved": resolved,
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low,
                "affected_hosts": affected_hosts,
                "monitored_hosts": len(hosts),
            },
            "by_severity": by_severity,
            "by_category": by_category,
            "by_status": by_status,
            "by_host": by_host,
            "by_mitre": by_mitre,
            "timeline": timeline,
            "resource_trends": resource_trends,
            "hosts": host_list,
            "host_names": host_names,
            # multi-host-only fields — null when scoped to a single host
            # or when the fleet only has one host reporting
            "by_category_by_host": by_category_by_host,
            "by_severity_by_host": by_severity_by_host,
            "timeline_by_host": timeline_by_host,
            "resource_trends_by_host": resource_trends_by_host,
        }

    finally:
        session.close()


def _count_map(rows, attr):
    counts = defaultdict(int)
    for row in rows:
        key = getattr(row, attr) or "Unknown"
        counts[key] += 1

    return [
        {"name": name, "count": count}
        for name, count in sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    ]


def _ordered_severity(incidents):
    order = ["Critical", "High", "Medium", "Low"]
    counts = defaultdict(int)
    for row in incidents:
        counts[row.severity or "Low"] += 1
    return [
        {"name": name, "count": counts[name]}
        for name in order
        if counts[name] > 0
    ]


def _ordered_status(incidents):
    order = ["Open", "Resolved"]
    counts = defaultdict(int)
    for row in incidents:
        counts[row.status or "Open"] += 1
    return [
        {"name": name, "count": counts[name]}
        for name in order
        if counts[name] > 0
    ]


def _build_timeline(incidents, cutoff, hours):
    buckets = {}
    now = _naive_utc_now()
    start = cutoff.replace(minute=0, second=0, microsecond=0)

    slot = start
    end = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
        ts = as_naive_utc(incident.timestamp)
        bucket = buckets.get(ts.replace(minute=0, second=0, microsecond=0).isoformat())
        if bucket is None:
            continue
        bucket["total"] += 1
        severity = (incident.severity or "").lower()
        if severity in bucket:
            bucket[severity] += 1
<<<<<<< HEAD
=======
=======
        ts = _as_naive(incident.timestamp)
        if ts is None:
            continue
        slot = ts.replace(minute=0, second=0, microsecond=0)
        key = slot.isoformat()
        if key not in buckets:
            continue
        buckets[key]["total"] += 1
        sev = (incident.severity or "").lower()
        if sev in buckets[key]:
            buckets[key][sev] += 1
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd

    return list(buckets.values())


<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
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
<<<<<<< HEAD
=======
=======
def _bucket_size(hours):
    """Pick a readable bucket width based on the selected window."""
    if hours <= 24:
        return timedelta(minutes=15)
    if hours <= 72:
        return timedelta(hours=1)
    return timedelta(hours=4)


def _pivot_by_host(incidents, attr, host_names):
    """Turn a flat list of rows into stacked-bar-ready rows:
    [{name: <attr value>, host_a: n, host_b: m, ...}]
    """

    grid = defaultdict(lambda: defaultdict(int))

    for row in incidents:
        key = getattr(row, attr) or "Unknown"
        grid[key][row.hostname] += 1

    result = []
    for key, counts in sorted(
        grid.items(), key=lambda x: (-sum(x[1].values()), x[0])
    ):
        entry = {"name": key}
        for host in host_names:
            entry[host] = counts.get(host, 0)
        result.append(entry)

    return result


def _build_timeline_by_host(incidents, cutoff, hours, host_names):
    """Hourly buckets, stacked by host, so a spike can be traced to
    the host that caused it instead of one blended total line."""

    bucket_width = _bucket_size(hours)
    now = _naive_utc_now()
    start = cutoff

    buckets = {}
    slot = start
    end = now + bucket_width
    while slot <= end:
        key = slot.isoformat()
        entry = {"time": key, "label": slot.strftime("%m/%d %H:%M"), "total": 0}
        for host in host_names:
            entry[host] = 0
        buckets[key] = entry
        slot += bucket_width

    sorted_keys = sorted(buckets.keys())

    def bucket_for(ts):
        # find the last bucket start <= ts
        idx = 0
        for i, key in enumerate(sorted_keys):
            if datetime.fromisoformat(key) <= ts:
                idx = i
            else:
                break
        return sorted_keys[idx]

    for incident in incidents:
        ts = _as_naive(incident.timestamp)
        if ts is None:
            continue
        key = bucket_for(ts)
        buckets[key]["total"] += 1
        if incident.hostname in buckets[key]:
            buckets[key][incident.hostname] += 1

    return [buckets[k] for k in sorted_keys]


def _resource_trends(session, hostname, hours):
    """Recent CPU/memory samples — newest first in query, returned chronological."""

    hours = max(1, int(hours))
    cutoff = _naive_utc_now() - timedelta(hours=hours)

    query = session.query(Telemetry)
    if hostname:
        query = query.filter(Telemetry.hostname == hostname)

    # Pull recent rows then keep those inside the window
    recent = (
        query
        .order_by(Telemetry.collection_time.desc())
        .limit(2000)
        .all()
    )

    rows = []
    for r in recent:
        ts = _as_naive(r.collection_time)
        if ts is None or ts < cutoff:
            continue
        rows.append(r)

    rows.reverse()  # chronological for charts

    if hostname:
        # Downsample to ~120 points for chart readability
        step = max(1, len(rows) // 120)
        sampled = rows[::step][-120:]
        return [
            {
                "time": _as_naive(r.collection_time).isoformat(),
                "label": _as_naive(r.collection_time).strftime("%H:%M"),
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
                "cpu": round(r.cpu_usage or 0, 1),
                "memory": round(r.memory_usage or 0, 1),
                "processes": r.process_count or 0,
            }
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
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
<<<<<<< HEAD
=======
=======
            for r in sampled
        ]

    grouped = defaultdict(lambda: {"cpu": [], "memory": [], "processes": []})

    for r in rows:
        ts = _as_naive(r.collection_time)
        slot = ts.replace(second=0, microsecond=0)
        key = slot.isoformat()
        grouped[key]["cpu"].append(r.cpu_usage or 0)
        grouped[key]["memory"].append(r.memory_usage or 0)
        grouped[key]["processes"].append(r.process_count or 0)
        grouped[key]["label"] = slot.strftime("%H:%M")
        grouped[key]["time"] = key

    result = []
    keys = sorted(grouped.keys())
    step = max(1, len(keys) // 120)
    for key in keys[::step][-120:]:
        bucket = grouped[key]
        n = len(bucket["cpu"]) or 1
        result.append({
            "time": bucket["time"],
            "label": bucket["label"],
            "cpu": round(sum(bucket["cpu"]) / n, 1),
            "memory": round(sum(bucket["memory"]) / n, 1),
            "processes": round(sum(bucket["processes"]) / n),
        })

    return result


def _resource_trends_by_host(session, host_names, hours):
    """Per-host CPU/memory series on a shared time grid, so the fleet
    view shows one line per host instead of a blended average.
    Returns {"cpu": [...], "memory": [...]} where each row is
    {time, label, <host_a>: value, <host_b>: value, ...} with nulls
    where a host had no sample in that bucket.
    """

    hours = max(1, int(hours))
    cutoff = _naive_utc_now() - timedelta(hours=hours)
    bucket_width = _bucket_size(hours)

    rows = (
        session.query(Telemetry)
        .filter(Telemetry.hostname.in_(host_names))
        .order_by(Telemetry.collection_time.asc())
        .all()
    )

    grid = defaultdict(lambda: defaultdict(list))  # bucket_key -> host -> [(cpu, mem)]

    for r in rows:
        ts = _as_naive(r.collection_time)
        if ts is None or ts < cutoff:
            continue

        # bucket index relative to cutoff
        elapsed = ts - cutoff
        bucket_index = int(elapsed / bucket_width)
        slot = cutoff + bucket_index * bucket_width
        key = slot.isoformat()

        grid[key][r.hostname].append((r.cpu_usage or 0, r.memory_usage or 0))

    sorted_keys = sorted(grid.keys())

    # cap number of points for chart readability
    if len(sorted_keys) > 120:
        step = max(1, len(sorted_keys) // 120)
        sorted_keys = sorted_keys[::step]

    cpu_series = []
    memory_series = []

    for key in sorted_keys:
        slot = datetime.fromisoformat(key)
        label = slot.strftime("%m/%d %H:%M") if hours > 24 else slot.strftime("%H:%M")

        cpu_row = {"time": key, "label": label}
        mem_row = {"time": key, "label": label}

        for host in host_names:
            samples = grid[key].get(host)
            if samples:
                cpu_row[host] = round(sum(s[0] for s in samples) / len(samples), 1)
                mem_row[host] = round(sum(s[1] for s in samples) / len(samples), 1)
            else:
                cpu_row[host] = None
                mem_row[host] = None

        cpu_series.append(cpu_row)
        memory_series.append(mem_row)

    return {"cpu": cpu_series, "memory": memory_series}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
