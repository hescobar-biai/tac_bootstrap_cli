"""
TAC Bootstrap Validation Service

Multi-layer validation service that performs comprehensive pre-scaffold validation
across domain, template, filesystem, and git layers. Accumulates all validation
issues before returning results, allowing users to fix all problems at once.

Example usage:
    from tac_bootstrap.application.validation_service import ValidationService
    from tac_bootstrap.infrastructure.template_repo import TemplateRepository
    from tac_bootstrap.domain.models import TACConfig
    from pathlib import Path

    # Initialize service with template repository
    template_repo = TemplateRepository()
    validator = ValidationService(template_repo)

    # Validate config
    result = validator.validate_config(config)
    if not result.valid:
        for error in result.errors():
            print(f"ERROR: {error.message}")
            if error.suggestion:
                print(f"  → {error.suggestion}")

    # Pre-scaffold validation (comprehensive gate)
    result = validator.validate_pre_scaffold(config, output_dir)
    if result.valid:
        print("✓ All validations passed")
    else:
        print(f"✗ Found {len(result.errors())} errors, {len(result.warnings())} warnings")
"""

import os
import re
import shutil
from enum import Enum
from pathlib import Path

from pydantic import BaseModel

from tac_bootstrap.domain.entity_config import EntitySpec
from tac_bootstrap.domain.models import (
    Architecture,
    Framework,
    Language,
    TACConfig,
)
from tac_bootstrap.infrastructure.git_adapter import GitAdapter
from tac_bootstrap.infrastructure.template_repo import TemplateRepository

# ============================================================================
# ENUMS AND MODELS
# ============================================================================


class ValidationLevel(str, Enum):
    """
    Validation layer where an issue occurred.

    Levels:
        SCHEMA: Pydantic validation (field types, required fields)
        DOMAIN: Business logic validation (framework compatibility, architecture)
        TEMPLATE: Template file existence and accessibility
        FILESYSTEM: File system permissions, conflicts, writability
        GIT: Git repository status and availability
    """

    SCHEMA = "schema"
    DOMAIN = "domain"
    TEMPLATE = "template"
    FILESYSTEM = "filesystem"
    GIT = "git"


class ValidationIssue(BaseModel):
    """
    A single validation issue discovered during validation.

    Attributes:
        level: The validation layer where issue occurred
        severity: "error" (blocks generation) or "warning" (informational)
        message: Clear description of the problem
        suggestion: Actionable guidance on how to resolve the issue
    """

    level: ValidationLevel
    severity: str  # "error" or "warning"
    message: str
    suggestion: str | None = None


class ValidationResult(BaseModel):
    """
    Complete result of a validation operation.

    Attributes:
        valid: True if no errors exist (warnings don't affect validity)
        issues: List of all validation issues found

    Methods:
        errors(): Returns only error-severity issues
        warnings(): Returns only warning-severity issues
    """

    valid: bool
    issues: list[ValidationIssue]

    def errors(self) -> list[ValidationIssue]:
        """
        Get only error-severity issues.

        Returns:
            List of issues with severity="error"
        """
        return [issue for issue in self.issues if issue.severity == "error"]

    def warnings(self) -> list[ValidationIssue]:
        """
        Get only warning-severity issues.

        Returns:
            List of issues with severity="warning"
        """
        return [issue for issue in self.issues if issue.severity == "warning"]


# ============================================================================
# VALIDATION SERVICE
# ============================================================================


