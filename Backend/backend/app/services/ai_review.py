import json
import logging
from google import genai
from backend.config import settings

logger = logging.getLogger(__name__)

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def build_promt(diff:str,findings:list[dict],risk:dict):
    findings_text = json.dumps(findings,indent=2)

    return f"""You are a Senior code reviewer analyzing a github pull request.
       Below is the diff, automated findings from static analysis(Bandit) and custom rule engine, and calculated risk score

       #Risk Score
        level: {risk["risk_level"]} (score: {risk["score"]}) 
       #Automated findings  
       {findings_text}

        #code Diff
        {diff[:10000]}

        Provide a concise review with these sections:
        1. **Summary** — 2-3 sentences on overall risk
        2. **Security Concerns** — specific issues and why they matter
        3. **Maintainability** — code quality and structural concerns
        4. **Recommended Fixes** — concrete, actionable steps

        Be direct and technical. Focus on the most important issues. """

async def generate_ai_review(diff:str,findings:list[dict],risk:dict):
    if not findings:
        return "No Issues Found. Code look clean "
    prompt = build_promt(diff,findings,risk)

    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
        )
        review = response.text
        logger.info("Ai review Generated -%d(chatacters)",len(review))
        return review
    except Exception as e:
        logger.error("AI review failed: %s",e)
        return "AI review could not be generated due to an error."


def format_pr_comment(risk: dict, findings: list[dict], ai_review: str) -> str:
    emoji = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢",
        "CLEAN": "✅",
    }
    level = risk["risk_level"]
    sev = risk.get("by_severity", {})

    return f"""## {emoji.get(level, '⚪')} Code Risk Analysis

**Risk Level:** {level} (score: {risk['score']})
**Total Findings:** {risk['total']}

| Severity | Count |
|----------|-------|
| HIGH     | {sev.get('HIGH', 0)} |
| MEDIUM   | {sev.get('MEDIUM', 0)} |
| LOW      | {sev.get('LOW', 0)} |

---

{ai_review}

---
*🤖 Automated review by Code Risk Analyzer*"""
