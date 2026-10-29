/** Titled surface that groups a chart, table or list. */
export default function Panel({
  title,
  subtitle,
  actions,
  className = "",
  children,
}) {
  return (
    <section className={`surface-panel rounded-2xl p-5 ${className}`}>
      <div className="mb-3 flex items-start justify-between gap-3">
        <div>
          <h2 className="font-display text-lg font-semibold text-white">
            {title}
          </h2>
          {subtitle && (
            <p className="mt-0.5 text-sm text-slate-500">{subtitle}</p>
          )}
        </div>
        {actions}
      </div>
      {children}
    </section>
  );
}
