import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";
import { RISK_COLORS } from "../utils/format";

export default function RiskDistributionChart({ data }) {
  // data is {CRITICAL: 2, HIGH: 5, ...} → convert to array, drop zeros
  const chartData = Object.entries(data || {})
    .filter(([, value]) => value > 0)
    .map(([name, value]) => ({ name, value }));

  if (chartData.length === 0) {
    return (
      <div className="text-slate-500 text-center py-12">
        No analysis data yet
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie
          data={chartData}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={100}
          paddingAngle={3}
        >
          {chartData.map((entry) => (
            <Cell key={entry.name} fill={RISK_COLORS[entry.name]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            background: "#0f172a",
            border: "1px solid #1e293b",
            borderRadius: "8px",
            color: "#fff",
          }}
        />
        <Legend wrapperStyle={{ fontSize: "13px" }} />
      </PieChart>
    </ResponsiveContainer>
  );
}
