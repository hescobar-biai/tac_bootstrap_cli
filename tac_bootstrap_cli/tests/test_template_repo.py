"""
Tests for TemplateRepository

Comprehensive unit tests for template loading, rendering, filtering,
and error handling.
"""

from pathlib import Path

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
from tac_bootstrap.infrastructure.template_repo import (
    TemplateNotFoundError,
    TemplateRenderError,
    TemplateRepository,
    to_kebab_case,
    to_pascal_case,
    to_snake_case,
)

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def sample_config() -> TACConfig:
    """Create a sample TACConfig for testing."""
    return TACConfig(
        project=ProjectSpec(
            name="my-test-app",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
            lint="uv run ruff check .",
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name="my-test-app")
        ),
    )


@pytest.fixture
def temp_templates_dir(tmp_path: Path) -> Path:
    """Create a temporary templates directory with test templates."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()

    # Create test templates
    (templates_dir / "simple.txt.j2").write_text("Hello, {{ config.project.name }}!")

    (templates_dir / "with_filter.txt.j2").write_text(
        "Snake: {{ config.project.name | snake_case }}\n"
        "Kebab: {{ config.project.name | kebab_case }}\n"
        "Pascal: {{ config.project.name | pascal_case }}"
    )

    (templates_dir / "multiline.txt.j2").write_text(
        "Project: {{ config.project.name }}\n"
        "Language: {{ config.project.language.value }}\n"
        "Start: {{ config.commands.start }}\n"
    )

    # Create category subdirectories
    claude_dir = templates_dir / "claude"
    claude_dir.mkdir()
    (claude_dir / "settings.json.j2").write_text(
        '{\n  "project_name": "{{ config.claude.settings.project_name }}"\n}\n'
    )

    adws_dir = templates_dir / "adws"
    adws_dir.mkdir()
    (adws_dir / "workflow.py.j2").write_text(
        "# Workflow for {{ config.project.name }}\n"
    )

    scripts_dir = templates_dir / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "setup.sh.j2").write_text(
        "#!/bin/bash\necho 'Setting up {{ config.project.name }}'\n"
    )

    return templates_dir


@pytest.fixture
def repo(temp_templates_dir: Path) -> TemplateRepository:
    """Create a TemplateRepository with temp templates directory."""
    return TemplateRepository(templates_dir=temp_templates_dir)


# ============================================================================
# TEST CASE CONVERSION FILTERS
# ============================================================================


class TestCaseConversion:
    """Test case conversion filter functions."""

    def test_to_snake_case_from_kebab(self):
        """Test converting kebab-case to snake_case."""
        assert to_snake_case("my-test-app") == "my_test_app"
        assert to_snake_case("foo-bar-baz") == "foo_bar_baz"

    def test_to_snake_case_from_pascal(self):
        """Test converting PascalCase to snake_case."""
        assert to_snake_case("MyTestApp") == "my_test_app"
        assert to_snake_case("FooBarBaz") == "foo_bar_baz"

    def test_to_snake_case_from_camel(self):
        """Test converting camelCase to snake_case."""
        assert to_snake_case("myTestApp") == "my_test_app"
        assert to_snake_case("fooBarBaz") == "foo_bar_baz"

    def test_to_snake_case_from_spaces(self):
        """Test converting spaces to snake_case."""
        assert to_snake_case("My Test App") == "my_test_app"
        assert to_snake_case("Foo Bar Baz") == "foo_bar_baz"

    def test_to_snake_case_already_snake(self):
        """Test that snake_case remains unchanged."""
        assert to_snake_case("my_test_app") == "my_test_app"
        assert to_snake_case("foo_bar_baz") == "foo_bar_baz"

    def test_to_snake_case_mixed(self):
        """Test mixed format conversion to snake_case."""
        assert to_snake_case("My-Test_App") == "my_test_app"
        assert to_snake_case("foo Bar-Baz") == "foo_bar_baz"

    def test_to_snake_case_with_numbers(self):
        """Test snake_case conversion with numbers."""
        assert to_snake_case("app2test") == "app2test"
        assert to_snake_case("MyApp2Test") == "my_app2_test"

    def test_to_kebab_case_from_snake(self):
        """Test converting snake_case to kebab-case."""
        assert to_kebab_case("my_test_app") == "my-test-app"
        assert to_kebab_case("foo_bar_baz") == "foo-bar-baz"

    def test_to_kebab_case_from_pascal(self):
        """Test converting PascalCase to kebab-case."""
        assert to_kebab_case("MyTestApp") == "my-test-app"
        assert to_kebab_case("FooBarBaz") == "foo-bar-baz"

    def test_to_kebab_case_from_camel(self):
        """Test converting camelCase to kebab-case."""
        assert to_kebab_case("myTestApp") == "my-test-app"
        assert to_kebab_case("fooBarBaz") == "foo-bar-baz"

    def test_to_kebab_case_from_spaces(self):
        """Test converting spaces to kebab-case."""
        assert to_kebab_case("My Test App") == "my-test-app"
        assert to_kebab_case("Foo Bar Baz") == "foo-bar-baz"

    def test_to_kebab_case_already_kebab(self):
        """Test that kebab-case remains unchanged."""
        assert to_kebab_case("my-test-app") == "my-test-app"
        assert to_kebab_case("foo-bar-baz") == "foo-bar-baz"

    def test_to_pascal_case_from_snake(self):
        """Test converting snake_case to PascalCase."""
        assert to_pascal_case("my_test_app") == "MyTestApp"
        assert to_pascal_case("foo_bar_baz") == "FooBarBaz"

    def test_to_pascal_case_from_kebab(self):
        """Test converting kebab-case to PascalCase."""
        assert to_pascal_case("my-test-app") == "MyTestApp"
        assert to_pascal_case("foo-bar-baz") == "FooBarBaz"

    def test_to_pascal_case_from_camel(self):
        """Test converting camelCase to PascalCase."""
        assert to_pascal_case("myTestApp") == "MyTestApp"
        assert to_pascal_case("fooBarBaz") == "FooBarBaz"

    def test_to_pascal_case_from_spaces(self):
        """Test converting spaces to PascalCase."""
        assert to_pascal_case("my test app") == "MyTestApp"
        assert to_pascal_case("foo bar baz") == "FooBarBaz"

    def test_to_pascal_case_already_pascal(self):
        """Test that PascalCase remains unchanged."""
        assert to_pascal_case("MyTestApp") == "MyTestApp"
        assert to_pascal_case("FooBarBaz") == "FooBarBaz"

    def test_case_conversion_edge_cases(self):
        """Test edge cases for case conversion."""
        # Empty strings
        assert to_snake_case("") == ""
        assert to_kebab_case("") == ""
        assert to_pascal_case("") == ""

        # Single word
        assert to_snake_case("app") == "app"
        assert to_kebab_case("App") == "app"
        assert to_pascal_case("app") == "App"

        # With consecutive uppercase
        assert to_snake_case("HTTPServer") == "http_server"
        assert to_kebab_case("HTTPServer") == "http-server"
        assert to_pascal_case("http_server") == "HttpServer"


# ============================================================================
# TEST TEMPLATE REPOSITORY INITIALIZATION
# ============================================================================


class TestTemplateRepositoryInit:
    """Test TemplateRepository initialization."""

    def test_init_with_custom_dir(self, temp_templates_dir: Path):
        """Test initialization with custom templates directory."""
        repo = TemplateRepository(templates_dir=temp_templates_dir)
        assert repo.templates_dir == temp_templates_dir
        assert repo.env is not None

    def test_init_creates_dir_if_not_exists(self, tmp_path: Path):
        """Test that templates directory is created if it doesn't exist."""
        new_dir = tmp_path / "new_templates"
        assert not new_dir.exists()

        repo = TemplateRepository(templates_dir=new_dir)
        assert new_dir.exists()
        assert repo.templates_dir == new_dir

    def test_custom_filters_registered(self, repo: TemplateRepository):
        """Test that custom filters are registered in Jinja2 environment."""
        assert "to_snake_case" in repo.env.filters
        assert "to_kebab_case" in repo.env.filters
        assert "to_pascal_case" in repo.env.filters
        assert "snake_case" in repo.env.filters  # Alias
        assert "kebab_case" in repo.env.filters  # Alias
        assert "pascal_case" in repo.env.filters  # Alias


