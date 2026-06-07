import { RISK_BADGE } from "../utils/format";

export default function RiskBadge({ level }) {
  const style = RISK_BADGE[level] || RISK_BADGE.CLEAN;
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${style}`}
    >
      {level}
    </span>
  );
}
