"""
IDK: template-repository, jinja2-rendering, case-conversion, template-discovery
Responsibility: Manages Jinja2 template loading, rendering, and custom filters
Invariants: Templates are immutable, rendering is idempotent, filters are stateless
"""

import re
from pathlib import Path
from typing import Any, List, Optional

from jinja2 import (
    Environment,
    FileSystemLoader,
    TemplateSyntaxError,
)
from jinja2 import (
    TemplateNotFound as Jinja2TemplateNotFound,
)

# ============================================================================
# EXCEPTIONS
# ============================================================================


class TemplateNotFoundError(Exception):
    """Raised when a template file cannot be found."""

    def __init__(self, template_name: str, search_paths: List[str]):
        self.template_name = template_name
        self.search_paths = search_paths
        paths_str = "\n  ".join(search_paths)
        super().__init__(f"Template '{template_name}' not found in:\n  {paths_str}")


class TemplateRenderError(Exception):
    """Raised when template rendering fails."""

    def __init__(self, template_name: str, original_error: Exception):
        self.template_name = template_name
        self.original_error = original_error
        super().__init__(f"Failed to render template '{template_name}': {str(original_error)}")


# ============================================================================
# CASE CONVERSION FILTERS
# ============================================================================


def to_snake_case(value: str) -> str:
    """
    Convert string to snake_case.

    Examples:
        "MyProject" -> "my_project"
        "my-project" -> "my_project"
        "My Project" -> "my_project"
        "myProject" -> "my_project"

    Args:
        value: Input string

    Returns:
        snake_case version of the string
    """
    # Replace hyphens and spaces with underscores
    value = value.replace("-", "_").replace(" ", "_")

    # Insert underscore before uppercase letters that follow lowercase letters
    # or that are followed by lowercase letters
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value)

    # Convert to lowercase and clean up multiple underscores
    value = value.lower()
    value = re.sub(r"_+", "_", value)

    # Strip leading/trailing underscores
    return value.strip("_")


def to_kebab_case(value: str) -> str:
    """
    Convert string to kebab-case.

    Examples:
        "MyProject" -> "my-project"
        "my_project" -> "my-project"
        "My Project" -> "my-project"
        "myProject" -> "my-project"

    Args:
        value: Input string

    Returns:
        kebab-case version of the string
    """
    # First convert to snake_case, then replace underscores with hyphens
    snake = to_snake_case(value)
    return snake.replace("_", "-")


def to_pascal_case(value: str) -> str:
    """
    Convert string to PascalCase.

    Examples:
        "my-project" -> "MyProject"
        "my_project" -> "MyProject"
        "My Project" -> "MyProject"
        "myProject" -> "MyProject"

    Args:
        value: Input string

    Returns:
        PascalCase version of the string
    """
    # Split on common delimiters and handle camelCase
    # Replace hyphens and underscores with spaces
    value = value.replace("-", " ").replace("_", " ")

    # Insert spaces before uppercase letters in camelCase
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)

    # Split and capitalize each word
    words = value.split()
    return "".join(word.capitalize() for word in words if word)


# ============================================================================
# TEMPLATE REPOSITORY
# ============================================================================


