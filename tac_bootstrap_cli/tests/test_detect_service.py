"""Tests for detect service.

Comprehensive unit tests for DetectService including language,
framework, package manager, and command detection.
"""

import json
import tempfile
from pathlib import Path

from tac_bootstrap.application.detect_service import DetectService
from tac_bootstrap.domain.models import Framework, Language, PackageManager

# ============================================================================
# TEST LANGUAGE DETECTION
# ============================================================================


class TestDetectServiceLanguage:
    """Tests for language detection."""

    def test_detect_python_by_pyproject_toml(self):
        """Should detect Python by pyproject.toml."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").write_text("[project]\nname='test'")
            result = detector.detect(Path(tmp))

            assert result.language == Language.PYTHON

    def test_detect_python_by_setup_py(self):
        """Should detect Python by setup.py."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "setup.py").write_text("from setuptools import setup")
            result = detector.detect(Path(tmp))

            assert result.language == Language.PYTHON

    def test_detect_python_by_requirements_txt(self):
        """Should detect Python by requirements.txt."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("fastapi==0.100.0")
            result = detector.detect(Path(tmp))

            assert result.language == Language.PYTHON

    def test_detect_typescript_by_tsconfig(self):
        """Should detect TypeScript by tsconfig.json."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "tsconfig.json").write_text("{}")
            result = detector.detect(Path(tmp))

            assert result.language == Language.TYPESCRIPT

    def test_detect_javascript_by_package_json(self):
        """Should detect JavaScript by package.json (without TypeScript)."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "package.json").write_text(json.dumps({"name": "test"}))
            result = detector.detect(Path(tmp))

            assert result.language == Language.JAVASCRIPT

    def test_detect_go_by_go_mod(self):
        """Should detect Go by go.mod."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "go.mod").write_text("module example.com/myapp\n\ngo 1.21")
            result = detector.detect(Path(tmp))

            assert result.language == Language.GO

    def test_detect_rust_by_cargo_toml(self):
        """Should detect Rust by Cargo.toml."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "Cargo.toml").write_text("[package]\nname = 'test'")
            result = detector.detect(Path(tmp))

            assert result.language == Language.RUST

    def test_detect_java_by_pom_xml(self):
        """Should detect Java by pom.xml."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pom.xml").write_text("<?xml version='1.0'?><project></project>")
            result = detector.detect(Path(tmp))

            assert result.language == Language.JAVA

    def test_detect_java_by_build_gradle(self):
        """Should detect Java by build.gradle."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "build.gradle").write_text("plugins { id 'java' }")
            result = detector.detect(Path(tmp))

            assert result.language == Language.JAVA


# ============================================================================
# TEST PACKAGE MANAGER DETECTION
# ============================================================================


class TestDetectServicePackageManager:
    """Tests for package manager detection."""

    def test_detect_uv_by_uv_lock(self):
        """Should detect UV by uv.lock."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").touch()
            (Path(tmp) / "uv.lock").write_text("# uv lock file")
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.UV

    def test_detect_poetry_by_poetry_lock(self):
        """Should detect Poetry by poetry.lock."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").touch()
            (Path(tmp) / "poetry.lock").write_text("# Poetry lock file")
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.POETRY

    def test_detect_pnpm_by_pnpm_lock(self):
        """Should detect pnpm by pnpm-lock.yaml."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "tsconfig.json").write_text("{}")  # Detect as TypeScript
            (Path(tmp) / "package.json").write_text("{}")
            (Path(tmp) / "pnpm-lock.yaml").write_text("lockfileVersion: 5.4")
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.PNPM

    def test_detect_yarn_by_yarn_lock(self):
        """Should detect Yarn by yarn.lock."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "tsconfig.json").write_text("{}")  # Detect as TypeScript
            (Path(tmp) / "package.json").write_text("{}")
            (Path(tmp) / "yarn.lock").write_text("# yarn lock file")
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.YARN

    def test_detect_npm_by_package_lock(self):
        """Should detect npm by package-lock.json."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "tsconfig.json").write_text("{}")  # Detect as TypeScript
            (Path(tmp) / "package.json").write_text("{}")
            (Path(tmp) / "package-lock.json").write_text("{}")
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.NPM

    def test_detect_bun_by_bun_lockb(self):
        """Should detect Bun by bun.lockb."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "tsconfig.json").write_text("{}")  # Detect as TypeScript
            (Path(tmp) / "package.json").write_text("{}")
            (Path(tmp) / "bun.lockb").write_bytes(b"bun lock")
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.BUN

    def test_detect_cargo_for_rust(self):
        """Should detect Cargo for Rust projects."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "Cargo.toml").write_text("[package]\nname = 'test'")
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.CARGO

    def test_detect_go_mod_for_go(self):
        """Should detect go mod for Go projects."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "go.mod").write_text("module test")
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.GO_MOD

    def test_detect_maven_by_pom_xml(self):
        """Should detect Maven by pom.xml."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pom.xml").write_text("<?xml version='1.0'?><project></project>")
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.MAVEN

    def test_detect_gradle_by_build_gradle(self):
        """Should detect Gradle by build.gradle."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "build.gradle").write_text("plugins { id 'java' }")
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.GRADLE


# ============================================================================
# TEST FRAMEWORK DETECTION
# ============================================================================


class TestDetectServiceFramework:
    """Tests for framework detection."""

    def test_detect_fastapi_from_pyproject(self):
        """Should detect FastAPI from pyproject.toml dependencies."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").write_text(
                "[project]\nname='test'\ndependencies=['fastapi>=0.100.0']"
            )
            result = detector.detect(Path(tmp))

            assert result.framework == Framework.FASTAPI

    def test_detect_django_from_requirements(self):
        """Should detect Django from requirements.txt."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("Django==4.2.0\npsycopg2-binary")
            result = detector.detect(Path(tmp))

            assert result.framework == Framework.DJANGO

    def test_detect_flask_from_requirements(self):
        """Should detect Flask from requirements.txt."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("Flask==2.3.0")
            result = detector.detect(Path(tmp))

            assert result.framework == Framework.FLASK

    def test_detect_nextjs_from_package_json(self):
        """Should detect Next.js from package.json."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "tsconfig.json").write_text("{}")
            (Path(tmp) / "package.json").write_text(
                json.dumps({"dependencies": {"next": "^14.0.0"}})
            )
            result = detector.detect(Path(tmp))

            assert result.framework == Framework.NEXTJS

    def test_detect_nestjs_from_package_json(self):
        """Should detect NestJS from package.json."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "tsconfig.json").write_text("{}")
            (Path(tmp) / "package.json").write_text(
                json.dumps({"dependencies": {"@nestjs/core": "^10.0.0"}})
            )
            result = detector.detect(Path(tmp))

            assert result.framework == Framework.NESTJS

    def test_detect_express_from_package_json(self):
        """Should detect Express from package.json."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "package.json").write_text(
                json.dumps({"dependencies": {"express": "^4.18.0"}})
            )
            result = detector.detect(Path(tmp))

            assert result.framework == Framework.EXPRESS

    def test_detect_react_from_package_json(self):
        """Should detect React from package.json."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "package.json").write_text(
                json.dumps({"dependencies": {"react": "^18.0.0"}})
            )
            result = detector.detect(Path(tmp))

            assert result.framework == Framework.REACT

    def test_detect_spring_from_pom_xml(self):
        """Should detect Spring from pom.xml."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pom.xml").write_text(
                "<?xml version='1.0'?><project>"
                "<dependencies><dependency>"
                "<artifactId>spring-boot-starter-web</artifactId>"
                "</dependency></dependencies></project>"
            )
            result = detector.detect(Path(tmp))

            assert result.framework == Framework.SPRING


# ============================================================================
# TEST APP ROOT DETECTION
# ============================================================================


class TestDetectServiceAppRoot:
    """Tests for app root detection."""

    def test_detect_src_directory(self):
        """Should detect src as app root."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").touch()
            (Path(tmp) / "src").mkdir()
            result = detector.detect(Path(tmp))

            assert result.app_root == "src"

    def test_detect_app_directory(self):
        """Should detect app as app root."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").touch()
            (Path(tmp) / "app").mkdir()
            result = detector.detect(Path(tmp))

            assert result.app_root == "app"

    def test_detect_lib_directory(self):
        """Should detect lib as app root."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").touch()
            (Path(tmp) / "lib").mkdir()
            result = detector.detect(Path(tmp))

            assert result.app_root == "lib"

    def test_no_app_root_returns_current_dir(self):
        """Should return current directory if no app root found."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").touch()
            result = detector.detect(Path(tmp))

            # Should be None or "."
            assert result.app_root in [None, "."]


# ============================================================================
# TEST COMMAND DETECTION
# ============================================================================


class TestDetectServiceCommands:
    """Tests for command detection."""

    def test_detect_commands_from_package_json_scripts(self):
        """Should detect commands from package.json scripts."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "package.json").write_text(
                json.dumps(
                    {
                        "scripts": {
                            "dev": "next dev",
                            "test": "jest",
                            "lint": "eslint .",
                            "build": "next build",
                        }
                    }
                )
            )
            result = detector.detect(Path(tmp))

            # Should have detected some commands
            assert "test" in result.commands or "start" in result.commands

    def test_detect_commands_for_python_uv(self):
        """Should provide default commands for Python + UV."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").write_text("[project]\nname='test'")
            (Path(tmp) / "uv.lock").touch()
            result = detector.detect(Path(tmp))

            # Commands should be populated (either detected or defaults)
            assert isinstance(result.commands, dict)


# ============================================================================
# TEST FULL DETECTION SCENARIOS
# ============================================================================


class TestDetectServiceFullScenarios:
    """Tests for complete detection scenarios."""

    def test_detect_python_fastapi_uv_project(self):
        """Should fully detect a Python FastAPI UV project."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").write_text(
                "[project]\nname='test'\ndependencies=['fastapi>=0.100.0']"
            )
            (Path(tmp) / "uv.lock").touch()
            (Path(tmp) / "src").mkdir()

            result = detector.detect(Path(tmp))

            assert result.language == Language.PYTHON
            assert result.package_manager == PackageManager.UV
            assert result.framework == Framework.FASTAPI
            assert result.app_root == "src"

    def test_detect_typescript_nextjs_pnpm_project(self):
        """Should fully detect a TypeScript Next.js pnpm project."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "tsconfig.json").write_text("{}")
            (Path(tmp) / "package.json").write_text(
                json.dumps(
                    {
                        "dependencies": {"next": "^14.0.0", "react": "^18.0.0"},
                        "scripts": {"dev": "next dev", "build": "next build"},
                    }
                )
            )
            (Path(tmp) / "pnpm-lock.yaml").touch()
            (Path(tmp) / "app").mkdir()

            result = detector.detect(Path(tmp))

            assert result.language == Language.TYPESCRIPT
            assert result.package_manager == PackageManager.PNPM
            assert result.framework == Framework.NEXTJS
            assert result.app_root == "app"

    def test_detect_go_project(self):
        """Should fully detect a Go project."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "go.mod").write_text("module example.com/app\n\ngo 1.21")
            (Path(tmp) / "main.go").write_text("package main")

            result = detector.detect(Path(tmp))

            assert result.language == Language.GO
            assert result.package_manager == PackageManager.GO_MOD

    def test_detect_rust_project(self):
        """Should fully detect a Rust project."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "Cargo.toml").write_text("[package]\nname = 'myapp'")
            (Path(tmp) / "src").mkdir()

            result = detector.detect(Path(tmp))

            assert result.language == Language.RUST
            assert result.package_manager == PackageManager.CARGO
            assert result.app_root == "src"

    def test_confidence_score(self):
        """Detection should include confidence score."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").touch()
            result = detector.detect(Path(tmp))

            assert 0.0 <= result.confidence <= 1.0
