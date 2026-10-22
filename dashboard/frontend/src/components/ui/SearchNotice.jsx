/** Banner reminding the user that the header search is filtering this page. */
export default function SearchNotice({ query, children }) {
  if (!query.trim()) return null;

  return (
    <div className="mb-4 rounded-xl border border-cyan-400/20 bg-cyan-400/5 px-4 py-2 text-sm text-cyan-200">
      {children}
    </div>
  );
}
