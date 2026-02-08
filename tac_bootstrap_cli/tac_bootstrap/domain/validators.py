"""
TAC Bootstrap Domain Validators

Domain-level validation rules for TAC Bootstrap configurations. Defines explicit
compatibility matrices between languages, frameworks, package managers, and architectures.

This module provides pairwise validation functions that check compatibility and return
structured ValidationIssue objects with clear error messages and actionable suggestions.

Example usage:
    from tac_bootstrap.domain.validators import (
        validate_framework_language,
        validate_package_manager_language,
        validate_architecture_framework,
        ValidationIssue
    )
    from tac_bootstrap.domain.models import Language, Framework, PackageManager, Architecture

    # Validate framework-language compatibility
    issue = validate_framework_language(Framework.FASTAPI, Language.GO)
    if issue:
        print(f"ERROR: {issue.message}")
        print(f"Suggestions: {', '.join(issue.suggestions)}")

    # Validate package manager-language compatibility
    issue = validate_package_manager_language(PackageManager.NPM, Language.PYTHON)
    if issue:
        print(f"ERROR: {issue.message}")

    # Validate architecture-framework compatibility
    issue = validate_architecture_framework(Architecture.DDD, Framework.NONE)
    if issue:
        print(f"ERROR: {issue.message}")
"""

from typing import Any

from pydantic import BaseModel

from tac_bootstrap.domain.models import Architecture, Framework, Language, PackageManager

# ============================================================================
# VALIDATION ISSUE MODEL
# ============================================================================


class ValidationIssue(BaseModel):
    """
    A single domain validation issue with actionable suggestions.

    This model represents a validation error discovered during domain-level
    compatibility checks. Unlike the ValidationService's ValidationIssue which
    includes severity levels and validation layers, this domain model focuses
    purely on compatibility violations.

    Attributes:
        message: Clear description of the compatibility problem
        field_name: Name of the field that has the invalid value
            (e.g., "framework", "package_manager")
        invalid_value: The actual value that failed validation
        suggestions: List[Any] of valid alternatives the user can choose from

    Example:
        issue = ValidationIssue(
            message="Framework fastapi is not compatible with language go",
            field_name="framework",
            invalid_value="fastapi",
            suggestions=["gin", "echo", "fiber", "chi", "none"]
        )
    """

    message: str
    field_name: str
    invalid_value: Any
    suggestions: list[str] | None = None


# ============================================================================
# COMPATIBILITY MATRICES
# ============================================================================

# Language → Valid Frameworks mapping
COMPATIBLE_FRAMEWORKS: dict[Language, list[Framework]] = {
    Language.PYTHON: [
        Framework.FASTAPI,
        Framework.DJANGO,
        Framework.FLASK,
        Framework.NONE,
    ],
    Language.TYPESCRIPT: [
        Framework.NEXTJS,
        Framework.EXPRESS,
        Framework.NESTJS,
        Framework.REACT,
        Framework.VUE,
        Framework.NONE,
    ],
    Language.JAVASCRIPT: [
        Framework.NEXTJS,
        Framework.EXPRESS,
        Framework.REACT,
        Framework.VUE,
        Framework.NONE,
    ],
    Language.GO: [
        Framework.GIN,
        Framework.ECHO,
        Framework.NONE,
    ],
    Language.RUST: [
        Framework.AXUM,
        Framework.ACTIX,
        Framework.NONE,
    ],
    Language.JAVA: [
        Framework.SPRING,
        Framework.NONE,
    ],
}

# Language → Valid Package Managers mapping
COMPATIBLE_PACKAGE_MANAGERS: dict[Language, list[PackageManager]] = {
    Language.PYTHON: [
        PackageManager.UV,
        PackageManager.POETRY,
        PackageManager.PIP,
        PackageManager.PIPENV,
    ],
    Language.TYPESCRIPT: [
        PackageManager.NPM,
        PackageManager.YARN,
        PackageManager.PNPM,
        PackageManager.BUN,
    ],
    Language.JAVASCRIPT: [
        PackageManager.NPM,
        PackageManager.YARN,
        PackageManager.PNPM,
        PackageManager.BUN,
    ],
    Language.GO: [
        PackageManager.GO_MOD,
    ],
    Language.RUST: [
        PackageManager.CARGO,
    ],
    Language.JAVA: [
        PackageManager.MAVEN,
        PackageManager.GRADLE,
    ],
}

# Architectures that require substantial frameworks (not Framework.NONE)
ARCHITECTURES_REQUIRING_BASE_CLASSES: list[Architecture] = [
    Architecture.DDD,
    Architecture.CLEAN,
    Architecture.HEXAGONAL,
]


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================


