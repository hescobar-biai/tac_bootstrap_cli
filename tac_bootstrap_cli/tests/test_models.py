"""Tests for domain models.

Comprehensive unit tests for Pydantic models, enums, validators,
and helper functions in the domain layer.
"""

import pytest

from tac_bootstrap.domain.models import (
    Architecture,
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Framework,
    Language,
    PackageManager,
    PathsSpec,
    ProjectSpec,
    TACConfig,
    get_default_commands,
    get_frameworks_for_language,
    get_package_managers_for_language,
)

# ============================================================================
# TEST PROJECT SPEC
# ============================================================================


class TestProjectSpec:
    """Tests for ProjectSpec model."""

    def test_name_sanitization_whitespace(self):
        """Project name should strip whitespace."""
        spec = ProjectSpec(
            name="  my-project  ",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        )
        assert spec.name == "my-project"

    def test_name_sanitization_spaces_to_hyphens(self):
        """Project name should replace spaces with hyphens."""
        spec = ProjectSpec(
            name="My Project Name",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        )
        assert spec.name == "my-project-name"

    def test_name_sanitization_lowercase(self):
        """Project name should be converted to lowercase."""
        spec = ProjectSpec(
            name="MyProject",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        )
        assert spec.name == "myproject"

    def test_name_sanitization_combined(self):
        """Project name should handle all sanitization rules together."""
        spec = ProjectSpec(
            name="  My Test App  ",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        )
        assert spec.name == "my-test-app"

    def test_empty_name_raises(self):
        """Empty name should raise ValueError."""
        with pytest.raises(ValueError, match="Project name cannot be empty"):
            ProjectSpec(
                name="",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            )

    def test_whitespace_only_name_raises(self):
        """Whitespace-only name should raise ValueError."""
        with pytest.raises(ValueError, match="Project name cannot be empty"):
            ProjectSpec(
                name="   ",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            )

    def test_default_framework(self):
        """Framework should default to NONE."""
        spec = ProjectSpec(
            name="test",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        )
        assert spec.framework == Framework.NONE

    def test_default_architecture(self):
        """Architecture should default to SIMPLE."""
        spec = ProjectSpec(
            name="test",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        )
        assert spec.architecture == Architecture.SIMPLE


# ============================================================================
# TEST TAC CONFIG
# ============================================================================


class TestTACConfig:
    """Tests for TACConfig model."""

    def test_minimal_config(self):
        """Minimal config should have defaults."""
        config = TACConfig(
            project=ProjectSpec(
                name="test",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="echo start", test="echo test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test")),
        )
        assert config.schema_version == 1
        assert config.paths.adws_dir == "adws"
        assert config.paths.specs_dir == "specs"
        assert config.paths.prompts_dir == "prompts"
        assert config.paths.logs_dir == "logs"

    def test_agentic_provider_default(self):
        """Agentic provider should default to claude_code."""
        config = TACConfig(
            project=ProjectSpec(
                name="test",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="echo start", test="echo test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test")),
        )
        assert config.agentic.provider.value == "claude_code"

    def test_version_default(self):
        """Version field should default to current __version__."""
        from tac_bootstrap import __version__

        config = TACConfig(
            project=ProjectSpec(
                name="test",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="echo start", test="echo test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test")),
        )
        assert config.version == __version__
        assert isinstance(config.version, str)

    def test_version_custom(self):
        """Should accept custom version string."""
        config = TACConfig(
            version="1.5.0",
            project=ProjectSpec(
                name="test",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="echo start", test="echo test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test")),
        )
        assert config.version == "1.5.0"

    def test_version_type(self):
        """Version should be string type."""
        config = TACConfig(
            project=ProjectSpec(
                name="test",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="echo start", test="echo test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test")),
        )
        assert isinstance(config.version, str)

    def test_version_in_model_dump(self):
        """Version should appear in model_dump() output."""
        from tac_bootstrap import __version__

        config = TACConfig(
            project=ProjectSpec(
                name="test",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="echo start", test="echo test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test")),
        )
        dump = config.model_dump()
        assert "version" in dump
        assert dump["version"] == __version__

    def test_custom_paths(self):
        """Should allow custom paths configuration."""
        custom_paths = PathsSpec(
            app_root="src",
            adws_dir="workflows",
            specs_dir="specifications",
        )
        config = TACConfig(
            project=ProjectSpec(
                name="test",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="echo start", test="echo test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test")),
            paths=custom_paths,
        )
        assert config.paths.app_root == "src"
        assert config.paths.adws_dir == "workflows"
        assert config.paths.specs_dir == "specifications"

    def test_worktree_enabled_default(self):
        """Worktrees should be enabled by default."""
        config = TACConfig(
            project=ProjectSpec(
                name="test",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="echo start", test="echo test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test")),
        )
        assert config.agentic.worktrees.enabled is True
        assert config.agentic.worktrees.max_parallel == 5