class ValidationService:
    """
    Multi-layer validation service for TAC Bootstrap configurations.

    Performs comprehensive validation across multiple layers before scaffold generation:
    - DOMAIN: Framework/language compatibility, architecture validity
    - TEMPLATE: Template file existence verification
    - FILESYSTEM: Output directory permissions, conflict detection
    - GIT: Repository status, uncommitted changes

    The service accumulates ALL validation issues before returning results,
    allowing users to see and fix all problems at once. Never raises exceptions -
    always returns ValidationResult for structured error handling.

    Attributes:
        template_repo: TemplateRepository instance for template existence checks

    Example:
        >>> template_repo = TemplateRepository()
        >>> validator = ValidationService(template_repo)
        >>> result = validator.validate_pre_scaffold(config, output_dir)
        >>> if not result.valid:
        ...     for error in result.errors():
        ...         print(f"{error.level}: {error.message}")
    """

    # Framework → Language compatibility matrix
    FRAMEWORK_LANGUAGE_COMPATIBILITY = {
        Framework.FASTAPI: {Language.PYTHON},
        Framework.DJANGO: {Language.PYTHON},
        Framework.FLASK: {Language.PYTHON},
        Framework.EXPRESS: {Language.TYPESCRIPT, Language.JAVASCRIPT},
        Framework.NESTJS: {Language.TYPESCRIPT},
        Framework.NEXTJS: {Language.TYPESCRIPT, Language.JAVASCRIPT},
        Framework.REACT: {Language.TYPESCRIPT, Language.JAVASCRIPT},
        Framework.VUE: {Language.TYPESCRIPT, Language.JAVASCRIPT},
        Framework.GIN: {Language.GO},
        Framework.ECHO: {Language.GO},
        Framework.AXUM: {Language.RUST},
        Framework.ACTIX: {Language.RUST},
        Framework.SPRING: {Language.JAVA},
        Framework.NONE: {
            Language.PYTHON,
            Language.TYPESCRIPT,
            Language.JAVASCRIPT,
            Language.GO,
            Language.RUST,
            Language.JAVA,
        },
    }

    # Framework → Architecture compatibility matrix
    FRAMEWORK_ARCHITECTURE_COMPATIBILITY = {
        Framework.FASTAPI: {
            Architecture.SIMPLE,
            Architecture.LAYERED,
            Architecture.DDD,
            Architecture.CLEAN,
            Architecture.HEXAGONAL,
        },
        Framework.DJANGO: {Architecture.SIMPLE, Architecture.LAYERED},
        Framework.FLASK: {Architecture.SIMPLE, Architecture.LAYERED, Architecture.CLEAN},
        Framework.EXPRESS: {
            Architecture.SIMPLE,
            Architecture.LAYERED,
            Architecture.DDD,
            Architecture.CLEAN,
        },
        Framework.NESTJS: {Architecture.LAYERED, Architecture.DDD, Architecture.CLEAN},
        Framework.NEXTJS: {Architecture.SIMPLE, Architecture.LAYERED, Architecture.CLEAN},
        Framework.REACT: {Architecture.SIMPLE, Architecture.LAYERED, Architecture.CLEAN},
        Framework.VUE: {Architecture.SIMPLE, Architecture.LAYERED, Architecture.CLEAN},
        Framework.GIN: {Architecture.SIMPLE, Architecture.LAYERED, Architecture.CLEAN},
        Framework.ECHO: {Architecture.SIMPLE, Architecture.LAYERED, Architecture.CLEAN},
        Framework.AXUM: {Architecture.SIMPLE, Architecture.LAYERED, Architecture.CLEAN},
        Framework.ACTIX: {Architecture.SIMPLE, Architecture.LAYERED, Architecture.CLEAN},
        Framework.SPRING: {Architecture.SIMPLE, Architecture.LAYERED, Architecture.CLEAN},
        Framework.NONE: {Architecture.SIMPLE},
    }

    def __init__(self, template_repo: TemplateRepository):
        """
        Initialize the ValidationService.

        Args:
            template_repo: TemplateRepository instance for template existence checks
        """
        self.template_repo = template_repo

    def validate_config(self, config: TACConfig) -> ValidationResult:
        """
        Validate TACConfig for domain and template layer issues.

        Checks:
        - Framework/language compatibility
        - Framework/architecture compatibility
        - Required template file existence

        Args:
            config: TACConfig instance to validate

        Returns:
            ValidationResult with all accumulated issues
        """
        issues: list[ValidationIssue] = []

        # DOMAIN LAYER: Framework/Language compatibility
        framework = config.project.framework
        language = config.project.language

        if framework not in self.FRAMEWORK_LANGUAGE_COMPATIBILITY:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.DOMAIN,
                    severity="error",
                    message=f"Unknown framework: {framework}",
                    suggestion="Use a supported framework from the Framework enum",
                )
            )
        else:
            compatible_languages = self.FRAMEWORK_LANGUAGE_COMPATIBILITY[framework]
            if language not in compatible_languages:
                valid_langs = ", ".join(sorted(lang.value for lang in compatible_languages))
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.DOMAIN,
                        severity="error",
                        message=(
                            f"Framework {framework.value} is not compatible "
                            f"with language {language.value}"
                        ),
                        suggestion=(
                            f"Use one of these languages with {framework.value}: "
                            f"{valid_langs}"
                        ),
                    )
                )

        # DOMAIN LAYER: Framework/Architecture compatibility
        architecture = config.project.architecture

        if framework not in self.FRAMEWORK_ARCHITECTURE_COMPATIBILITY:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.DOMAIN,
                    severity="error",
                    message=f"Unknown framework: {framework}",
                    suggestion="Use a supported framework from the Framework enum",
                )
            )
        else:
            compatible_architectures = self.FRAMEWORK_ARCHITECTURE_COMPATIBILITY[framework]
            if architecture not in compatible_architectures:
                valid_archs = ", ".join(sorted(arch.value for arch in compatible_architectures))
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.DOMAIN,
                        severity="error",
                        message=(
                            f"Framework {framework.value} does not support "
                            f"{architecture.value} architecture"
                        ),
                        suggestion=(
                            f"Use one of these architectures with {framework.value}: "
                            f"{valid_archs}"
                        ),
                    )
                )

        # TEMPLATE LAYER: Check critical template existence
        # Note: This is a basic check - specific templates depend on config values
        # Future enhancement: validate all templates needed for this specific config
        critical_templates = [
            ".claude/settings.json.j2",
            ".claude/hooks/user-prompt-submit-hook.sh.j2",
        ]

        for template_name in critical_templates:
            if not self.template_repo.template_exists(template_name):
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.TEMPLATE,
                        severity="error",
                        message=f"Required template not found: {template_name}",
                        suggestion=(
                            f"Ensure template exists at "
                            f"{self.template_repo.templates_dir / template_name}"
                        ),
                    )
                )

        return ValidationResult(
            valid=len([i for i in issues if i.severity == "error"]) == 0,
            issues=issues,
        )

    def validate_entity(self, entity: EntitySpec, project_root: Path) -> ValidationResult:
        """
        Validate an EntitySpec for entity-specific issues.

        Checks:
        - Entity name is valid Python/TypeScript identifier
        - No duplicate field names
        - Field names are non-empty
        - Field types are appropriate (basic check)

        Args:
            entity: EntitySpec instance to validate
            project_root: Path to project root (for reading config if needed)

        Returns:
            ValidationResult with all accumulated issues
        """
        issues: list[ValidationIssue] = []

        # Validate entity name is a valid identifier
        # Python/TypeScript identifier pattern: starts with letter/underscore,
        # followed by letters/numbers/underscores
        identifier_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

        if not identifier_pattern.match(entity.name):
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.DOMAIN,
                    severity="error",
                    message=f"Entity name '{entity.name}' is not a valid identifier",
                    suggestion=(
                        "Entity name must start with a letter or underscore, "
                        "followed by letters, numbers, or underscores"
                    ),
                )
            )

        # Check for duplicate field names
        field_names = [field.name for field in entity.fields]
        seen = set()
        duplicates = set()

        for name in field_names:
            if name in seen:
                duplicates.add(name)
            seen.add(name)

        if duplicates:
            dup_list = ", ".join(sorted(duplicates))
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.DOMAIN,
                    severity="error",
                    message=f"Duplicate field names found: {dup_list}",
                    suggestion="Ensure all field names are unique within the entity",
                )
            )

        # Check for empty field names
        empty_fields = [
            i
            for i, field in enumerate(entity.fields)
            if not field.name or not field.name.strip()
        ]

        if empty_fields:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.DOMAIN,
                    severity="error",
                    message=f"Empty field names found at positions: {empty_fields}",
                    suggestion="All fields must have non-empty names",
                )
            )

        # Field type validation is handled by Pydantic FieldType enum
        # No additional validation needed here

        return ValidationResult(
            valid=len([i for i in issues if i.severity == "error"]) == 0,
            issues=issues,
        )

    def validate_pre_scaffold(self, config: TACConfig, output_dir: Path) -> ValidationResult:
        """
        Comprehensive pre-scaffold validation gate.

        Runs all validation layers:
        - DOMAIN: Framework/language/architecture compatibility
        - TEMPLATE: Required template existence
        - FILESYSTEM: Output directory permissions and conflicts
        - GIT: Git availability and repository status

        This is the main validation entry point before scaffold generation.

        Args:
            config: TACConfig instance to validate
            output_dir: Target output directory for scaffold

        Returns:
            ValidationResult with all accumulated issues from all layers
        """
        issues: list[ValidationIssue] = []

        # Run DOMAIN and TEMPLATE validations
        config_result = self.validate_config(config)
        issues.extend(config_result.issues)

        # FILESYSTEM LAYER: Output directory validation
        issues.extend(self._validate_filesystem(output_dir))

        # GIT LAYER: Git availability and status
        issues.extend(self._validate_git(output_dir))

        return ValidationResult(
            valid=len([i for i in issues if i.severity == "error"]) == 0,
            issues=issues,
        )

    def _validate_filesystem(self, output_dir: Path) -> list[ValidationIssue]:
        """
        Validate filesystem layer: permissions, conflicts, writability.

        Args:
            output_dir: Target output directory

        Returns:
            List of ValidationIssue objects
        """
        issues: list[ValidationIssue] = []

        if output_dir.exists():
            # Directory exists - check if writable
            if not os.access(output_dir, os.W_OK):
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.FILESYSTEM,
                        severity="error",
                        message=f"Output directory is not writable: {output_dir}",
                        suggestion=(
                            "Check directory permissions or choose a different "
                            "output directory"
                        ),
                    )
                )

            # Check for .tac_config.yaml conflict
            tac_config_file = output_dir / ".tac_config.yaml"
            if tac_config_file.exists():
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.FILESYSTEM,
                        severity="error",
                        message=(
                            f"Output directory already contains .tac_config.yaml: "
                            f"{output_dir}"
                        ),
                        suggestion=(
                            "Use a different output directory or use --force flag "
                            "to overwrite"
                        ),
                    )
                )
        else:
            # Directory doesn't exist - check parent directory
            parent = output_dir.parent

            if not parent.exists():
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.FILESYSTEM,
                        severity="error",
                        message=f"Parent directory does not exist: {parent}",
                        suggestion=f"Create parent directory first: mkdir -p {parent}",
                    )
                )
            elif not os.access(parent, os.W_OK):
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.FILESYSTEM,
                        severity="error",
                        message=f"Parent directory is not writable: {parent}",
                        suggestion=(
                            "Check directory permissions or choose a different "
                            "output directory"
                        ),
                    )
                )

        return issues

    def _validate_git(self, output_dir: Path) -> list[ValidationIssue]:
        """
        Validate git layer: availability and repository status.

        Args:
            output_dir: Target output directory

        Returns:
            List of ValidationIssue objects
        """
        issues: list[ValidationIssue] = []

        # Check if git is available
        if not shutil.which("git"):
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.GIT,
                    severity="warning",
                    message="Git is not installed or not available in PATH",
                    suggestion="Install git for version control features (optional)",
                )
            )
            return issues

        # If output_dir exists and is a git repo, check for uncommitted changes
        if output_dir.exists():
            git_adapter = GitAdapter(output_dir)

            if git_adapter.is_repo():
                if git_adapter.has_changes():
                    issues.append(
                        ValidationIssue(
                            level=ValidationLevel.GIT,
                            severity="warning",
                            message=f"Git repository has uncommitted changes: {output_dir}",
                            suggestion="Consider committing changes before scaffold generation",
                        )
                    )

        return issues
