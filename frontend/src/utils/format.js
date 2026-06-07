export const RISK_COLORS = {
  CRITICAL: "#dc2626", // red-600
  HIGH: "#ea580c", // orange-600
  MEDIUM: "#ca8a04", // yellow-600
  LOW: "#16a34a", // green-600
  CLEAN: "#0891b2", // cyan-600
};

export const RISK_BADGE = {
  CRITICAL: "bg-red-500/15 text-red-400 border-red-500/30",
  HIGH: "bg-orange-500/15 text-orange-400 border-orange-500/30",
  MEDIUM: "bg-yellow-500/15 text-yellow-400 border-yellow-500/30",
  LOW: "bg-green-500/15 text-green-400 border-green-500/30",
  CLEAN: "bg-cyan-500/15 text-cyan-400 border-cyan-500/30",
};

export const SEVERITY_COLORS = {
  HIGH: "#dc2626",
  MEDIUM: "#ca8a04",
  LOW: "#16a34a",
};

export function formatDate(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
