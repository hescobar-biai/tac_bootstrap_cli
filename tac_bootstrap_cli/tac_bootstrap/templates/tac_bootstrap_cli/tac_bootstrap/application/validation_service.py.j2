"""
IDK: validation-service, config-validation, pre-scaffold-checks, multi-layer, system-requirements
Responsibility: Performs pre-scaffold validation across domain, template, filesystem, git, and system layers
Invariants: Accumulates all issues, never raises exceptions, distinguishes errors
"""

import os
import re
import shutil
import subprocess
from enum import Enum
from pathlib import Path

from pydantic import BaseModel

from tac_bootstrap.domain.entity_config import EntitySpec
from tac_bootstrap.domain.models import (
    Architecture,
    Framework,
    Language,
    PackageManager,
    SystemRequirement,
    TACConfig,
)
from tac_bootstrap.infrastructure.git_adapter import GitAdapter
from tac_bootstrap.infrastructure.template_repo import TemplateRepository

# ============================================================================
# ENUMS AND MODELS
# ============================================================================


class ValidationLevel(str, Enum):
    """
    IDK: validation-layer, issue-categorization
    Responsibility: Categorizes validation issues by layer
    Invariants: Each level represents a distinct validation concern
    """

    SCHEMA = "schema"
    DOMAIN = "domain"
    TEMPLATE = "template"
    FILESYSTEM = "filesystem"
    GIT = "git"
    SYSTEM = "system"


class ValidationIssue(BaseModel):
    """
    IDK: validation-issue, error-reporting, actionable-feedback
    Responsibility: Represents validation issue with severity and actionable suggestion
    Invariants: Severity is error or warning, message always set, suggestion optional
    """

    level: ValidationLevel
    severity: str  # "error" or "warning"
    message: str
    suggestion: str | None = None


