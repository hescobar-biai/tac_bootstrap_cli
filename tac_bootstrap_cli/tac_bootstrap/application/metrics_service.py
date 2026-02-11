"""
IDK: metrics-service, code-analysis, project-health, complexity-metrics, coverage-tracking
Responsibility: Analyzes project code to generate complexity, coverage, dependency, and health metrics
Invariants: All analysis is local (no network), metrics are JSON-serializable,
            supports Python/TypeScript projects, health score is 0-100

Example usage:
    from tac_bootstrap.application.metrics_service import MetricsService

    service = MetricsService()
    metrics = service.generate_metrics(Path("/my/project"))
    complexity = service.get_complexity_metrics(Path("/my/project"))
    health = service.calculate_health_score(Path("/my/project"))
"""

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class FileMetrics(BaseModel):
    """Metrics for a single file."""

    path: str = Field(..., description="Relative file path")
    lines_of_code: int = Field(default=0, description="Lines of code (excluding blanks/comments)")
    blank_lines: int = Field(default=0, description="Number of blank lines")
    comment_lines: int = Field(default=0, description="Number of comment lines")
    total_lines: int = Field(default=0, description="Total line count")
    functions: int = Field(default=0, description="Number of functions/methods")
    classes: int = Field(default=0, description="Number of classes")
    imports: int = Field(default=0, description="Number of import statements")
    complexity_score: float = Field(default=0.0, description="Estimated cyclomatic complexity")


class ComplexityMetrics(BaseModel):
    """Code complexity analysis results."""

    total_files: int = Field(default=0, description="Total files analyzed")
    total_lines: int = Field(default=0, description="Total lines of code")
    total_functions: int = Field(default=0, description="Total functions/methods")
    total_classes: int = Field(default=0, description="Total classes")
    average_file_length: float = Field(default=0.0, description="Average lines per file")
    average_complexity: float = Field(default=0.0, description="Average complexity score")
    most_complex_files: List[FileMetrics] = Field(
        default_factory=list, description="Top 10 most complex files"
    )
    file_metrics: List[FileMetrics] = Field(
        default_factory=list, description="Metrics for all analyzed files"
    )


class DependencyMetrics(BaseModel):
    """Dependency analysis results."""

    total_dependencies: int = Field(default=0, description="Total dependencies")
    direct_dependencies: int = Field(default=0, description="Direct dependencies")
    dev_dependencies: int = Field(default=0, description="Development dependencies")
    dependency_list: List[Dict[str, str]] = Field(
        default_factory=list, description="List of dependencies with versions"
    )


class ProjectMetrics(BaseModel):
    """Complete project metrics."""

    project_name: str = Field(default="", description="Project name")
    project_path: str = Field(default="", description="Project path")
    generated_at: str = Field(default="", description="ISO 8601 generation timestamp")
    complexity: ComplexityMetrics = Field(
        default_factory=ComplexityMetrics, description="Code complexity metrics"
    )
    dependencies: DependencyMetrics = Field(
        default_factory=DependencyMetrics, description="Dependency metrics"
    )
    health_score: float = Field(default=0.0, description="Overall health score (0-100)")
    health_grade: str = Field(default="", description="Letter grade (A-F)")
    has_tests: bool = Field(default=False, description="Whether project has test files")
    has_ci: bool = Field(default=False, description="Whether project has CI configuration")
    has_docs: bool = Field(default=False, description="Whether project has documentation")
    has_config: bool = Field(default=False, description="Whether project has config.yml")
    test_file_count: int = Field(default=0, description="Number of test files")
    source_file_count: int = Field(default=0, description="Number of source files")
    language_distribution: Dict[str, int] = Field(
        default_factory=dict, description="File count by language/extension"
    )
    recommendations: List[str] = Field(
        default_factory=list, description="Health improvement recommendations"
    )


class MetricsHistory(BaseModel):
    """Historical metrics tracking."""

    entries: List[Dict[str, Any]] = Field(default_factory=list, description="Historical entries")


