export const SEVERITIES = ["Critical", "High", "Medium", "Low"];

/** Sort order: lower rank = more severe. */
export const SEVERITY_RANK = { Critical: 0, High: 1, Medium: 2, Low: 3 };

/** Chart fills. */
export const SEVERITY_COLORS = {
  Critical: "#fb7185",
  High: "#fbbf24",
  Medium: "#fde047",
  Low: "#94a3b8",
};

/** Badge classes. */
export const SEVERITY_BADGE = {
  Critical: "bg-rose-500/20 text-rose-300 border-rose-500/30",
  High: "bg-amber-500/20 text-amber-300 border-amber-500/30",
  Medium: "bg-yellow-500/20 text-yellow-200 border-yellow-500/30",
  Low: "bg-slate-500/20 text-slate-300 border-slate-500/30",
};

export const STATUS_COLORS = {
  Open: "#fbbf24",
  Resolved: "#34d399",
};

export const TOOLTIP_STYLE = {
  background: "#0b1220",
  border: "1px solid #1e293b",
  borderRadius: 12,
  color: "#e2e8f0",
};
