"""
IDK: detect-service, auto-detection, tech-stack, language-detection, framework-detection
Responsibility: Auto-detects project technology stack from existing files
Invariants: Detection is read-only, never modifies files, returns confidence scores
"""

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from tac_bootstrap.domain.models import Framework, Language, PackageManager

# Python 3.11+ has tomllib builtin, 3.10 and below need tomli
if sys.version_info >= (3, 11):
    import tomllib  # type: ignore[import-not-found,unused-ignore]
else:
    try:
        import tomli as tomllib  # type: ignore[import-not-found,unused-ignore]
    except ImportError:
        tomllib = None  # type: ignore[assignment,unused-ignore]


@dataclass
class DetectedProject:
    """
    IDK: detection-result, confidence-scoring, tech-metadata
    Responsibility: Contains detected technology stack with confidence score
    Invariants: Confidence is between 0-1, language is always set, framework may be None
    """

    language: Language
    framework: Optional[Framework] = None
    package_manager: PackageManager = PackageManager.PIP
    app_root: Optional[str] = None
    commands: Dict[str, str] = field(default_factory=dict)
    confidence: float = 0.0


class DetectService:
    """
    IDK: stack-analysis, dependency-parsing, file-inspection
    Responsibility: Analyzes repository to identify language, framework, and commands
    Invariants: All detection methods are pure functions, defaults to Python if unknown
    """

    def detect(self, repo_path: Path) -> DetectedProject:
        """
        Detect project technology stack from repository.

        Args:
            repo_path: Path to repository root

        Returns:
            DetectedProject with all detected values
        """
        language = self._detect_language(repo_path)
        package_manager = self._detect_package_manager(repo_path, language)
        framework = self._detect_framework(repo_path, language)
        app_root = self._detect_app_root(repo_path, language)
        commands = self._detect_commands(repo_path, language, package_manager)

        return DetectedProject(
            language=language,
            framework=framework,
            package_manager=package_manager,
            app_root=app_root,
            commands=commands,
            confidence=0.8,  # TODO: calculate real confidence
        )

    def _detect_language(self, repo_path: Path) -> Language:
        """
        Detect programming language by checking for language-specific files.

        Args:
            repo_path: Path to repository root

        Returns:
            Detected Language (defaults to PYTHON if none found)
        """
        # Python detection
        python_files = [
            "pyproject.toml",
            "setup.py",
            "requirements.txt",
            "Pipfile",
            "poetry.lock",
            "uv.lock",
        ]
        if any((repo_path / file).exists() for file in python_files):
            return Language.PYTHON

        # TypeScript detection
        if (repo_path / "tsconfig.json").exists():
            return Language.TYPESCRIPT

        # JavaScript with TypeScript dependency
        pkg_json = self._read_package_json(repo_path)
        if pkg_json:
            deps = {**pkg_json.get("dependencies", {}), **pkg_json.get("devDependencies", {})}
            if "typescript" in deps:
                return Language.TYPESCRIPT
            return Language.JAVASCRIPT

        # Go detection
        if (repo_path / "go.mod").exists():
            return Language.GO

        # Rust detection
        if (repo_path / "Cargo.toml").exists():
            return Language.RUST

        # Java detection
        java_files = ["pom.xml", "build.gradle", "build.gradle.kts"]
        if any((repo_path / file).exists() for file in java_files):
            return Language.JAVA

        # Default
        return Language.PYTHON

    def _detect_package_manager(self, repo_path: Path, language: Language) -> PackageManager:
        """
        Detect package manager based on language and lock files.

        Args:
            repo_path: Path to repository root
            language: Detected programming language

        Returns:
            Detected PackageManager
        """
        if language == Language.PYTHON:
            if (repo_path / "uv.lock").exists() or (repo_path / ".python-version").exists():
                return PackageManager.UV
            if (repo_path / "poetry.lock").exists():
                return PackageManager.POETRY
            if (repo_path / "Pipfile.lock").exists():
                return PackageManager.PIPENV
            return PackageManager.PIP

        if language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            if (repo_path / "pnpm-lock.yaml").exists():
                return PackageManager.PNPM
            if (repo_path / "yarn.lock").exists():
                return PackageManager.YARN
            if (repo_path / "bun.lockb").exists():
                return PackageManager.BUN
            return PackageManager.NPM

        if language == Language.GO:
            return PackageManager.GO_MOD

        if language == Language.RUST:
            return PackageManager.CARGO

        if language == Language.JAVA:
            if (repo_path / "pom.xml").exists():
                return PackageManager.MAVEN
            return PackageManager.GRADLE

        return PackageManager.PIP

    def _detect_framework(self, repo_path: Path, language: Language) -> Optional[Framework]:
        """
        Detect web framework by analyzing dependencies.

        Args:
            repo_path: Path to repository root
            language: Detected programming language

        Returns:
            Detected Framework or None
        """
        # Python frameworks
        if language == Language.PYTHON:
            deps = self._get_python_deps(repo_path)
            if "fastapi" in deps:
                return Framework.FASTAPI
            if "django" in deps:
                return Framework.DJANGO
            if "flask" in deps:
                return Framework.FLASK

        # TypeScript/JavaScript frameworks
        if language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            pkg_json = self._read_package_json(repo_path)
            if pkg_json:
                js_deps: Dict[str, Any] = {
                    **pkg_json.get("dependencies", {}),
                    **pkg_json.get("devDependencies", {}),
                }
                if "next" in js_deps:
                    return Framework.NEXTJS
                if "@nestjs/core" in js_deps:
                    return Framework.NESTJS
                if "express" in js_deps:
                    return Framework.EXPRESS
                if "react" in js_deps:
                    return Framework.REACT
                if "vue" in js_deps:
                    return Framework.VUE

        # Go frameworks
        if language == Language.GO:
            go_mod_path = repo_path / "go.mod"
            if go_mod_path.exists():
                content = go_mod_path.read_text()
                if "gin-gonic/gin" in content:
                    return Framework.GIN
                if "labstack/echo" in content:
                    return Framework.ECHO

        # Rust frameworks
        if language == Language.RUST:
            cargo_path = repo_path / "Cargo.toml"
            if cargo_path.exists():
                content = cargo_path.read_text()
                if "axum" in content:
                    return Framework.AXUM
                if "actix" in content:
                    return Framework.ACTIX

        # Java frameworks
        if language == Language.JAVA:
            pom_path = repo_path / "pom.xml"
            if pom_path.exists():
                content = pom_path.read_text().lower()
                if "spring" in content:
                    return Framework.SPRING

        return Framework.NONE

    def _detect_app_root(self, repo_path: Path, language: Language) -> Optional[str]:
        """
        Detect application root directory.

        Args:
            repo_path: Path to repository root
            language: Detected programming language

        Returns:
            App root directory name or "."
        """
        # Check common root directories
        common_roots = ["src", "app", "lib"]
        for root in common_roots:
            if (repo_path / root).is_dir():
                return root

        # Python: look for directory with __init__.py
        if language == Language.PYTHON:
            try:
                for item in repo_path.iterdir():
                    if item.is_dir() and (item / "__init__.py").exists():
                        return item.name
            except (PermissionError, OSError):
                pass

        return "."

    def _detect_commands(
        self, repo_path: Path, language: Language, package_manager: PackageManager
    ) -> Dict[str, str]:
        """
        Detect existing project commands from configuration files.

        Args:
            repo_path: Path to repository root
            language: Detected programming language
            package_manager: Detected package manager

        Returns:
            Dictionary mapping command names to command strings
        """
        commands = {}

        # TypeScript/JavaScript commands from package.json
        if language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            pkg_json = self._read_package_json(repo_path)
            if pkg_json and "scripts" in pkg_json:
                scripts = pkg_json["scripts"]

                # Start/dev command
                if "start" in scripts:
                    commands["start"] = f"{package_manager.value} run start"
                elif "dev" in scripts:
                    commands["start"] = f"{package_manager.value} run dev"

                # Test command
                if "test" in scripts:
                    commands["test"] = f"{package_manager.value} test"

                # Lint command
                if "lint" in scripts:
                    commands["lint"] = f"{package_manager.value} run lint"

                # Build command
                if "build" in scripts:
                    commands["build"] = f"{package_manager.value} run build"

        # Python commands from pyproject.toml
        if language == Language.PYTHON:
            pyproject_path = repo_path / "pyproject.toml"
            if pyproject_path.exists() and tomllib is not None:
                try:
                    with open(pyproject_path, "rb") as f:
                        data = tomllib.load(f)
                        scripts = data.get("project", {}).get("scripts", {})
                        # Map common scripts if they exist
                        # Note: pyproject.toml scripts are entry points, not commands
                        # This is optional/limited functionality
                except Exception:
                    pass

        return commands

    def _read_package_json(self, repo_path: Path) -> Optional[Dict[str, Any]]:
        """
        Read and parse package.json file.

        Args:
            repo_path: Path to repository root

        Returns:
            Parsed package.json as dict, or None if not found/invalid
        """
        pkg_path = repo_path / "package.json"
        if not pkg_path.exists():
            return None

        try:
            result: Dict[str, Any] = json.loads(pkg_path.read_text())
            return result
        except json.JSONDecodeError:
            return None

    def _get_python_deps(self, repo_path: Path) -> List[str]:
        """
        Get list of Python dependencies from pyproject.toml and requirements.txt.

        Args:
            repo_path: Path to repository root

        Returns:
            List of dependency names (lowercase)
        """
        deps = []

        # Parse pyproject.toml
        pyproject_path = repo_path / "pyproject.toml"
        if pyproject_path.exists() and tomllib is not None:
            try:
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    project_deps = data.get("project", {}).get("dependencies", [])
                    for dep in project_deps:
                        # Extract package name from dependency spec
                        # Examples: "fastapi>=0.100.0" -> "fastapi"
                        #           "django[extra]" -> "django"
                        name = dep.split("[")[0].split(">=")[0].split("==")[0].strip().lower()
                        deps.append(name)
            except Exception:
                pass

        # Parse requirements.txt
        req_path = repo_path / "requirements.txt"
        if req_path.exists():
            try:
                for line in req_path.read_text().splitlines():
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith("#"):
                        continue
                    # Extract package name
                    name = line.split("[")[0].split(">=")[0].split("==")[0].strip().lower()
                    deps.append(name)
            except Exception:
                pass

        return deps
