"""Tests for application layer exceptions."""


from tac_bootstrap.application.exceptions import ApplicationError, ScaffoldValidationError
from tac_bootstrap.application.validation_service import (
    ValidationIssue,
    ValidationLevel,
    ValidationResult,
)


class TestScaffoldValidationError:
    """Test suite for ScaffoldValidationError formatting."""

    def test_scaffold_validation_error_formats_single_error(self):
        """Test formatting with a single error."""
        issues = [
            ValidationIssue(
                level=ValidationLevel.DOMAIN,
                severity="error",
                message="Framework fastapi is not compatible with language rust",
                suggestion="Use one of these languages with fastapi: python",
            )
        ]
        result = ValidationResult(valid=False, issues=issues)
        error = ScaffoldValidationError(result)

        error_msg = str(error)

        assert "Validation failed with 1 error(s):" in error_msg
        assert "1. [DOMAIN] Framework fastapi is not compatible with language rust" in error_msg
        assert "→ Use one of these languages with fastapi: python" in error_msg
        assert "Suggestions:" in error_msg
        assert "- Use one of these languages with fastapi: python" in error_msg

    def test_scaffold_validation_error_formats_multiple_errors(self):
        """Test formatting with multiple errors."""
        issues = [
            ValidationIssue(
                level=ValidationLevel.DOMAIN,
                severity="error",
                message="Framework fastapi is not compatible with language rust",
                suggestion="Use one of these languages with fastapi: python",
            ),
            ValidationIssue(
                level=ValidationLevel.TEMPLATE,
                severity="error",
                message="Required template not found: settings.json.j2",
                suggestion="Ensure template exists at /path/to/templates/settings.json.j2",
            ),
        ]
        result = ValidationResult(valid=False, issues=issues)
        error = ScaffoldValidationError(result)

        error_msg = str(error)

        assert "Validation failed with 2 error(s):" in error_msg
        assert "1. [DOMAIN] Framework fastapi is not compatible with language rust" in error_msg
        assert "2. [TEMPLATE] Required template not found: settings.json.j2" in error_msg

    def test_scaffold_validation_error_includes_suggestions(self):
        """Test that suggestions section is included."""
        issues = [
            ValidationIssue(
                level=ValidationLevel.DOMAIN,
                severity="error",
                message="Architecture hexagonal is not compatible with framework django",
                suggestion="Use framework fastapi or flask with hexagonal architecture",
            ),
            ValidationIssue(
                level=ValidationLevel.FILESYSTEM,
                severity="error",
                message="Output directory does not exist",
                suggestion="Create directory with: mkdir -p /path/to/output",
            ),
        ]
        result = ValidationResult(valid=False, issues=issues)
        error = ScaffoldValidationError(result)

        error_msg = str(error)

        assert "Suggestions:" in error_msg
        assert "- Use framework fastapi or flask with hexagonal architecture" in error_msg
        assert "- Create directory with: mkdir -p /path/to/output" in error_msg

    def test_scaffold_validation_error_shows_severity_and_level(self):
        """Test that severity and level tags are shown correctly."""
        issues = [
            ValidationIssue(
                level=ValidationLevel.DOMAIN,
                severity="error",
                message="Framework incompatibility",
                suggestion=None,
            ),
            ValidationIssue(
                level=ValidationLevel.TEMPLATE,
                severity="error",
                message="Template missing",
                suggestion=None,
            ),
            ValidationIssue(
                level=ValidationLevel.FILESYSTEM,
                severity="error",
                message="Permission denied",
                suggestion=None,
            ),
            ValidationIssue(
                level=ValidationLevel.GIT,
                severity="error",
                message="Git not available",
                suggestion=None,
            ),
        ]
        result = ValidationResult(valid=False, issues=issues)
        error = ScaffoldValidationError(result)

        error_msg = str(error)

        assert "[DOMAIN]" in error_msg
        assert "[TEMPLATE]" in error_msg
        assert "[FILESYSTEM]" in error_msg
        assert "[GIT]" in error_msg

    def test_scaffold_validation_error_ignores_warnings(self):
        """Test that only errors are included, not warnings."""
        issues = [
            ValidationIssue(
                level=ValidationLevel.DOMAIN,
                severity="error",
                message="Framework incompatibility",
                suggestion="Use compatible framework",
            ),
            ValidationIssue(
                level=ValidationLevel.GIT,
                severity="warning",
                message="Git not available - some features may be limited",
                suggestion=None,
            ),
        ]
        result = ValidationResult(valid=False, issues=issues)
        error = ScaffoldValidationError(result)

        error_msg = str(error)

        assert "Validation failed with 1 error(s):" in error_msg
        assert "Framework incompatibility" in error_msg
        assert "Git not available" not in error_msg

    def test_scaffold_validation_error_without_suggestions(self):
        """Test formatting when errors have no suggestions."""
        issues = [
            ValidationIssue(
                level=ValidationLevel.DOMAIN,
                severity="error",
                message="Framework incompatibility",
                suggestion=None,
            )
        ]
        result = ValidationResult(valid=False, issues=issues)
        error = ScaffoldValidationError(result)

        error_msg = str(error)

        assert "Validation failed with 1 error(s):" in error_msg
        assert "1. [DOMAIN] Framework incompatibility" in error_msg
        # No suggestions section should be present
        assert "Suggestions:" not in error_msg

    def test_scaffold_validation_error_is_application_error(self):
        """Test that ScaffoldValidationError is an ApplicationError."""
        issues = [
            ValidationIssue(
                level=ValidationLevel.DOMAIN,
                severity="error",
                message="Test error",
                suggestion=None,
            )
        ]
        result = ValidationResult(valid=False, issues=issues)
        error = ScaffoldValidationError(result)

        assert isinstance(error, ApplicationError)
        assert isinstance(error, Exception)
