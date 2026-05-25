import ast
import re 
import logging

logger = logging.getLogger(__name__)

# function to check for nested loops in the code
def check_nested_loops(code: str, filename: str) -> list[dict]:
    findings = []

    try:
        tree = ast.parse(code,filename=filename)
        loop_type = (ast.For, ast.While)

        for node in ast.walk(tree):
            if isinstance(node,loop_type):
                for child in node.body:
                    if isinstance(child,loop_type):
                        findings.append({
                            filename: filename,
                            "line": node.lineno,
                            "severity": "Medium",
                            "rule": "Nestded Loops",
                            "issue": "Direct Nested loop dectected "
                        })
                        break
    except SyntaxError as e:
        logger.error("Syntax error in file %s: %s", filename, e)
    return findings

def large_functions(code: str, filename: str) -> list[dict]:
    findings = []
    try:
        tree = ast.parse(code, filename=filename)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                end_line = getattr(node, 'end_lineno', node.lineno)
                length = end_line - node.lineno + 1
                if length > 50:
                    findings.append({
                        "filename": filename,
                        "line": node.lineno,
                        "severity": "Medium",
                        "rule": "Large Function",
                        "issue": f"Function '{node.name}' is too long ({length} lines) consider refactoring."
                    })
    except SyntaxError as e:
        logger.error("Syntax error in file %s: %s", filename, e)
    return findings


def check_eval_exec(filename: str, code: str) -> list[dict]:
    findings = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id in ("eval", "exec"):
                    findings.append(
                        {
                            "filename": filename,
                            "line": node.lineno,
                            "severity": "HIGH",
                            "rule": "EVAL_EXEC_USAGE",
                            "issue": f"Dangerous use of '{func.id}()' detected",
                        }
                    )
    except SyntaxError:
        logger.warning("AST parse failed for %s", filename)
    return findings


def check_bare_except(filename: str, code: str) -> list[dict]:
    findings = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    findings.append(
                        {
                            "filename": filename,
                            "line": node.lineno,
                            "severity": "MEDIUM",
                            "rule": "BARE_EXCEPT",
                            "issue": "Bare except clause — catches all exceptions including SystemExit",
                        }
                    )
    except SyntaxError:
        logger.warning("AST parse failed for %s", filename)
    return findings


def check_hardcoded_secrets(filename: str, code: str) -> list[dict]:

    findings = []

    pattern = re.compile(
        r"(?i)\b(password|secret|api_key|token|passwd)\b" r'\s*=\s*["\'][^"\']{8,}["\']'
    )

    for line_number, line in enumerate(code.splitlines(), start=1):

        if pattern.search(line):

            findings.append(
                {
                    "filename": filename,
                    "line": line_number,
                    "severity": "HIGH",
                    "source": "rule_engine",
                    "rule": "HARDCODED_SECRET",
                    "issue": "Possible hardcoded secret",
                }
            )

    return findings


def check_sql_concatenation(filename: str, code: str) -> list[dict]:

    findings = []

    pattern = re.compile(
        r"(?i)(select|insert|update|delete|where).*" r'(\+|\.format\(|f["\'])'
    )

    for line_number, line in enumerate(code.splitlines(), start=1):

        if pattern.search(line):

            findings.append(
                {
                    "filename": filename,
                    "line": line_number,
                    "severity": "HIGH",
                    "source": "rule_engine",
                    "rule": "SQL_INJECTION_RISK",
                    "issue": "Possible SQL query string building",
                }
            )

    return findings


def check_todos(filename: str, code: str) -> list[dict]:

    findings = []

    pattern = re.compile(r"(?i)#.*(todo|fixme|hack|xxx)")

    for line_number, line in enumerate(code.splitlines(), start=1):

        if pattern.search(line):

            findings.append(
                {
                    "filename": filename,
                    "line": line_number,
                    "severity": "LOW",
                    "source": "rule_engine",
                    "rule": "TODO_COMMENT",
                    "issue": "Unresolved TODO/FIXME",
                }
            )

    return findings


def check_print_statements(filename: str, code: str) -> list[dict]:

    if "test" in filename.lower():
        return []

    findings = []

    pattern = re.compile(r"^\s*print\s*\(")

    for line_number, line in enumerate(code.splitlines(), start=1):

        if pattern.search(line):

            findings.append(
                {
                    "filename": filename,
                    "line": line_number,
                    "severity": "LOW",
                    "source": "rule_engine",
                    "rule": "PRINT_STATEMENT",
                    "issue": "print() found; use logging",
                }
            )

    return findings


AST_RULES = [
    check_eval_exec,
    check_nested_loops,
    check_bare_except,
]

REGEX_RULES = [
    check_hardcoded_secrets,
    check_sql_concatenation,
    check_todos,
    check_print_statements,
]


def run_rules(filename: str, code: str) -> list[dict]:

    findings = []

    for rule in AST_RULES + REGEX_RULES:
        findings.extend(rule(filename, code))

    logger.info("Rule engine found %d issues in %s", len(findings), filename)

    return findings