def validate_framework_language(
    framework: Framework, language: Language
) -> ValidationIssue | None:
    """
    Validate that a framework is compatible with a language.

    Checks if the given framework can be used with the specified language.
    Returns None if valid, or a ValidationIssue with suggestions if invalid.

    Args:
        framework: The framework to validate
        language: The programming language to check compatibility with

    Returns:
        None if valid, ValidationIssue with suggestions if invalid

    Example:
        >>> issue = validate_framework_language(Framework.FASTAPI, Language.GO)
        >>> if issue:
        ...     print(issue.message)
        Framework fastapi is not compatible with language go.
        Valid frameworks for go: gin, echo, none
    """
    if language not in COMPATIBLE_FRAMEWORKS:
        return ValidationIssue(
            message=f"Unknown language: {language.value}",
            field_name="language",
            invalid_value=language.value,
            suggestions=None,
        )

    valid_frameworks = COMPATIBLE_FRAMEWORKS[language]

    if framework not in valid_frameworks:
        suggestions = [fw.value for fw in valid_frameworks]
        return ValidationIssue(
            message=(
                f"Framework {framework.value} is not compatible with language {language.value}. "
                f"Valid frameworks for {language.value}: {', '.join(suggestions)}"
            ),
            field_name="framework",
            invalid_value=framework.value,
            suggestions=suggestions,
        )

    return None


def validate_package_manager_language(
    package_manager: PackageManager, language: Language
) -> ValidationIssue | None:
    """
    Validate that a package manager is compatible with a language.

    Checks if the given package manager can be used with the specified language.
    Returns None if valid, or a ValidationIssue with suggestions if invalid.

    Args:
        package_manager: The package manager to validate
        language: The programming language to check compatibility with

    Returns:
        None if valid, ValidationIssue with suggestions if invalid

    Example:
        >>> issue = validate_package_manager_language(
        ...     PackageManager.NPM, Language.PYTHON
        ... )
        >>> if issue:
        ...     print(issue.message)
        Package manager npm is not compatible with language python.
        Valid package managers for python: uv, poetry, pip, pipenv
    """
    if language not in COMPATIBLE_PACKAGE_MANAGERS:
        return ValidationIssue(
            message=f"Unknown language: {language.value}",
            field_name="language",
            invalid_value=language.value,
            suggestions=None,
        )

    valid_package_managers = COMPATIBLE_PACKAGE_MANAGERS[language]

    if package_manager not in valid_package_managers:
        suggestions = [pm.value for pm in valid_package_managers]
        return ValidationIssue(
            message=(
                f"Package manager {package_manager.value} is not compatible "
                f"with language {language.value}. "
                f"Valid package managers for {language.value}: "
                f"{', '.join(suggestions)}"
            ),
            field_name="package_manager",
            invalid_value=package_manager.value,
            suggestions=suggestions,
        )

    return None


def validate_architecture_framework(
    architecture: Architecture, framework: Framework
) -> ValidationIssue | None:
    """
    Validate that an architecture has sufficient framework support.

    Advanced architectures (DDD, Clean, Hexagonal) require substantial frameworks
    and cannot be used with Framework.NONE. Simple and Layered architectures
    work with any framework.

    Args:
        architecture: The software architecture pattern to validate
        framework: The framework to check compatibility with

    Returns:
        None if valid, ValidationIssue with suggestions if invalid

    Example:
        >>> issue = validate_architecture_framework(
        ...     Architecture.DDD, Framework.NONE
        ... )
        >>> if issue:
        ...     print(issue.message)
        Architecture ddd requires a substantial framework.
        Framework 'none' is not sufficient.
        DDD/Clean/Hexagonal architectures need frameworks that support
        dependency injection and layering.
    """
    if architecture in ARCHITECTURES_REQUIRING_BASE_CLASSES:
        if framework == Framework.NONE:
            return ValidationIssue(
                message=(
                    f"Architecture {architecture.value} requires a substantial framework. "
                    f"Framework 'none' is not sufficient. "
                    f"DDD/Clean/Hexagonal architectures need frameworks that support "
                    f"dependency injection and layering."
                ),
                field_name="architecture",
                invalid_value=architecture.value,
                suggestions=[
                    (
                        "Use Architecture.SIMPLE or Architecture.LAYERED "
                        "with Framework.NONE"
                    ),
                    (
                        "Choose a substantial framework (FastAPI, NestJS, "
                        "Spring, etc.) for advanced architectures"
                    ),
                ],
            )

    return None
