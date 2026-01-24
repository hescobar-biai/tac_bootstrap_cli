"""
IDK: code-generation, entity-creation, template-instantiation, ddd-scaffolding
Responsibility: Orchestrates CRUD entity generation following vertical slice architecture
Invariants: Validates before writing, all-or-nothing file creation, no rollback
"""

import re
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, Field

from tac_bootstrap.domain.models import EntitySpec, TACConfig
from tac_bootstrap.infrastructure.fs import FileSystem
from tac_bootstrap.infrastructure.template_repo import TemplateRepository

# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================


class ValidationError(Exception):
    """Raised when EntitySpec validation fails."""

    pass


class PreconditionError(Exception):
    """Raised when required preconditions are not met (e.g., missing base classes)."""

    pass


class FileSystemError(Exception):
    """Raised when filesystem operations fail."""

    pass


# ============================================================================
# RESULT MODEL
# ============================================================================


class GenerateResult(BaseModel):
    """
    IDK: generation-result, entity-metadata, file-tracking
    Responsibility: Contains metadata about generated entity with file paths and location
    Invariants: All file paths are relative to project root, directory is absolute path
    """

    entity_name: str = Field(..., description="Name of the generated entity (PascalCase)")
    capability: str = Field(..., description="Capability/vertical slice name (snake_case)")
    files_created: List[str] = Field(
        ..., description="List of created file paths (relative to project_root)"
    )
    directory: str = Field(
        ..., description="Absolute path to the generated capability directory"
    )


# ============================================================================
# GENERATE SERVICE
# ============================================================================


