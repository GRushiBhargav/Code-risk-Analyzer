import { useEffect, useState } from "react";
import {
  ShieldAlert,
  GitPullRequest,
  Activity,
  AlertTriangle,
} from "lucide-react";
import {
  getStats,
  getRiskDistribution,
  getTopRisky,
  getRecentActivity,
} from "../api/client";
import StatCard from "../components/StatCard";
import RiskDistributionChart from "../components/RiskDistributionChart";
import TopRiskyTable from "../components/TopRiskyTable";
import RecentActivity from "../components/RecentActivity";
import Loading from "../components/Loading";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [risk, setRisk] = useState(null);
  const [topRisky, setTopRisky] = useState([]);
  const [activity, setActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        // fetch all in parallel
        const [s, r, t, a] = await Promise.all([
          getStats(),
          getRiskDistribution(),
          getTopRisky(10),
          getRecentActivity(15),
        ]);
        setStats(s);
        setRisk(r);
        setTopRisky(t);
        setActivity(a);
      } catch (err) {
        console.error(err);
        setError("Failed to load dashboard. Is the backend running?");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <Loading />;

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <AlertTriangle className="w-10 h-10 text-red-400 mb-3" />
        <p className="text-slate-300">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">
          Code Risk Dashboard
        </h1>
        <p className="text-slate-400 mt-1">
          Automated PR analysis & risk monitoring
        </p>
      </div>

      {/* KPI cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          label="Total PRs"
          value={stats.total_prs}
          icon={GitPullRequest}
          accent="text-cyan-400"
        />
        <StatCard
          label="Analyses Run"
          value={stats.total_analyses}
          icon={Activity}
          accent="text-green-400"
        />
        <StatCard
          label="Avg Risk Score"
          value={stats.avg_risk_score}
          icon={ShieldAlert}
          accent="text-orange-400"
        />
        <StatCard
          label="Total Findings"
          value={stats.total_findings}
          icon={AlertTriangle}
          accent="text-red-400"
        />
      </div>

      {/* Charts + activity row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Risk distribution */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4">Risk Distribution</h2>
          <RiskDistributionChart data={risk} />
        </div>

        {/* Recent activity */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
          <div className="max-h-[280px] overflow-y-auto pr-2">
            <RecentActivity data={activity} />
          </div>
        </div>
      </div>

      {/* Top risky PRs */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold mb-4">Top Risky Pull Requests</h2>
        <TopRiskyTable data={topRisky} />
      </div>
    </div>
  );
}
