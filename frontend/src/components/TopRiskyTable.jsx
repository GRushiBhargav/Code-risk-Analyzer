import { useNavigate } from "react-router-dom";
import RiskBadge from "./RiskBadge";

export default function TopRiskyTable({ data }) {
  const navigate = useNavigate();

  if (!data || data.length === 0) {
    return (
      <div className="text-slate-500 text-center py-12">
        No PRs analyzed yet
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-slate-400 text-left border-b border-slate-800">
            <th className="pb-3 font-medium">PR</th>
            <th className="pb-3 font-medium">Repo</th>
            <th className="pb-3 font-medium">Score</th>
            <th className="pb-3 font-medium">Level</th>
          </tr>
        </thead>
        <tbody>
          {data.map((pr) => (
            <tr
              key={pr.analysis_id}
              onClick={() => navigate(`/analysis/${pr.analysis_id}`)}
              className="border-b border-slate-800/50 hover:bg-slate-800/40 cursor-pointer transition-colors"
            >
              <td className="py-3">
                <div className="font-medium">#{pr.pr_number}</div>
                <div className="text-slate-500 text-xs truncate max-w-[180px]">
                  {pr.title}
                </div>
              </td>
              <td className="py-3 text-slate-400 text-xs">{pr.repo}</td>
              <td className="py-3 font-bold">{pr.risk_score}</td>
              <td className="py-3">
                <RiskBadge level={pr.risk_level} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