class MetricsService:
    """
    IDK: metrics-core, code-analyzer, health-calculator, complexity-engine
    Responsibility: Analyzes project source code and generates comprehensive metrics
    Invariants: All analysis is local, no file modification, metrics are deterministic
    """

    # File extensions to analyze by language
    LANGUAGE_EXTENSIONS: Dict[str, List[str]] = {
        "python": [".py"],
        "typescript": [".ts", ".tsx"],
        "javascript": [".js", ".jsx"],
        "go": [".go"],
        "rust": [".rs"],
        "java": [".java"],
    }

    # Directories to skip during analysis
    SKIP_DIRS = {
        ".git", "__pycache__", "node_modules", ".venv", "venv",
        "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
        ".ruff_cache", "trees", ".next", ".nuxt",
    }

    def __init__(self, history_dir: Optional[Path] = None) -> None:
        """Initialize metrics service.

        Args:
            history_dir: Directory for metrics history storage.
                        Defaults to ~/.tac-bootstrap/metrics/
        """
        self._history_dir = history_dir or (Path.home() / ".tac-bootstrap" / "metrics")

    def _should_analyze(self, path: Path) -> bool:
        """Check if a file should be analyzed.

        Args:
            path: File path to check

        Returns:
            True if the file should be analyzed
        """
        for part in path.parts:
            if part in self.SKIP_DIRS:
                return False
        return path.suffix in {ext for exts in self.LANGUAGE_EXTENSIONS.values() for ext in exts}

    def _analyze_file(self, file_path: Path, project_root: Path) -> FileMetrics:
        """Analyze a single file for metrics.

        Args:
            file_path: Absolute path to the file
            project_root: Project root for relative path calculation

        Returns:
            FileMetrics for the file
        """
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return FileMetrics(path=str(file_path.relative_to(project_root)))

        lines = content.splitlines()
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = 0
        code_lines = 0
        functions = 0
        classes = 0
        imports = 0
        complexity = 0

        in_multiline_comment = False

        for line in lines:
            stripped = line.strip()

            # Python comments
            if file_path.suffix == ".py":
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    if in_multiline_comment:
                        in_multiline_comment = False
                        comment_lines += 1
                        continue
                    elif stripped.count('"""') >= 2 or stripped.count("'''") >= 2:
                        comment_lines += 1
                        continue
                    else:
                        in_multiline_comment = True
                        comment_lines += 1
                        continue

                if in_multiline_comment:
                    comment_lines += 1
                    continue

                if stripped.startswith("#"):
                    comment_lines += 1
                    continue

                if stripped.startswith("def ") or stripped.startswith("async def "):
                    functions += 1
                if stripped.startswith("class "):
                    classes += 1
                if stripped.startswith("import ") or stripped.startswith("from "):
                    imports += 1

                # Complexity indicators
                if any(
                    stripped.startswith(kw)
                    for kw in ("if ", "elif ", "for ", "while ", "except ", "with ")
                ):
                    complexity += 1

            # TypeScript/JavaScript comments
            elif file_path.suffix in (".ts", ".tsx", ".js", ".jsx"):
                if "/*" in stripped:
                    in_multiline_comment = True
                if in_multiline_comment:
                    comment_lines += 1
                    if "*/" in stripped:
                        in_multiline_comment = False
                    continue
                if stripped.startswith("//"):
                    comment_lines += 1
                    continue
                if re.match(r"(export\s+)?(async\s+)?function\s+", stripped):
                    functions += 1
                if re.match(r"(export\s+)?class\s+", stripped):
                    classes += 1
                if stripped.startswith("import "):
                    imports += 1
                if any(
                    stripped.startswith(kw)
                    for kw in ("if ", "else if ", "for ", "while ", "catch ", "switch ")
                ):
                    complexity += 1

            if stripped and not stripped.startswith("#") and not stripped.startswith("//"):
                code_lines += 1

        return FileMetrics(
            path=str(file_path.relative_to(project_root)),
            lines_of_code=code_lines,
            blank_lines=blank_lines,
            comment_lines=comment_lines,
            total_lines=total_lines,
            functions=functions,
            classes=classes,
            imports=imports,
            complexity_score=float(complexity),
        )

    def get_complexity_metrics(self, project_path: Path) -> ComplexityMetrics:
        """Analyze code complexity for a project.

        Args:
            project_path: Path to the project root

        Returns:
            ComplexityMetrics with analysis results
        """
        project_path = project_path.resolve()
        file_metrics: List[FileMetrics] = []

        for file_path in project_path.rglob("*"):
            if file_path.is_file() and self._should_analyze(file_path.relative_to(project_path)):
                metrics = self._analyze_file(file_path, project_path)
                file_metrics.append(metrics)

        if not file_metrics:
            return ComplexityMetrics()

        total_lines = sum(m.total_lines for m in file_metrics)
        total_functions = sum(m.functions for m in file_metrics)
        total_classes = sum(m.classes for m in file_metrics)
        avg_length = total_lines / len(file_metrics) if file_metrics else 0
        avg_complexity = (
            sum(m.complexity_score for m in file_metrics) / len(file_metrics)
            if file_metrics
            else 0
        )

        # Sort by complexity for top files
        sorted_by_complexity = sorted(
            file_metrics, key=lambda m: m.complexity_score, reverse=True
        )

        return ComplexityMetrics(
            total_files=len(file_metrics),
            total_lines=total_lines,
            total_functions=total_functions,
            total_classes=total_classes,
            average_file_length=round(avg_length, 1),
            average_complexity=round(avg_complexity, 2),
            most_complex_files=sorted_by_complexity[:10],
            file_metrics=file_metrics,
        )

    def get_dependency_metrics(self, project_path: Path) -> DependencyMetrics:
        """Analyze project dependencies.

        Args:
            project_path: Path to the project root

        Returns:
            DependencyMetrics with dependency information
        """
        project_path = project_path.resolve()
        deps: List[Dict[str, str]] = []
        dev_deps: List[Dict[str, str]] = []

        # Check pyproject.toml
        pyproject = project_path / "pyproject.toml"
        if pyproject.exists():
            try:
                content = pyproject.read_text()
                # Simple parsing for dependencies
                in_deps = False
                in_dev_deps = False
                for line in content.splitlines():
                    stripped = line.strip()
                    if stripped.startswith("dependencies"):
                        in_deps = True
                        in_dev_deps = False
                        continue
                    if "dev" in stripped.lower() and "dependencies" in stripped.lower():
                        in_dev_deps = True
                        in_deps = False
                        continue
                    if stripped.startswith("[") and not stripped.startswith('["'):
                        in_deps = False
                        in_dev_deps = False
                        continue
                    if stripped.startswith('"') and (in_deps or in_dev_deps):
                        dep = stripped.strip('",').strip()
                        if dep:
                            entry = {"name": dep.split(">=")[0].split("==")[0].split("<")[0].strip(), "spec": dep}
                            if in_dev_deps:
                                dev_deps.append(entry)
                            else:
                                deps.append(entry)
            except OSError:
                pass

        # Check package.json
        package_json = project_path / "package.json"
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                for name, version in data.get("dependencies", {}).items():
                    deps.append({"name": name, "spec": f"{name}@{version}"})
                for name, version in data.get("devDependencies", {}).items():
                    dev_deps.append({"name": name, "spec": f"{name}@{version}"})
            except (json.JSONDecodeError, OSError):
                pass

        all_deps = deps + dev_deps
        return DependencyMetrics(
            total_dependencies=len(all_deps),
            direct_dependencies=len(deps),
            dev_dependencies=len(dev_deps),
            dependency_list=all_deps,
        )

    def calculate_health_score(self, project_path: Path) -> float:
        """Calculate overall project health score (0-100).

        Factors:
        - Has tests (20 points)
        - Has CI/CD (10 points)
        - Has documentation (10 points)
        - Has config.yml (10 points)
        - Code complexity is reasonable (20 points)
        - Has type hints / lint config (10 points)
        - Has proper structure (20 points)

        Args:
            project_path: Path to the project root

        Returns:
            Health score between 0 and 100
        """
        project_path = project_path.resolve()
        score = 0.0

        # Has tests (20 points)
        test_files = list(project_path.rglob("test_*.py")) + list(project_path.rglob("*.test.ts"))
        test_files = [f for f in test_files if not any(s in str(f) for s in self.SKIP_DIRS)]
        if test_files:
            score += min(20.0, len(test_files) * 2.0)

        # Has CI/CD (10 points)
        ci_files = [
            project_path / ".github" / "workflows",
            project_path / ".gitlab-ci.yml",
            project_path / "Jenkinsfile",
            project_path / ".circleci",
        ]
        if any(p.exists() for p in ci_files):
            score += 10.0

        # Has documentation (10 points)
        doc_files = [
            project_path / "README.md",
            project_path / "docs",
            project_path / "ai_docs",
        ]
        if any(p.exists() for p in doc_files):
            score += 10.0

        # Has config.yml (10 points)
        if (project_path / "config.yml").exists():
            score += 10.0

        # Code complexity (20 points - higher for lower complexity)
        complexity = self.get_complexity_metrics(project_path)
        if complexity.total_files > 0:
            avg_complexity = complexity.average_complexity
            if avg_complexity < 5:
                score += 20.0
            elif avg_complexity < 10:
                score += 15.0
            elif avg_complexity < 20:
                score += 10.0
            else:
                score += 5.0

        # Has lint/type config (10 points)
        lint_configs = [
            project_path / "pyproject.toml",
            project_path / ".eslintrc.json",
            project_path / ".eslintrc.js",
            project_path / "tsconfig.json",
            project_path / "ruff.toml",
        ]
        if any(p.exists() for p in lint_configs):
            score += 10.0

        # Proper structure (20 points)
        structure_indicators = [
            project_path / ".claude",
            project_path / "adws",
            project_path / "scripts",
            project_path / "src",
        ]
        structure_score = sum(5.0 for p in structure_indicators if p.exists())
        score += min(20.0, structure_score)

        return min(100.0, round(score, 1))

    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade.

        Args:
            score: Health score (0-100)

        Returns:
            Letter grade (A+, A, B+, B, C+, C, D, F)
        """
        if score >= 95:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 75:
            return "B+"
        elif score >= 65:
            return "B"
        elif score >= 55:
            return "C+"
        elif score >= 45:
            return "C"
        elif score >= 35:
            return "D"
        return "F"

    def generate_metrics(self, project_path: Path) -> ProjectMetrics:
        """Generate comprehensive project metrics.

        Args:
            project_path: Path to the project root

        Returns:
            ProjectMetrics with all analysis results
        """
        project_path = project_path.resolve()

        complexity = self.get_complexity_metrics(project_path)
        dependencies = self.get_dependency_metrics(project_path)
        health_score = self.calculate_health_score(project_path)
        health_grade = self._score_to_grade(health_score)

        # Count files by extension
        lang_dist: Dict[str, int] = {}
        for fm in complexity.file_metrics:
            ext = Path(fm.path).suffix
            lang_dist[ext] = lang_dist.get(ext, 0) + 1

        # Check for various project features
        test_files = [
            f for f in project_path.rglob("test_*.py")
            if not any(s in str(f) for s in self.SKIP_DIRS)
        ]

        # Generate recommendations
        recommendations = self._generate_recommendations(
            project_path, complexity, health_score
        )

        return ProjectMetrics(
            project_name=project_path.name,
            project_path=str(project_path),
            generated_at=datetime.now(timezone.utc).isoformat(),
            complexity=complexity,
            dependencies=dependencies,
            health_score=health_score,
            health_grade=health_grade,
            has_tests=len(test_files) > 0,
            has_ci=(project_path / ".github" / "workflows").exists(),
            has_docs=(project_path / "README.md").exists(),
            has_config=(project_path / "config.yml").exists(),
            test_file_count=len(test_files),
            source_file_count=complexity.total_files,
            language_distribution=lang_dist,
            recommendations=recommendations,
        )

    def _generate_recommendations(
        self,
        project_path: Path,
        complexity: ComplexityMetrics,
        health_score: float,
    ) -> List[str]:
        """Generate improvement recommendations based on metrics.

        Args:
            project_path: Project path
            complexity: Complexity metrics
            health_score: Current health score

        Returns:
            List of recommendation strings
        """
        recommendations: List[str] = []

        if not (project_path / "config.yml").exists():
            recommendations.append(
                "Add config.yml: Run 'tac-bootstrap add-agentic' to set up the Agentic Layer"
            )

        test_files = list(project_path.rglob("test_*.py"))
        test_files = [f for f in test_files if not any(s in str(f) for s in self.SKIP_DIRS)]
        if not test_files:
            recommendations.append(
                "Add tests: Create test files to improve code quality and health score"
            )

        if not (project_path / "README.md").exists():
            recommendations.append(
                "Add README.md: Document your project for better maintainability"
            )

        if not (project_path / ".github" / "workflows").exists():
            recommendations.append(
                "Add CI/CD: Set up GitHub Actions or similar for automated testing"
            )

        if complexity.average_complexity > 15:
            recommendations.append(
                "Reduce complexity: Consider refactoring files with high complexity scores"
            )

        if complexity.average_file_length > 300:
            recommendations.append(
                "Split large files: Average file length is high; consider breaking into smaller modules"
            )

        for fm in complexity.most_complex_files[:3]:
            if fm.complexity_score > 20:
                recommendations.append(
                    f"Refactor {fm.path}: Complexity score of {fm.complexity_score} is high"
                )

        return recommendations

    def save_metrics_history(self, project_path: Path, metrics: ProjectMetrics) -> None:
        """Save metrics to history for trend tracking.

        Args:
            project_path: Project path
            metrics: Metrics to save
        """
        import hashlib

        path_hash = hashlib.sha256(str(project_path.resolve()).encode()).hexdigest()[:12]
        history_file = self._history_dir / f"{path_hash}.json"
        history_file.parent.mkdir(parents=True, exist_ok=True)

        history = MetricsHistory()
        if history_file.exists():
            try:
                data = json.loads(history_file.read_text())
                history = MetricsHistory(**data)
            except Exception:
                pass

        entry = {
            "timestamp": metrics.generated_at,
            "health_score": metrics.health_score,
            "health_grade": metrics.health_grade,
            "total_files": metrics.source_file_count,
            "total_lines": metrics.complexity.total_lines,
            "avg_complexity": metrics.complexity.average_complexity,
            "test_files": metrics.test_file_count,
        }
        history.entries.append(entry)

        # Keep last 100 entries
        if len(history.entries) > 100:
            history.entries = history.entries[-100:]

        history_file.write_text(history.model_dump_json(indent=2))

    def get_metrics_history(self, project_path: Path, days: int = 30) -> List[Dict[str, Any]]:
        """Get metrics history for a project.

        Args:
            project_path: Project path
            days: Number of days of history to return

        Returns:
            List of historical metric entries
        """
        import hashlib

        path_hash = hashlib.sha256(str(project_path.resolve()).encode()).hexdigest()[:12]
        history_file = self._history_dir / f"{path_hash}.json"

        if not history_file.exists():
            return []

        try:
            data = json.loads(history_file.read_text())
            history = MetricsHistory(**data)
            return history.entries
        except Exception:
            return []