# ============================================================================
# TEST TEMPLATE RENDERING
# ============================================================================


class TestTemplateRendering:
    """Test template rendering methods."""

    def test_render_simple_template(self, repo: TemplateRepository, sample_config: TACConfig):
        """Test rendering a simple template."""
        result = repo.render("simple.txt.j2", sample_config)
        assert result == "Hello, my-test-app!"

    def test_render_template_with_filters(self, repo: TemplateRepository, sample_config: TACConfig):
        """Test rendering template with case conversion filters."""
        result = repo.render("with_filter.txt.j2", sample_config)
        assert "Snake: my_test_app" in result
        assert "Kebab: my-test-app" in result
        assert "Pascal: MyTestApp" in result

    def test_render_multiline_template(self, repo: TemplateRepository, sample_config: TACConfig):
        """Test rendering multiline template."""
        result = repo.render("multiline.txt.j2", sample_config)
        assert "Project: my-test-app" in result
        assert "Language: python" in result
        assert "Start: uv run python -m app" in result

    def test_render_nested_template(self, repo: TemplateRepository, sample_config: TACConfig):
        """Test rendering template in subdirectory."""
        result = repo.render("claude/settings.json.j2", sample_config)
        assert '"project_name": "my-test-app"' in result

    def test_render_template_not_found(self, repo: TemplateRepository, sample_config: TACConfig):
        """Test that TemplateNotFoundError is raised for missing template."""
        with pytest.raises(TemplateNotFoundError) as exc_info:
            repo.render("nonexistent.txt.j2", sample_config)

        assert "nonexistent.txt.j2" in str(exc_info.value)
        assert exc_info.value.template_name == "nonexistent.txt.j2"

    def test_render_string_simple(self, repo: TemplateRepository, sample_config: TACConfig):
        """Test rendering a simple template string."""
        result = repo.render_string("Project: {{ config.project.name }}", sample_config)
        assert result == "Project: my-test-app"

    def test_render_string_with_filter(self, repo: TemplateRepository, sample_config: TACConfig):
        """Test rendering template string with filter."""
        result = repo.render_string(
            "{{ config.project.name | snake_case }}",
            sample_config
        )
        assert result == "my_test_app"

    def test_render_string_multiline(self, repo: TemplateRepository, sample_config: TACConfig):
        """Test rendering multiline template string."""
        template_str = (
            "Name: {{ config.project.name }}\n"
            "Language: {{ config.project.language.value }}"
        )
        result = repo.render_string(template_str, sample_config)
        assert "Name: my-test-app" in result
        assert "Language: python" in result

    def test_render_string_syntax_error(self, repo: TemplateRepository, sample_config: TACConfig):
        """Test that TemplateRenderError is raised for syntax errors."""
        with pytest.raises(TemplateRenderError) as exc_info:
            repo.render_string("{{ config.project.name", sample_config)

        assert "<string>" in str(exc_info.value)


