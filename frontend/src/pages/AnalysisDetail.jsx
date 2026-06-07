import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, FileCode, AlertTriangle } from "lucide-react";
import { getAnalysisDetails } from "../api/client";
import RiskBadge from "../components/RiskBadge";
import Loading from "../components/Loading";
import { formatDate } from "../utils/format";
import ReactMarkdown from "react-markdown";
const SEV_STYLE = {
  HIGH: "text-red-400 bg-red-500/10",
  MEDIUM: "text-yellow-400 bg-yellow-500/10",
  LOW: "text-green-400 bg-green-500/10",
};

export default function AnalysisDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const result = await getAnalysisDetails(id);
        setData(result);
      } catch (err) {
        console.error(err);
        setError("Could not load this analysis.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  if (loading) return <Loading />;
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <AlertTriangle className="w-10 h-10 text-red-400 mb-3" />
        <p className="text-slate-300">{error}</p>
        <button
          onClick={() => navigate("/")}
          className="mt-4 text-cyan-400 hover:underline"
        >
          Back to dashboard
        </button>
      </div>
    );
  }

  const sev = data.by_severity || {};

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      {/* Back */}
      <button
        onClick={() => navigate("/")}
        className="flex items-center gap-2 text-slate-400 hover:text-slate-200 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Back to dashboard
      </button>

      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold">
              PR #{data.pr_number} · {data.title}
            </h1>
            <p className="text-slate-400 text-sm mt-1">{data.repo}</p>
            <p className="text-slate-500 text-xs mt-2">
              {data.head_branch} → {data.base_branch} · by {data.sender} ·{" "}
              {formatDate(data.created_at)}
            </p>
          </div>
          <div className="text-right shrink-0">
            <div className="text-3xl font-bold">{data.risk_score}</div>
            <div className="mt-1">
              <RiskBadge level={data.risk_level} />
            </div>
          </div>
        </div>

        {/* Severity counts */}
        <div className="flex gap-3 mt-5">
          {["HIGH", "MEDIUM", "LOW"].map((s) => (
            <div
              key={s}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium ${SEV_STYLE[s]}`}
            >
              {s}: {sev[s] || 0}
            </div>
          ))}
          <div className="px-3 py-1.5 rounded-lg text-sm font-medium text-slate-300 bg-slate-800">
            Total: {data.total_findings}
          </div>
        </div>
      </div>

      {/* AI Review */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
        <h2 className="text-lg font-semibold mb-3">🤖 AI Review</h2>
        <div className="prose-review text-sm text-slate-300 leading-relaxed">
          <ReactMarkdown
            components={{
              h1: (p) => (
                <h1
                  className="text-xl font-bold text-slate-100 mt-4 mb-2"
                  {...p}
                />
              ),
              h2: (p) => (
                <h2
                  className="text-lg font-bold text-slate-100 mt-4 mb-2"
                  {...p}
                />
              ),
              h3: (p) => (
                <h3
                  className="text-base font-semibold text-slate-200 mt-3 mb-1.5"
                  {...p}
                />
              ),
              h4: (p) => (
                <h4
                  className="text-sm font-semibold text-slate-200 mt-3 mb-1"
                  {...p}
                />
              ),
              p: (p) => <p className="mb-3" {...p} />,
              ul: (p) => (
                <ul className="list-disc pl-5 mb-3 space-y-1" {...p} />
              ),
              ol: (p) => (
                <ol className="list-decimal pl-5 mb-3 space-y-1" {...p} />
              ),
              li: (p) => <li className="text-slate-300" {...p} />,
              strong: (p) => (
                <strong className="font-semibold text-slate-100" {...p} />
              ),
              code: (p) => (
                <code
                  className="px-1.5 py-0.5 rounded bg-slate-800 text-cyan-300 text-xs font-mono"
                  {...p}
                />
              ),
            }}
          >
            {data.ai_review || "No AI review available."}
          </ReactMarkdown>
        </div>
      </div>

      {/* Findings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold mb-4">
          Findings ({data.findings?.length || 0})
        </h2>
        <div className="space-y-2">
          {(data.findings || []).map((f, i) => (
            <div
              key={i}
              className="flex items-start gap-3 p-3 rounded-lg bg-slate-800/40 border border-slate-800"
            >
              <FileCode className="w-4 h-4 mt-0.5 text-slate-500 shrink-0" />
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <span
                    className={`px-2 py-0.5 rounded text-xs font-semibold ${SEV_STYLE[f.severity] || "text-slate-400 bg-slate-700"}`}
                  >
                    {f.severity}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">
                    {f.rule || f.test_id}
                  </span>
                  <span className="text-xs text-slate-500">
                    {f.filename}:{f.line}
                  </span>
                </div>
                <p className="text-sm text-slate-300 mt-1">{f.issue}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
