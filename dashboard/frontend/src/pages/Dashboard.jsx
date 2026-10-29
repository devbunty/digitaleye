import { useCallback, useState } from "react";
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

import { getDashboardSummary } from "../services/dashboard";
import { useAutoRefresh } from "../hooks/useAutoRefresh";
import AutoRefreshControl from "../components/common/AutoRefreshControl";
import { PageHero } from "../components/common/Controls";
import SearchNotice from "../components/ui/SearchNotice";

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

      <SearchNotice query={searchQuery}>
        Showing results matching <strong>{searchQuery}</strong> in host inventory and threat feed.
      </SearchNotice>

      <div className="grid gap-5 xl:grid-cols-4 lg:grid-cols-2 md:grid-cols-2 sm:grid-cols-1">
        <StatCard
          title="Total Hosts"
          value={summary ? summary.total_hosts : "..."}
          icon={Server}
          color="text-cyan-300"
          change={
            summary?.online_hosts != null
              ? `${summary.online_hosts} online`
              : ""
          }
        />
        <StatCard
          title="Security Health"
          value={summary ? `${summary.security_health}%` : "..."}
          icon={ShieldCheck}
          color="text-emerald-300"
          change=""
        />
        <StatCard
          title="Critical Alerts"
          value={summary ? summary.critical_alerts : "..."}
          icon={TriangleAlert}
          color="text-rose-300"
          change=""
        />
        <StatCard
          title="Open Incidents"
          value={summary ? summary.open_incidents : "..."}
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
