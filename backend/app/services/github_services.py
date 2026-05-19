#webhook Signature Verification
from backend.config import settings
import hmac , hashlib , os


def verify_github_signature(payload_bytes:bytes, signature:str) -> bool:
    if not signature:
        return False
    excepted_signature = "sha256="+hmac.new(settings.GITHUB_WEBHOOK_SECRET.encode(), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(excepted_signature, signature)
