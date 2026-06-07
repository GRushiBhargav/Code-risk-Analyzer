from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from backend.app.database.session import Base


class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    pr_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    repo = Column(String, nullable=False)
    action = Column(String, nullable=False)
    merged = Column(Boolean, default=False)
    base_branch = Column(String, nullable=True)
    head_branch = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class AnalysisResult(Base):
    __tablename__ = "analysis_result"

    id = Column(Integer,primary_key=True,index=True)
    pr_number = Column(Integer,ForeignKey("pull_requests.id"))
    risk_score = Column(Integer,nullable=False)
    risk_level = Column(String,nullable=False)
    total_findings = Column(Integer,nullable=False)
    findings = Column(JSON,nullable=False)
    by_severity = Column(JSON, nullable=True)
    by_rule = Column(JSON, nullable=True)
    ai_review = Column(String,nullable=True)
    created_at = Column(DateTime, server_default=func.now())
