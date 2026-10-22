<<<<<<< HEAD
import { useCallback, useState } from "react";
=======
import { useCallback, useMemo, useState } from "react";
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
import {
  Plus,
  Server,
  ShieldCheck,
  TriangleAlert,
  ShieldAlert,
} from "lucide-react";

import StatCard from "../components/cards/StatCard";
import ThreatIntelligence from "../components/cards/ThreatIntelligence";
import TopMitreTechniques from "../components/cards/TopMitreTechniques";
import HostResourceInventory from "../components/inventory/HostResourceInventory";
import LiveThreatFeed from "../components/threats/LiveThreatFeed";
import AddHostModal from "../components/common/AddHostModal";

<<<<<<< HEAD
import { getDashboardSummary } from "../services/dashboard";
import { useAutoRefresh } from "../hooks/useAutoRefresh";
import AutoRefreshControl from "../components/common/AutoRefreshControl";
import { PageHero } from "../components/common/Controls";
import SearchNotice from "../components/ui/SearchNotice";
=======
import { getDashboardSummary } from "../services/dashboardService";
import { useAutoRefresh } from "../hooks/useAutoRefresh";
import AutoRefreshControl from "../components/common/AutoRefreshControl";
import { PageHero } from "../components/common/Controls";
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15

export default function Dashboard({ searchQuery = "" }) {
  const [summary, setSummary] = useState(null);
  const [refreshToken, setRefreshToken] = useState(0);
  const [showAddHost, setShowAddHost] = useState(false);

  const loader = useCallback(async () => {
    const data = await getDashboardSummary();
    setSummary(data);
    setRefreshToken((n) => n + 1);
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

<<<<<<< HEAD
=======
  const query = searchQuery.trim().toLowerCase();

  const filteredSummary = useMemo(() => {
    if (!summary || !query) return summary;
    return summary;
  }, [summary, query]);

>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
  return (
    <>
      <PageHero
        title="Security Overview"
        subtitle="Fleet posture, live threats, and host load at a glance."
        actions={
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowAddHost(true)}
              className="flex items-center gap-1.5 rounded-xl bg-cyan-600 px-3 py-2 text-sm font-semibold transition hover:bg-cyan-500"
            >
              <Plus size={15} />
              Add Host
            </button>
            <AutoRefreshControl
              autoUpdate={autoUpdate}
              setAutoUpdate={setAutoUpdate}
              intervalMs={intervalMs}
              setIntervalMs={setIntervalMs}
              lastUpdated={
                lastUpdated ||
                (summary?.last_sync ? new Date(summary.last_sync) : null)
              }
              loading={loading}
              onRefresh={() => refresh()}
            />
          </div>
        }
      />

      {showAddHost && (
        <AddHostModal
          onClose={() => setShowAddHost(false)}
          onCreated={() => refresh()}
        />
      )}

<<<<<<< HEAD
      <SearchNotice query={searchQuery}>
        Showing results matching <strong>{searchQuery}</strong> in host inventory and threat feed.
      </SearchNotice>
=======
      {query && (
        <div className="mb-4 rounded-xl border border-cyan-400/20 bg-cyan-400/5 px-4 py-2 text-sm text-cyan-200">
          Showing results matching <strong>{searchQuery}</strong> in host inventory and threat feed.
        </div>
      )}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15

      <div className="grid gap-5 xl:grid-cols-4 lg:grid-cols-2 md:grid-cols-2 sm:grid-cols-1">
        <StatCard
          title="Total Hosts"
<<<<<<< HEAD
          value={summary ? summary.total_hosts : "..."}
          icon={Server}
          color="text-cyan-300"
          change={
            summary?.online_hosts != null
              ? `${summary.online_hosts} online`
=======
          value={filteredSummary ? filteredSummary.total_hosts : "..."}
          icon={Server}
          color="text-cyan-300"
          change={
            filteredSummary?.online_hosts != null
              ? `${filteredSummary.online_hosts} online`
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
              : ""
          }
        />
        <StatCard
          title="Security Health"
<<<<<<< HEAD
          value={summary ? `${summary.security_health}%` : "..."}
=======
          value={filteredSummary ? `${filteredSummary.security_health}%` : "..."}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
          icon={ShieldCheck}
          color="text-emerald-300"
          change=""
        />
        <StatCard
          title="Critical Alerts"
<<<<<<< HEAD
          value={summary ? summary.critical_alerts : "..."}
=======
          value={filteredSummary ? filteredSummary.critical_alerts : "..."}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
          icon={TriangleAlert}
          color="text-rose-300"
          change=""
        />
        <StatCard
          title="Open Incidents"
<<<<<<< HEAD
          value={summary ? summary.open_incidents : "..."}
=======
          value={filteredSummary ? filteredSummary.open_incidents : "..."}
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
          icon={ShieldAlert}
          color="text-amber-300"
          change=""
        />
      </div>

      <div className="mt-6">
        <HostResourceInventory searchQuery={searchQuery} refreshToken={refreshToken} />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-5 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <LiveThreatFeed searchQuery={searchQuery} refreshToken={refreshToken} />
        </div>
        <div className="flex flex-col gap-5">
          <ThreatIntelligence refreshToken={refreshToken} />
          <TopMitreTechniques refreshToken={refreshToken} />
        </div>
      </div>
    </>
  );
}
