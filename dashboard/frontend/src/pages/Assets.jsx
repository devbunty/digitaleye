<<<<<<< HEAD
import { useCallback, useMemo, useState } from "react";
=======
<<<<<<< HEAD
import { useCallback, useMemo, useState } from "react";
=======
import { useCallback, useEffect, useMemo, useState } from "react";
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd

import AssetTable from "../components/assets/AssetTable";
import HostOverview from "../components/assets/HostOverview";
import HostTelemetry from "../components/assets/HostTelemetry";
import AssetSecurityPosture from "../components/assets/AssetSecurityPosture";
import QuickActions from "../components/assets/QuickActions";

import { getAssets } from "../services/assets";
import { getIncidents } from "../services/incidents";
import { useAutoRefresh } from "../hooks/useAutoRefresh";
import AutoRefreshControl from "../components/common/AutoRefreshControl";
<<<<<<< HEAD
import ErrorBanner from "../components/ui/ErrorBanner";
import Metric from "../components/ui/Metric";
import SearchNotice from "../components/ui/SearchNotice";
=======
<<<<<<< HEAD
import ErrorBanner from "../components/ui/ErrorBanner";
import Metric from "../components/ui/Metric";
import SearchNotice from "../components/ui/SearchNotice";
=======
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
import {
  ControlBar,
  FilterSelect,
  PageHero,
  SortSelect,
} from "../components/common/Controls";
import { computePosture } from "../utils/assetHelpers";

