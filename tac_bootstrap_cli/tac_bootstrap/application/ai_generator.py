"""
IDK: ai-generator, code-generation, claude-api, context-aware, prompt-templates
Responsibility: Provides AI-assisted code generation using Claude API with project context
Invariants: Requires ANTHROPIC_API_KEY, generates code following project conventions,
            supports multi-step workflows, context-aware generation

Example usage:
    from tac_bootstrap.application.ai_generator import AIGeneratorService

    service = AIGeneratorService()
    result = service.generate_endpoint(path="/users", method="GET", project_path=Path("."))
    result = service.suggest_refactor(file_path=Path("src/app.py"))
    result = service.suggest_tests(module_path=Path("src/domain/user.py"))
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AIGenerationResult(BaseModel):
    """Result of an AI code generation request."""

    success: bool = Field(default=True, description="Whether generation succeeded")
    code: str = Field(default="", description="Generated code")
    file_path: Optional[str] = Field(default=None, description="Suggested file path")
    explanation: str = Field(default="", description="Explanation of generated code")
    suggestions: List[str] = Field(default_factory=list, description="Additional suggestions")
    language: str = Field(default="python", description="Programming language of generated code")
    tokens_used: int = Field(default=0, description="Approximate tokens used")
    error: Optional[str] = Field(default=None, description="Error message if generation failed")


class AIRefactorSuggestion(BaseModel):
    """A refactoring suggestion from AI analysis."""

    file_path: str = Field(..., description="File path being analyzed")
    category: str = Field(..., description="Category: performance, readability, security, pattern")
    severity: str = Field(default="info", description="Severity: info, warning, critical")
    description: str = Field(..., description="Description of the suggestion")
    current_code: str = Field(default="", description="Current code snippet")
    suggested_code: str = Field(default="", description="Suggested improvement")
    reasoning: str = Field(default="", description="Why this change is recommended")


class AITestSuggestion(BaseModel):
    """AI-generated test suggestion."""

    test_name: str = Field(..., description="Suggested test name")
    test_code: str = Field(..., description="Generated test code")
    test_type: str = Field(default="unit", description="Type: unit, integration, e2e")
    description: str = Field(default="", description="What the test validates")
    priority: str = Field(default="medium", description="Priority: low, medium, high")


# Prompt templates for different generation types
ENDPOINT_PROMPT_TEMPLATE = """Generate a {method} endpoint for path "{path}" in a {framework} application.

Project context:
- Language: {language}
- Framework: {framework}
- Architecture: {architecture}
- Package manager: {package_manager}

Requirements:
- Follow {architecture} architecture pattern
- Include proper error handling
- Add type hints
- Include docstrings
- Follow RESTful conventions

{additional_context}

Generate only the code, no explanations. Use proper imports."""

MIGRATION_PROMPT_TEMPLATE = """Generate a database migration for: {migration_type}

Details:
- Column/table name: {name}
- Type: {data_type}
- Framework: {framework}
- ORM: {orm}

{additional_context}

Generate the migration code following the project's conventions."""

REFACTOR_PROMPT_TEMPLATE = """Analyze this code and suggest refactoring improvements:

File: {file_path}
```{language}
{code}
```

Focus on:
1. Performance improvements
2. Readability enhancements
3. Security concerns
4. Design pattern adherence ({architecture} architecture)
5. Code duplication

Provide specific suggestions with before/after code snippets.
Format each suggestion as JSON with fields: category, severity, description, current_code, suggested_code, reasoning."""

TEST_PROMPT_TEMPLATE = """Suggest unit tests for this module:

File: {file_path}
```{language}
{code}
```

Requirements:
- Use {test_framework} as testing framework
- Include edge cases
- Test error paths
- Mock external dependencies
- Follow AAA (Arrange-Act-Assert) pattern

Generate test code with clear test names and descriptions.
Format as JSON array with fields: test_name, test_code, test_type, description, priority."""


