import { useCallback, useMemo, useState } from "react";
import { Download, RotateCcw } from "lucide-react";

import AutoRefreshControl from "../components/common/AutoRefreshControl";
import {
  ControlBar,
  FilterSelect,
  PageHero,
  SortSelect,
} from "../components/common/Controls";
import Pagination from "../components/common/Pagination";
import IncidentDetail from "../components/incidents/IncidentDetail";
import SortableHeader from "../components/incidents/SortableHeader";
import ErrorBanner from "../components/ui/ErrorBanner";
import Metric from "../components/ui/Metric";
import { BRAND } from "../brand";
import { SEVERITIES, SEVERITY_BADGE } from "../constants/severity";
import { useAutoRefresh } from "../hooks/useAutoRefresh";
import { getHosts } from "../services/hosts";
import { getIncidents } from "../services/incidents";
import { formatDateTime, formatRelativeTime } from "../utils/assetHelpers";
import { downloadJson } from "../utils/download";
import {
  ALL,
  DEFAULT_FILTERS,
  DEFAULT_SORT,
  DESCENDING_FIRST,
  TIME_RANGES,
  filterIncidents,
  summarizeIncidents,
} from "../utils/incidentFilters";

const PAGE_SIZES = [10, 25, 50, 100];

const STATUS_OPTIONS = [
  { value: ALL, label: "All statuses" },
  { value: "Open", label: "Open" },
  { value: "Resolved", label: "Resolved" },
];

const SEVERITY_OPTIONS = [
  { value: ALL, label: "All severities" },
  ...SEVERITIES.map((s) => ({ value: s, label: s })),
];

const TIME_OPTIONS = TIME_RANGES.map(({ value, label }) => ({ value, label }));

const SORT_OPTIONS = [
  { value: "timestamp:desc", label: "Newest first" },
  { value: "timestamp:asc", label: "Oldest first" },
  { value: "severity:desc", label: "Severity (high → low)" },
  { value: "severity:asc", label: "Severity (low → high)" },
  { value: "hostname:asc", label: "Host A → Z" },
  { value: "title:asc", label: "Title A → Z" },
  { value: "id:desc", label: "ID (newest)" },
];

const toOptions = (allLabel, values) => [
  { value: ALL, label: allLabel },
  ...[...values].sort().map((v) => ({ value: v, label: v })),
];