# ============================================================================
# TEST TEMPLATE DISCOVERY AND UTILITIES
# ============================================================================


class TestTemplateDiscovery:
    """Test template discovery and utility methods."""

    def test_template_exists_true(self, repo: TemplateRepository):
        """Test template_exists returns True for existing template."""
        assert repo.template_exists("simple.txt.j2") is True
        assert repo.template_exists("claude/settings.json.j2") is True

    def test_template_exists_false(self, repo: TemplateRepository):
        """Test template_exists returns False for missing template."""
        assert repo.template_exists("nonexistent.txt.j2") is False
        assert repo.template_exists("claude/missing.j2") is False

    def test_list_templates_all(self, repo: TemplateRepository):
        """Test listing all templates."""
        templates = repo.list_templates()

        # Should include all test templates
        assert "simple.txt.j2" in templates
        assert "with_filter.txt.j2" in templates
        assert "multiline.txt.j2" in templates
        assert "claude/settings.json.j2" in templates
        assert "adws/workflow.py.j2" in templates
        assert "scripts/setup.sh.j2" in templates

        # Should be sorted
        assert templates == sorted(templates)

    def test_list_templates_by_category(self, repo: TemplateRepository):
        """Test listing templates filtered by category."""
        claude_templates = repo.list_templates("claude")
        assert "claude/settings.json.j2" in claude_templates
        assert "adws/workflow.py.j2" not in claude_templates

        adws_templates = repo.list_templates("adws")
        assert "adws/workflow.py.j2" in adws_templates
        assert "claude/settings.json.j2" not in adws_templates

    def test_list_templates_nonexistent_category(self, repo: TemplateRepository):
        """Test listing templates for nonexistent category returns empty list."""
        templates = repo.list_templates("nonexistent")
        assert templates == []

    def test_list_templates_ignores_hidden_files(
        self, temp_templates_dir: Path, repo: TemplateRepository
    ):
        """Test that hidden files are ignored when listing templates."""
        # Create a hidden file
        (temp_templates_dir / ".hidden").write_text("hidden content")

        templates = repo.list_templates()
        assert ".hidden" not in templates

    def test_get_template_content(self, repo: TemplateRepository):
        """Test getting raw template content."""
        content = repo.get_template_content("simple.txt.j2")
        assert content == "Hello, {{ config.project.name }}!"

    def test_get_template_content_multiline(self, repo: TemplateRepository):
        """Test getting raw content of multiline template."""
        content = repo.get_template_content("multiline.txt.j2")
        assert "Project: {{ config.project.name }}" in content
        assert "Language: {{ config.project.language.value }}" in content

    def test_get_template_content_not_found(self, repo: TemplateRepository):
        """Test that TemplateNotFoundError is raised for missing template."""
        with pytest.raises(TemplateNotFoundError) as exc_info:
            repo.get_template_content("nonexistent.txt.j2")

        assert "nonexistent.txt.j2" in str(exc_info.value)