# ============================================================================
# TEST HELPER FUNCTIONS
# ============================================================================


class TestHelperFunctions:
    """Tests for helper functions."""

    # Test get_frameworks_for_language
    def test_frameworks_for_python(self):
        """Python should have FastAPI, Django, Flask."""
        frameworks = get_frameworks_for_language(Language.PYTHON)
        assert Framework.FASTAPI in frameworks
        assert Framework.DJANGO in frameworks
        assert Framework.FLASK in frameworks

    def test_frameworks_for_typescript(self):
        """TypeScript should have Next.js, NestJS, React, Express."""
        frameworks = get_frameworks_for_language(Language.TYPESCRIPT)
        assert Framework.NEXTJS in frameworks
        assert Framework.NESTJS in frameworks
        assert Framework.REACT in frameworks
        assert Framework.EXPRESS in frameworks

    def test_frameworks_for_javascript(self):
        """JavaScript should have Next.js, Express, React, Vue."""
        frameworks = get_frameworks_for_language(Language.JAVASCRIPT)
        assert Framework.NEXTJS in frameworks
        assert Framework.EXPRESS in frameworks
        assert Framework.REACT in frameworks
        assert Framework.VUE in frameworks

    def test_frameworks_for_go(self):
        """Go should have Gin, Echo."""
        frameworks = get_frameworks_for_language(Language.GO)
        assert Framework.GIN in frameworks
        assert Framework.ECHO in frameworks

    def test_frameworks_for_rust(self):
        """Rust should have Axum, Actix."""
        frameworks = get_frameworks_for_language(Language.RUST)
        assert Framework.AXUM in frameworks
        assert Framework.ACTIX in frameworks

    def test_frameworks_for_java(self):
        """Java should have Spring."""
        frameworks = get_frameworks_for_language(Language.JAVA)
        assert Framework.SPRING in frameworks

    # Test get_package_managers_for_language
    def test_package_managers_for_python(self):
        """Python should have UV, Poetry, Pip, Pipenv."""
        managers = get_package_managers_for_language(Language.PYTHON)
        assert PackageManager.UV in managers
        assert PackageManager.POETRY in managers
        assert PackageManager.PIP in managers
        assert PackageManager.PIPENV in managers

    def test_package_managers_for_typescript(self):
        """TypeScript should have pnpm, npm, yarn, bun."""
        managers = get_package_managers_for_language(Language.TYPESCRIPT)
        assert PackageManager.PNPM in managers
        assert PackageManager.NPM in managers
        assert PackageManager.YARN in managers
        assert PackageManager.BUN in managers

    def test_package_managers_for_javascript(self):
        """JavaScript should have pnpm, npm, yarn, bun."""
        managers = get_package_managers_for_language(Language.JAVASCRIPT)
        assert PackageManager.PNPM in managers
        assert PackageManager.NPM in managers
        assert PackageManager.YARN in managers
        assert PackageManager.BUN in managers

    def test_package_managers_for_go(self):
        """Go should have go mod."""
        managers = get_package_managers_for_language(Language.GO)
        assert PackageManager.GO_MOD in managers

    def test_package_managers_for_rust(self):
        """Rust should have Cargo."""
        managers = get_package_managers_for_language(Language.RUST)
        assert PackageManager.CARGO in managers

    def test_package_managers_for_java(self):
        """Java should have Maven, Gradle."""
        managers = get_package_managers_for_language(Language.JAVA)
        assert PackageManager.MAVEN in managers
        assert PackageManager.GRADLE in managers

    # Test get_default_commands
    def test_default_commands_python_uv(self):
        """Python + UV should have correct defaults."""
        commands = get_default_commands(Language.PYTHON, PackageManager.UV)
        assert "uv run pytest" in commands["test"]
        assert "uv run ruff" in commands["lint"]
        assert "uv run mypy" in commands["typecheck"]
        assert "uv run python" in commands["start"]

    def test_default_commands_python_poetry(self):
        """Python + Poetry should have correct defaults."""
        commands = get_default_commands(Language.PYTHON, PackageManager.POETRY)
        assert "poetry run pytest" in commands["test"]
        assert "poetry run ruff" in commands["lint"]
        assert "poetry run mypy" in commands["typecheck"]

    def test_default_commands_python_pip(self):
        """Python + pip should have correct defaults."""
        commands = get_default_commands(Language.PYTHON, PackageManager.PIP)
        assert commands["test"] == "pytest"
        assert commands["lint"] == "ruff check ."
        assert commands["typecheck"] == "mypy ."

    def test_default_commands_typescript_pnpm(self):
        """TypeScript + pnpm should have correct defaults."""
        commands = get_default_commands(Language.TYPESCRIPT, PackageManager.PNPM)
        assert commands["test"] == "pnpm test"
        assert commands["lint"] == "pnpm lint"
        assert commands["typecheck"] == "pnpm typecheck"
        assert commands["start"] == "pnpm dev"
        assert commands["build"] == "pnpm build"

    def test_default_commands_typescript_npm(self):
        """TypeScript + npm should have correct defaults."""
        commands = get_default_commands(Language.TYPESCRIPT, PackageManager.NPM)
        assert commands["test"] == "npm test"
        assert commands["start"] == "npm run dev"

    def test_default_commands_typescript_yarn(self):
        """TypeScript + yarn should have correct defaults."""
        commands = get_default_commands(Language.TYPESCRIPT, PackageManager.YARN)
        assert commands["test"] == "yarn test"
        assert commands["start"] == "yarn dev"
        assert commands["build"] == "yarn build"

    def test_default_commands_typescript_bun(self):
        """TypeScript + bun should have correct defaults."""
        commands = get_default_commands(Language.TYPESCRIPT, PackageManager.BUN)
        assert commands["test"] == "bun test"
        assert commands["start"] == "bun run dev"
        assert commands["build"] == "bun run build"

    def test_default_commands_go(self):
        """Go should have correct defaults."""
        commands = get_default_commands(Language.GO, PackageManager.GO_MOD)
        assert commands["test"] == "go test ./..."
        assert commands["lint"] == "golangci-lint run"
        assert commands["start"] == "go run ."
        assert commands["build"] == "go build"

    def test_default_commands_rust(self):
        """Rust should have correct defaults."""
        commands = get_default_commands(Language.RUST, PackageManager.CARGO)
        assert commands["test"] == "cargo test"
        assert commands["lint"] == "cargo clippy"
        assert commands["start"] == "cargo run"
        assert commands["build"] == "cargo build --release"

    def test_default_commands_java_maven(self):
        """Java + Maven should have correct defaults."""
        commands = get_default_commands(Language.JAVA, PackageManager.MAVEN)
        assert commands["test"] == "mvn test"
        assert commands["build"] == "mvn package"
        assert "mvn" in commands["start"]

    def test_default_commands_java_gradle(self):
        """Java + Gradle should have correct defaults."""
        commands = get_default_commands(Language.JAVA, PackageManager.GRADLE)
        assert commands["test"] == "gradle test"
        assert commands["build"] == "gradle build"
        assert commands["start"] == "gradle bootRun"

    def test_default_commands_all_have_required_keys(self):
        """All command dictionaries should have required keys."""
        test_cases = [
            (Language.PYTHON, PackageManager.UV),
            (Language.TYPESCRIPT, PackageManager.PNPM),
            (Language.GO, PackageManager.GO_MOD),
            (Language.RUST, PackageManager.CARGO),
        ]
        required_keys = {"start", "test", "lint", "typecheck", "format", "build"}

        for lang, pm in test_cases:
            commands = get_default_commands(lang, pm)
            assert set(commands.keys()) == required_keys, f"Missing keys for {lang} + {pm}"


# ============================================================================
# TEST COMMANDS SPEC
# ============================================================================


class TestCommandsSpec:
    """Tests for CommandsSpec model."""

    def test_required_commands(self):
        """Start and test commands are required."""
        commands = CommandsSpec(start="npm start", test="npm test")
        assert commands.start == "npm start"
        assert commands.test == "npm test"

    def test_optional_commands_defaults(self):
        """Optional commands should have empty string defaults."""
        commands = CommandsSpec(start="npm start", test="npm test")
        assert commands.lint == ""
        assert commands.typecheck == ""
        assert commands.format == ""
        assert commands.build == ""

    def test_all_commands_provided(self):
        """Should accept all commands."""
        commands = CommandsSpec(
            start="npm start",
            test="npm test",
            lint="npm run lint",
            typecheck="tsc --noEmit",
            format="prettier --write .",
            build="npm run build",
        )
        assert commands.start == "npm start"
        assert commands.test == "npm test"
        assert commands.lint == "npm run lint"
        assert commands.typecheck == "tsc --noEmit"
        assert commands.format == "prettier --write ."
        assert commands.build == "npm run build"