class GenerateService:
    """
    IDK: entity-orchestration, vertical-slice-generation, precondition-checking, template-rendering
    Responsibility: Coordinates entity generation with validation-first approach
    Invariants: Fails fast on validation errors, no rollback logic, all-or-nothing file creation
    """

    def __init__(self, template_repo: TemplateRepository, fs: FileSystem):
        """
        Initialize GenerateService with dependencies.

        Args:
            template_repo: TemplateRepository for rendering Jinja2 templates
            fs: FileSystem for safe, idempotent filesystem operations
        """
        self.template_repo = template_repo
        self.fs = fs

    def generate_entity(
        self,
        entity: EntitySpec,
        project_root: Path,
        config: TACConfig,
        force: bool = False,
    ) -> GenerateResult:
        """
        Generate a complete CRUD entity following vertical slice architecture.

        This method orchestrates the entire entity generation process:
        1. Validates EntitySpec format
        2. Checks that base classes exist
        3. Checks for existing files (raises error if any exist when force=False)
        4. Creates directory structure (domain/, application/, infrastructure/, api/)
        5. Renders entity templates
        6. Writes files to filesystem
        7. Returns GenerateResult with metadata

        Args:
            entity: EntitySpec defining the entity to generate
            project_root: Root directory of the target project
            config: TACConfig with project configuration (paths, etc.)
            force: If True, overwrite existing files; if False, raise error if files exist

        Returns:
            GenerateResult containing entity metadata and list of created files

        Raises:
            ValidationError: If EntitySpec validation fails (invalid name or capability)
            PreconditionError: If required base classes don't exist
            FileExistsError: If target files exist and force=False
            FileSystemError: If filesystem operations fail (template rendering, I/O errors)

        Example:
            >>> service = GenerateService(template_repo, fs)
            >>> entity = EntitySpec(name="User", capability="users")
            >>> result = service.generate_entity(entity, Path("/project"), config)
            >>> print(result.files_created)
            ['src/users/domain/user.py', 'src/users/application/schemas.py', ...]
        """
        # Phase 1: Validation
        self._validate_entity_spec(entity)
        self._check_base_classes(project_root, config)

        # Phase 2: Determine output directory
        output_dir = project_root / config.paths.app_root / entity.capability

        # Phase 3: Check for existing files (all-or-nothing)
        self._check_existing_files(output_dir, entity, force)

        # Phase 4: Create directory structure
        # Create app_root if it doesn't exist (mkdir -p behavior)
        app_root_path = project_root / config.paths.app_root
        self.fs.ensure_directory(app_root_path)

        # Create capability directory
        self.fs.ensure_directory(output_dir)

        # Create vertical slice subdirectories
        for subdir in ["domain", "application", "infrastructure", "api"]:
            self.fs.ensure_directory(output_dir / subdir)

        # Phase 5: Render templates
        rendered_templates = self._render_templates(entity, config)

        # Phase 6: Write files
        files_created = self._write_files(output_dir, rendered_templates, project_root)

        # Phase 7: Return result
        return GenerateResult(
            entity_name=entity.name,
            capability=entity.capability,
            files_created=files_created,
            directory=str(output_dir),
        )

    def _validate_entity_spec(self, entity: EntitySpec) -> None:
        """
        Validate EntitySpec format.

        Checks that entity name and capability meet required format constraints:
        - Entity name must be a valid Python identifier
        - Capability must be a valid package name (lowercase, alphanumeric + underscore,
          starts with letter, max 50 chars)
        - Both must be non-empty

        Args:
            entity: EntitySpec to validate

        Raises:
            ValidationError: If any validation rule fails
        """
        # Validate entity name is non-empty
        if not entity.name or not entity.name.strip():
            raise ValidationError("Entity name cannot be empty")

        # Validate entity name is valid Python identifier
        if not entity.name.isidentifier():
            raise ValidationError(
                f"Entity name '{entity.name}' must be a valid Python identifier "
                "(alphanumeric and underscores, cannot start with a number)"
            )

        # Validate capability is non-empty
        if not entity.capability or not entity.capability.strip():
            raise ValidationError("Capability name cannot be empty")

        # Validate capability is valid package name
        # Pattern: lowercase, alphanumeric + underscore, starts with letter, max 50 chars
        if not re.match(r"^[a-z][a-z0-9_]{0,49}$", entity.capability):
            raise ValidationError(
                f"Capability name '{entity.capability}' must be lowercase, start with a letter, "
                "contain only alphanumeric characters and underscores, and be max 50 characters"
            )

    def _check_base_classes(self, project_root: Path, config: TACConfig) -> None:
        """
        Check that required base classes exist.

        Verifies that all required base class files exist in the shared directory:
        - base_entity.py (domain layer)
        - base_repository.py (infrastructure layer)
        - base_schema.py (domain layer)
        - base_service.py (application layer)

        These base classes are required for generated entities to inherit from.

        Args:
            project_root: Root directory of the target project
            config: TACConfig with paths configuration

        Raises:
            PreconditionError: If any required base class file is missing
        """
        shared_dir = project_root / config.paths.app_root / "shared"

        # Define required base class files
        required_base_classes = {
            "base_entity.py": shared_dir / "domain" / "base_entity.py",
            "base_repository.py": shared_dir / "infrastructure" / "base_repository.py",
            "base_schema.py": shared_dir / "domain" / "base_schema.py",
            "base_service.py": shared_dir / "application" / "base_service.py",
        }

        # Check for missing base classes
        missing_files = []
        for name, path in required_base_classes.items():
            if not self.fs.file_exists(path):
                missing_files.append(str(path))

        if missing_files:
            raise PreconditionError(
                "Required base classes are missing. Please ensure the shared/ directory "
                "exists with all base classes. Missing files:\n"
                + "\n".join(f"  - {f}" for f in missing_files)
            )

    def _check_existing_files(
        self, output_dir: Path, entity: EntitySpec, force: bool
    ) -> None:
        """
        Check for existing files with all-or-nothing approach.

        If force=False, checks that NONE of the target files exist. If ANY file exists,
        raises FileExistsError with the list of conflicting files.

        If force=True, skips the check (files will be overwritten).

        This all-or-nothing approach prevents partial/corrupted state where some files
        are generated and others already exist.

        Args:
            output_dir: Target directory for entity generation
            entity: EntitySpec with entity information
            force: If True, skip the check; if False, enforce no existing files

        Raises:
            FileExistsError: If ANY target file exists when force=False
        """
        if force:
            return  # Skip check when force=True

        # Build list of target file paths
        target_files = [
            output_dir / "domain" / f"{entity.snake_name}.py",
            output_dir / "application" / "schemas.py",
            output_dir / "application" / "service.py",
            output_dir / "infrastructure" / "repository.py",
            output_dir / "infrastructure" / "models.py",
            output_dir / "api" / "routes.py",
        ]

        # Check for existing files
        existing_files = []
        for file_path in target_files:
            if self.fs.file_exists(file_path):
                existing_files.append(str(file_path))

        if existing_files:
            raise FileExistsError(
                f"Cannot generate entity '{entity.name}': the following files already exist:\n"
                + "\n".join(f"  - {f}" for f in existing_files)
                + "\n\nUse force=True to overwrite existing files."
            )

    def _render_templates(
        self, entity: EntitySpec, config: TACConfig
    ) -> Dict[str, str]:
        """
        Render entity templates with context.

        Renders all 6 entity templates (domain, schemas, service, repository, models, routes)
        using the provided entity and config as template context.

        Template mapping:
        - domain/{snake_name}.py <- entity/domain.py.j2
        - application/schemas.py <- entity/schemas.py.j2
        - application/service.py <- entity/service.py.j2
        - infrastructure/repository.py <- entity/repository.py.j2
        - infrastructure/models.py <- entity/models.py.j2
        - api/routes.py <- entity/routes.py.j2

        Args:
            entity: EntitySpec to pass to templates
            config: TACConfig to pass to templates

        Returns:
            Dictionary mapping output file paths (relative) to rendered content

        Raises:
            FileSystemError: If template rendering fails
        """
        # Define template mapping
        template_mapping = {
            f"domain/{entity.snake_name}.py": "entity/domain.py.j2",
            "application/schemas.py": "entity/schemas.py.j2",
            "application/service.py": "entity/service.py.j2",
            "infrastructure/repository.py": "entity/repository.py.j2",
            "infrastructure/models.py": "entity/models.py.j2",
            "api/routes.py": "entity/routes.py.j2",
        }

        # Create template context
        context = {"entity": entity, "config": config}

        # Render templates
        rendered_templates = {}
        try:
            for output_path, template_name in template_mapping.items():
                content = self.template_repo.render(template_name, context)
                rendered_templates[output_path] = content
        except Exception as e:
            raise FileSystemError(f"Failed to render template '{template_name}': {e}")

        return rendered_templates

    def _write_files(
        self,
        output_dir: Path,
        rendered_templates: Dict[str, str],
        project_root: Path,
    ) -> List[str]:
        """
        Write rendered templates to filesystem.

        Writes all rendered template content to the filesystem and creates empty
        __init__.py files in each subdirectory to make them valid Python packages.

        Args:
            output_dir: Target directory for entity generation
            rendered_templates: Dictionary mapping output paths to rendered content
            project_root: Project root for computing relative paths

        Returns:
            List of created file paths (relative to project_root)

        Raises:
            FileSystemError: If filesystem I/O operations fail
        """
        files_created = []

        try:
            # Write rendered templates
            for output_path, content in rendered_templates.items():
                full_path = output_dir / output_path
                self.fs.write_file(full_path, content)
                # Store relative path
                relative_path = str(full_path.relative_to(project_root))
                files_created.append(relative_path)

            # Create empty __init__.py files in each subdirectory
            for subdir in ["domain", "application", "infrastructure", "api"]:
                init_path = output_dir / subdir / "__init__.py"
                self.fs.write_file(init_path, "")
                relative_path = str(init_path.relative_to(project_root))
                files_created.append(relative_path)

        except Exception as e:
            raise FileSystemError(f"Failed to write files: {e}")

        return files_created
