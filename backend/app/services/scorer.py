import logging

logger = logging.getLogger(__name__)

SEVERITY_WEIGHTS = {
    "HIGH": 10,
    "MEDIUM": 5,
    "LOW": 1,
}

RULE_WEIGHTS = {
    "HARDCODED_SECRET": 15,
    "SQL_INJECTION_RISK": 15,
    "EVAL_EXEC_USAGE": 12,
    "NESTED_LOOP": 5,
    "BARE_EXCEPT": 4,
    "LARGE_FUNCTION": 3,
    "MUTABLE_DEFAULT_ARG": 3,
    "TODO_COMMENT": 1,
    "PRINT_STATEMENT": 1,
}


def get_risk_level(score: int) -> str:
    if score >= 50:
        return "CRITICAL"
    elif score >= 30:
        return "HIGH"
    elif score >= 15:
        return "MEDIUM"
    elif score > 0:
        return "LOW"
    return "CLEAN"


def calculate_risk_score(findings: list[dict]) -> dict:
    if not findings:
        return {
            "score": 0,
            "risk_level": "CLEAN",
            "total": 0,
            "by_severity": {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
            "by_rule": {},
        }

    score = 0
    by_severity = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    by_rule = {}

    for finding in findings:
        severity = finding.get("severity", "LOW").upper()
        rule = finding.get("rule", finding.get("test_id", "UNKNOWN"))

        score += SEVERITY_WEIGHTS.get(severity, 1)
        score += RULE_WEIGHTS.get(rule, 0)

        by_severity[severity] = by_severity.get(severity, 0) + 1
        by_rule[rule] = by_rule.get(rule, 0) + 1

    risk_level = get_risk_level(score)
    logger.info("Risk score: %d — level: %s", score, risk_level)

    return {
        "score": score,
        "risk_level": risk_level,
        "total": len(findings),
        "by_severity": by_severity,
        "by_rule": by_rule,
    }
