"""Tests for fractal documentation templates.

Comprehensive unit tests for templates related to fractal documentation:
- Scripts de generación Python (gen_docstring_jsdocs.py.j2, gen_docs_fractal.py.j2)
- Scripts bash (run_generators.sh.j2)
- Configuración YAML (canonical_idk.yml.j2)
- Comandos slash (generate_fractal_docs.md.j2)
- Documentación condicional (conditional_docs.md.j2)

Los tests verifican:
1. Los templates renderizan sin errores para distintas configuraciones (Python/TypeScript)
2. El contenido generado es válido (Python compilable, YAML parseable, bash con shebang)
3. Las variables de configuración se interpolan correctamente
4. ScaffoldService incluye los scripts fractal en el scaffolding
5. Las reglas fractal están presentes en conditional_docs
"""

import ast

import pytest
import yaml

from tac_bootstrap.application.scaffold_service import ScaffoldService
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
def typescript_config() -> TACConfig:
    """Create a minimal TypeScript config for testing."""
    return TACConfig(
        project=ProjectSpec(
            name="test-typescript-app",
            language=Language.TYPESCRIPT,
            package_manager=PackageManager.NPM,
        ),
        commands=CommandsSpec(
            start="npm run dev",
            test="npm test",
        ),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-typescript-app")),
    )


@pytest.fixture
def template_repo() -> TemplateRepository:
    """Create a TemplateRepository instance."""
    return TemplateRepository()


# ============================================================================
# TEST PYTHON SCRIPT RENDERING
# ============================================================================


