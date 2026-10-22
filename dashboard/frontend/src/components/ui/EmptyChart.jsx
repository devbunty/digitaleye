/** Placeholder shown where a chart or list has nothing to display. */
export default function EmptyChart({ text }) {
  return (
    <div className="flex h-full items-center justify-center rounded-xl border border-dashed border-white/10 text-sm text-slate-500">
      {text}
    </div>
  );
}
