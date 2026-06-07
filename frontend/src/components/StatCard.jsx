export default function StatCard({
  label,
  value,
  icon: Icon,
  accent = "text-cyan-400",
}) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors">
      <div className="flex items-center justify-between">
        <span className="text-slate-400 text-sm font-medium">{label}</span>
        {Icon && <Icon className={`w-5 h-5 ${accent}`} />}
      </div>
      <div className="mt-3 text-3xl font-bold tracking-tight">{value}</div>
    </div>
  );
}