class AIGeneratorService:
    """
    IDK: ai-generation-core, claude-integration, code-suggestion, context-analysis
    Responsibility: Orchestrates AI-assisted code generation with project context awareness
    Invariants: Requires valid API key, respects project conventions, provides fallback prompts
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize AI generator service.

        Args:
            api_key: Anthropic API key. If None, reads from ANTHROPIC_API_KEY env var.
        """
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self._prompt_templates: Dict[str, str] = {
            "endpoint": ENDPOINT_PROMPT_TEMPLATE,
            "migration": MIGRATION_PROMPT_TEMPLATE,
            "refactor": REFACTOR_PROMPT_TEMPLATE,
            "test": TEST_PROMPT_TEMPLATE,
        }

    @property
    def is_configured(self) -> bool:
        """Check if the API key is configured."""
        return bool(self._api_key)

    def _read_file_content(self, file_path: Path, max_lines: int = 500) -> str:
        """Read file content with line limit for context.

        Args:
            file_path: Path to the file
            max_lines: Maximum number of lines to read

        Returns:
            File content as string
        """
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                lines.append(f"\n# ... truncated at {max_lines} lines ...")
            return "\n".join(lines)
        except (OSError, UnicodeDecodeError):
            return ""

    def _detect_project_context(self, project_path: Path) -> Dict[str, str]:
        """Detect project context from config.yml or common files.

        Args:
            project_path: Path to the project root

        Returns:
            Dict with language, framework, architecture, package_manager
        """
        context = {
            "language": "python",
            "framework": "fastapi",
            "architecture": "simple",
            "package_manager": "uv",
            "test_framework": "pytest",
            "orm": "sqlalchemy",
        }

        config_file = project_path / "config.yml"
        if config_file.exists():
            try:
                import yaml
                with open(config_file, "r") as f:
                    config = yaml.safe_load(f)
                if config:
                    project = config.get("project", {})
                    context["language"] = project.get("language", "python")
                    context["framework"] = project.get("framework", "fastapi")
                    context["architecture"] = project.get("architecture", "simple")
                    context["package_manager"] = project.get("package_manager", "uv")
            except Exception:
                pass

        # Detect test framework
        if context["language"] in ("typescript", "javascript"):
            context["test_framework"] = "jest"
        elif context["language"] == "python":
            context["test_framework"] = "pytest"

        return context

    def _call_api(self, prompt: str, max_tokens: int = 4096) -> str:
        """Call the Claude API with a prompt.

        This is a simplified implementation that can work with or without
        the anthropic SDK installed.

        Args:
            prompt: The prompt to send
            max_tokens: Maximum response tokens

        Returns:
            API response text

        Raises:
            RuntimeError: If API call fails
        """
        if not self._api_key:
            raise RuntimeError(
                "Claude API key not configured. "
                "Set ANTHROPIC_API_KEY environment variable or pass api_key to constructor."
            )

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self._api_key)
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except ImportError:
            # Fallback: use urllib for basic API call
            import urllib.request
            import urllib.error

            data = json.dumps({
                "model": "claude-sonnet-4-20250514",
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            }).encode()

            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self._api_key,
                    "anthropic-version": "2023-06-01",
                },
            )
            try:
                with urllib.request.urlopen(req) as resp:
                    result = json.loads(resp.read())
                    return result.get("content", [{}])[0].get("text", "")
            except urllib.error.URLError as e:
                raise RuntimeError(f"API call failed: {e}")

    def generate_endpoint(
        self,
        path: str,
        method: str = "GET",
        project_path: Optional[Path] = None,
        additional_context: str = "",
    ) -> AIGenerationResult:
        """Generate an API endpoint implementation.

        Args:
            path: URL path for the endpoint (e.g., "/users")
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            project_path: Path to project for context detection
            additional_context: Additional instructions

        Returns:
            AIGenerationResult with generated code
        """
        context = self._detect_project_context(project_path or Path.cwd())

        prompt = self._prompt_templates["endpoint"].format(
            path=path,
            method=method.upper(),
            language=context["language"],
            framework=context["framework"],
            architecture=context["architecture"],
            package_manager=context["package_manager"],
            additional_context=additional_context,
        )

        try:
            code = self._call_api(prompt)
            # Extract code block if wrapped in markdown
            code_match = re.search(r"```\w*\n(.*?)```", code, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()

            return AIGenerationResult(
                success=True,
                code=code,
                file_path=f"interfaces/api{path}_routes.py",
                explanation=f"Generated {method} endpoint for {path}",
                language=context["language"],
            )
        except Exception as e:
            return AIGenerationResult(
                success=False,
                error=str(e),
            )

    def generate_migration(
        self,
        migration_type: str,
        name: str,
        data_type: str = "string",
        project_path: Optional[Path] = None,
        additional_context: str = "",
    ) -> AIGenerationResult:
        """Generate a database migration.

        Args:
            migration_type: Type of migration (add-column, create-table, etc.)
            name: Name of the column/table
            data_type: Data type for the column
            project_path: Path to project for context detection
            additional_context: Additional instructions

        Returns:
            AIGenerationResult with generated migration code
        """
        context = self._detect_project_context(project_path or Path.cwd())

        prompt = self._prompt_templates["migration"].format(
            migration_type=migration_type,
            name=name,
            data_type=data_type,
            framework=context["framework"],
            orm=context["orm"],
            additional_context=additional_context,
        )

        try:
            code = self._call_api(prompt)
            code_match = re.search(r"```\w*\n(.*?)```", code, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()

            return AIGenerationResult(
                success=True,
                code=code,
                explanation=f"Generated {migration_type} migration for '{name}'",
                language=context["language"],
            )
        except Exception as e:
            return AIGenerationResult(
                success=False,
                error=str(e),
            )

    def suggest_refactor(
        self,
        file_path: Path,
        project_path: Optional[Path] = None,
    ) -> List[AIRefactorSuggestion]:
        """Analyze a file and suggest refactoring improvements.

        Args:
            file_path: Path to the file to analyze
            project_path: Path to project root

        Returns:
            List of refactoring suggestions
        """
        if not file_path.exists():
            return []

        context = self._detect_project_context(project_path or Path.cwd())
        code = self._read_file_content(file_path)

        if not code:
            return []

        prompt = self._prompt_templates["refactor"].format(
            file_path=str(file_path),
            language=context["language"],
            code=code,
            architecture=context["architecture"],
        )

        try:
            response = self._call_api(prompt)
            # Try to parse JSON suggestions from response
            suggestions = self._parse_refactor_suggestions(response, str(file_path))
            return suggestions
        except Exception:
            return []

    def _parse_refactor_suggestions(
        self, response: str, file_path: str
    ) -> List[AIRefactorSuggestion]:
        """Parse refactoring suggestions from API response.

        Args:
            response: Raw API response text
            file_path: File being analyzed

        Returns:
            List of parsed suggestions
        """
        suggestions: List[AIRefactorSuggestion] = []

        # Try to extract JSON array from response
        json_match = re.search(r"\[.*\]", response, re.DOTALL)
        if json_match:
            try:
                items = json.loads(json_match.group())
                for item in items:
                    if isinstance(item, dict):
                        suggestions.append(
                            AIRefactorSuggestion(
                                file_path=file_path,
                                category=item.get("category", "general"),
                                severity=item.get("severity", "info"),
                                description=item.get("description", ""),
                                current_code=item.get("current_code", ""),
                                suggested_code=item.get("suggested_code", ""),
                                reasoning=item.get("reasoning", ""),
                            )
                        )
            except (json.JSONDecodeError, KeyError):
                pass

        # Fallback: create a single suggestion from the raw response
        if not suggestions and response.strip():
            suggestions.append(
                AIRefactorSuggestion(
                    file_path=file_path,
                    category="general",
                    severity="info",
                    description=response[:500],
                    reasoning="AI-generated analysis",
                )
            )

        return suggestions

    def suggest_tests(
        self,
        module_path: Path,
        project_path: Optional[Path] = None,
    ) -> List[AITestSuggestion]:
        """Suggest tests for a module.

        Args:
            module_path: Path to the module to generate tests for
            project_path: Path to project root

        Returns:
            List of test suggestions
        """
        if not module_path.exists():
            return []

        context = self._detect_project_context(project_path or Path.cwd())
        code = self._read_file_content(module_path)

        if not code:
            return []

        prompt = self._prompt_templates["test"].format(
            file_path=str(module_path),
            language=context["language"],
            code=code,
            test_framework=context["test_framework"],
        )

        try:
            response = self._call_api(prompt)
            return self._parse_test_suggestions(response)
        except Exception:
            return []

    def _parse_test_suggestions(self, response: str) -> List[AITestSuggestion]:
        """Parse test suggestions from API response.

        Args:
            response: Raw API response text

        Returns:
            List of parsed test suggestions
        """
        suggestions: List[AITestSuggestion] = []

        json_match = re.search(r"\[.*\]", response, re.DOTALL)
        if json_match:
            try:
                items = json.loads(json_match.group())
                for item in items:
                    if isinstance(item, dict):
                        suggestions.append(
                            AITestSuggestion(
                                test_name=item.get("test_name", "test_unnamed"),
                                test_code=item.get("test_code", ""),
                                test_type=item.get("test_type", "unit"),
                                description=item.get("description", ""),
                                priority=item.get("priority", "medium"),
                            )
                        )
            except (json.JSONDecodeError, KeyError):
                pass

        if not suggestions and response.strip():
            # Extract code blocks as test suggestions
            code_blocks = re.findall(r"```\w*\n(.*?)```", response, re.DOTALL)
            for i, block in enumerate(code_blocks):
                suggestions.append(
                    AITestSuggestion(
                        test_name=f"test_suggestion_{i + 1}",
                        test_code=block.strip(),
                        description=f"AI-suggested test {i + 1}",
                    )
                )

        return suggestions

    def get_custom_prompt_templates(self) -> Dict[str, str]:
        """Get the current prompt templates (for customization).

        Returns:
            Dict of template name to template string
        """
        return dict(self._prompt_templates)

    def set_prompt_template(self, name: str, template: str) -> None:
        """Set a custom prompt template.

        Args:
            name: Template name (endpoint, migration, refactor, test)
            template: Template string with format placeholders
        """
        self._prompt_templates[name] = template