class ValidationResult(BaseModel):
    """
    IDK: validation-result, issue-aggregation, error-filtering
    Responsibility: Aggregates all validation issues and provides filtering by severity
    Invariants: Valid is true only when no errors exist, warnings don't affect validity
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
# CONSTANTS
# ============================================================================

# Windows reserved device names that cannot be used as file or directory names
WINDOWS_RESERVED_NAMES = frozenset({
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
})

# Pattern for valid project name: lowercase letters, numbers, hyphens
# No leading/trailing hyphens, 3-50 characters
PROJECT_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,48}[a-z0-9]$")

# Pattern to detect special unicode characters (beyond ASCII printable range)
SPECIAL_UNICODE_PATTERN = re.compile(r"[^\x20-\x7E]")

# Maximum path length for cross-platform compatibility
MAX_PATH_LENGTH = 255


# ============================================================================
# VALIDATION SERVICE
# ============================================================================


class ValidationService:
    """
    IDK: multi-layer-validation, compatibility-checking, issue-accumulation, system-requirements
    Responsibility: Validates configs across domain, template, filesystem, git, and system layers
    Invariants: Never raises exceptions, accumulates issues, returns ValidationResult
    """

    # Framework -> Language compatibility matrix
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

    # Framework -> Architecture compatibility matrix
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

    # Package managers that require specific CLI tools
    JS_PACKAGE_MANAGERS = {
        PackageManager.NPM,
        PackageManager.YARN,
        PackageManager.PNPM,
        PackageManager.BUN,
    }

    def __init__(self, template_repo: TemplateRepository) -> None:
        """
        Initialize the ValidationService.

        Args:
            template_repo: TemplateRepository instance for template existence checks
        """
        self.template_repo = template_repo

    # ========================================================================
    # PUBLIC METHODS - Core Validation
    # ========================================================================

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
            "claude/settings.json.j2",
            "claude/hooks/user_prompt_submit.py.j2",
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
        seen: set[str] = set()
        duplicates: set[str] = set()

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

    # ========================================================================
    # PUBLIC METHODS - System Requirements Validation
    # ========================================================================

    def validate_system_requirements(self, config: TACConfig) -> ValidationResult:
        """
        Check all system dependencies needed for project generation.

        Validates that required tools are installed and meet minimum version requirements:
        - git >= 2.30 (always required)
        - python >= 3.10 (always required)
        - uv (if package_manager is uv)
        - npm/yarn/pnpm/bun (if package_manager is a JS package manager)
        - gh CLI (if orchestrator.enabled is true)

        Args:
            config: TACConfig instance containing project configuration

        Returns:
            ValidationResult with system-level issues for missing or outdated tools
        """
        issues: list[ValidationIssue] = []
        requirements: list[SystemRequirement] = []

        # Always required: git >= 2.30
        git_ok, git_version = self._check_git_version("2.30")
        git_req = SystemRequirement(
            name="git",
            min_version="2.30",
            installed=git_version is not None,
            version=git_version,
        )
        requirements.append(git_req)

        if not git_req.installed:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.SYSTEM,
                    severity="error",
                    message="git is not installed or not available in PATH",
                    suggestion="Install git: https://git-scm.com/downloads",
                )
            )
        elif not git_ok:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.SYSTEM,
                    severity="error",
                    message=(
                        f"git version {git_version} does not meet "
                        f"minimum requirement (>= 2.30)"
                    ),
                    suggestion="Upgrade git to version 2.30 or later",
                )
            )

        # Always required: python >= 3.10
        python_ok, python_version = self._check_python_version("3.10")
        python_req = SystemRequirement(
            name="python",
            min_version="3.10",
            installed=python_version is not None,
            version=python_version,
        )
        requirements.append(python_req)

        if not python_req.installed:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.SYSTEM,
                    severity="error",
                    message="python is not installed or not available in PATH",
                    suggestion="Install Python 3.10+: https://python.org/downloads",
                )
            )
        elif not python_ok:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.SYSTEM,
                    severity="error",
                    message=(
                        f"Python version {python_version} does not meet "
                        f"minimum requirement (>= 3.10)"
                    ),
                    suggestion="Upgrade Python to version 3.10 or later",
                )
            )

        # Conditional: uv (if package_manager is uv)
        if config.project.package_manager == PackageManager.UV:
            uv_installed, uv_version = self._check_command_exists("uv")
            uv_req = SystemRequirement(
                name="uv",
                min_version=None,
                installed=uv_installed,
                version=uv_version,
            )
            requirements.append(uv_req)

            if not uv_installed:
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.SYSTEM,
                        severity="error",
                        message=(
                            "uv is not installed but is configured as the package manager"
                        ),
                        suggestion=(
                            "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
                        ),
                    )
                )

        # Conditional: JS package managers (npm, yarn, pnpm, bun)
        if config.project.package_manager in self.JS_PACKAGE_MANAGERS:
            pm_name = config.project.package_manager.value
            pm_installed, pm_version = self._check_command_exists(pm_name)
            pm_req = SystemRequirement(
                name=pm_name,
                min_version=None,
                installed=pm_installed,
                version=pm_version,
            )
            requirements.append(pm_req)

            if not pm_installed:
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.SYSTEM,
                        severity="error",
                        message=(
                            f"{pm_name} is not installed but is configured "
                            f"as the package manager"
                        ),
                        suggestion=f"Install {pm_name}: https://nodejs.org/ or npm install -g {pm_name}",
                    )
                )

        # Conditional: gh CLI (if orchestrator.enabled is true)
        if config.orchestrator.enabled:
            gh_installed, gh_version = self._check_command_exists("gh")
            gh_req = SystemRequirement(
                name="gh",
                min_version=None,
                installed=gh_installed,
                version=gh_version,
            )
            requirements.append(gh_req)

            if not gh_installed:
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.SYSTEM,
                        severity="warning",
                        message=(
                            "GitHub CLI (gh) is not installed; "
                            "orchestrator features may be limited"
                        ),
                        suggestion=(
                            "Install gh CLI: https://cli.github.com/"
                        ),
                    )
                )

        return ValidationResult(
            valid=len([i for i in issues if i.severity == "error"]) == 0,
            issues=issues,
        )

    # ========================================================================
    # PUBLIC METHODS - Project Name Validation
    # ========================================================================

    def validate_project_name(self, config: TACConfig) -> ValidationResult:
        """
        Validate project name is in slug format.

        Rules:
        - Lowercase letters, numbers, and hyphens only
        - No leading or trailing hyphens
        - Between 3 and 50 characters in length
        - Not a Windows reserved device name (CON, PRN, AUX, NUL, etc.)

        Args:
            config: TACConfig instance containing project configuration

        Returns:
            ValidationResult with domain-level issues for invalid project names
        """
        issues: list[ValidationIssue] = []
        name = config.project.name

        # Check length
        if len(name) < 3:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.DOMAIN,
                    severity="error",
                    message=(
                        f"Project name '{name}' is too short "
                        f"(minimum 3 characters, got {len(name)})"
                    ),
                    suggestion="Use a project name with at least 3 characters",
                )
            )
        elif len(name) > 50:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.DOMAIN,
                    severity="error",
                    message=(
                        f"Project name '{name}' is too long "
                        f"(maximum 50 characters, got {len(name)})"
                    ),
                    suggestion="Use a shorter project name (50 characters max)",
                )
            )

        # Check slug format: lowercase letters, numbers, hyphens only
        if not PROJECT_NAME_PATTERN.match(name):
            # Provide specific feedback
            if name.startswith("-"):
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.DOMAIN,
                        severity="error",
                        message=f"Project name '{name}' cannot start with a hyphen",
                        suggestion="Remove the leading hyphen from the project name",
                    )
                )
            elif name.endswith("-"):
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.DOMAIN,
                        severity="error",
                        message=f"Project name '{name}' cannot end with a hyphen",
                        suggestion="Remove the trailing hyphen from the project name",
                    )
                )
            elif name != name.lower():
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.DOMAIN,
                        severity="error",
                        message=f"Project name '{name}' must be lowercase",
                        suggestion=f"Use '{name.lower()}' instead",
                    )
                )
            elif re.search(r"[^a-z0-9-]", name):
                bad_chars = set(re.findall(r"[^a-z0-9-]", name))
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.DOMAIN,
                        severity="error",
                        message=(
                            f"Project name '{name}' contains invalid characters: "
                            f"{', '.join(sorted(repr(c) for c in bad_chars))}"
                        ),
                        suggestion=(
                            "Use only lowercase letters (a-z), numbers (0-9), "
                            "and hyphens (-)"
                        ),
                    )
                )
            # For names that are too short (1-2 chars) but valid chars,
            # the length check above already handles it. This else handles
            # any remaining edge cases.
            elif 1 <= len(name) <= 2:
                pass  # Already handled by length check above
            else:
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.DOMAIN,
                        severity="error",
                        message=(
                            f"Project name '{name}' does not match slug format"
                        ),
                        suggestion=(
                            "Use lowercase letters, numbers, and hyphens only. "
                            "No leading/trailing hyphens. 3-50 characters."
                        ),
                    )
                )

        # Check for Windows reserved names
        name_upper = name.upper()
        # Check both the full name and the name without extension
        name_base = name_upper.split(".")[0] if "." in name_upper else name_upper
        if name_base in WINDOWS_RESERVED_NAMES:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.DOMAIN,
                    severity="error",
                    message=(
                        f"Project name '{name}' is a Windows reserved device name"
                    ),
                    suggestion=(
                        "Choose a different project name. "
                        f"Reserved names: {', '.join(sorted(WINDOWS_RESERVED_NAMES))}"
                    ),
                )
            )

        return ValidationResult(
            valid=len([i for i in issues if i.severity == "error"]) == 0,
            issues=issues,
        )

    # ========================================================================
    # PUBLIC METHODS - Project Path Validation
    # ========================================================================

    def validate_project_path(self, config: TACConfig, output_dir: Path) -> ValidationResult:
        """
        Validate output directory path is safe for scaffolding.

        Checks:
        - No special Unicode characters in path
        - Total path length < 255 characters
        - Writable permissions on parent directory
        - No Windows reserved device names in any path segment

        Args:
            config: TACConfig instance (used for validation_mode context)
            output_dir: Target output directory path

        Returns:
            ValidationResult with domain-level issues for unsafe paths
        """
        issues: list[ValidationIssue] = []
        path_str = str(output_dir)

        # Check for special Unicode characters
        if SPECIAL_UNICODE_PATTERN.search(path_str):
            unicode_chars = set(SPECIAL_UNICODE_PATTERN.findall(path_str))
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.DOMAIN,
                    severity="error",
                    message=(
                        f"Output path contains special Unicode characters: "
                        f"{', '.join(sorted(repr(c) for c in unicode_chars))}"
                    ),
                    suggestion=(
                        "Use only ASCII characters in the output path to "
                        "ensure cross-platform compatibility"
                    ),
                )
            )

        # Check total path length
        if len(path_str) > MAX_PATH_LENGTH:
            issues.append(
                ValidationIssue(
                    level=ValidationLevel.DOMAIN,
                    severity="error",
                    message=(
                        f"Output path is too long ({len(path_str)} characters, "
                        f"maximum {MAX_PATH_LENGTH})"
                    ),
                    suggestion=(
                        "Use a shorter path for the output directory "
                        f"(maximum {MAX_PATH_LENGTH} characters)"
                    ),
                )
            )

        # Check writable permissions (skip if path is too long for the OS)
        try:
            path_exists = output_dir.exists()
        except OSError:
            # Path is too long or otherwise invalid for the OS filesystem
            # The length check above already reported the issue
            path_exists = False

        if path_exists:
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
        else:
            try:
                parent = output_dir.parent
                parent_exists = parent.exists()
            except OSError:
                parent_exists = False

            if parent_exists and not os.access(parent, os.W_OK):
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

        # Check for Windows reserved names in path segments
        for part in output_dir.parts:
            part_upper = part.upper()
            # Strip extension for comparison
            part_base = part_upper.split(".")[0] if "." in part_upper else part_upper
            if part_base in WINDOWS_RESERVED_NAMES:
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.DOMAIN,
                        severity="warning",
                        message=(
                            f"Path segment '{part}' is a Windows reserved device name"
                        ),
                        suggestion=(
                            "This path may cause issues on Windows systems. "
                            "Consider renaming the directory."
                        ),
                    )
                )

        return ValidationResult(
            valid=len([i for i in issues if i.severity == "error"]) == 0,
            issues=issues,
        )

    # ========================================================================
    # PUBLIC METHODS - Preflight Checks (Master Gate)
    # ========================================================================

    def run_preflight_checks(self, config: TACConfig, output_dir: Path) -> ValidationResult:
        """
        Master validation gate: run all checks before scaffold generation.

        Combines all validation layers in order:
        1. System requirements (git, python, package manager, gh)
        2. Project name validation (slug format)
        3. Project path validation (special chars, length, permissions)
        4. Config validation (framework/language/architecture compatibility)
        5. Filesystem validation (permissions, conflicts)
        6. Git validation (availability, uncommitted changes)

        This is the recommended entry point for complete pre-scaffold validation.

        Args:
            config: TACConfig instance to validate
            output_dir: Target output directory for scaffold

        Returns:
            ValidationResult with all accumulated issues from all validation layers
        """
        issues: list[ValidationIssue] = []

        # 1. System requirements
        system_result = self.validate_system_requirements(config)
        issues.extend(system_result.issues)

        # 2. Project name validation
        name_result = self.validate_project_name(config)
        issues.extend(name_result.issues)

        # 3. Project path validation
        path_result = self.validate_project_path(config, output_dir)
        issues.extend(path_result.issues)

        # 4. Config + Template + Filesystem + Git (existing pre_scaffold)
        scaffold_result = self.validate_pre_scaffold(config, output_dir)
        issues.extend(scaffold_result.issues)

        return ValidationResult(
            valid=len([i for i in issues if i.severity == "error"]) == 0,
            issues=issues,
        )

    # ========================================================================
    # PRIVATE METHODS - Filesystem Validation
    # ========================================================================

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

    # ========================================================================
    # PRIVATE METHODS - Git Validation
    # ========================================================================

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

    # ========================================================================
    # PRIVATE METHODS - System Requirement Helpers
    # ========================================================================

    def _check_git_version(self, min_version: str = "2.30") -> tuple[bool, str | None]:
        """
        Check if git is installed and meets minimum version requirement.

        Runs `git --version` and parses the output to extract the version number,
        then compares it against the specified minimum version.

        Args:
            min_version: Minimum required git version (e.g., "2.30")

        Returns:
            Tuple of (meets_requirement, detected_version_string_or_none)
        """
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                return False, None

            # Parse version from "git version X.Y.Z"
            output = result.stdout.strip()
            version_match = re.search(r"(\d+\.\d+(?:\.\d+)*)", output)
            if not version_match:
                return False, None

            version_str = version_match.group(1)
            meets_min = self._compare_versions(version_str, min_version)
            return meets_min, version_str

        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False, None

    def _check_python_version(self, min_version: str = "3.10") -> tuple[bool, str | None]:
        """
        Check if python is installed and meets minimum version requirement.

        Tries `python3 --version` first, then falls back to `python --version`.
        Parses the output to extract the version number and compares it against
        the specified minimum version.

        Args:
            min_version: Minimum required Python version (e.g., "3.10")

        Returns:
            Tuple of (meets_requirement, detected_version_string_or_none)
        """
        # Try python3 first, then python
        for cmd in ["python3", "python"]:
            try:
                result = subprocess.run(
                    [cmd, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode != 0:
                    continue

                # Parse version from "Python X.Y.Z"
                output = result.stdout.strip()
                version_match = re.search(r"(\d+\.\d+(?:\.\d+)*)", output)
                if not version_match:
                    continue

                version_str = version_match.group(1)
                meets_min = self._compare_versions(version_str, min_version)
                return meets_min, version_str

            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue

        return False, None

    def _check_command_exists(self, cmd: str) -> tuple[bool, str | None]:
        """
        Check if a command is available on the system PATH and attempt to get its version.

        Runs `<cmd> --version` and captures both stdout and stderr to extract
        version information. Returns whether the command exists and its version
        string if detectable.

        Args:
            cmd: Command name to check (e.g., "uv", "npm", "gh")

        Returns:
            Tuple of (is_installed, version_string_or_none)
        """
        if not shutil.which(cmd):
            return False, None

        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            # Some tools output to stderr, so check both
            output = result.stdout.strip() or result.stderr.strip()
            if output:
                version_match = re.search(r"(\d+\.\d+(?:\.\d+)*)", output)
                if version_match:
                    return True, version_match.group(1)
            return True, None

        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            # Command exists (shutil.which found it) but can't get version
            return True, None

    def _parse_version(self, version_str: str) -> tuple[int, ...]:
        """
        Parse a version string into a tuple of integers for comparison.

        Splits the version string on dots and converts each component to an integer.
        Non-numeric suffixes (e.g., "-rc1", "beta") are stripped from the last component.

        Args:
            version_str: Version string (e.g., "2.39.1", "3.10", "3.10.0-rc1")

        Returns:
            Tuple of version integers (e.g., (2, 39, 1), (3, 10))
        """
        parts = version_str.split(".")
        result: list[int] = []
        for part in parts:
            # Strip non-numeric suffixes (e.g., "1-rc1" -> "1")
            numeric_match = re.match(r"(\d+)", part)
            if numeric_match:
                result.append(int(numeric_match.group(1)))
            else:
                break
        return tuple(result)

    def _compare_versions(self, version: str, min_version: str) -> bool:
        """
        Compare two version strings.

        Parses both version strings into tuples of integers and performs a
        lexicographic comparison. Missing trailing components are treated as zero
        (e.g., "2.30" is equivalent to "2.30.0").

        Args:
            version: Detected version string (e.g., "2.39.1")
            min_version: Minimum required version string (e.g., "2.30")

        Returns:
            True if version >= min_version, False otherwise
        """
        v = self._parse_version(version)
        m = self._parse_version(min_version)

        # Pad shorter tuple with zeros for comparison
        max_len = max(len(v), len(m))
        v_padded = v + (0,) * (max_len - len(v))
        m_padded = m + (0,) * (max_len - len(m))

        return v_padded >= m_padded
