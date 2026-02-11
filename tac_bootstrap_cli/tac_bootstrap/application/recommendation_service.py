"""
IDK: recommendation-service, smart-suggestions, security-check, dependency-update, pattern-detection
Responsibility: Provides intelligent suggestions for project improvements including missing components,
                performance issues, security vulnerabilities, and dependency updates
Invariants: Rule-based heuristics (no AI required), all checks are local, recommendations are
            prioritized by severity

Example usage:
    from tac_bootstrap.application.recommendation_service import RecommendationService

    service = RecommendationService()
    recommendations = service.analyze(Path("/my/project"))
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    """A single improvement recommendation."""

    id: str = Field(..., description="Unique recommendation identifier")
    category: str = Field(
        ...,
        description="Category: security, performance, structure, testing, dependency, pattern",
    )
    severity: str = Field(default="info", description="Severity: critical, warning, info")
    title: str = Field(..., description="Short recommendation title")
    description: str = Field(default="", description="Detailed description")
    suggestion: str = Field(default="", description="Actionable suggestion")
    file_path: Optional[str] = Field(default=None, description="Related file path")
    auto_fixable: bool = Field(default=False, description="Whether this can be auto-fixed")


class RecommendationReport(BaseModel):
    """Complete recommendation report for a project."""

    project_path: str = Field(default="", description="Analyzed project path")
    total: int = Field(default=0, description="Total recommendations")
    critical: int = Field(default=0, description="Number of critical items")
    warnings: int = Field(default=0, description="Number of warnings")
    info: int = Field(default=0, description="Number of info items")
    recommendations: List[Recommendation] = Field(
        default_factory=list, description="List of recommendations"
    )
    categories: Dict[str, int] = Field(
        default_factory=dict, description="Count by category"
    )


class RecommendationService:
    """
    IDK: recommendation-core, rule-engine, heuristic-analysis, security-scanner
    Responsibility: Analyzes project structure and code for improvement opportunities
    Invariants: All analysis is local, rules are deterministic, no file modification
    """

    # Directories to skip
    SKIP_DIRS = {
        ".git", "__pycache__", "node_modules", ".venv", "venv",
        "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
        "trees",
    }

    # Known security patterns to detect
    SECURITY_PATTERNS = [
        {
            "pattern": r"password\s*=\s*['\"][^'\"]+['\"]",
            "id": "sec-hardcoded-password",
            "title": "Hardcoded password detected",
            "severity": "critical",
            "suggestion": "Use environment variables or a secret manager for passwords",
        },
        {
            "pattern": r"api[_-]?key\s*=\s*['\"][A-Za-z0-9]{20,}['\"]",
            "id": "sec-hardcoded-api-key",
            "title": "Hardcoded API key detected",
            "severity": "critical",
            "suggestion": "Move API keys to .env file and use os.environ",
        },
        {
            "pattern": r"secret[_-]?key\s*=\s*['\"][^'\"]+['\"]",
            "id": "sec-hardcoded-secret",
            "title": "Hardcoded secret key detected",
            "severity": "critical",
            "suggestion": "Use environment variables for secret keys",
        },
        {
            "pattern": r"eval\s*\(",
            "id": "sec-eval-usage",
            "title": "Use of eval() detected",
            "severity": "warning",
            "suggestion": "Avoid eval() as it can execute arbitrary code. Use ast.literal_eval() for safe evaluation",
        },
        {
            "pattern": r"pickle\.loads?\s*\(",
            "id": "sec-pickle-usage",
            "title": "Use of pickle detected",
            "severity": "warning",
            "suggestion": "Pickle can execute arbitrary code during deserialization. Consider using JSON or msgpack",
        },
        {
            "pattern": r"subprocess\.(call|run|Popen)\s*\([^)]*shell\s*=\s*True",
            "id": "sec-shell-injection",
            "title": "Shell injection risk",
            "severity": "warning",
            "suggestion": "Avoid shell=True with user input. Use list arguments instead",
        },
    ]

    # Structure recommendations
    EXPECTED_FILES = [
        {
            "path": "config.yml",
            "id": "struct-config",
            "title": "Missing config.yml",
            "suggestion": "Run 'tac-bootstrap add-agentic' to create configuration",
        },
        {
            "path": "README.md",
            "id": "struct-readme",
            "title": "Missing README.md",
            "suggestion": "Add a README.md to document your project",
        },
        {
            "path": ".gitignore",
            "id": "struct-gitignore",
            "title": "Missing .gitignore",
            "suggestion": "Add a .gitignore to prevent committing unwanted files",
        },
    ]

    EXPECTED_DIRS = [
        {
            "path": ".claude",
            "id": "struct-claude",
            "title": "Missing .claude/ directory",
            "suggestion": "Run 'tac-bootstrap add-agentic' to set up the Agentic Layer",
        },
        {
            "path": "adws",
            "id": "struct-adws",
            "title": "Missing adws/ directory",
            "suggestion": "Run 'tac-bootstrap add-agentic' to add AI Developer Workflows",
        },
    ]

    def _should_skip(self, path: Path) -> bool:
        """Check if a path should be skipped during analysis."""
        return any(part in self.SKIP_DIRS for part in path.parts)

    def check_security(self, project_path: Path) -> List[Recommendation]:
        """Check for security vulnerabilities in source code.

        Args:
            project_path: Path to the project root

        Returns:
            List of security-related recommendations
        """
        recommendations: List[Recommendation] = []
        seen_ids: set = set()

        for file_path in project_path.rglob("*.py"):
            if self._should_skip(file_path.relative_to(project_path)):
                continue
            try:
                content = file_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            for pattern_info in self.SECURITY_PATTERNS:
                matches = re.findall(pattern_info["pattern"], content, re.IGNORECASE)
                if matches:
                    rec_id = f"{pattern_info['id']}-{file_path.name}"
                    if rec_id not in seen_ids:
                        seen_ids.add(rec_id)
                        recommendations.append(
                            Recommendation(
                                id=rec_id,
                                category="security",
                                severity=pattern_info["severity"],
                                title=pattern_info["title"],
                                description=f"Found in {file_path.relative_to(project_path)}",
                                suggestion=pattern_info["suggestion"],
                                file_path=str(file_path.relative_to(project_path)),
                            )
                        )

        # Check for .env in git
        env_file = project_path / ".env"
        gitignore = project_path / ".gitignore"
        if env_file.exists():
            env_ignored = False
            if gitignore.exists():
                try:
                    gitignore_content = gitignore.read_text()
                    env_ignored = ".env" in gitignore_content
                except OSError:
                    pass
            if not env_ignored:
                recommendations.append(
                    Recommendation(
                        id="sec-env-not-ignored",
                        category="security",
                        severity="critical",
                        title=".env file not in .gitignore",
                        description="The .env file may contain secrets and should not be committed",
                        suggestion="Add '.env' to .gitignore",
                        file_path=".gitignore",
                        auto_fixable=True,
                    )
                )

        return recommendations

    def check_structure(self, project_path: Path) -> List[Recommendation]:
        """Check for missing project structure components.

        Args:
            project_path: Path to the project root

        Returns:
            List of structure-related recommendations
        """
        recommendations: List[Recommendation] = []

        for expected in self.EXPECTED_FILES:
            if not (project_path / expected["path"]).exists():
                recommendations.append(
                    Recommendation(
                        id=expected["id"],
                        category="structure",
                        severity="info",
                        title=expected["title"],
                        suggestion=expected["suggestion"],
                    )
                )

        for expected in self.EXPECTED_DIRS:
            if not (project_path / expected["path"]).is_dir():
                recommendations.append(
                    Recommendation(
                        id=expected["id"],
                        category="structure",
                        severity="info",
                        title=expected["title"],
                        suggestion=expected["suggestion"],
                    )
                )

        return recommendations

    def check_testing(self, project_path: Path) -> List[Recommendation]:
        """Check testing coverage and quality.

        Args:
            project_path: Path to the project root

        Returns:
            List of testing-related recommendations
        """
        recommendations: List[Recommendation] = []

        # Count source and test files
        source_files = []
        test_files = []
        for f in project_path.rglob("*.py"):
            rel = f.relative_to(project_path)
            if self._should_skip(rel):
                continue
            if f.name.startswith("test_") or f.name.endswith("_test.py"):
                test_files.append(f)
            elif f.name != "__init__.py" and not f.name.startswith("."):
                source_files.append(f)

        if not test_files:
            recommendations.append(
                Recommendation(
                    id="test-no-tests",
                    category="testing",
                    severity="warning",
                    title="No test files found",
                    description="A project without tests is harder to maintain and refactor safely",
                    suggestion="Create test files following the pattern test_*.py",
                )
            )
        elif len(test_files) < len(source_files) * 0.3:
            recommendations.append(
                Recommendation(
                    id="test-low-coverage",
                    category="testing",
                    severity="info",
                    title="Low test file count relative to source files",
                    description=f"Found {len(test_files)} test files for {len(source_files)} source files",
                    suggestion="Aim for at least one test file per source module",
                )
            )

        # Check for test configuration
        if not any(
            (project_path / f).exists()
            for f in ("pytest.ini", "setup.cfg", "pyproject.toml", "tox.ini")
        ):
            recommendations.append(
                Recommendation(
                    id="test-no-config",
                    category="testing",
                    severity="info",
                    title="No test configuration found",
                    description="Configure pytest in pyproject.toml for consistent test execution",
                    suggestion="Add [tool.pytest.ini_options] to pyproject.toml",
                )
            )

        return recommendations

    def check_performance(self, project_path: Path) -> List[Recommendation]:
        """Check for performance improvement opportunities.

        Args:
            project_path: Path to the project root

        Returns:
            List of performance-related recommendations
        """
        recommendations: List[Recommendation] = []

        for file_path in project_path.rglob("*.py"):
            if self._should_skip(file_path.relative_to(project_path)):
                continue
            try:
                content = file_path.read_text(encoding="utf-8")
                lines = content.splitlines()
            except (OSError, UnicodeDecodeError):
                continue

            rel_path = str(file_path.relative_to(project_path))

            # Check for large files
            if len(lines) > 500:
                recommendations.append(
                    Recommendation(
                        id=f"perf-large-file-{file_path.name}",
                        category="performance",
                        severity="info",
                        title=f"Large file: {rel_path} ({len(lines)} lines)",
                        description="Large files are harder to maintain and may indicate a need to split",
                        suggestion="Consider breaking into smaller, focused modules",
                        file_path=rel_path,
                    )
                )

            # Check for star imports
            if re.search(r"from\s+\S+\s+import\s+\*", content):
                recommendations.append(
                    Recommendation(
                        id=f"perf-star-import-{file_path.name}",
                        category="pattern",
                        severity="info",
                        title=f"Star import in {rel_path}",
                        description="Star imports can slow startup and cause namespace pollution",
                        suggestion="Import specific names instead of using import *",
                        file_path=rel_path,
                    )
                )

        return recommendations

    def check_dependencies(self, project_path: Path) -> List[Recommendation]:
        """Check for dependency-related recommendations.

        Args:
            project_path: Path to the project root

        Returns:
            List of dependency-related recommendations
        """
        recommendations: List[Recommendation] = []

        # Check for unpinned dependencies
        pyproject = project_path / "pyproject.toml"
        if pyproject.exists():
            try:
                content = pyproject.read_text()
                # Look for dependencies without version constraints
                in_deps = False
                for line in content.splitlines():
                    stripped = line.strip()
                    if "dependencies" in stripped and not "dev" in stripped.lower():
                        in_deps = True
                        continue
                    if stripped.startswith("[") and not stripped.startswith('["'):
                        in_deps = False
                        continue
                    if in_deps and stripped.startswith('"'):
                        dep = stripped.strip('",')
                        if dep and ">=" not in dep and "==" not in dep and "<" not in dep:
                            recommendations.append(
                                Recommendation(
                                    id=f"dep-unpinned-{dep}",
                                    category="dependency",
                                    severity="info",
                                    title=f"Unpinned dependency: {dep}",
                                    description="Unpinned dependencies can cause unexpected breaking changes",
                                    suggestion=f"Pin version: {dep}>=X.Y.Z",
                                    file_path="pyproject.toml",
                                )
                            )
            except OSError:
                pass

        return recommendations

    def analyze(self, project_path: Path) -> RecommendationReport:
        """Run all checks and generate a comprehensive recommendation report.

        Args:
            project_path: Path to the project root

        Returns:
            RecommendationReport with all recommendations
        """
        project_path = project_path.resolve()
        all_recommendations: List[Recommendation] = []

        all_recommendations.extend(self.check_security(project_path))
        all_recommendations.extend(self.check_structure(project_path))
        all_recommendations.extend(self.check_testing(project_path))
        all_recommendations.extend(self.check_performance(project_path))
        all_recommendations.extend(self.check_dependencies(project_path))

        # Sort by severity (critical first)
        severity_order = {"critical": 0, "warning": 1, "info": 2}
        all_recommendations.sort(key=lambda r: severity_order.get(r.severity, 3))

        # Count by category
        categories: Dict[str, int] = {}
        for rec in all_recommendations:
            categories[rec.category] = categories.get(rec.category, 0) + 1

        return RecommendationReport(
            project_path=str(project_path),
            total=len(all_recommendations),
            critical=sum(1 for r in all_recommendations if r.severity == "critical"),
            warnings=sum(1 for r in all_recommendations if r.severity == "warning"),
            info=sum(1 for r in all_recommendations if r.severity == "info"),
            recommendations=all_recommendations,
            categories=categories,
        )