class TemplateRepository:
    """
    IDK: template-management, jinja2-environment, filter-registration
    Responsibility: Loads and renders Jinja2 templates with case conversion filters
    Invariants: Templates dir exists, filters registered at init, rendering immutable
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize the template repository.

        Args:
            templates_dir: Optional custom templates directory.
                          Defaults to package's templates/ directory.
        """
        # Determine templates directory
        if templates_dir is None:
            # Default to package's templates directory
            package_root = Path(__file__).parent.parent
            templates_dir = package_root / "templates"

        self.templates_dir = Path(templates_dir)

        # Create templates directory if it doesn't exist
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=self._select_autoescape,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        # Register custom filters
        self._register_filters()

    def _select_autoescape(self, template_name: Optional[str]) -> bool:
        """
        Determine whether to autoescape based on template file extension.

        Only HTML/XML templates should be autoescaped. Code templates
        (Python, TypeScript, etc.) should not be autoescaped.

        Args:
            template_name: Name of the template file

        Returns:
            True if template should be autoescaped, False otherwise
        """
        if template_name is None:
            return False

        # Autoescape for HTML/XML templates only
        autoescape_extensions = {".html", ".htm", ".xml", ".xhtml"}
        return any(template_name.endswith(ext) for ext in autoescape_extensions)

    def _register_filters(self) -> None:
        """Register custom Jinja2 filters for case conversion."""
        self.env.filters["to_snake_case"] = to_snake_case
        self.env.filters["to_kebab_case"] = to_kebab_case
        self.env.filters["to_pascal_case"] = to_pascal_case

        # Aliases for convenience
        self.env.filters["snake_case"] = to_snake_case
        self.env.filters["kebab_case"] = to_kebab_case
        self.env.filters["pascal_case"] = to_pascal_case

    def render(self, template_name: str, context: Any) -> str:
        """
        Render a template file with the given context.

        The context can be:
        - A TACConfig instance (available as 'config')
        - A dict (keys available as variables directly)
        - Any object (available as 'config')

        Args:
            template_name: Name of the template file (relative to templates_dir)
            context: Context object or dict

        Returns:
            Rendered template string

        Raises:
            TemplateNotFoundError: If template file doesn't exist
            TemplateRenderError: If rendering fails

        Example:
            >>> repo = TemplateRepository()
            >>> output = repo.render("settings.json.j2", my_config)
        """
        try:
            template = self.env.get_template(template_name)
            # If context is a dict, unpack it; otherwise use as 'config'
            if isinstance(context, dict):
                return template.render(**context)
            else:
                return template.render(config=context)
        except Jinja2TemplateNotFound as e:
            raise TemplateNotFoundError(template_name, [str(self.templates_dir)]) from e
        except (TemplateSyntaxError, Exception) as e:
            raise TemplateRenderError(template_name, e) from e

    def render_string(self, template_str: str, context: Any) -> str:
        """
        Render a template string with the given context.

        Useful for inline templates or dynamically generated template strings.

        Args:
            template_str: Template string to render
            context: Context object (usually TACConfig instance)

        Returns:
            Rendered template string

        Raises:
            TemplateRenderError: If rendering fails

        Example:
            >>> repo = TemplateRepository()
            >>> output = repo.render_string("{{ config.project.name }}", my_config)
        """
        try:
            template = self.env.from_string(template_str)
            return template.render(config=context)
        except Exception as e:
            raise TemplateRenderError("<string>", e) from e

    def template_exists(self, template_name: str) -> bool:
        """
        Check if a template file exists.

        Args:
            template_name: Name of the template file

        Returns:
            True if template exists, False otherwise

        Example:
            >>> repo = TemplateRepository()
            >>> if repo.template_exists("settings.json.j2"):
            ...     print("Template found!")
        """
        template_path = self.templates_dir / template_name
        return template_path.is_file()

    def list_templates(self, category: Optional[str] = None) -> List[str]:
        """
        List all available templates, optionally filtered by category.

        Templates are organized in subdirectories (categories) like:
        - templates/claude/
        - templates/adws/
        - templates/scripts/

        Args:
            category: Optional category (subdirectory) to filter by.
                     If None, returns all templates.

        Returns:
            List of template paths relative to templates_dir

        Example:
            >>> repo = TemplateRepository()
            >>> all_templates = repo.list_templates()
            >>> claude_templates = repo.list_templates("claude")
        """
        if category:
            # List templates in specific category
            category_path = self.templates_dir / category
            if not category_path.is_dir():
                return []

            pattern = "**/*"
        else:
            # List all templates
            category_path = self.templates_dir
            pattern = "**/*"

        templates = []
        for path in category_path.glob(pattern):
            if path.is_file() and not path.name.startswith("."):
                # Get path relative to templates_dir
                rel_path = path.relative_to(self.templates_dir)
                templates.append(str(rel_path))

        return sorted(templates)

    def get_template_content(self, template_name: str) -> str:
        """
        Get raw template content without rendering.

        Useful for debugging or inspecting template source.

        Args:
            template_name: Name of the template file

        Returns:
            Raw template content as string

        Raises:
            TemplateNotFoundError: If template file doesn't exist

        Example:
            >>> repo = TemplateRepository()
            >>> source = repo.get_template_content("settings.json.j2")
        """
        template_path = self.templates_dir / template_name

        if not template_path.is_file():
            raise TemplateNotFoundError(template_name, [str(self.templates_dir)])

        return template_path.read_text(encoding="utf-8")