export default function Assets({ searchQuery = "", setPage }) {
  const [assets, setAssets] = useState([]);
  const [incidents, setIncidents] = useState([]);
<<<<<<< HEAD
  const [selectedHostname, setSelectedHostname] = useState(null);
=======
<<<<<<< HEAD
  const [selectedHostname, setSelectedHostname] = useState(null);
=======
  const [selectedHost, setSelectedHost] = useState(null);
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
  const [statusFilter, setStatusFilter] = useState("All");
  const [osFilter, setOsFilter] = useState("All");
  const [sortBy, setSortBy] = useState("hostname");
  const [error, setError] = useState(null);

  const loader = useCallback(async () => {
    setError(null);
    try {
      const [assetData, incidentData] = await Promise.all([
        getAssets(),
        getIncidents({ status: "Open" }),
      ]);
      setAssets(assetData);
      setIncidents(incidentData);
    } catch (err) {
      console.error(err);
      setError("Failed to refresh asset inventory.");
    }
  }, []);

  const {
    autoUpdate,
    setAutoUpdate,
    intervalMs,
    setIntervalMs,
    lastUpdated,
    loading,
    refresh,
  } = useAutoRefresh(loader, {
    enabled: true,
    intervalMs: 10000,
  });

  const incidentsByHost = useMemo(() => {
    const map = {};
    incidents.forEach((inc) => {
      if (!map[inc.hostname]) map[inc.hostname] = [];
      map[inc.hostname].push(inc);
    });
    return map;
  }, [incidents]);

  const enrichedAssets = useMemo(
    () =>
      assets.map((host) => {
        const openAlerts = incidentsByHost[host.hostname] || [];
        const posture = computePosture(host, openAlerts);
        return {
          ...host,
          open_alerts: openAlerts.length,
          posture: posture.label,
          posture_tone: posture.tone,
        };
      }),
    [assets, incidentsByHost]
  );

  const osOptions = useMemo(() => {
    const set = new Set(["All"]);
    assets.forEach((h) => {
      if (h.os) set.add(h.os);
    });
    return Array.from(set).map((os) => ({
      value: os,
      label: os === "All" ? "All operating systems" : os,
    }));
  }, [assets]);

  const filteredAssets = useMemo(() => {
    let data = [...enrichedAssets];
    const query = searchQuery.trim().toLowerCase();

    if (query) {
      data = data.filter(
        (host) =>
          host.hostname?.toLowerCase().includes(query) ||
          host.ip?.toLowerCase().includes(query) ||
          host.os?.toLowerCase().includes(query) ||
          host.kernel?.toLowerCase().includes(query)
      );
    }

    if (statusFilter !== "All") {
      data = data.filter((host) => host.status === statusFilter);
    }

    if (osFilter !== "All") {
      data = data.filter((host) => host.os === osFilter);
    }

    data.sort((a, b) => {
      switch (sortBy) {
        case "last_seen":
          return new Date(b.last_seen || 0) - new Date(a.last_seen || 0);
        case "processes":
          return (b.processes || 0) - (a.processes || 0);
        case "open_alerts":
          return (b.open_alerts || 0) - (a.open_alerts || 0);
        case "status":
          return (a.status || "").localeCompare(b.status || "");
        case "posture":
          return (a.posture || "").localeCompare(b.posture || "");
        default:
          return (a.hostname || "").localeCompare(b.hostname || "");
      }
    });

    return data;
  }, [enrichedAssets, searchQuery, statusFilter, osFilter, sortBy]);

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
  // Derived from the latest data, so the detail view stays fresh and closes
  // by itself when the host leaves the filtered list.
  const selectedHost =
    filteredAssets.find((h) => h.hostname === selectedHostname) ?? null;
<<<<<<< HEAD
=======
=======
  useEffect(() => {
    if (!selectedHost) return;
    const fresh = filteredAssets.find(
      (h) => h.hostname === selectedHost.hostname
    );
    if (!fresh) setSelectedHost(null);
    else if (fresh !== selectedHost) setSelectedHost(fresh);
  }, [filteredAssets, selectedHost]);
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd

  const onlineHosts = assets.filter((h) => h.status === "Online").length;
  const offlineHosts = assets.length - onlineHosts;
  const withAlerts = enrichedAssets.filter((h) => h.open_alerts > 0).length;
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
  const countOs = (name) =>
    assets.filter((h) => (h.os || "").toLowerCase().includes(name)).length;
  const linuxHosts = countOs("linux");
  const windowsHosts = countOs("windows");
<<<<<<< HEAD
=======
=======
  const linuxHosts = assets.filter((h) =>
    (h.os || "").toLowerCase().includes("linux")
  ).length;
  const windowsHosts = assets.filter((h) =>
    (h.os || "").toLowerCase().includes("windows")
  ).length;
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
  const avgProcesses = assets.length
    ? Math.round(
        assets.reduce((s, h) => s + (h.processes || 0), 0) / assets.length
      )
    : 0;

  const selectedIncidents = selectedHost
    ? incidentsByHost[selectedHost.hostname] || []
    : [];

  return (
    <>
      <PageHero
        title="Assets"
        subtitle="Endpoint inventory and agent posture — identity, coverage, and open exposure."
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

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
      <SearchNotice query={searchQuery}>
        Showing assets matching <strong>{searchQuery}</strong>
      </SearchNotice>

      <div className="mb-5 grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
        <Metric size="sm" label="Endpoints" value={assets.length} />
        <Metric size="sm" label="Agents online" value={onlineHosts} accent="text-emerald-300" />
        <Metric size="sm" label="Unreachable" value={offlineHosts} accent="text-rose-300" />
        <Metric size="sm" label="With open alerts" value={withAlerts} accent="text-amber-300" />
        <Metric size="sm" label="Linux / Windows" value={`${linuxHosts} / ${windowsHosts}`} />
        <Metric size="sm" label="Avg process inventory" value={avgProcesses} accent="text-cyan-300" />
<<<<<<< HEAD
=======
=======
      {searchQuery.trim() && (
        <div className="mb-4 rounded-xl border border-cyan-400/20 bg-cyan-400/5 px-4 py-2 text-sm text-cyan-200">
          Showing assets matching <strong>{searchQuery}</strong>
        </div>
      )}

      <div className="mb-5 grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
        <MiniStat label="Endpoints" value={assets.length} />
        <MiniStat label="Agents online" value={onlineHosts} accent="text-emerald-300" />
        <MiniStat label="Unreachable" value={offlineHosts} accent="text-rose-300" />
        <MiniStat label="With open alerts" value={withAlerts} accent="text-amber-300" />
        <MiniStat label="Linux / Windows" value={`${linuxHosts} / ${windowsHosts}`} />
        <MiniStat label="Avg process inventory" value={avgProcesses} accent="text-cyan-300" />
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
      </div>

      <ControlBar>
        <div className="flex flex-wrap items-center gap-3">
          <FilterSelect
            label="Status"
            value={statusFilter}
            onChange={setStatusFilter}
            options={[
              { value: "All", label: "All statuses" },
              { value: "Online", label: "Online" },
              { value: "Offline", label: "Offline" },
            ]}
          />
          <FilterSelect
            label="OS"
            value={osFilter}
            onChange={setOsFilter}
            options={osOptions}
          />
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-500">
            {filteredAssets.length} endpoint{filteredAssets.length === 1 ? "" : "s"}
          </span>
          <SortSelect
            value={sortBy}
            onChange={setSortBy}
            options={[
              { value: "hostname", label: "Hostname" },
              { value: "last_seen", label: "Last seen" },
              { value: "processes", label: "Process inventory" },
              { value: "open_alerts", label: "Open alerts" },
              { value: "posture", label: "Posture" },
              { value: "status", label: "Agent status" },
            ]}
          />
        </div>
      </ControlBar>

<<<<<<< HEAD
      <ErrorBanner>{error}</ErrorBanner>
=======
<<<<<<< HEAD
      <ErrorBanner>{error}</ErrorBanner>
=======
      {error && (
        <div className="mb-4 rounded-2xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-rose-300">
          {error}
        </div>
      )}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd

      <AssetTable
        assets={filteredAssets}
        selectedHost={selectedHost}
<<<<<<< HEAD
        setSelectedHost={(host) => setSelectedHostname(host?.hostname ?? null)}
=======
<<<<<<< HEAD
        setSelectedHost={(host) => setSelectedHostname(host?.hostname ?? null)}
=======
        setSelectedHost={setSelectedHost}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
      />

      {selectedHost ? (
        <div className="mt-6 grid grid-cols-1 gap-5 xl:grid-cols-3">
          <div className="space-y-5 xl:col-span-2">
            <HostOverview host={selectedHost} />
            <AssetSecurityPosture
              host={selectedHost}
              incidents={selectedIncidents}
            />
          </div>
          <div className="space-y-5">
            <HostTelemetry host={selectedHost} />
            <QuickActions host={selectedHost} setPage={setPage} />
          </div>
        </div>
      ) : (
        <div className="surface-panel-soft mt-6 rounded-2xl border-dashed p-14 text-center">
          <h2 className="font-display text-2xl font-semibold">Select an endpoint</h2>
          <p className="mx-auto mt-3 max-w-md text-slate-400">
            Review identity, agent coverage, open alerts, and response actions
            for any host in your fleet.
          </p>
        </div>
      )}
    </>
  );
}
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======

function MiniStat({ label, value, accent = "text-white" }) {
  return (
    <div className="surface-panel rounded-2xl px-4 py-3.5">
      <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-500">
        {label}
      </p>
      <p className={`metric-value mt-1.5 text-2xl font-semibold ${accent}`}>
        {value}
      </p>
    </div>
  );
}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
