"""Tests for prime_cc command template.

Unit tests for the prime_cc.md.j2 template:
- Verifies template renders without errors
- Validates all expected sections are present
- Confirms Jinja2 variables are properly substituted
- Tests conditional blocks for optional paths (adws_dir, scripts_dir)
- Validates Claude Code-specific content and patterns
"""

import pytest

from tac_bootstrap.domain.models import (
    AgenticProvider,
    AgenticSpec,
    Architecture,
    ClaudeCommandsConfig,
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Language,
    PackageManager,
    PathsSpec,
    ProjectSpec,
    TACConfig,
)
from tac_bootstrap.infrastructure.template_repo import TemplateRepository

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def python_config() -> TACConfig:
    """Create a minimal Python config for testing."""
    return TACConfig(
        project=ProjectSpec(
            name="test-python-app",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
            architecture=Architecture.DDD,
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
            lint="uv run ruff check .",
            typecheck="uv run mypy .",
            build="uv build",
        ),
        paths=PathsSpec(
            adws_dir="adws",
            scripts_dir="scripts",
            specs_dir="specs",
            app_root="src",
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name="test-python-app"),
            commands=ClaudeCommandsConfig(),
        ),
        agentic=AgenticSpec(provider=AgenticProvider.CLAUDE_CODE),
    )


@pytest.fixture
def minimal_config() -> TACConfig:
    """Create a minimal config without optional features."""
    return TACConfig(
        project=ProjectSpec(
            name="minimal-app",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
        ),
        paths=PathsSpec(
            app_root="src",
            specs_dir="specs",
        ),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="minimal-app")),
    )


@pytest.fixture
def template_repo() -> TemplateRepository:
    """Create a TemplateRepository instance."""
    return TemplateRepository()


# ============================================================================
# TEST TEMPLATE RENDERING
# ============================================================================


