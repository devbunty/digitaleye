import { motion } from "framer-motion";
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
import Card from "../ui/Card";
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
import { ArrowUpRight } from "lucide-react";

export default function StatCard({
  title,
  value,
  icon: Icon,
  color,
  change,
}) {
  return (
    <motion.div
      whileHover={{ y: -6 }}
      transition={{ duration: 0.25 }}
      className="h-full"
    >
<<<<<<< HEAD
      <div className="group relative h-full overflow-hidden rounded-2xl border border-slate-700/80 bg-slate-900/70 p-6 shadow-2xl backdrop-blur-md transition-all duration-300 hover:border-slate-500 hover:shadow-cyan-500/10">
=======
<<<<<<< HEAD
      <div className="group relative h-full overflow-hidden rounded-2xl border border-slate-700/80 bg-slate-900/70 p-6 shadow-2xl backdrop-blur-md transition-all duration-300 hover:border-slate-500 hover:shadow-cyan-500/10">
=======
      <Card className="relative overflow-hidden h-full p-6 group border-slate-700/80 hover:border-slate-500">
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd

        {/* Background Glow */}
        <div className="absolute -right-12 -top-12 h-36 w-36 rounded-full bg-white/5 blur-3xl transition-all duration-500 group-hover:bg-white/10" />

        {/* Header */}
        <div className="relative flex items-start justify-between">

          <div>
            <p className="text-sm font-bold uppercase tracking-[0.18em] text-slate-100">
              {title}
            </p>

            <h2 className={`mt-4 text-5xl font-extrabold tracking-tight ${color}`}>
              {value}
            </h2>
          </div>

          {/* Icon */}
          <div className="rounded-2xl border border-slate-700 bg-slate-800/90 p-4 shadow-lg transition group-hover:scale-110">
            <Icon
              size={30}
              className={color}
            />
          </div>

        </div>


        {/* Progress Bar */}
        <div className="relative mt-8">

          <div className="h-1.5 overflow-hidden rounded-full bg-slate-800">

            <div
              className={`h-full rounded-full bg-gradient-to-r from-white/20 to-current ${color}`}
              style={{
                width: typeof value === "number"
                  ? `${Math.min(100, Math.max(8, Number(value) || 0))}%`
                  : String(value).includes("%")
                  ? String(value)
                  : "40%",
              }}
            />

          </div>

        </div>


        {/* Footer */}
        <div className="relative mt-5 flex items-center justify-between">

          <div className="flex items-center gap-2">

            {change ? (
              <>
                <ArrowUpRight
                  size={17}
                  className="text-emerald-400"
                />

                <span className="text-sm font-semibold text-emerald-400">
                  {change}
                </span>
              </>
            ) : (
              <span className="text-sm text-slate-500">Live</span>
            )}

          </div>


          <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
            Fleet
          </span>

        </div>


<<<<<<< HEAD
      </div>
=======
<<<<<<< HEAD
      </div>
=======
      </Card>
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
    </motion.div>
  );
}
