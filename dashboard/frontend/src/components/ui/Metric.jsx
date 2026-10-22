const SIZES = {
  md: { box: "px-4 py-4", label: "tracking-[0.18em]", value: "mt-2 text-3xl" },
  sm: { box: "px-4 py-3.5", label: "tracking-[0.16em]", value: "mt-1.5 text-2xl" },
};

/** Small KPI tile: label on top, big number below. */
export default function Metric({
  label,
  value,
  icon: Icon,
  accent = "text-white",
  hint,
  size = "md",
  compact = false,
  placeholder = "...",
}) {
  const styles = SIZES[size];

  return (
    <div className={`surface-panel rounded-2xl ${styles.box}`}>
      <div className="flex items-center justify-between">
        <p
          className={`text-[11px] font-semibold uppercase text-slate-500 ${styles.label}`}
        >
          {label}
        </p>
        {Icon && <Icon size={16} className={accent} />}
      </div>

      <p
        className={`metric-value font-semibold ${accent} ${
          compact ? "mt-2 truncate text-lg" : styles.value
        }`}
        title={String(value ?? "")}
      >
        {value ?? placeholder}
      </p>

      {hint && <p className="mt-1 text-xs text-slate-500">{hint}</p>}
    </div>
  );
}
