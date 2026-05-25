import subprocess # for running bandit command
import os # to remove tempoorary file
import tempfile # to create temporary file
import json # to parse bandit output
import logging # for logging activities and errors
from .rule_base_analysis import run_rules
logger = logging.getLogger(__name__)

async def Static_analysis(diff: str):
    file = extract_python_files(diff)
    all_findings = []
    for filename, code in file.items():
        logger.info("running bandit on %s",filename)
        findings =run_bandit(filename, code)
        rule_findings = run_rules(filename, code)
        all_findings.extend(findings)
        all_findings.extend(rule_findings)
        

    logging.info("Bandit found %d issues", len(all_findings))
    return all_findings

def extract_python_files(diff: str) -> dict:
    files ={}
    current_file = None
    lines = []

    for line in diff.splitlines():
        if line.startswith("+++ b/") and line.endswith(".py"):
            if current_file and lines:
                files[current_file] = "\n".join(lines)
            current_file = line[6:]
            lines = []
        elif line.startswith("+") and not line.startswith("+++"):
            lines.append(line[1:])  # Remove the leading "+" for added lines
    if current_file and lines:
        files[current_file] = "\n".join(lines)

    logger.info("Extracted Python files: %s", list(files.keys()))
    return files

def run_bandit(filename: str, code: str) -> list:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        temp_path = f.name
    try:
        result = subprocess.run(["bandit", "-f", "json", "-q",temp_path], capture_output=True, text=True)
        if not result.stdout:
            return []
        data = json.loads(result.stdout)
        findings = []
        for issues in data.get("results", []):
            findings.append({
                "filename": filename,
                "line": issues.get("line_number"),
                "severity": issues.get("issue_severity"),
                "Confidence": issues.get("issue_confidence"),
                "issue": issues.get("issue_text"),
                "test_id": issues.get("test_id")
                })
        return findings
    except Exception as e:
        logger.error("Error running bandit on %s: %s", filename, str(e))
        return []
    finally:
        os.remove(temp_path)