# ============================================================================
# TEST AUTOESCAPE CONFIGURATION
# ============================================================================


class TestAutoescape:
    """Test autoescape configuration for different file types."""

    def test_autoescape_disabled_for_code_templates(self, temp_templates_dir: Path):
        """Test that autoescape is disabled for code templates."""
        # Create templates with special characters
        (temp_templates_dir / "code.py.j2").write_text("value = '{{ config.data }}'")
        (temp_templates_dir / "code.js.j2").write_text("const value = '{{ config.data }}';")

        repo = TemplateRepository(templates_dir=temp_templates_dir)

        # Mock context with HTML special characters
        class MockContext:
            data = "<script>alert('test')</script>"

        context = MockContext()

        # Code templates should NOT autoescape
        py_result = repo.render("code.py.j2", context)
        assert "<script>alert('test')</script>" in py_result

        js_result = repo.render("code.js.j2", context)
        assert "<script>alert('test')</script>" in js_result

    def test_autoescape_enabled_for_html_templates(self, temp_templates_dir: Path):
        """Test that autoescape is enabled for HTML templates."""
        (temp_templates_dir / "page.html").write_text("<div>{{ config.data }}</div>")

        repo = TemplateRepository(templates_dir=temp_templates_dir)

        class MockContext:
            data = "<script>alert('test')</script>"

        context = MockContext()

        # HTML templates SHOULD autoescape
        result = repo.render("page.html", context)
        assert "&lt;script&gt;" in result
        assert "&lt;/script&gt;" in result


# ============================================================================
# TEST ERROR MESSAGES
# ============================================================================


class TestErrorMessages:
    """Test that error messages are descriptive and helpful."""

    def test_template_not_found_error_message(
        self, repo: TemplateRepository, sample_config: TACConfig
    ):
        """Test that TemplateNotFoundError has helpful message."""
        with pytest.raises(TemplateNotFoundError) as exc_info:
            repo.render("missing/template.j2", sample_config)

        error_msg = str(exc_info.value)
        assert "missing/template.j2" in error_msg
        assert "not found" in error_msg.lower()
        # Should include search paths
        assert str(repo.templates_dir) in error_msg

    def test_template_render_error_message(
        self, repo: TemplateRepository, sample_config: TACConfig
    ):
        """Test that TemplateRenderError has helpful message."""
        # Create template with undefined variable
        invalid_template = "{{ config.nonexistent.field }}"

        with pytest.raises(TemplateRenderError) as exc_info:
            repo.render_string(invalid_template, sample_config)

        error_msg = str(exc_info.value)
        assert "failed to render" in error_msg.lower() or "render" in error_msg.lower()
        assert "<string>" in error_msg
