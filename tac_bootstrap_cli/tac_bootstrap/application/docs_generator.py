"""
IDK: documentation-generation, api-docs, architecture-docs, adr-generator, diagram-generator
Responsibility: Auto-generates comprehensive project documentation including API docs,
                architecture docs, ADRs, Mermaid diagrams, and guides
Invariants: Generated docs are idempotent, output is pure markdown, diagrams use Mermaid syntax,
            all operations are filesystem-safe
"""

import http.server
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from tac_bootstrap.infrastructure.docs_templates import DocsTemplates

# ============================================================================
# DOCS GENERATOR
# ============================================================================


class DocsGenerator:
    """
    IDK: doc-generator, doc-orchestrator, markdown-writer, diagram-renderer
    Responsibility: Orchestrates generation of all documentation types for a project,
                    including API docs, architecture docs, ADRs, Mermaid diagrams,
                    and operational guides
    Invariants: All output is valid markdown, docs directory is created if missing,
                existing docs are not overwritten without force flag,
                diagrams use Mermaid syntax compatible with GitHub/GitLab
    """

    def __init__(
        self,
        project_name: str = "",
        language: str = "python",
        framework: str = "none",
        architecture: str = "simple",
        config: Any = None,
    ) -> None:
        """
        Initialize DocsGenerator.

        Args:
            project_name: Name of the project
            language: Programming language
            framework: Framework used
            architecture: Architecture pattern
            config: Optional TACConfig instance for richer documentation
        """
        self.project_name = project_name
        self.language = language
        self.framework = framework
        self.architecture = architecture
        self.config = config

        # Extract config values if available
        if config is not None:
            if hasattr(config, "project"):
                self.project_name = self.project_name or config.project.name
                self.language = config.project.language.value
                self.framework = config.project.framework.value
                self.architecture = config.project.architecture.value

    def generate_all(
        self,
        project_path: Path,
        force: bool = False,
        with_diagrams: bool = True,
    ) -> List[Path]:
        """
        Generate all documentation files.

        Creates a docs/ directory with comprehensive documentation including
        API docs, architecture docs, deployment guide, and contributing guide.

        Args:
            project_path: Root path of the project
            force: Overwrite existing files if True
            with_diagrams: Include Mermaid diagrams if True

        Returns:
            List of paths to generated documentation files
        """
        docs_dir = project_path / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)

        generated: List[Path] = []

        # API Documentation
        api_path = docs_dir / "api.md"
        if force or not api_path.exists():
            content = self.generate_api_docs()
            api_path.write_text(content, encoding="utf-8")
            generated.append(api_path)

        # Architecture Documentation
        arch_path = docs_dir / "architecture.md"
        if force or not arch_path.exists():
            content = self.generate_architecture_docs()
            arch_path.write_text(content, encoding="utf-8")
            generated.append(arch_path)

        # Deployment Guide
        deploy_path = docs_dir / "deployment.md"
        if force or not deploy_path.exists():
            content = DocsTemplates.deployment_guide(
                project_name=self.project_name,
                language=self.language,
            )
            deploy_path.write_text(content, encoding="utf-8")
            generated.append(deploy_path)

        # Contributing Guide
        contrib_path = docs_dir / "contributing.md"
        if force or not contrib_path.exists():
            content = DocsTemplates.contributing_guide(
                project_name=self.project_name,
            )
            contrib_path.write_text(content, encoding="utf-8")
            generated.append(contrib_path)

        # Diagrams
        if with_diagrams:
            diagram_paths = self.generate_diagrams(docs_dir, force=force)
            generated.extend(diagram_paths)

        # ADR directory
        adr_dir = docs_dir / "adr"
        adr_dir.mkdir(exist_ok=True)

        # Generate initial ADR
        adr_path = adr_dir / "0001-initial-architecture.md"
        if force or not adr_path.exists():
            content = self.generate_adr(
                decision=f"Use {self.architecture} architecture with {self.framework}",
                context=f"Setting up {self.project_name} project architecture. "
                f"Need to choose an appropriate architecture pattern for a "
                f"{self.language} project using {self.framework}.",
                consequence=f"The project will follow {self.architecture} architecture patterns, "
                f"providing clear separation of concerns and maintainability.",
                number=1,
            )
            adr_path.write_text(content, encoding="utf-8")
            generated.append(adr_path)

        return generated

    def generate_api_docs(
        self,
        endpoints: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Generate API documentation.

        Args:
            endpoints: Optional list of endpoint definitions

        Returns:
            API documentation as markdown string
        """
        base_url = "http://localhost:8000"
        if self.config and hasattr(self.config, "orchestrator"):
            base_url = self.config.orchestrator.api_base_url

        return DocsTemplates.api_docs_template(
            project_name=self.project_name,
            base_url=base_url,
            endpoints=endpoints,
        )

    def generate_architecture_docs(self) -> str:
        """
        Generate architecture documentation with embedded diagrams.

        Returns:
            Architecture documentation as markdown string
        """
        arch_doc = DocsTemplates.architecture_docs_template(
            project_name=self.project_name,
            architecture=self.architecture,
            language=self.language,
            framework=self.framework,
        )

        # Append architecture diagram
        arch_doc += "\n## Architecture Diagram\n\n"
        arch_doc += DocsTemplates.architecture_diagram(self.architecture)
        arch_doc += "\n\n"

        # Append component diagram
        arch_doc += "## Component Diagram\n\n"
        arch_doc += DocsTemplates.component_diagram(self.project_name)
        arch_doc += "\n\n"

        # Append data flow diagram
        arch_doc += "## Data Flow\n\n"
        arch_doc += DocsTemplates.data_flow_diagram(self.project_name)
        arch_doc += "\n"

        return arch_doc

    def generate_adr(
        self,
        decision: str,
        context: str,
        consequence: str,
        number: Optional[int] = None,
        status: str = "Accepted",
    ) -> str:
        """
        Generate an Architecture Decision Record.

        Args:
            decision: The decision made
            context: Context and problem statement
            consequence: Consequences of the decision
            number: ADR number (auto-incremented if not specified)
            status: Decision status

        Returns:
            ADR as markdown string
        """
        if number is None:
            number = 1  # Default to 1; caller can manage auto-increment

        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        return DocsTemplates.adr_template(
            number=number,
            title=decision,
            status=status,
            context=context,
            decision=decision,
            consequences=consequence,
            date=date,
        )

    def generate_diagrams(
        self,
        output_dir: Path,
        force: bool = False,
    ) -> List[Path]:
        """
        Generate all Mermaid diagram files.

        Creates separate markdown files for each diagram type.

        Args:
            output_dir: Directory to write diagram files
            force: Overwrite existing files

        Returns:
            List of paths to generated diagram files
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        generated: List[Path] = []

        diagrams = {
            "component-diagram.md": self.generate_component_diagram(),
            "data-flow-diagram.md": self.generate_data_flow_diagram(),
            "architecture-diagram.md": self.generate_architecture_diagram(),
        }

        for filename, content in diagrams.items():
            file_path = output_dir / filename
            if force or not file_path.exists():
                full_content = f"# {filename.replace('-', ' ').replace('.md', '').title()}\n\n"
                full_content += content + "\n"
                file_path.write_text(full_content, encoding="utf-8")
                generated.append(file_path)

        return generated

    def generate_component_diagram(self) -> str:
        """
        Generate a Mermaid component diagram.

        Returns:
            Mermaid diagram string
        """
        return DocsTemplates.component_diagram(self.project_name)

    def generate_data_flow_diagram(self) -> str:
        """
        Generate a Mermaid data flow diagram.

        Returns:
            Mermaid diagram string
        """
        return DocsTemplates.data_flow_diagram(self.project_name)

    def generate_architecture_diagram(self) -> str:
        """
        Generate a Mermaid architecture diagram based on project pattern.

        Returns:
            Mermaid diagram string
        """
        return DocsTemplates.architecture_diagram(self.architecture)

    def serve_docs(self, docs_dir: Path, port: int = 3000) -> None:
        """
        Serve documentation locally using a simple HTTP server.

        Args:
            docs_dir: Directory containing documentation files
            port: Port to serve on (default: 3000)
        """
        import os

        os.chdir(str(docs_dir))

        handler = http.server.SimpleHTTPRequestHandler
        server = http.server.HTTPServer(("localhost", port), handler)

        print(f"Serving docs at http://localhost:{port}")
        print("Press Ctrl+C to stop")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
            server.shutdown()

    def get_next_adr_number(self, docs_dir: Path) -> int:
        """
        Get the next ADR number based on existing ADRs.

        Args:
            docs_dir: Documentation directory containing adr/ subdirectory

        Returns:
            Next available ADR number
        """
        adr_dir = docs_dir / "adr"
        if not adr_dir.is_dir():
            return 1

        existing = list(adr_dir.glob("*.md"))
        if not existing:
            return 1

        max_number = 0
        for file in existing:
            try:
                # Extract number from filename like "0001-title.md"
                num_str = file.stem.split("-")[0]
                num = int(num_str)
                max_number = max(max_number, num)
            except (ValueError, IndexError):
                continue

        return max_number + 1
