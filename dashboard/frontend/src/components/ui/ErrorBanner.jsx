export default function ErrorBanner({ children, className = "mb-4" }) {
  if (!children) return null;

  return (
    <div
      className={`rounded-2xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-rose-300 ${className}`}
    >
      {children}
    </div>
  );
}