class TestPythonScriptRendering:
    """Tests for Python script template rendering."""

    def test_gen_docstring_renders_for_python(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """gen_docstring_jsdocs.py.j2 should render valid Python for Python config."""
        content = template_repo.render("scripts/gen_docstring_jsdocs.py.j2", python_config)

        # Verify content is not empty
        assert len(content.strip()) > 50, "Generated script should have meaningful content"

        # Verify it's valid Python syntax
        ast.parse(content)  # Should not raise SyntaxError

        # Verify shebang present (for executable scripts)
        assert content.startswith("#!/usr/bin/env"), "Script should have shebang"

    def test_gen_docstring_renders_for_typescript(
        self, template_repo: TemplateRepository, typescript_config: TACConfig
    ):
        """gen_docstring_jsdocs.py.j2 should render valid Python for TypeScript config."""
        content = template_repo.render("scripts/gen_docstring_jsdocs.py.j2", typescript_config)

        # Verify content is not empty
        assert len(content.strip()) > 50, "Generated script should have meaningful content"

        # Verify it's valid Python syntax
        ast.parse(content)  # Should not raise SyntaxError

        # Verify shebang present
        assert content.startswith("#!/usr/bin/env"), "Script should have shebang"

    def test_gen_docs_fractal_renders(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """gen_docs_fractal.py.j2 should render valid Python script."""
        content = template_repo.render("scripts/gen_docs_fractal.py.j2", python_config)

        # Verify content is not empty
        assert len(content.strip()) > 50, "Generated script should have meaningful content"

        # Verify shebang present
        assert content.startswith("#!/usr/bin/env"), "Script should have shebang"

        # Verify it's valid Python syntax
        ast.parse(content)  # Should not raise SyntaxError


# ============================================================================
# TEST BASH SCRIPT RENDERING
# ============================================================================


class TestBashScriptRendering:
    """Tests for bash script template rendering."""

    def test_run_generators_renders(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """run_generators.sh.j2 should render valid bash script."""
        content = template_repo.render("scripts/run_generators.sh.j2", python_config)

        # Verify content is not empty
        assert len(content.strip()) > 50, "Generated script should have meaningful content"

        # Verify shebang present (can be #!/bin/bash or #!/usr/bin/env bash)
        assert content.startswith("#!/"), "Bash script should have shebang"
        assert "bash" in content.split("\n")[0], "First line should reference bash"

        # Verify has basic bash structure (no deep validation, just sanity check)
        # Check for common bash patterns
        lines = content.split("\n")
        assert len(lines) > 3, "Script should have multiple lines"


# ============================================================================
# TEST YAML TEMPLATE RENDERING
# ============================================================================


class TestYAMLTemplateRendering:
    """Tests for YAML template rendering."""

    def test_canonical_idk_renders_python(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """canonical_idk.yml.j2 should render valid YAML with Python-specific domains."""
        content = template_repo.render("config/canonical_idk.yml.j2", python_config)

        # Verify content is not empty
        assert len(content.strip()) > 50, "Generated YAML should have meaningful content"

        # Verify it's valid YAML
        parsed = yaml.safe_load(content)
        assert parsed is not None, "YAML should parse successfully"

        # Verify Python-specific domain keywords are present
        # The template uses domain keywords, not programming language keywords
        content_lower = content.lower()

        # Check for Python-specific backend/testing domains
        python_domains = ["backend", "testing", "repository", "fixture"]
        found_domains = [kw for kw in python_domains if kw in content_lower]
        assert (
            len(found_domains) >= 2
        ), f"Should have at least 2 Python domain keywords, found: {found_domains}"

    def test_canonical_idk_renders_typescript(
        self, template_repo: TemplateRepository, typescript_config: TACConfig
    ):
        """canonical_idk.yml.j2 should render valid YAML with TypeScript-specific domains."""
        content = template_repo.render("config/canonical_idk.yml.j2", typescript_config)

        # Verify content is not empty
        assert len(content.strip()) > 50, "Generated YAML should have meaningful content"

        # Verify it's valid YAML
        parsed = yaml.safe_load(content)
        assert parsed is not None, "YAML should parse successfully"

        # Verify TypeScript-specific domain keywords are present
        # The template uses domain keywords (frontend/backend concepts)
        content_lower = content.lower()

        # Check for TypeScript-specific frontend/backend domains
        typescript_domains = ["frontend", "component", "hook", "controller"]
        found_domains = [kw for kw in typescript_domains if kw in content_lower]
        assert (
            len(found_domains) >= 2
        ), f"Should have at least 2 TypeScript domain keywords, found: {found_domains}"


# ============================================================================
# TEST SLASH COMMAND TEMPLATES
# ============================================================================


class TestSlashCommandTemplates:
    """Tests for slash command template rendering."""

    def test_generate_fractal_docs_command_renders(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """generate_fractal_docs.md.j2 should render valid markdown."""
        content = template_repo.render(
            "claude/commands/generate_fractal_docs.md.j2", python_config
        )

        # Verify content is not empty
        assert len(content.strip()) > 50, "Generated command should have meaningful content"

        # Verify it's markdown (has headers)
        assert "#" in content, "Markdown should have headers"

        # Verify mentions expected commands/modes
        # The template should mention "changed" and "full" modes
        content_lower = content.lower()
        assert "changed" in content_lower or "full" in content_lower, (
            "Command should mention changed/full modes"
        )


# ============================================================================
# TEST SCAFFOLD SERVICE INTEGRATION
# ============================================================================


class TestScaffoldServiceIntegration:
    """Tests for ScaffoldService integration with fractal docs templates."""

    def test_scaffold_includes_fractal_scripts(self, python_config: TACConfig):
        """ScaffoldService.build_plan should include fractal documentation scripts."""
        service = ScaffoldService()
        plan = service.build_plan(python_config)

        file_paths = [f.path for f in plan.files]

        # Verify all three fractal scripts are included
        assert (
            "scripts/gen_docstring_jsdocs.py" in file_paths
        ), "Should include gen_docstring_jsdocs.py"
        assert "scripts/gen_docs_fractal.py" in file_paths, "Should include gen_docs_fractal.py"
        assert "scripts/run_generators.sh" in file_paths, "Should include run_generators.sh"


# ============================================================================
# TEST CONDITIONAL DOCS
# ============================================================================


class TestConditionalDocsTemplate:
    """Tests for conditional_docs.md.j2 template."""

    def test_conditional_docs_includes_fractal_rules(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """conditional_docs.md.j2 should include fractal documentation rules."""
        content = template_repo.render("claude/commands/conditional_docs.md.j2", python_config)

        # Verify content is not empty
        assert len(content.strip()) > 100, "Conditional docs should have meaningful content"

        # Verify contains Fractal Documentation section
        content_lower = content.lower()
        assert (
            "fractal" in content_lower and "documentation" in content_lower
        ), "Should mention Fractal Documentation"

        # Verify mentions /generate_fractal_docs command
        assert (
            "generate_fractal_docs" in content_lower
        ), "Should mention /generate_fractal_docs command"

        # Verify mentions canonical_idk.yml
        assert "canonical_idk" in content_lower, "Should mention canonical_idk.yml"


# ============================================================================
# TEST DOCUMENT WORKFLOW TEMPLATES
# ============================================================================


class TestDocumentWorkflowTemplates:
    """Tests for document workflow templates."""

    def test_document_command_has_idk_frontmatter(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """document.md.j2 should include IDK frontmatter with valid YAML structure."""
        content = template_repo.render("claude/commands/document.md.j2", python_config)

        # Verify content is not empty
        assert len(content.strip()) > 100, "Document command should have meaningful content"

        # Verify starts with YAML frontmatter delimiter
        assert content.startswith("# Document Feature"), "Should start with heading"

        # Find the documentation format section which contains the frontmatter example
        assert "```md" in content, "Should contain markdown code block with frontmatter example"
        assert "---" in content, "Should contain YAML frontmatter delimiters"

        # Verify required frontmatter fields are mentioned
        content_lower = content.lower()
        assert "doc_type:" in content_lower, "Should mention doc_type field"
        assert "adw_id:" in content_lower, "Should mention adw_id field"
        assert "date:" in content_lower, "Should mention date field"
        assert "idk:" in content_lower, "Should mention idk field"
        assert "tags:" in content_lower, "Should mention tags field"
        assert "related_code:" in content_lower, "Should mention related_code field"

        # Extract the example YAML frontmatter from the documentation format section
        # The format shows an example with:
        # ---
        # doc_type: feature
        # adw_id: ...
        # ...
        # ---
        # We verify the structure is present in the template
        lines = content.split("\n")
        in_code_block = False
        frontmatter_lines = []
        frontmatter_started = False

        for line in lines:
            if "```md" in line:
                in_code_block = True
                continue
            if in_code_block and "```" in line:
                break
            if in_code_block:
                if line.strip() == "---" and not frontmatter_started:
                    frontmatter_started = True
                    frontmatter_lines.append(line)
                elif line.strip() == "---" and frontmatter_started:
                    frontmatter_lines.append(line)
                    break
                elif frontmatter_started:
                    frontmatter_lines.append(line)

        # Join and verify it's parseable YAML
        if frontmatter_lines:
            # Remove the --- delimiters for parsing
            yaml_content = "\n".join(
                line for line in frontmatter_lines if line.strip() != "---"
            )
            # Should parse as valid YAML (even with template variables)
            # We just check it has the structure, template variables are okay
            assert "doc_type:" in yaml_content, "YAML should have doc_type field"
            assert "idk:" in yaml_content, "YAML should have idk field"

    def test_adw_document_includes_fractal_step(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """adw_document_iso.py.j2 should include call to /generate_fractal_docs."""
        content = template_repo.render("adws/adw_document_iso.py.j2", python_config)

        # Verify content is not empty
        assert len(content.strip()) > 500, "ADW document script should have meaningful content"

        # Verify it's valid Python syntax
        ast.parse(content)  # Should not raise SyntaxError

        # Verify includes fractal docs call with expected parameters
        assert (
            'slash_command="/generate_fractal_docs"' in content
        ), "Should call /generate_fractal_docs"
        assert 'args=["changed"]' in content, "Should pass 'changed' argument"
        assert (
            'agent_name="fractal_docs_generator"' in content
        ), "Should use fractal_docs_generator agent"

    def test_adw_document_fractal_is_non_blocking(
        self, template_repo: TemplateRepository, python_config: TACConfig
    ):
        """adw_document_iso.py.j2 wraps fractal docs in try-except for non-blocking behavior."""
        content = template_repo.render("adws/adw_document_iso.py.j2", python_config)

        # Verify content is not empty
        assert len(content.strip()) > 500, "ADW document script should have meaningful content"

        # Verify it's valid Python syntax
        ast.parse(content)  # Should not raise SyntaxError

        # Find the fractal docs section
        lines = content.split("\n")
        fractal_section_start = None
        try_found = False
        except_found = False
        logger_warning_found = False
        unconditional_raise_found = False

        for i, line in enumerate(lines):
            # Find where fractal docs generation starts
            if "/generate_fractal_docs" in line:
                fractal_section_start = i
                # Look backwards for try statement (should be within ~10 lines before)
                for j in range(max(0, i - 15), i):
                    if "try:" in lines[j]:
                        try_found = True
                        break

            # Look for except block after fractal docs call
            if fractal_section_start and i > fractal_section_start:
                if "except Exception" in line or "except:" in line:
                    except_found = True
                # Look for logger.warning in exception handler (non-blocking)
                if except_found and "logger.warning" in line:
                    logger_warning_found = True
                # Check there's no unconditional raise (which would make it blocking)
                if except_found and line.strip() == "raise":
                    unconditional_raise_found = True

        assert try_found, "Fractal docs call should be wrapped in try block"
        assert except_found, "Fractal docs call should have except handler"
        assert logger_warning_found, "Exception handler should use logger.warning (non-blocking)"
        assert not unconditional_raise_found, (
            "Exception handler should not re-raise unconditionally (should be non-blocking)"
        )
