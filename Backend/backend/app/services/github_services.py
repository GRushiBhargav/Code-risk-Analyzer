# webhook Signature Verification
from backend.config import settings
import hmac , hashlib , os
import httpx
import logging

logger = logging.getLogger(__name__)

def verify_github_signature(payload_bytes:bytes, signature:str) -> bool:
    if not signature:
        return False
    excepted_signature = "sha256="+hmac.new(settings.GITHUB_WEBHOOK_SECRET.encode(), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(excepted_signature, signature)

async def fetch_pr_data(repo:str, pr_number:int):
    url = f'https://api.github.com/repos/{repo}/pulls/{pr_number}'
    headers = {
        "Authorization": f'Bearer {settings.GITHUB_TOKEN}',
        "Accept": "application/vnd.github.v3.diff"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url ,headers=headers)
        if response.status_code == 404:
            logger.warning("PR #%s not found in %s", pr_number, repo)
            return None
        response.raise_for_status()
        return response.text

async def post_pr_comment(repo:str,pr_number:int,comments:str):

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    header = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url,headers=header,json={"body":comments})
        if response.status_code == 201:
            logger.info("Comment posted to PR #%s", pr_number)
            return True
        logger.error(
            "Failed to post comment: %s — %s", response.status_code, response.text
        )
        return False
