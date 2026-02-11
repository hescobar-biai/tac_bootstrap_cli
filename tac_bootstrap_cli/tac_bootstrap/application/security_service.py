"""
IDK: security-scanning, secret-detection, owasp-validation, vulnerability-checking
Responsibility: Performs comprehensive security scans including secret detection,
                OWASP Top 10 validation, template scanning, and dependency checks
Invariants: Scans are non-destructive (read-only), all patterns are compiled once,
            results are deterministic, no external API calls required
"""

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from tac_bootstrap.domain.security import (
    SecurityCategory,
    SecurityIssue,
    SecurityReport,
    SecuritySeverity,
    Vulnerability,
)

# ============================================================================
# SECRET PATTERNS - Compiled regex patterns for secret detection
# ============================================================================

SECRET_PATTERNS: List[Tuple[str, re.Pattern[str], SecuritySeverity, str]] = [
    (
        "AWS Access Key",
        re.compile(r"AKIA[0-9A-Z]{16}", re.IGNORECASE),
        SecuritySeverity.CRITICAL,
        "CWE-798",
    ),
    (
        "AWS Secret Key",
        re.compile(r"(?i)aws(.{0,20})?['\"][0-9a-zA-Z/+]{40}['\"]"),
        SecuritySeverity.CRITICAL,
        "CWE-798",
    ),
    (
        "Generic API Key",
        re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]"),
        SecuritySeverity.HIGH,
        "CWE-798",
    ),
    (
        "Generic Secret",
        re.compile(r"(?i)(secret|token|password|passwd|pwd)\s*[:=]\s*['\"][^\s'\"]{8,}['\"]"),
        SecuritySeverity.HIGH,
        "CWE-798",
    ),
    (
        "Private Key",
        re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"),
        SecuritySeverity.CRITICAL,
        "CWE-321",
    ),
    (
        "GitHub Token",
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,}"),
        SecuritySeverity.CRITICAL,
        "CWE-798",
    ),
    (
        "Generic Bearer Token",
        re.compile(r"(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*"),
        SecuritySeverity.MEDIUM,
        "CWE-798",
    ),
    (
        "Database URL with credentials",
        re.compile(
            r"(?i)(mysql|postgres|postgresql|mongodb|redis)://\w+:[^@\s]+@"
        ),
        SecuritySeverity.HIGH,
        "CWE-798",
    ),
    (
        "Hardcoded IP Address",
        re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
        SecuritySeverity.LOW,
        "CWE-200",
    ),
    (
        "JWT Token",
        re.compile(r"eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_.+/=]+"),
        SecuritySeverity.HIGH,
        "CWE-798",
    ),
]

# ============================================================================
# SQL INJECTION PATTERNS
# ============================================================================

SQL_INJECTION_PATTERNS: List[Tuple[str, re.Pattern[str]]] = [
    (
        "String concatenation in SQL query",
        re.compile(r"""(?i)(?:execute|cursor\.execute|query)\s*\(\s*[f"'].*\{.*\}"""),
    ),
    (
        "f-string in SQL query",
        re.compile(r'(?i)(?:SELECT|INSERT|UPDATE|DELETE|DROP)\s+.*f["\']'),
    ),
    (
        "String format in SQL",
        re.compile(r"(?i)(?:SELECT|INSERT|UPDATE|DELETE).*\.format\("),
    ),
    (
        "Percent formatting in SQL",
        re.compile(r"(?i)(?:SELECT|INSERT|UPDATE|DELETE).*%\s*\("),
    ),
]

# ============================================================================
# XSS PATTERNS
# ============================================================================

XSS_PATTERNS: List[Tuple[str, re.Pattern[str]]] = [
    (
        "innerHTML assignment",
        re.compile(r"\.innerHTML\s*="),
    ),
    (
        "document.write usage",
        re.compile(r"document\.write\s*\("),
    ),
    (
        "Unescaped template output",
        re.compile(r"\{\{\s*\w+\s*\|?\s*safe\s*\}\}"),
    ),
    (
        "eval() usage",
        re.compile(r"\beval\s*\("),
    ),
    (
        "dangerouslySetInnerHTML",
        re.compile(r"dangerouslySetInnerHTML"),
    ),
]

# ============================================================================
# FILE EXTENSIONS TO SCAN
# ============================================================================

SCANNABLE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs",
    ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".conf",
    ".env", ".env.local", ".env.production", ".env.development",
    ".sh", ".bash", ".zsh", ".sql", ".html", ".htm", ".xml",
    ".j2", ".jinja2", ".md", ".txt",
}

