"""Tests for the Enhanced Documentation Generator (Feature 8).

Comprehensive test suite covering docs generator, docs templates,
Mermaid diagram generation, ADR creation, and documentation serving.
"""

from pathlib import Path
from typing import Any, Dict

import pytest

from tac_bootstrap.application.docs_generator import DocsGenerator
from tac_bootstrap.infrastructure.docs_templates import DocsTemplates


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def docs_generator() -> DocsGenerator:
    """Create a DocsGenerator instance."""
    return DocsGenerator(
        project_name="test-project",
        language="python",
        framework="fastapi",
        architecture="ddd",
    )


@pytest.fixture
def simple_generator() -> DocsGenerator:
    """Create a simple architecture DocsGenerator."""
    return DocsGenerator(
        project_name="simple-app",
        language="python",
        framework="none",
        architecture="simple",
    )


@pytest.fixture
def project_dir(tmp_path: Path) -> Path:
    """Create a temporary project directory."""
    return tmp_path


# ============================================================================
# TEST DOCS TEMPLATES
# ============================================================================


class TestDocsTemplates:
    """Tests for DocsTemplates static methods."""

    def test_adr_template(self):
        """ADR template should contain all sections."""
        adr = DocsTemplates.adr_template(
            number=1,
            title="Use PostgreSQL",
            status="Accepted",
            context="We need a database",
            decision="Use PostgreSQL",
            consequences="Good performance",
            date="2024-01-15",
        )
        assert "ADR-0001" in adr
        assert "Use PostgreSQL" in adr
        assert "Accepted" in adr
        assert "We need a database" in adr
        assert "2024-01-15" in adr

    def test_adr_template_numbering(self):
        """ADR numbering should be zero-padded."""
        adr = DocsTemplates.adr_template(number=42, title="Test", date="2024-01-01")
        assert "ADR-0042" in adr

    def test_api_docs_template(self):
        """API docs template should contain project name and endpoints."""
        docs = DocsTemplates.api_docs_template(
            project_name="MyAPI",
            base_url="http://localhost:3000",
        )
        assert "MyAPI" in docs
        assert "http://localhost:3000" in docs
        assert "GET" in docs

    def test_api_docs_template_custom_endpoints(self):
        """API docs should include custom endpoints."""
        endpoints = [
            {"method": "POST", "path": "/api/users", "description": "Create user"},
        ]
        docs = DocsTemplates.api_docs_template(
            project_name="MyAPI",
            endpoints=endpoints,
        )
        assert "POST /api/users" in docs
        assert "Create user" in docs

    def test_architecture_docs_template(self):
        """Architecture docs should contain project details."""
        docs = DocsTemplates.architecture_docs_template(
            project_name="MyApp",
            architecture="ddd",
            language="python",
            framework="fastapi",
        )
        assert "MyApp" in docs
        assert "python" in docs
        assert "fastapi" in docs
        assert "ddd" in docs

    def test_component_diagram(self):
        """Component diagram should be valid Mermaid."""
        diagram = DocsTemplates.component_diagram("MyApp")
        assert "```mermaid" in diagram
        assert "graph TB" in diagram
        assert "MyApp" in diagram

    def test_component_diagram_custom(self):
        """Component diagram should accept custom components."""
        components = ["Auth", "Users", "Products"]
        diagram = DocsTemplates.component_diagram("MyApp", components=components)
        assert "Auth" in diagram
        assert "Users" in diagram
        assert "Products" in diagram

    def test_data_flow_diagram(self):
        """Data flow diagram should be valid Mermaid."""
        diagram = DocsTemplates.data_flow_diagram("MyApp")
        assert "```mermaid" in diagram
        assert "flowchart" in diagram

    def test_architecture_diagram_ddd(self):
        """DDD architecture diagram should have domain layer."""
        diagram = DocsTemplates.architecture_diagram("ddd")
        assert "Domain Layer" in diagram
        assert "Application Layer" in diagram

    def test_architecture_diagram_hexagonal(self):
        """Hexagonal architecture diagram should have ports."""
        diagram = DocsTemplates.architecture_diagram("hexagonal")
        assert "Input Port" in diagram
        assert "Output Port" in diagram

    def test_architecture_diagram_simple(self):
        """Simple architecture diagram should be basic."""
        diagram = DocsTemplates.architecture_diagram("simple")
        assert "```mermaid" in diagram

    def test_deployment_guide(self):
        """Deployment guide should contain project name."""
        guide = DocsTemplates.deployment_guide("MyApp", language="python")
        assert "MyApp" in guide
        assert "Docker" in guide
        assert "Environment Variables" in guide

    def test_contributing_guide(self):
        """Contributing guide should contain project name."""
        guide = DocsTemplates.contributing_guide("MyApp")
        assert "MyApp" in guide
        assert "Pull Request" in guide
        assert "Getting Started" in guide


# ============================================================================
# TEST DOCS GENERATOR
# ============================================================================


