from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.models import AnalysisResult,PullRequest

async def list_analysis(db:AsyncSession,limit:int = 20, offset: int = 0):
    statement = (select(AnalysisResult,PullRequest).join(PullRequest,AnalysisResult.pr_number == PullRequest.id).order_by(desc(AnalysisResult.created_at)).limit(limit).offset(offset))
    result = await db.execute(statement)
    rows = result.all()
    return [
        {
            "analysis_id": a.id,
            "pr_number": pull.pr_number,
            "title": pull.title,
            "repo": pull.repo,
            "sender": pull.sender,
            "risk_score": a.risk_score,
            "risk_level": a.risk_level,
            "total_findings": a.total_findings,
            "created_at": a.created_at,
        }
        for a, pull in rows
    ]


async def get_analysis_details(db: AsyncSession, analysis_id: int):
    statement = (
        select(AnalysisResult, PullRequest)
        .join(PullRequest, AnalysisResult.pr_number == PullRequest.id)
        .where(AnalysisResult.id == analysis_id)
    )
    result = await db.execute(statement)
    row = result.first()
    if not row:
        return None
    analysis,pull = row
    return {
            "analysis_id": analysis.id,
            "pr_number": pull.pr_number,
            "title": pull.title,
            "repo": pull.repo,
            "sender": pull.sender,
            "base_branch": pull.base_branch,
            "head_branch": pull.head_branch,
            "risk_score": analysis.risk_score,
            "risk_level": analysis.risk_level,
            "total_findings": analysis.total_findings,
            "findings": analysis.findings,
            "by_severity": analysis.by_severity,
            "by_rule": analysis.by_rule,
            "ai_review": analysis.ai_review,
            "created_at": analysis.created_at,
        }


async def get_dashboard_stats(db: AsyncSession):
    total_prs = await db.scalar(select(func.count(PullRequest.id)))
    total_analyses = await db.scalar(select(func.count(AnalysisResult.id)))
    avg_score = await db.scalar(select(func.avg(AnalysisResult.risk_score)))
    total_findings = await db.scalar(select(func.sum(AnalysisResult.total_findings)))

    return {
        "total_prs": total_prs or 0,
        "total_analyses": total_analyses or 0,
        "avg_risk_score": round(float(avg_score), 1) if avg_score else 0,
        "total_findings": total_findings or 0,
    }


async def get_risk_distribution(db: AsyncSession):
    stmt = select(AnalysisResult.risk_level, func.count(AnalysisResult.id)).group_by(
        AnalysisResult.risk_level
    )
    result = await db.execute(stmt)
    rows = result.all()
    distribution = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "CLEAN": 0}
    for level, count in rows:
        distribution[level] = count
    return distribution


async def get_top_risky_prs(db: AsyncSession, limit: int = 10):
    stmt = (
        select(AnalysisResult, PullRequest)
        .join(PullRequest, AnalysisResult.pr_number == PullRequest.id)
        .order_by(desc(AnalysisResult.risk_score))
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [
        {
            "analysis_id": a.id,
            "pr_number": pr.pr_number,
            "title": pr.title,
            "repo": pr.repo,
            "risk_score": a.risk_score,
            "risk_level": a.risk_level,
        }
        for a, pr in rows
    ]

async def get_recent_activity(db: AsyncSession, limit: int = 15):
    stmt = select(PullRequest).order_by(desc(PullRequest.created_at)).limit(limit)
    result = await db.execute(stmt)
    prs = result.scalars().all()
    return [
        {
            "pr_number": pr.pr_number,
            "title": pr.title,
            "repo": pr.repo,
            "sender": pr.sender,
            "action": pr.action,
            "merged": pr.merged,
            "created_at": pr.created_at,
        }
        for pr in prs
    ]
