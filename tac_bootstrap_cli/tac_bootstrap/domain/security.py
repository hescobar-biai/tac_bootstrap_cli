"""
IDK: security-models, vulnerability-types, security-issue-classification
Responsibility: Defines domain models for security scanning and vulnerability reporting
Invariants: Severity levels are ordered (critical > high > medium > low > info),
            all issues have a category and actionable suggestion
"""

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

# ============================================================================
# ENUMS
# ============================================================================


class SecuritySeverity(str, Enum):
    """Severity levels for security issues, ordered from most to least critical."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class SecurityCategory(str, Enum):
    """Categories of security issues aligned with OWASP Top 10 and common concerns."""

    SECRET_EXPOSURE = "secret_exposure"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    CSRF = "csrf"
    BROKEN_AUTH = "broken_auth"
    SENSITIVE_DATA = "sensitive_data"
    INSECURE_CONFIG = "insecure_config"
    DEPENDENCY_VULN = "dependency_vuln"
    PATH_TRAVERSAL = "path_traversal"
    COMMAND_INJECTION = "command_injection"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    INSUFFICIENT_LOGGING = "insufficient_logging"


# ============================================================================
# SECURITY MODELS
# ============================================================================


class SecurityIssue(BaseModel):
    """
    Represents a single security issue found during scanning.

    Attributes:
        category: Security issue category
        severity: Severity level
        message: Human-readable description of the issue
        file_path: Path to the file where issue was found (relative)
        line_number: Line number where issue was found (0 if unknown)
        matched_pattern: The pattern or content that triggered the finding
        suggestion: Actionable fix suggestion
        cwe_id: Optional CWE (Common Weakness Enumeration) identifier
    """

    category: SecurityCategory = Field(..., description="Issue category")
    severity: SecuritySeverity = Field(..., description="Severity level")
    message: str = Field(..., description="Human-readable issue description")
    file_path: str = Field(default="", description="File path where issue was found")
    line_number: int = Field(default=0, description="Line number of the issue", ge=0)
    matched_pattern: str = Field(default="", description="Pattern that triggered the finding")
    suggestion: str = Field(default="", description="Actionable fix suggestion")
    cwe_id: Optional[str] = Field(default=None, description="CWE identifier (e.g., 'CWE-798')")


class Vulnerability(BaseModel):
    """
    Represents a dependency vulnerability.

    Attributes:
        package: Package/dependency name
        current_version: Currently used version
        affected_versions: Version range affected by vulnerability
        severity: Severity level
        description: Vulnerability description
        fix_version: Version that fixes the vulnerability
        cve_id: CVE identifier if available
    """

    package: str = Field(..., description="Package name")
    current_version: str = Field(default="", description="Currently used version")
    affected_versions: str = Field(default="", description="Affected version range")
    severity: SecuritySeverity = Field(
        default=SecuritySeverity.MEDIUM, description="Severity level"
    )
    description: str = Field(default="", description="Vulnerability description")
    fix_version: Optional[str] = Field(default=None, description="Fixed version")
    cve_id: Optional[str] = Field(default=None, description="CVE identifier")


class SecurityReport(BaseModel):
    """
    Aggregated security scan report.

    Attributes:
        scan_timestamp: ISO8601 timestamp of when scan was performed
        target_path: Path that was scanned
        issues: List of security issues found
        vulnerabilities: List of dependency vulnerabilities
        total_files_scanned: Number of files scanned
        summary: Summary statistics by severity
    """

    scan_timestamp: str = Field(..., description="ISO8601 scan timestamp")
    target_path: str = Field(default="", description="Scanned path")
    issues: List[SecurityIssue] = Field(default_factory=list, description="Security issues found")
    vulnerabilities: List[Vulnerability] = Field(
        default_factory=list, description="Dependency vulnerabilities"
    )
    total_files_scanned: int = Field(default=0, description="Files scanned count")
    summary: Dict[str, int] = Field(default_factory=dict, description="Summary by severity")

    @property
    def has_critical(self) -> bool:
        """Check if any critical issues were found."""
        return any(
            i.severity == SecuritySeverity.CRITICAL
            for i in self.issues
        ) or any(
            v.severity == SecuritySeverity.CRITICAL
            for v in self.vulnerabilities
        )

    @property
    def has_issues(self) -> bool:
        """Check if any issues were found."""
        return len(self.issues) > 0 or len(self.vulnerabilities) > 0

    @property
    def total_issues(self) -> int:
        """Total count of all issues and vulnerabilities."""
        return len(self.issues) + len(self.vulnerabilities)

    def get_issues_by_severity(self, severity: SecuritySeverity) -> List[SecurityIssue]:
        """Get issues filtered by severity."""
        return [i for i in self.issues if i.severity == severity]

    def compute_summary(self) -> Dict[str, int]:
        """Compute summary statistics by severity."""
        summary: Dict[str, int] = {}
        for severity in SecuritySeverity:
            count = sum(1 for i in self.issues if i.severity == severity)
            count += sum(1 for v in self.vulnerabilities if v.severity == severity)
            if count > 0:
                summary[severity.value] = count
        self.summary = summary
        return summary