class TestDocsGenerator:
    """Tests for DocsGenerator application service."""

    def test_generator_initialization(self, docs_generator: DocsGenerator):
        """Generator should store configuration."""
        assert docs_generator.project_name == "test-project"
        assert docs_generator.language == "python"
        assert docs_generator.framework == "fastapi"
        assert docs_generator.architecture == "ddd"

    def test_generate_all(self, docs_generator: DocsGenerator, project_dir: Path):
        """generate_all should create all documentation files."""
        files = docs_generator.generate_all(project_dir)
        assert len(files) >= 5  # api, arch, deploy, contrib, + diagrams + ADR

        # Check that files exist
        docs_dir = project_dir / "docs"
        assert (docs_dir / "api.md").exists()
        assert (docs_dir / "architecture.md").exists()
        assert (docs_dir / "deployment.md").exists()
        assert (docs_dir / "contributing.md").exists()

    def test_generate_all_creates_adr(self, docs_generator: DocsGenerator, project_dir: Path):
        """generate_all should create initial ADR."""
        docs_generator.generate_all(project_dir)
        adr_dir = project_dir / "docs" / "adr"
        assert adr_dir.is_dir()
        assert (adr_dir / "0001-initial-architecture.md").exists()

    def test_generate_all_no_overwrite(self, docs_generator: DocsGenerator, project_dir: Path):
        """generate_all should not overwrite without force."""
        docs_generator.generate_all(project_dir)
        first_count = len(list((project_dir / "docs").rglob("*.md")))

        # Call again without force - should not create duplicates
        files = docs_generator.generate_all(project_dir, force=False)
        assert len(files) == 0  # No new files created

    def test_generate_all_force_overwrite(self, docs_generator: DocsGenerator, project_dir: Path):
        """generate_all with force should overwrite existing files."""
        docs_generator.generate_all(project_dir)
        files = docs_generator.generate_all(project_dir, force=True)
        assert len(files) >= 5

    def test_generate_api_docs(self, docs_generator: DocsGenerator):
        """generate_api_docs should return markdown string."""
        content = docs_generator.generate_api_docs()
        assert "test-project" in content
        assert "API" in content

    def test_generate_architecture_docs(self, docs_generator: DocsGenerator):
        """generate_architecture_docs should include embedded diagrams."""
        content = docs_generator.generate_architecture_docs()
        assert "Architecture" in content
        assert "```mermaid" in content  # Should include diagrams
        assert "Component Diagram" in content

    def test_generate_adr(self, docs_generator: DocsGenerator):
        """generate_adr should produce valid ADR markdown."""
        adr = docs_generator.generate_adr(
            decision="Use PostgreSQL for data storage",
            context="Need a relational database",
            consequence="Better query performance",
        )
        assert "ADR-0001" in adr
        assert "Use PostgreSQL" in adr

    def test_generate_adr_custom_number(self, docs_generator: DocsGenerator):
        """generate_adr should accept custom number."""
        adr = docs_generator.generate_adr(
            decision="Add caching",
            context="Performance",
            consequence="Faster responses",
            number=42,
        )
        assert "ADR-0042" in adr

    def test_generate_diagrams(self, docs_generator: DocsGenerator, project_dir: Path):
        """generate_diagrams should create diagram files."""
        diagrams_dir = project_dir / "diagrams"
        files = docs_generator.generate_diagrams(diagrams_dir)
        assert len(files) == 3
        assert all(f.exists() for f in files)

    def test_generate_component_diagram(self, docs_generator: DocsGenerator):
        """generate_component_diagram should produce Mermaid output."""
        diagram = docs_generator.generate_component_diagram()
        assert "```mermaid" in diagram

    def test_generate_data_flow_diagram(self, docs_generator: DocsGenerator):
        """generate_data_flow_diagram should produce Mermaid output."""
        diagram = docs_generator.generate_data_flow_diagram()
        assert "```mermaid" in diagram
        assert "flowchart" in diagram

    def test_generate_architecture_diagram(self, docs_generator: DocsGenerator):
        """generate_architecture_diagram should use project's architecture."""
        diagram = docs_generator.generate_architecture_diagram()
        assert "```mermaid" in diagram
        assert "Domain" in diagram  # DDD architecture

    def test_simple_architecture_diagram(self, simple_generator: DocsGenerator):
        """Simple architecture should produce basic diagram."""
        diagram = simple_generator.generate_architecture_diagram()
        assert "```mermaid" in diagram

    def test_get_next_adr_number_empty(self, docs_generator: DocsGenerator, project_dir: Path):
        """Next ADR number should be 1 for empty directory."""
        docs_dir = project_dir / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        assert docs_generator.get_next_adr_number(docs_dir) == 1

    def test_get_next_adr_number_existing(self, docs_generator: DocsGenerator, project_dir: Path):
        """Next ADR number should increment from existing."""
        adr_dir = project_dir / "docs" / "adr"
        adr_dir.mkdir(parents=True, exist_ok=True)
        (adr_dir / "0001-first.md").write_text("ADR 1")
        (adr_dir / "0002-second.md").write_text("ADR 2")

        assert docs_generator.get_next_adr_number(project_dir / "docs") == 3

    def test_generate_all_without_diagrams(self, docs_generator: DocsGenerator, project_dir: Path):
        """generate_all with with_diagrams=False should skip diagrams."""
        files = docs_generator.generate_all(project_dir, with_diagrams=False)
        diagram_files = [f for f in files if "diagram" in f.name]
        assert len(diagram_files) == 0

    def test_generator_with_config(self, project_dir: Path):
        """Generator should extract values from config object."""

        class MockProject:
            name = "config-project"
            language = type("L", (), {"value": "typescript"})()
            framework = type("F", (), {"value": "nextjs"})()
            architecture = type("A", (), {"value": "hexagonal"})()

        class MockConfig:
            project = MockProject()
            orchestrator = type("O", (), {"api_base_url": "http://localhost:3000"})()

        gen = DocsGenerator(config=MockConfig())
        assert gen.project_name == "config-project"
        assert gen.language == "typescript"
        assert gen.framework == "nextjs"
        assert gen.architecture == "hexagonal"
