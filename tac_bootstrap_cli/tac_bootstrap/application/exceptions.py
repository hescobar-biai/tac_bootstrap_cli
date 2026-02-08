"""
IDK: exception-hierarchy, error-types, validation-errors, domain-exceptions
Responsibility: Defines application exceptions for translating validation results
Invariants: All inherit from ApplicationError, validation errors contain ValidationResult
"""

from tac_bootstrap.application.validation_service import ValidationResult


class ApplicationError(Exception):
    """
    IDK: base-exception, error-hierarchy
    Responsibility: Base class for all application layer exceptions
    Invariants: All application exceptions inherit from this class
    """

    pass


class ScaffoldValidationError(ApplicationError):
    """
    IDK: validation-exception, error-formatting, multi-line-messages
    Responsibility: Translates ValidationResult with errors into clear multi-line error message
    Invariants: Contains ValidationResult, formats all errors with suggestions
    """

    def __init__(self, validation_result: ValidationResult) -> None:
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
