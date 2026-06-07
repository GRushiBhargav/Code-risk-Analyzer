import { GitPullRequest, GitMerge, CircleDot } from "lucide-react";
import { formatDate } from "../utils/format";

const ACTION_ICON = {
  opened: { icon: GitPullRequest, color: "text-green-400" },
  closed: { icon: CircleDot, color: "text-red-400" },
  reopened: { icon: GitPullRequest, color: "text-cyan-400" },
  synchronize: { icon: GitPullRequest, color: "text-slate-400" },
};

export default function RecentActivity({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="text-slate-500 text-center py-12">No recent activity</div>
    );
  }

  return (
    <div className="space-y-3">
      {data.map((pr, i) => {
        const merged = pr.merged && pr.action === "closed";
        const conf = merged
          ? { icon: GitMerge, color: "text-purple-400" }
          : ACTION_ICON[pr.action] || ACTION_ICON.synchronize;
        const Icon = conf.icon;
        return (
          <div key={i} className="flex items-start gap-3">
            <Icon className={`w-4 h-4 mt-0.5 shrink-0 ${conf.color}`} />
            <div className="min-w-0 flex-1">
              <div className="text-sm truncate">
                <span className="font-medium">#{pr.pr_number}</span>{" "}
                <span className="text-slate-400">{pr.title}</span>
              </div>
              <div className="text-xs text-slate-500">
                {merged ? "merged" : pr.action} · {pr.sender} ·{" "}
                {formatDate(pr.created_at)}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
