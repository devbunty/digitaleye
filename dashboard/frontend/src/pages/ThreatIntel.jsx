import { useCallback, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  AlertCircle,
  AlertTriangle,
  Clock,
  Info,
  Server,
  ShieldAlert,
} from "lucide-react";

import AutoRefreshControl from "../components/common/AutoRefreshControl";
import { PageHero } from "../components/common/Controls";
import EmptyChart from "../components/ui/EmptyChart";
import Metric from "../components/ui/Metric";
import Panel from "../components/ui/Panel";
import { BRAND } from "../brand";
import {
  SEVERITY_BADGE,
  SEVERITY_COLORS,
  TOOLTIP_STYLE,
} from "../constants/severity";
import { useAutoRefresh } from "../hooks/useAutoRefresh";
import { useFetch } from "../hooks/useFetch";
import { getAnalytics } from "../services/analytics";
import { getHosts } from "../services/hosts";
import { getIncidents } from "../services/incidents";
import { buildRiskRanking } from "../utils/risk";

const NO_HOSTS = [];
const ALL = "All";

export default function ThreatIntel() {
  const [hostSelection, setHostSelection] = useState(ALL);
  const [data, setData] = useState(null);
  const [recent, setRecent] = useState([]);

  // The dropdown lists every known host, independent of the current scope.
  const knownHosts = useFetch(getHosts, NO_HOSTS);
  const hostNames = useMemo(
    () => knownHosts.map((host) => host.hostname),
    [knownHosts]
  );

  // Fall back to the fleet view if the selected host no longer exists.
  const hostFilter = hostNames.includes(hostSelection) ? hostSelection : ALL;

  const loader = useCallback(async () => {
    const [analytics, incidents] = await Promise.all([
      getAnalytics({ hostname: hostFilter === ALL ? null : hostFilter }),
      getIncidents(),
    ]);
    setData(analytics);
    setRecent(incidents);
  }, [hostFilter]);

  const { autoUpdate, setAutoUpdate, intervalMs, setIntervalMs, lastUpdated, loading, refresh } =
    useAutoRefresh(loader, { enabled: true, intervalMs: 10000 });

  const mitreData = (data?.by_mitre || []).slice(0, 8);

  const riskRanking = useMemo(
    () => buildRiskRanking(data?.by_severity_by_host, data?.host_names ?? []),
    [data]
  );

  const recentCriticalHigh = useMemo(
    () =>
      recent
        .filter((i) => i.severity === "Critical" || i.severity === "High")
        .filter((i) => hostFilter === ALL || i.hostname === hostFilter)
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
        .slice(0, 8),
    [recent, hostFilter]
  );

  const summary = data?.summary;
  const isFleetView = hostFilter === ALL && hostNames.length > 1;

  return (
    <>
      <PageHero
        title="Threat Intelligence"
        subtitle={
          isFleetView
            ? `MITRE ATT&CK techniques and host risk across ${hostNames.length} hosts.`
            : "MITRE ATT&CK techniques for the selected scope."
        }
        actions={
          <div className="flex items-center gap-3">
            <select
              value={hostFilter}
              onChange={(e) => setHostSelection(e.target.value)}
              className="rounded-xl border border-white/10 bg-slate-900 px-3 py-2 text-sm outline-none focus:border-cyan-500"
            >
              <option value={ALL}>All Hosts ({hostNames.length})</option>
              {hostNames.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
            <AutoRefreshControl
              autoUpdate={autoUpdate}
              setAutoUpdate={setAutoUpdate}
              intervalMs={intervalMs}
              setIntervalMs={setIntervalMs}
              lastUpdated={lastUpdated}
              loading={loading}
              onRefresh={() => refresh()}
            />
          </div>
        }
      />

      <div className="grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
        <Metric label="Critical" value={summary?.critical} icon={ShieldAlert} accent="text-rose-300" />
        <Metric label="High" value={summary?.high} icon={AlertTriangle} accent="text-amber-300" />
        <Metric label="Medium" value={summary?.medium} icon={AlertCircle} accent="text-yellow-200" />
        <Metric label="Low" value={summary?.low} icon={Info} accent="text-slate-300" />
        <Metric label="Affected Hosts" value={summary?.affected_hosts} icon={Server} accent="text-cyan-300" />
        <Metric label="Open Incidents" value={summary?.open} icon={Clock} accent="text-violet-300" />
      </div>

      <div className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-12">
        <Panel
          className="xl:col-span-12"
          title="Top MITRE ATT&CK techniques"
          subtitle={`Most frequent technique categories in scope — ${
            hostFilter === ALL ? "all hosts" : hostFilter
          }`}
        >
          <div className="h-72">
            {mitreData.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={mitreData} layout="vertical" margin={{ left: 4, right: 12 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis type="number" stroke="#64748b" allowDecimals={false} />
                  <YAxis type="category" dataKey="name" stroke="#64748b" width={220} tick={{ fontSize: 12 }} />
                  <Tooltip contentStyle={TOOLTIP_STYLE} />
                  <Bar dataKey="count" fill="#38bdf8" radius={[0, 8, 8, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyChart text="No technique data yet" />
            )}
          </div>
        </Panel>

        {isFleetView && riskRanking && (
          <Panel
            className="xl:col-span-12"
            title="Host risk ranking"
            subtitle="Incidents by severity, per host (last 72 hours) — highest risk first"
          >
            <div style={{ height: Math.max(riskRanking.length * 44, 160) }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={riskRanking} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis type="number" stroke="#64748b" allowDecimals={false} />
                  <YAxis type="category" dataKey="hostname" stroke="#64748b" width={140} tick={{ fontSize: 12 }} />
                  <Tooltip contentStyle={TOOLTIP_STYLE} />
                  <Bar dataKey="Critical" stackId="risk" fill={SEVERITY_COLORS.Critical} />
                  <Bar dataKey="High" stackId="risk" fill={SEVERITY_COLORS.High} />
                  <Bar dataKey="Medium" stackId="risk" fill={SEVERITY_COLORS.Medium} />
                  <Bar dataKey="Low" stackId="risk" fill={SEVERITY_COLORS.Low} radius={[0, 6, 6, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Panel>
        )}

        <Panel
          className="xl:col-span-12"
          title="Recent critical & high detections"
          subtitle="Latest 8, most recent first"
        >
          {recentCriticalHigh.length === 0 ? (
            <EmptyChart text="No critical or high severity detections" />
          ) : (
            <div className="divide-y divide-white/5">
              {recentCriticalHigh.map((incident) => (
                <div key={incident.id} className="flex items-center justify-between gap-4 py-3">
                  <div className="min-w-0">
                    <p className="truncate font-medium text-slate-200">{incident.title}</p>
                    <p className="mt-0.5 text-xs text-slate-500">
                      {incident.hostname} · {incident.category} · {new Date(incident.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <span className={`shrink-0 rounded-full border px-2.5 py-1 text-xs font-semibold ${SEVERITY_BADGE[incident.severity]}`}>
                    {incident.severity}
                  </span>
                </div>
              ))}
            </div>
          )}
        </Panel>
      </div>

      <div className="surface-panel-soft mt-4 rounded-2xl p-5 text-sm text-slate-500">
        IOC, CVE and hash lookups aren't wired to a live feed yet — this page
        reflects detections produced by {BRAND.name}'s own drift-detection
        engine only.
      </div>
    </>
  );
}
