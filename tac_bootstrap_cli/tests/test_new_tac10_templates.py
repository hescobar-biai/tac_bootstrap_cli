"""Tests for TAC-10 new templates.

Unit tests for the new templates introduced in TAC-10:
- Comandos slash: parallel_subagents.md.j2, t_metaprompt_workflow.md.j2, build_w_report.md.j2
- Expert command: cc_hook_expert_improve.md.j2
- Configuración actualizada: settings.json.j2 con 9 nuevos hooks

Los tests verifican:
1. Los templates renderizan sin errores
2. El contenido generado tiene estructura válida (markdown, JSON)
3. Los settings.json incluyen todos los hooks esperados
4. Los hooks referencian los scripts correctos
"""

import json

import pytest

from tac_bootstrap.domain.models import (
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Language,
    PackageManager,
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
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
        ),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-python-app")),
    )


@pytest.fixture
def template_repo() -> TemplateRepository:
    """Create a TemplateRepository instance."""
    return TemplateRepository()


# ============================================================================
# TEST COMMAND TEMPLATES (MARKDOWN)
# ============================================================================


class TestParallelSubagentsTemplate:
    """Tests for parallel_subagents.md.j2 template."""

    def test_parallel_subagents_renders_valid_markdown(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """parallel_subagents.md.j2 should render valid markdown with expected sections."""
        content = template_repo.render(
            "claude/commands/parallel_subagents.md.j2", python_config
        )

        # Verify content is not empty
        assert len(content.strip()) > 100, "Generated command should have meaningful content"

        # Verify key sections exist
        assert "## Variables" in content, "Command should have Variables section"
        assert "## Instructions" in content, "Command should have Instructions section"
        assert "## Workflow" in content, "Command should have Workflow section"


class TestMetapromptWorkflowTemplate:
    """Tests for t_metaprompt_workflow.md.j2 template."""

    def test_metaprompt_workflow_renders_valid_markdown(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """t_metaprompt_workflow.md.j2 should render valid markdown with expected sections."""
        content = template_repo.render(
            "claude/commands/t_metaprompt_workflow.md.j2", python_config
        )

        # Verify content is not empty
        assert len(content.strip()) > 100, "Generated command should have meaningful content"

        # Verify key sections exist
        assert "## Variables" in content, "Command should have Variables section"
        assert "## Instructions" in content, "Command should have Instructions section"
        assert "## Workflow" in content, "Command should have Workflow section"


class TestBuildWithReportTemplate:
    """Tests for build_w_report.md.j2 template."""

    def test_build_w_report_renders_valid_markdown(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """build_w_report.md.j2 should render valid markdown with expected sections."""
        content = template_repo.render(
            "claude/commands/build_w_report.md.j2", python_config
        )

        # Verify content is not empty
        assert len(content.strip()) > 100, "Generated command should have meaningful content"

        # Verify key sections exist
        assert "## Variables" in content, "Command should have Variables section"
        assert "## Instructions" in content, "Command should have Instructions section"


# ============================================================================
# TEST EXPERT TEMPLATE
# ============================================================================


class TestCCHookExpertImproveTemplate:
    """Tests for cc_hook_expert_improve.md.j2 template."""

    def test_cc_hook_expert_improve_renders_valid_markdown(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """cc_hook_expert_improve.md.j2 should render valid markdown with expected sections."""
        content = template_repo.render(
            "claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2",
            python_config,
        )

        # Verify content is not empty
        assert len(content.strip()) > 100, "Generated expert command should have meaningful content"

        # Verify key sections exist
        assert "## Variables" in content, "Expert command should have Variables section"
        assert "## Instructions" in content, "Expert command should have Instructions section"

        # Verify semantic content related to hooks and expert
        content_lower = content.lower()
        assert (
            "hook" in content_lower or "expert" in content_lower
        ), "Expert command should mention 'hook' or 'expert'"


# ============================================================================
# TEST SETTINGS.JSON.J2 WITH HOOKS
# ============================================================================


class TestSettingsTemplateWithHooks:
    """Tests for settings.json.j2 template with new hooks validation."""

    def test_settings_renders_valid_json(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """settings.json.j2 should render valid JSON with expected structure."""
        content = template_repo.render("claude/settings.json.j2", python_config)

        # Verify content is not empty
        assert len(content.strip()) > 50, "Generated settings should have meaningful content"

        # Verify it's valid JSON
        parsed = json.loads(content)

        # Verify expected structure
        assert "permissions" in parsed, "Settings should have 'permissions' key"
        assert "hooks" in parsed, "Settings should have 'hooks' key"

    def test_settings_includes_all_nine_hooks(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """settings.json.j2 should include all 9 expected hooks."""
        content = template_repo.render("claude/settings.json.j2", python_config)
        parsed = json.loads(content)

        # Verify hooks section exists
        assert "hooks" in parsed, "Settings should have 'hooks' key"

        # Verify all 9 hooks are present
        expected_hooks = [
            "PreToolUse",
            "PostToolUse",
            "Stop",
            "UserPromptSubmit",
            "SubagentStop",
            "Notification",
            "PreCompact",
            "SessionStart",
            "SessionEnd",
        ]

        for hook_name in expected_hooks:
            assert (
                hook_name in parsed["hooks"]
            ), f"Settings should include '{hook_name}' hook"

    def test_settings_hooks_reference_correct_scripts(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """settings.json.j2 hooks should reference correct scripts."""
        content = template_repo.render("claude/settings.json.j2", python_config)
        parsed = json.loads(content)

        hooks = parsed.get("hooks", {})

        # Helper function to extract command from hook structure
        def get_hook_command(hook_name: str) -> str:
            hook_list = hooks.get(hook_name, [])
            if hook_list and len(hook_list) > 0:
                hook_entry = hook_list[0]
                if "hooks" in hook_entry and len(hook_entry["hooks"]) > 0:
                    return hook_entry["hooks"][0].get("command", "")
            return ""

        # Verify PostToolUse and UserPromptSubmit mention context_bundle_builder.py
        post_tool_use = get_hook_command("PostToolUse")
        assert (
            "context_bundle_builder.py" in post_tool_use
        ), "PostToolUse should reference context_bundle_builder.py"

        user_prompt_submit = get_hook_command("UserPromptSubmit")
        assert (
            "context_bundle_builder.py" in user_prompt_submit
        ), "UserPromptSubmit should reference context_bundle_builder.py"

        # Verify hooks that should use universal_hook_logger.py
        universal_logger_hooks = [
            "PreToolUse",
            "Stop",
            "SubagentStop",
            "Notification",
            "PreCompact",
            "SessionStart",
            "SessionEnd",
        ]

        for hook_name in universal_logger_hooks:
            hook_command = get_hook_command(hook_name)
            assert (
                "universal_hook_logger.py" in hook_command
            ), f"{hook_name} should reference universal_hook_logger.py"
