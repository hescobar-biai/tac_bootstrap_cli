"""
Tests for ADW trigger templates.

Unit tests for trigger_cron.py and trigger_webhook.py template rendering.
"""

import pytest

from tac_bootstrap.domain.models import (
    AgenticSpec,
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Language,
    PackageManager,
    ProjectSpec,
    TACConfig,
)
from tac_bootstrap.infrastructure.template_repo import TemplateRepository


@pytest.fixture
def sample_config_with_cron() -> TACConfig:
    """Create a TACConfig with agentic.cron_interval configured."""
    return TACConfig(
        project=ProjectSpec(
            name="TestProject",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
            lint="uv run ruff check .",
        ),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="TestProject")),
        agentic=AgenticSpec(cron_interval=30),
    )


@pytest.fixture
def sample_config_without_cron() -> TACConfig:
    """Create a TACConfig without agentic.cron_interval (should use default)."""
    return TACConfig(
        project=ProjectSpec(
            name="AnotherProject",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
            lint="uv run ruff check .",
        ),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="AnotherProject")),
    )


def test_trigger_cron_template_with_custom_interval(
    sample_config_with_cron: TACConfig,
):
    """Verify trigger_cron.py template renders with custom interval."""
    repo = TemplateRepository()

    rendered = repo.render(
        "adws/adw_triggers/trigger_cron.py.j2",
        sample_config_with_cron,
    )

    # Verify project name appears in docstring (sanitized to lowercase)
    assert "testproject" in rendered

    # Verify custom interval appears as DEFAULT_INTERVAL
    assert "DEFAULT_INTERVAL = 30" in rendered

    # Verify interval appears in usage examples
    assert "Default 30s interval" in rendered

    # Verify interval appears in arg parser help (as f-string variable reference)
    assert "default: {DEFAULT_INTERVAL}" in rendered

    # Verify workflow detection logic is present
    assert "extract_adw_info" in rendered
    assert "DEPENDENT_WORKFLOWS" in rendered
    assert "ADW_BOT_IDENTIFIER" in rendered
    assert "ADWState" in rendered


def test_trigger_cron_template_with_default_interval(
    sample_config_without_cron: TACConfig,
):
    """Verify trigger_cron.py template uses default interval when not configured."""
    repo = TemplateRepository()

    rendered = repo.render(
        "adws/adw_triggers/trigger_cron.py.j2",
        sample_config_without_cron,
    )

    # Verify project name appears in docstring (sanitized to lowercase)
    assert "anotherproject" in rendered

    # Verify default interval (20s) is used
    assert "DEFAULT_INTERVAL = 20" in rendered

    # Verify default interval appears in usage examples
    assert "Default 20s interval" in rendered

    # Verify default interval appears in arg parser help (as f-string variable reference)
    assert "default: {DEFAULT_INTERVAL}" in rendered


def test_trigger_cron_template_structure(sample_config_with_cron: TACConfig):
    """Verify trigger_cron.py template has all required structural elements."""
    repo = TemplateRepository()

    rendered = repo.render(
        "adws/adw_triggers/trigger_cron.py.j2",
        sample_config_with_cron,
    )

    # Verify shebang and PEP 723 inline script metadata
    assert "#!/usr/bin/env uv run" in rendered
    assert "# /// script" in rendered
    assert '"schedule"' in rendered
    assert '"python-dotenv"' in rendered

    # Verify imports
    assert "import argparse" in rendered
    assert "import schedule" in rendered
    assert "from adw_modules.github import" in rendered
    assert (
        "from adw_modules.workflow_ops import AVAILABLE_ADW_WORKFLOWS, extract_adw_info"
        in rendered
    )
    assert "from adw_modules.state import ADWState" in rendered

    # Verify core functions exist
    assert "def check_issue_for_workflow(issue_number: int)" in rendered
    assert "def trigger_workflow(issue_number: int, workflow_info: Dict)" in rendered
    assert "def check_and_process_issues():" in rendered
    assert "def parse_args():" in rendered
    assert "def main():" in rendered

    # Verify workflow validation logic
    assert "DEPENDENT_WORKFLOWS = [" in rendered
    assert '"adw_build_iso"' in rendered
    assert '"adw_test_iso"' in rendered
    assert '"adw_review_iso"' in rendered
    assert '"adw_document_iso"' in rendered
    assert '"adw_ship_iso"' in rendered

    # Verify anti-loop protection
    assert "ADW_BOT_IDENTIFIER" in rendered

    # Verify state management
    assert "ADWState.load" in rendered
    assert "state.save" in rendered

    # Verify background process launch
    assert "subprocess.Popen" in rendered
    assert "start_new_session=True" in rendered


def test_trigger_cron_template_no_syntax_errors(sample_config_with_cron: TACConfig):
    """Verify rendered trigger_cron.py has valid Python syntax."""
    repo = TemplateRepository()

    rendered = repo.render(
        "adws/adw_triggers/trigger_cron.py.j2",
        sample_config_with_cron,
    )

    # Try to compile the rendered Python code
    try:
        compile(rendered, "trigger_cron.py", "exec")
    except SyntaxError as e:
        pytest.fail(f"Rendered template has syntax error: {e}")


def test_trigger_cron_template_special_project_name():
    """Verify trigger_cron.py handles project names with special characters."""
    # Create a new config with special characters in the name
    # Note: ProjectSpec validator will sanitize this during creation
    config = TACConfig(
        project=ProjectSpec(
            name="My-Special_Project 2.0",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
            lint="uv run ruff check .",
        ),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="TestProject")),
        agentic=AgenticSpec(cron_interval=30),
    )

    repo = TemplateRepository()

    rendered = repo.render(
        "adws/adw_triggers/trigger_cron.py.j2",
        config,
    )

    # Verify project name appears sanitized (lowercase, spaces to hyphens)
    # "My-Special_Project 2.0" -> "my-special_project-2.0"
    assert "my-special_project-2.0" in rendered

    # Verify template still renders valid Python
    try:
        compile(rendered, "trigger_cron.py", "exec")
    except SyntaxError as e:
        pytest.fail(f"Template with special project name has syntax error: {e}")
