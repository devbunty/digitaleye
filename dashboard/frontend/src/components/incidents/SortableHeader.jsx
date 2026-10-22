import { ArrowDownUp, ChevronDown, ChevronUp } from "lucide-react";

export default function SortableHeader({ column, sort, onSort, children }) {
  const active = sort.key === column;

  return (
    <th className="p-4 text-left">
      <button
        type="button"
        onClick={() => onSort(column)}
        className={`inline-flex items-center gap-1.5 font-semibold transition ${
          active ? "text-cyan-300" : "text-slate-300 hover:text-white"
        }`}
      >
        {children}
        {active ? (
          sort.dir === "asc" ? <ChevronUp size={14} /> : <ChevronDown size={14} />
        ) : (
          <ArrowDownUp size={12} className="opacity-40" />
        )}
      </button>
    </th>
  );
}
