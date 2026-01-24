"""
Application layer exceptions for TAC Bootstrap.

This module defines custom exceptions for the application layer that translate
domain-level validation results into user-facing error messages.
"""

from tac_bootstrap.application.validation_service import ValidationResult


class ApplicationError(Exception):
    """Base class for all application layer exceptions."""

    pass


class ScaffoldValidationError(ApplicationError):
    """
    Exception raised when pre-scaffold validation fails.

    This exception translates a ValidationResult with errors into a clear,
    multi-line error message that shows all validation issues and suggestions.

    Attributes:
        validation_result: The ValidationResult containing all validation issues

    Example:
        >>> from tac_bootstrap.application.validation_service import (
        ...     ValidationResult, ValidationIssue, ValidationLevel
        ... )
        >>> issues = [
        ...     ValidationIssue(
        ...         level=ValidationLevel.DOMAIN,
        ...         severity="error",
        ...         message="Framework fastapi is not compatible with language rust",
        ...         suggestion="Use one of these languages with fastapi: python"
        ...     )
        ... ]
        >>> result = ValidationResult(valid=False, issues=issues)
        >>> raise ScaffoldValidationError(result)
    """

    def __init__(self, validation_result: ValidationResult):
        """
        Initialize ScaffoldValidationError with validation result.

        Args:
            validation_result: ValidationResult containing validation issues
        """
        self.validation_result = validation_result
        super().__init__(str(self))

    def __str__(self) -> str:
        """
        Format validation errors into a clear, multi-line message.

        Returns:
            Formatted error message with all issues and suggestions
        """
        errors = self.validation_result.errors()
        error_count = len(errors)

        if error_count == 0:
            return "Validation failed with no specific errors"

        # Build header
        lines = [f"Validation failed with {error_count} error(s):"]
        lines.append("")

        # Add numbered error list
        for i, error in enumerate(errors, start=1):
            # Format: "1. [DOMAIN] Framework fastapi is not compatible with language rust"
            level_tag = f"[{error.level.value.upper()}]"
            lines.append(f"{i}. {level_tag} {error.message}")

            # Add suggestion indented with arrow
            if error.suggestion:
                lines.append(f"   → {error.suggestion}")

        # Add suggestions section if any error has a suggestion
        suggestions = [e.suggestion for e in errors if e.suggestion]
        if suggestions:
            lines.append("")
            lines.append("Suggestions:")
            for suggestion in suggestions:
                lines.append(f"- {suggestion}")

        return "\n".join(lines)