class TestPrimeCCTemplateRendering:
    """Tests for prime_cc.md.j2 template rendering."""

    def test_prime_cc_renders_valid_markdown(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should render valid markdown with meaningful content."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Verify content is substantial
        assert len(content.strip()) > 100, "Generated command should have meaningful content"
        assert content.strip().startswith("---"), "Should start with YAML frontmatter"

    def test_prime_cc_has_required_sections(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include all required command sections."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Verify all required sections
        required_sections = [
            "## Variables",
            "## Instructions",
            "## Run",
            "## Read",
            "## Understand",
            "## Examples",
            "## Report",
        ]

        for section in required_sections:
            assert section in content, f"Command should have {section} section"

    def test_prime_cc_has_frontmatter(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should have valid YAML frontmatter with description."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Check frontmatter markers
        assert content.startswith("---\n"), "Should start with frontmatter delimiter"
        assert "description:" in content[:200], "Frontmatter should include description"

    def test_prime_cc_renders_with_minimal_config(
        self, template_repo: TemplateRepository, minimal_config: TACConfig
    ):
        """prime_cc.md.j2 should render successfully with minimal config."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", minimal_config)

        assert len(content.strip()) > 100, "Should render with minimal config"
        assert "## Variables" in content, "Should include Variables section"


# ============================================================================
# TEST CONFIG VARIABLE SUBSTITUTION
# ============================================================================


class TestPrimeCCConfigVariables:
    """Tests for config variable substitution in prime_cc template."""

    def test_prime_cc_uses_project_name(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should substitute project name from config."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        assert "test-python-app" in content, "Should include project name from config"

    def test_prime_cc_uses_language(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include language from config."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Should mention the language in the Report section
        assert (
            "Language.PYTHON" in content or "PYTHON" in content
        ), "Should reference language"

    def test_prime_cc_uses_architecture(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include architecture from config."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Should mention the architecture in the Report section
        assert (
            "Architecture.DDD" in content or "DDD" in content
        ), "Should reference architecture"

    def test_prime_cc_uses_package_manager(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include package manager from config."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Should mention the package manager in the Report section
        assert (
            "PackageManager.UV" in content or "UV" in content
        ), "Should reference package manager"

    def test_prime_cc_uses_agentic_provider(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include agentic provider from config."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Should mention the provider in the Understand section
        assert "AgenticProvider.CLAUDE_CODE" in content or "CLAUDE_CODE" in content, (
            "Should reference agentic provider"
        )


# ============================================================================
# TEST CONDITIONAL SECTIONS
# ============================================================================


class TestPrimeCCConditionalBlocks:
    """Tests for conditional sections based on config."""

    def test_prime_cc_includes_adws_when_configured(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include ADW sections when adws_dir is configured."""
        # Ensure ADW is configured
        python_config.paths.adws_dir = "adws"
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        assert "adws/README.md" in content, "Should reference ADW README"
        assert "AI Developer Workflows" in content, "Should mention AI Developer Workflows"
        assert "adw_modules/" in content, "Should reference adw_modules"

    def test_prime_cc_uses_configured_adws_path(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should use the configured adws_dir path."""
        # Set a custom ADW path
        python_config.paths.adws_dir = "custom_adws"
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        assert "custom_adws/README.md" in content, "Should use custom ADW path"
        assert "custom_adws/adw_modules/" in content, "Should use custom ADW path for modules"

    def test_prime_cc_includes_scripts_when_configured(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include scripts sections when scripts_dir is configured."""
        # Ensure scripts is configured
        python_config.paths.scripts_dir = "scripts"
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        assert "scripts/" in content, "Should reference scripts directory"

    def test_prime_cc_uses_configured_scripts_path(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should use the configured scripts_dir path."""
        # Set a custom scripts path
        python_config.paths.scripts_dir = "bin"
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Should use the custom scripts path
        assert "bin/" in content, "Should use custom scripts path"

    def test_prime_cc_includes_commands_when_configured(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include command sections when commands are configured."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Should include conditional sections for configured commands
        assert "start.md" in content, "Should mention start command"
        assert "test.md" in content, "Should mention test command"
        assert "build.md" in content, "Should mention build command"


# ============================================================================
# TEST CLAUDE CODE PATTERNS
# ============================================================================


class TestPrimeCCClaudeCodePatterns:
    """Tests for Claude Code-specific patterns and content."""

    def test_prime_cc_includes_tool_preferences(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include Claude Code tool preferences."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Check for tool usage guidance
        assert "Read tool" in content or "Read" in content, "Should mention Read tool"
        assert "Edit tool" in content or "Edit" in content, "Should mention Edit tool"
        assert "Bash tool" in content or "Bash" in content, "Should mention Bash tool"
        assert "Grep tool" in content or "Grep" in content, "Should mention Grep tool"
        assert "Glob tool" in content or "Glob" in content, "Should mention Glob tool"

    def test_prime_cc_mentions_claude_code_config(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should reference Claude Code configuration files."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Check for Claude Code configuration references
        assert ".claude/commands/" in content, "Should reference commands directory"
        assert ".claude/settings.json" in content, "Should reference settings.json"
        assert ".claude/hooks/" in content, "Should reference hooks directory"

    def test_prime_cc_includes_slash_command_discovery(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should emphasize slash command discovery."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Check for command discovery guidance
        assert "slash command" in content.lower(), "Should mention slash commands"
        assert "prime.md" in content, "Should reference prime command"
        assert "prime_cc.md" in content, "Should reference itself"

    def test_prime_cc_includes_automation_hooks(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should reference automation hooks."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Check for automation hook references
        assert (
            "context_bundle_builder.py" in content
        ), "Should mention context_bundle_builder"
        assert "Automation" in content or "automation" in content, "Should discuss automation"

    def test_prime_cc_includes_cli_workflows(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include CLI workflow examples."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Check for CLI commands from config
        assert "uv run pytest" in content, "Should include test command"
        assert "uv run ruff check ." in content, "Should include lint command"

    def test_prime_cc_extends_prime_command(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should indicate it extends /prime command."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Check that it references running /prime first
        assert "/prime" in content, "Should reference /prime command"
        assert "extends" in content.lower() or "first run" in content.lower(), (
            "Should indicate it extends or builds on /prime"
        )


# ============================================================================
# TEST MARKDOWN STRUCTURE
# ============================================================================


class TestPrimeCCMarkdownStructure:
    """Tests for valid markdown structure in prime_cc template."""

    def test_prime_cc_has_proper_header_hierarchy(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should have proper markdown header hierarchy."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Should have h1 title
        assert "\n# " in content, "Should have h1 header"

        # Should have h2 sections
        assert "\n## " in content, "Should have h2 headers for sections"

        # Should have h3 subsections
        assert "\n### " in content, "Should have h3 headers for subsections"

    def test_prime_cc_has_code_blocks(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should include code blocks for examples."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Should have code blocks (bash, json, etc.)
        assert "```" in content, "Should include code blocks"
        assert "```bash" in content or "```" in content, "Should have bash code examples"

    def test_prime_cc_has_lists(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """prime_cc.md.j2 should use lists for structured information."""
        content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)

        # Should have bullet lists
        assert "\n- " in content or "\n* " in content, "Should include bullet lists"


# ============================================================================
# TEST EDGE CASES
# ============================================================================


class TestPrimeCCEdgeCases:
    """Tests for edge cases in prime_cc template."""

    def test_prime_cc_with_typescript_project(
        self, template_repo: TemplateRepository
    ):
        """prime_cc.md.j2 should work with TypeScript projects."""
        ts_config = TACConfig(
            project=ProjectSpec(
                name="test-ts-app",
                language=Language.TYPESCRIPT,
                package_manager=PackageManager.NPM,
            ),
            commands=CommandsSpec(
                start="npm run dev",
                test="npm test",
            ),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-ts-app")),
        )

        content = template_repo.render("claude/commands/prime_cc.md.j2", ts_config)

        assert "test-ts-app" in content, "Should include TypeScript project name"
        assert "Language.TYPESCRIPT" in content or "TYPESCRIPT" in content, (
            "Should reference TypeScript"
        )

    def test_prime_cc_with_go_project(self, template_repo: TemplateRepository):
        """prime_cc.md.j2 should work with Go projects."""
        go_config = TACConfig(
            project=ProjectSpec(
                name="test-go-app",
                language=Language.GO,
                package_manager=PackageManager.GO_MOD,
            ),
            commands=CommandsSpec(
                start="go run main.go",
                test="go test ./...",
            ),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-go-app")),
        )

        content = template_repo.render("claude/commands/prime_cc.md.j2", go_config)

        assert "test-go-app" in content, "Should include Go project name"
        assert "Language.GO" in content or "GO" in content, "Should reference Go"

    def test_prime_cc_with_different_package_managers(self, template_repo: TemplateRepository):
        """prime_cc.md.j2 should work with different package managers."""
        npm_config = TACConfig(
            project=ProjectSpec(
                name="test-npm-app",
                language=Language.TYPESCRIPT,
                package_manager=PackageManager.NPM,
            ),
            commands=CommandsSpec(
                start="npm run dev",
                test="npm test",
            ),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-npm-app")),
        )

        content = template_repo.render("claude/commands/prime_cc.md.j2", npm_config)

        # Should still render successfully
        assert len(content.strip()) > 100, "Should render with NPM package manager"
        assert "test-npm-app" in content, "Should include project name"
