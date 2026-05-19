from sqlalchemy import Column, Integer, String, Boolean, DateTime
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
