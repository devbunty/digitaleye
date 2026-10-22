import { X } from "lucide-react";

import { formatDateTime, formatRelativeTime } from "../../utils/assetHelpers";

function Detail({ label, value }) {
  return (
    <div className="rounded-xl border border-white/8 bg-black/20 p-3">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 text-sm font-medium text-slate-200">{value || "—"}</p>
    </div>
  );
}

export default function IncidentDetail({ incident, onClose }) {
  return (
    <div className="surface-panel mt-5 rounded-2xl p-6">
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-wider text-slate-500">
            Incident #{incident.id}
          </p>
          <h2 className="mt-1 font-display text-xl font-semibold">
            {incident.title}
          </h2>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="rounded-lg border border-white/10 p-2 text-slate-400 hover:text-white"
        >
          <X size={18} />
        </button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Detail label="Host" value={incident.hostname} />
        <Detail label="Severity" value={incident.severity} />
        <Detail label="Status" value={incident.status} />
        <Detail label="Rule" value={incident.rule_id} />
        <Detail label="Category" value={incident.category} />
        <Detail label="MITRE" value={incident.mitre} />
        <Detail label="Detected" value={formatDateTime(incident.timestamp)} />
        <Detail label="Age" value={formatRelativeTime(incident.timestamp)} />
      </div>

      <div className="mt-5">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-500">
          Evidence
        </p>
        <pre className="max-h-48 overflow-auto whitespace-pre-wrap break-all rounded-xl border border-white/8 bg-black/30 p-4 text-sm text-slate-300">
          {incident.evidence || "No evidence recorded."}
        </pre>
      </div>
    </div>
  );
}