export default function Incidents({ searchQuery = "" }) {
  const [incidents, setIncidents] = useState([]);
  const [hosts, setHosts] = useState([]);
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [sort, setSort] = useState(DEFAULT_SORT);
  const [pageSize, setPageSize] = useState(25);
  // Remember which search the page number belongs to; a new search starts at page 1.
  const [pageState, setPageState] = useState({ page: 1, search: searchQuery });
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState(null);

  const loader = useCallback(async () => {
    setError(null);
    try {
      const [incidentData, hostData] = await Promise.all([
        getIncidents(),
        getHosts(),
      ]);
      setIncidents(incidentData);
      setHosts(hostData);
    } catch (err) {
      console.error(err);
      setError("Failed to load incidents.");
    }
  }, []);

  const { autoUpdate, setAutoUpdate, intervalMs, setIntervalMs, lastUpdated, loading, refresh } =
    useAutoRefresh(loader, { enabled: true, intervalMs: 10000 });

  const hostOptions = useMemo(
    () =>
      toOptions("All hosts", [
        ...hosts.map((h) => h.hostname),
        ...incidents.map((i) => i.hostname),
      ].filter((name, i, all) => all.indexOf(name) === i)),
    [hosts, incidents]
  );

  const categoryOptions = useMemo(
    () => toOptions("All categories", new Set(incidents.map((i) => i.category).filter(Boolean))),
    [incidents]
  );

  // The time-range filter is anchored to the last refresh, keeping render pure.
  const now = lastUpdated?.getTime() ?? 0;

  const rows = useMemo(
    () => filterIncidents(incidents, { filters, search: searchQuery, sort, now }),
    [incidents, filters, searchQuery, sort, now]
  );

  const stats = useMemo(() => summarizeIncidents(rows), [rows]);

  const totalPages = Math.max(1, Math.ceil(rows.length / pageSize));
  const page =
    pageState.search === searchQuery ? Math.min(pageState.page, totalPages) : 1;
  const pageRows = rows.slice((page - 1) * pageSize, page * pageSize);

  const goToPage = (next) => setPageState({ page: next, search: searchQuery });

  const hasActiveFilters =
    searchQuery.trim() !== "" ||
    Object.keys(DEFAULT_FILTERS).some((key) => filters[key] !== DEFAULT_FILTERS[key]);

  function updateFilter(key, value) {
    setFilters((current) => ({ ...current, [key]: value }));
    goToPage(1);
  }

  function updateSort(next) {
    setSort(next);
    goToPage(1);
  }

  function toggleSort(key) {
    if (sort.key === key) {
      updateSort({ key, dir: sort.dir === "asc" ? "desc" : "asc" });
    } else {
      updateSort({ key, dir: DESCENDING_FIRST.has(key) ? "desc" : "asc" });
    }
  }

  function resetFilters() {
    setFilters(DEFAULT_FILTERS);
    setSort(DEFAULT_SORT);
    goToPage(1);
    setSelected(null);
  }

  function exportVisible() {
    const day = new Date().toISOString().slice(0, 10);
    downloadJson(`${BRAND.slug}-incidents-${day}.json`, rows);
  }

  return (
    <>
      <PageHero
        title="Incidents"
        subtitle="Investigate detections across the fleet — filter, paginate, and export the current view."
        actions={
          <AutoRefreshControl
            autoUpdate={autoUpdate}
            setAutoUpdate={setAutoUpdate}
            intervalMs={intervalMs}
            setIntervalMs={setIntervalMs}
            lastUpdated={lastUpdated}
            loading={loading}
            onRefresh={() => refresh()}
          />
        }
      />

      {searchQuery.trim() && (
        <div className="mb-4 flex items-center justify-between rounded-xl border border-cyan-400/20 bg-cyan-400/5 px-4 py-2 text-sm text-cyan-200">
          <span>
            Search filter: <strong>{searchQuery}</strong>
          </span>
          <span className="text-xs text-cyan-300/70">
            Clear the search bar and press Enter to show all incidents
          </span>
        </div>
      )}

      <div className="mb-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        <Metric label="In view" value={stats.total} />
        <Metric label="Open" value={stats.open} accent="text-amber-300" />
        <Metric label="Resolved" value={stats.resolved} accent="text-emerald-300" />
        <Metric label="Critical" value={stats.critical} accent="text-rose-300" />
        <Metric label="Affected hosts" value={stats.hostsHit} accent="text-cyan-300" />
      </div>

      <ControlBar>
        <div className="flex flex-wrap items-center gap-3">
          <FilterSelect label="Status" value={filters.status} onChange={(v) => updateFilter("status", v)} options={STATUS_OPTIONS} />
          <FilterSelect label="Severity" value={filters.severity} onChange={(v) => updateFilter("severity", v)} options={SEVERITY_OPTIONS} />
          <FilterSelect label="Host" value={filters.host} onChange={(v) => updateFilter("host", v)} options={hostOptions} />
          <FilterSelect label="Category" value={filters.category} onChange={(v) => updateFilter("category", v)} options={categoryOptions} />
          <FilterSelect label="Time" value={filters.timeRange} onChange={(v) => updateFilter("timeRange", v)} options={TIME_OPTIONS} />
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <SortSelect
            label="Sort"
            value={`${sort.key}:${sort.dir}`}
            onChange={(value) => {
              const [key, dir] = value.split(":");
              updateSort({ key, dir });
            }}
            options={SORT_OPTIONS}
          />

          {hasActiveFilters && (
            <button
              type="button"
              onClick={resetFilters}
              className="inline-flex items-center gap-1.5 rounded-xl border border-white/10 px-3 py-2 text-sm text-slate-400 hover:text-white"
            >
              <RotateCcw size={14} />
              Reset filters
            </button>
          )}

          <button
            type="button"
            onClick={exportVisible}
            disabled={rows.length === 0}
            className="inline-flex items-center gap-1.5 rounded-xl border border-cyan-400/30 bg-cyan-400/10 px-3 py-2 text-sm font-medium text-cyan-300 hover:bg-cyan-400/15 disabled:opacity-40"
          >
            <Download size={14} />
            Export view
          </button>
        </div>
      </ControlBar>

      <ErrorBanner>{error}</ErrorBanner>

      <div className="surface-panel overflow-hidden rounded-2xl">
        <table className="w-full">
          <thead className="border-b border-white/10 bg-black/20">
            <tr>
              <SortableHeader column="id" sort={sort} onSort={toggleSort}>ID</SortableHeader>
              <SortableHeader column="title" sort={sort} onSort={toggleSort}>Title</SortableHeader>
              <SortableHeader column="hostname" sort={sort} onSort={toggleSort}>Host</SortableHeader>
              <th className="p-4 text-left font-semibold text-slate-400">Category</th>
              <th className="p-4 text-left font-semibold text-slate-400">MITRE</th>
              <SortableHeader column="severity" sort={sort} onSort={toggleSort}>Severity</SortableHeader>
              <SortableHeader column="status" sort={sort} onSort={toggleSort}>Status</SortableHeader>
              <SortableHeader column="timestamp" sort={sort} onSort={toggleSort}>Detected</SortableHeader>
            </tr>
          </thead>
          <tbody>
            {pageRows.length === 0 ? (
              <tr>
                <td colSpan="8" className="p-10 text-center text-slate-500">
                  {loading ? "Loading incidents..." : "No incidents match the current filters."}
                </td>
              </tr>
            ) : (
              pageRows.map((incident, index) => {
                const isSelected = selected?.id === incident.id;
                return (
                  <tr
                    key={incident.id}
                    onClick={() => setSelected(isSelected ? null : incident)}
                    className={`cursor-pointer border-b border-white/[0.04] transition hover:bg-white/[0.03] ${
                      isSelected ? "bg-cyan-400/5" : ""
                    }`}
                  >
                    <td className="p-4 font-medium text-slate-500">
                      #{(page - 1) * pageSize + index + 1}
                    </td>
                    <td className="p-4 font-medium">{incident.title}</td>
                    <td className="p-4 text-cyan-200/90">{incident.hostname}</td>
                    <td className="p-4 text-slate-400">{incident.category}</td>
                    <td className="p-4 text-slate-400">{incident.mitre}</td>
                    <td className="p-4">
                      <span
                        className={`rounded-full border px-3 py-1 text-sm font-semibold ${
                          SEVERITY_BADGE[incident.severity] || SEVERITY_BADGE.Low
                        }`}
                      >
                        {incident.severity}
                      </span>
                    </td>
                    <td className="p-4">
                      <span
                        className={`rounded-full px-3 py-1 text-sm font-semibold ${
                          incident.status === "Open"
                            ? "bg-amber-500/20 text-amber-300"
                            : "bg-emerald-500/20 text-emerald-300"
                        }`}
                      >
                        {incident.status}
                      </span>
                    </td>
                    <td className="p-4 text-slate-400">
                      <p>{formatRelativeTime(incident.timestamp)}</p>
                      <p className="text-xs text-slate-600">{formatDateTime(incident.timestamp)}</p>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>

        <Pagination
          page={page}
          pageSize={pageSize}
          total={rows.length}
          onPageChange={goToPage}
          onPageSizeChange={(size) => {
            setPageSize(size);
            goToPage(1);
          }}
          pageSizeOptions={PAGE_SIZES}
        />
      </div>

      {selected && (
        <IncidentDetail incident={selected} onClose={() => setSelected(null)} />
      )}
    </>
  );
}