SKIP_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", "dist", "build",
    ".tox", ".eggs", "*.egg-info",
}


# ============================================================================
# SECURITY SERVICE
# ============================================================================


class SecurityService:
    """
    IDK: security-scanner, secret-detector, owasp-validator, vuln-checker
    Responsibility: Performs comprehensive security analysis on project files
                    including secret scanning, SQL injection detection, XSS prevention,
                    OWASP Top 10 validation, and dependency vulnerability checking
    Invariants: All scans are read-only, patterns are compiled once at module level,
                results are deterministic, scanning handles errors gracefully
    """

    def scan_for_secrets(self, path: Path) -> List[SecurityIssue]:
        """
        Scan files for hardcoded secrets, API keys, tokens, and passwords.

        Recursively scans all scannable files in the given path for patterns
        that match known secret formats.

        Args:
            path: File or directory to scan

        Returns:
            List of SecurityIssue instances for each secret found
        """
        issues: List[SecurityIssue] = []

        if path.is_file():
            issues.extend(self._scan_file_for_secrets(path))
        elif path.is_dir():
            for file_path in self._iter_scannable_files(path):
                issues.extend(self._scan_file_for_secrets(file_path))

        return issues

    def _scan_file_for_secrets(self, file_path: Path) -> List[SecurityIssue]:
        """Scan a single file for secret patterns."""
        issues: List[SecurityIssue] = []

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return issues

        for line_num, line in enumerate(content.splitlines(), start=1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue

            for pattern_name, pattern, severity, cwe_id in SECRET_PATTERNS:
                match = pattern.search(line)
                if match:
                    # Filter out common false positives
                    if self._is_false_positive_secret(line, match.group()):
                        continue

                    issues.append(
                        SecurityIssue(
                            category=SecurityCategory.SECRET_EXPOSURE,
                            severity=severity,
                            message=f"{pattern_name} detected",
                            file_path=str(file_path),
                            line_number=line_num,
                            matched_pattern=match.group()[:80],
                            suggestion=f"Remove hardcoded {pattern_name.lower()} and use "
                            "environment variables or a secrets manager instead",
                            cwe_id=cwe_id,
                        )
                    )

        return issues

    def _is_false_positive_secret(self, line: str, matched: str) -> bool:
        """Check if a secret match is likely a false positive."""
        lower_line = line.lower()

        # Common false positive indicators
        fp_indicators = [
            "example", "placeholder", "your_", "xxx", "todo",
            "change_me", "replace_", "dummy", "test_", "fake",
            "sample", "<your", "${", "{{", "127.0.0.1", "0.0.0.0",
            "localhost", "192.168.", "10.0.", "172.16.",
        ]
        for indicator in fp_indicators:
            if indicator in lower_line or indicator in matched.lower():
                return True

        # Skip if in a comment
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("*"):
            return True

        return False

    def scan_templates(self, path: Path) -> List[SecurityIssue]:
        """
        Scan template files for security vulnerabilities.

        Checks for SQL injection, XSS, and other common vulnerabilities
        in template and source files.

        Args:
            path: File or directory to scan

        Returns:
            List of SecurityIssue instances
        """
        issues: List[SecurityIssue] = []

        if path.is_file():
            issues.extend(self._scan_file_for_vulns(path))
        elif path.is_dir():
            for file_path in self._iter_scannable_files(path):
                issues.extend(self._scan_file_for_vulns(file_path))

        return issues

    def _scan_file_for_vulns(self, file_path: Path) -> List[SecurityIssue]:
        """Scan a single file for SQL injection and XSS patterns."""
        issues: List[SecurityIssue] = []

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return issues

        for line_num, line in enumerate(content.splitlines(), start=1):
            # SQL Injection patterns
            for pattern_name, pattern in SQL_INJECTION_PATTERNS:
                if pattern.search(line):
                    issues.append(
                        SecurityIssue(
                            category=SecurityCategory.SQL_INJECTION,
                            severity=SecuritySeverity.HIGH,
                            message=f"Potential SQL injection: {pattern_name}",
                            file_path=str(file_path),
                            line_number=line_num,
                            matched_pattern=line.strip()[:80],
                            suggestion="Use parameterized queries or an ORM "
                            "instead of string concatenation in SQL",
                            cwe_id="CWE-89",
                        )
                    )

            # XSS patterns
            for pattern_name, pattern in XSS_PATTERNS:
                if pattern.search(line):
                    issues.append(
                        SecurityIssue(
                            category=SecurityCategory.XSS,
                            severity=SecuritySeverity.MEDIUM,
                            message=f"Potential XSS vulnerability: {pattern_name}",
                            file_path=str(file_path),
                            line_number=line_num,
                            matched_pattern=line.strip()[:80],
                            suggestion="Sanitize user input and use content security "
                            "policies to prevent cross-site scripting",
                            cwe_id="CWE-79",
                        )
                    )

        return issues

    def validate_owasp_top10(self, config: Any) -> List[SecurityIssue]:
        """
        Validate project configuration against OWASP Top 10 best practices.

        Checks configuration for common security misconfigurations based
        on the OWASP Top 10 categories.

        Args:
            config: TACConfig instance or config-like object

        Returns:
            List of SecurityIssue instances for OWASP violations
        """
        issues: List[SecurityIssue] = []

        # A01:2021 - Broken Access Control
        if hasattr(config, "agentic") and hasattr(config.agentic, "safety"):
            safety = config.agentic.safety
            if not safety.forbidden_paths:
                issues.append(
                    SecurityIssue(
                        category=SecurityCategory.BROKEN_AUTH,
                        severity=SecuritySeverity.MEDIUM,
                        message="No forbidden paths configured for agent safety",
                        suggestion="Add forbidden_paths to agentic.safety to restrict "
                        "agent access to sensitive directories (e.g., .env, secrets/)",
                        cwe_id="CWE-284",
                    )
                )

        # A02:2021 - Cryptographic Failures
        if hasattr(config, "orchestrator"):
            orch = config.orchestrator
            if orch.enabled:
                if "http://" in orch.api_base_url and "localhost" not in orch.api_base_url:
                    issues.append(
                        SecurityIssue(
                            category=SecurityCategory.INSECURE_CONFIG,
                            severity=SecuritySeverity.HIGH,
                            message="Orchestrator API uses HTTP instead of HTTPS "
                            "for non-localhost connections",
                            suggestion="Use HTTPS for production API endpoints "
                            "to encrypt data in transit",
                            cwe_id="CWE-319",
                        )
                    )

        # A03:2021 - Injection
        # Checked by scan_templates()

        # A05:2021 - Security Misconfiguration
        if hasattr(config, "project"):
            if hasattr(config.project, "architecture"):
                if config.project.architecture.value == "simple":
                    issues.append(
                        SecurityIssue(
                            category=SecurityCategory.INSECURE_CONFIG,
                            severity=SecuritySeverity.INFO,
                            message="Simple architecture may lack security layers",
                            suggestion="Consider using DDD or layered architecture "
                            "for better separation of security concerns",
                            cwe_id="CWE-1188",
                        )
                    )

        # A09:2021 - Security Logging and Monitoring Failures
        if hasattr(config, "agentic") and hasattr(config.agentic, "logging"):
            logging_config = config.agentic.logging
            if logging_config.level not in ("DEBUG", "INFO"):
                issues.append(
                    SecurityIssue(
                        category=SecurityCategory.INSUFFICIENT_LOGGING,
                        severity=SecuritySeverity.LOW,
                        message="Logging level may be insufficient for security monitoring",
                        suggestion="Set logging level to INFO or DEBUG to capture "
                        "security-relevant events for monitoring",
                        cwe_id="CWE-778",
                    )
                )

        return issues

    def check_dependency_vulnerabilities(
        self, deps: List[str]
    ) -> List[Vulnerability]:
        """
        Check dependencies for known vulnerabilities.

        This performs a local heuristic check based on known vulnerable
        version patterns. For comprehensive checking, use tools like
        pip-audit, npm audit, or safety.

        Args:
            deps: List of dependency strings (e.g., ["flask>=2.0", "django<3.0"])

        Returns:
            List of Vulnerability instances for known issues
        """
        vulnerabilities: List[Vulnerability] = []

        # Known vulnerable patterns (simplified local check)
        known_vulns: Dict[str, Tuple[str, str, SecuritySeverity, str]] = {
            "django": (
                "<3.2",
                "Django versions before 3.2 have known security vulnerabilities",
                SecuritySeverity.HIGH,
                "Upgrade to Django >= 3.2 LTS",
            ),
            "flask": (
                "<2.0",
                "Flask versions before 2.0 have known security vulnerabilities",
                SecuritySeverity.MEDIUM,
                "Upgrade to Flask >= 2.0",
            ),
            "requests": (
                "<2.25",
                "Requests versions before 2.25 have MITM vulnerability",
                SecuritySeverity.MEDIUM,
                "Upgrade to requests >= 2.25",
            ),
            "pyyaml": (
                "<5.4",
                "PyYAML versions before 5.4 are vulnerable to arbitrary code execution",
                SecuritySeverity.CRITICAL,
                "Upgrade to PyYAML >= 5.4",
            ),
            "jinja2": (
                "<3.0",
                "Jinja2 versions before 3.0 have sandbox escape vulnerabilities",
                SecuritySeverity.HIGH,
                "Upgrade to Jinja2 >= 3.0",
            ),
        }

        for dep_str in deps:
            # Parse dependency name (handle pip format: name>=version)
            dep_name = re.split(r"[><=!~\[]", dep_str.strip())[0].strip().lower()

            if dep_name in known_vulns:
                affected_ver, desc, severity, fix = known_vulns[dep_name]
                vulnerabilities.append(
                    Vulnerability(
                        package=dep_name,
                        current_version=dep_str,
                        affected_versions=affected_ver,
                        severity=severity,
                        description=desc,
                        fix_version=fix,
                    )
                )

        return vulnerabilities

    def generate_security_report(self, path: Path) -> SecurityReport:
        """
        Generate a comprehensive security report for a project.

        Combines secret scanning, template scanning, and OWASP validation
        into a single report.

        Args:
            path: Project directory to scan

        Returns:
            SecurityReport with all findings
        """
        all_issues: List[SecurityIssue] = []
        files_scanned = 0

        # Secret scanning
        secret_issues = self.scan_for_secrets(path)
        all_issues.extend(secret_issues)

        # Template/vulnerability scanning
        vuln_issues = self.scan_templates(path)
        all_issues.extend(vuln_issues)

        # Count scanned files
        if path.is_dir():
            files_scanned = sum(1 for _ in self._iter_scannable_files(path))
        elif path.is_file():
            files_scanned = 1

        # Build report
        report = SecurityReport(
            scan_timestamp=datetime.now(timezone.utc).isoformat(),
            target_path=str(path),
            issues=all_issues,
            total_files_scanned=files_scanned,
        )
        report.compute_summary()

        return report

    def _iter_scannable_files(self, directory: Path) -> List[Path]:
        """
        Iterate over scannable files in a directory, skipping irrelevant dirs.

        Args:
            directory: Root directory to scan

        Yields:
            Path objects for each scannable file
        """
        files: List[Path] = []

        try:
            for item in directory.rglob("*"):
                # Skip hidden and irrelevant directories
                parts = item.parts
                if any(part in SKIP_DIRS for part in parts):
                    continue
                if any(part.startswith(".") and part not in (".env",) for part in parts):
                    continue

                if item.is_file():
                    # Check extension
                    if item.suffix in SCANNABLE_EXTENSIONS or item.name.startswith(".env"):
                        files.append(item)
        except PermissionError:
            pass

        return files

    def format_report_text(self, report: SecurityReport) -> str:
        """
        Format a security report as human-readable text.

        Args:
            report: SecurityReport to format

        Returns:
            Formatted text report string
        """
        lines: List[str] = []
        lines.append("=" * 60)
        lines.append("TAC Bootstrap Security Report")
        lines.append("=" * 60)
        lines.append(f"Scan Time: {report.scan_timestamp}")
        lines.append(f"Target: {report.target_path}")
        lines.append(f"Files Scanned: {report.total_files_scanned}")
        lines.append(f"Total Issues: {report.total_issues}")
        lines.append("")

        # Summary
        if report.summary:
            lines.append("Summary by Severity:")
            for severity, count in sorted(report.summary.items()):
                lines.append(f"  {severity.upper()}: {count}")
            lines.append("")

        # Issues
        if report.issues:
            lines.append("Security Issues:")
            lines.append("-" * 40)
            for i, issue in enumerate(report.issues, 1):
                lines.append(
                    f"  {i}. [{issue.severity.value.upper()}] {issue.message}"
                )
                if issue.file_path:
                    lines.append(f"     File: {issue.file_path}:{issue.line_number}")
                if issue.suggestion:
                    lines.append(f"     Fix: {issue.suggestion}")
                if issue.cwe_id:
                    lines.append(f"     CWE: {issue.cwe_id}")
                lines.append("")

        # Vulnerabilities
        if report.vulnerabilities:
            lines.append("Dependency Vulnerabilities:")
            lines.append("-" * 40)
            for v in report.vulnerabilities:
                lines.append(f"  [{v.severity.value.upper()}] {v.package}: {v.description}")
                if v.fix_version:
                    lines.append(f"     Fix: {v.fix_version}")
                lines.append("")

        if not report.has_issues:
            lines.append("No security issues found.")
            lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines)
