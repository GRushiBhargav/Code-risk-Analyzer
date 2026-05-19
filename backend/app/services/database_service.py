from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.models import PullRequest


async def save_pull_request_event(db: AsyncSession, pr_data: dict):
    pr = PullRequest(
        pr_number=pr_data["number"],
        title=pr_data["title"],
        sender=pr_data["sender"],  # ← already a string
        repo=pr_data["repo"],  # ← already extracted
        action=pr_data["action"],
        merged=pr_data["merged"],
        base_branch=pr_data["base_branch"],  # ← already extracted
        head_branch=pr_data["head_branch"],  # ← already extracted
    )
    db.add(pr)
    await db.commit()
    await db.refresh(pr)
    return pr
