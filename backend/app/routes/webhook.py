import json
import logging
from fastapi import APIRouter, Request, HTTPException, Header , Depends
from backend.app.services.github_services import verify_github_signature
from backend.app.services.database_service import save_pull_request_event
from backend.app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_ACTIONS = {"opened", "synchronize", "reopened", "closed"}


@router.post("/webhook")
async def webhook(
    request: Request, x_hub_signature_256: str | None = Header(default=None), db: AsyncSession = Depends(get_db) ):
    raw_body = await request.body()

    if not verify_github_signature(raw_body, x_hub_signature_256):
        raise HTTPException(status_code=400, detail="Invalid signature")

    payload = json.loads(raw_body)  # now it's a dict

    action = payload.get("action")
    if action not in ALLOWED_ACTIONS:
        return {"ignored": True}

    pr = payload.get("pull_request", {})

    pr_data = {
        "action": action,
        "number": pr.get("number"),
        "title": pr.get("title"),
        "merged": pr.get("merged"),
        "base_branch": pr.get("base", {}).get("ref"),
        "head_branch": pr.get("head", {}).get("ref"),
        "repo": payload.get("repository", {}).get("full_name"),
        "sender": payload.get("sender", {}).get("login"),
    }
    record = await save_pull_request_event(db, pr_data)
    logger.info("PR #%s - action: %s", pr.get("number"), action)
    print(f'message:"webhook received successfully, record_id: {record.id}')
    return {"message": "Webhook received successfully", "record_id": record.id}
