import { SEVERITY_RANK } from "../constants/severity";

export const ALL = "All";

export const TIME_RANGES = [
  { value: "all", label: "All time", hours: null },
  { value: "24h", label: "Last 24 hours", hours: 24 },
  { value: "7d", label: "Last 7 days", hours: 168 },
  { value: "30d", label: "Last 30 days", hours: 720 },
];

export const DEFAULT_FILTERS = {
  status: ALL,
  severity: ALL,
  host: ALL,
  category: ALL,
  timeRange: "all",
};

export const DEFAULT_SORT = { key: "timestamp", dir: "desc" };

const HOUR_MS = 3600 * 1000;
const time = (incident) => new Date(incident.timestamp || 0).getTime();
const text = (a, b) => (a || "").localeCompare(b || "");

const COMPARATORS = {
  severity: (a, b) => (SEVERITY_RANK[a.severity] ?? 9) - (SEVERITY_RANK[b.severity] ?? 9),
  hostname: (a, b) => text(a.hostname, b.hostname),
  status: (a, b) => text(a.status, b.status),
  title: (a, b) => text(a.title, b.title),
  id: (a, b) => (a.id || 0) - (b.id || 0),
  timestamp: (a, b) => time(a) - time(b),
};

const SEARCH_FIELDS = [
  "hostname",
  "severity",
  "title",
  "rule_id",
  "category",
  "mitre",
  "evidence",
];

function matchesSearch(incident, query) {
  return (
    String(incident.id).includes(query) ||
    SEARCH_FIELDS.some((field) => incident[field]?.toLowerCase().includes(query))
  );
}

/** Columns that read best newest/most severe first when first clicked. */
export const DESCENDING_FIRST = new Set(["timestamp", "severity", "id"]);

/**
 * Apply filters, free-text search and sorting.
 * `now` is passed in (ms since epoch) so this stays a pure function.
 */
export function filterIncidents(incidents, { filters, search, sort, now }) {
  const query = search.trim().toLowerCase();
  const range = TIME_RANGES.find((r) => r.value === filters.timeRange);
  const cutoff = range?.hours ? now - range.hours * HOUR_MS : null;

  const rows = incidents.filter(
    (i) =>
      (filters.status === ALL || i.status === filters.status) &&
      (filters.severity === ALL || i.severity === filters.severity) &&
      (filters.host === ALL || i.hostname === filters.host) &&
      (filters.category === ALL || i.category === filters.category) &&
      (cutoff === null || time(i) >= cutoff) &&
      (!query || matchesSearch(i, query))
  );

  const compare = COMPARATORS[sort.key] ?? COMPARATORS.timestamp;
  const direction = sort.dir === "asc" ? 1 : -1;
  return rows.sort((a, b) => direction * compare(a, b));
}

export function summarizeIncidents(rows) {
  const count = (predicate) => rows.filter(predicate).length;
  return {
    total: rows.length,
    open: count((i) => i.status === "Open"),
    resolved: count((i) => i.status === "Resolved"),
    critical: count((i) => i.severity === "Critical"),
    hostsHit: new Set(rows.map((i) => i.hostname)).size,
  };
}
