"""
Entity Generator Service

Orchestrates the generation of complete CRUD vertical slices for entities.
Validates project configuration, checks for conflicts, builds generation plans,
and applies templates to the filesystem.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml

from tac_bootstrap.domain.entity_config import EntitySpec
from tac_bootstrap.domain.models import Architecture, TACConfig
from tac_bootstrap.infrastructure.fs import FileSystem
from tac_bootstrap.infrastructure.template_repo import TemplateRepository

# ============================================================================
# DATA MODELS
# ============================================================================


@dataclass
class FileOperation:
    """Represents a file to be created during entity generation."""

    path: Path
    template_name: str
    description: str


@dataclass
class GenerationResult:
    """Result of entity generation operation."""

    success: bool
    files_created: List[Path]
    message: str


# ============================================================================
# ENTITY GENERATOR SERVICE
# ============================================================================


class EntityGeneratorService:
    """
    Service for generating complete CRUD entities.

    Orchestrates validation, conflict detection, plan building, and file creation
    for entity generation following vertical slice architecture.
    """

    def __init__(
        self,
        template_repo: TemplateRepository | None = None,
        filesystem: FileSystem | None = None,
    ):
        """
        Initialize the entity generator service.

        Args:
            template_repo: Template repository for rendering templates
            filesystem: Filesystem interface for file operations
        """
        self.template_repo = template_repo or TemplateRepository()
        self.filesystem = filesystem or FileSystem()

    def validate_project(self, target_dir: Path) -> TACConfig:
        """
        Validate project configuration and architecture.

        Args:
            target_dir: Target project directory

        Returns:
            Validated TACConfig instance

        Raises:
            ValueError: If config.yml is missing, invalid, or architecture is not DDD
        """
        config_path = target_dir / "config.yml"

        # Check config.yml exists
        if not config_path.exists():
            raise ValueError(
                f"No config.yml found at {target_dir}. "
                "Run this command from a TAC Bootstrap project root."
            )

        # Load YAML
        try:
            with open(config_path, "r") as f:
                raw_config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse config.yml: {e}") from e

        # Validate with Pydantic
        try:
            config = TACConfig(**raw_config)
        except Exception as e:
            raise ValueError(f"Invalid config.yml: {e}") from e

        # Validate architecture
        supported_architectures = [
            Architecture.DDD,
            Architecture.CLEAN,
            Architecture.HEXAGONAL,
        ]
        if config.project.architecture not in supported_architectures:
            supported_values = [a.value for a in supported_architectures]
            raise ValueError(
                f"Entity generation requires architecture in {supported_values}. "
                f"Current architecture: {config.project.architecture.value}"
            )

        return config

    def check_conflicts(
        self, target_dir: Path, entity_spec: EntitySpec, force: bool
    ) -> None:
        """
        Check for conflicting entity files.

        Args:
            target_dir: Target project directory
            entity_spec: Entity specification
            force: Whether to allow overwriting existing files

        Raises:
            ValueError: If entity already exists and force is False
        """
        # Build path to domain entity file
        capability_path = entity_spec.capability.replace("-", "_")
        entity_file = (
            target_dir
            / "domain"
            / capability_path
            / "entities"
            / f"{entity_spec.snake_name}.py"
        )

        # Check if entity exists
        if entity_file.exists() and not force:
            relative_path = entity_file.relative_to(target_dir)
            raise ValueError(
                f"Entity '{entity_spec.name}' already exists at {relative_path}. "
                "Use --force to overwrite."
            )

    def build_generation_plan(
        self, entity_spec: EntitySpec, config: TACConfig
    ) -> List[FileOperation]:
        """
        Build a plan of files to create for the entity.

        Args:
            entity_spec: Entity specification
            config: Project configuration

        Returns:
            List of file operations to perform
        """
        capability_path = entity_spec.capability.replace("-", "_")
        plan: List[FileOperation] = []

        # Domain entity model
        plan.append(
            FileOperation(
                path=Path("domain")
                / capability_path
                / "entities"
                / f"{entity_spec.snake_name}.py",
                template_name="entity/entity.py.j2",
                description=f"Domain entity: {entity_spec.name}",
            )
        )

        # Pydantic schemas
        plan.append(
            FileOperation(
                path=Path("domain")
                / capability_path
                / "schemas"
                / f"{entity_spec.snake_name}_schemas.py",
                template_name="entity/schemas.py.j2",
                description=(
                    f"Pydantic schemas: {entity_spec.name}Create, "
                    f"{entity_spec.name}Update, {entity_spec.name}Response"
                ),
            )
        )

        # Repository (sync or async)
        if entity_spec.async_mode:
            plan.append(
                FileOperation(
                    path=Path("infrastructure")
                    / capability_path
                    / "repositories"
                    / f"{entity_spec.snake_name}_repository.py",
                    template_name="entity/repository_async.py.j2",
                    description=f"Async repository: {entity_spec.name}Repository",
                )
            )
        else:
            plan.append(
                FileOperation(
                    path=Path("infrastructure")
                    / capability_path
                    / "repositories"
                    / f"{entity_spec.snake_name}_repository.py",
                    template_name="entity/repository.py.j2",
                    description=f"Repository: {entity_spec.name}Repository",
                )
            )

        # Service layer
        plan.append(
            FileOperation(
                path=Path("application")
                / capability_path
                / "services"
                / f"{entity_spec.snake_name}_service.py",
                template_name="entity/service.py.j2",
                description=f"Service: {entity_spec.name}Service",
            )
        )

        # API routes
        plan.append(
            FileOperation(
                path=Path("interfaces")
                / "api"
                / capability_path
                / f"{entity_spec.snake_name}_routes.py",
                template_name="entity/routes.py.j2",
                description=f"API routes: /{entity_spec.plural_name}",
            )
        )

        # Domain events (conditional)
        if entity_spec.with_events:
            plan.append(
                FileOperation(
                    path=Path("domain")
                    / capability_path
                    / "events"
                    / f"{entity_spec.snake_name}_events.py",
                    template_name="entity/events.py.j2",
                    description=(
                        f"Domain events: {entity_spec.name}Created, "
                        f"{entity_spec.name}Updated, {entity_spec.name}Deleted"
                    ),
                )
            )

        return plan

    def generate(
        self,
        entity_spec: EntitySpec,
        target_dir: Path,
        dry_run: bool = False,
        force: bool = False,
    ) -> GenerationResult:
        """
        Generate entity files.

        Args:
            entity_spec: Entity specification
            target_dir: Target project directory
            dry_run: If True, return plan without creating files
            force: If True, overwrite existing files

        Returns:
            GenerationResult with files created and success status

        Raises:
            ValueError: If validation fails or conflicts are detected
        """
        # Validate project
        config = self.validate_project(target_dir)

        # Check for conflicts
        self.check_conflicts(target_dir, entity_spec, force)

        # Build generation plan
        plan = self.build_generation_plan(entity_spec, config)

        # Dry run: return plan without creating files
        if dry_run:
            return GenerationResult(
                success=True,
                files_created=[op.path for op in plan],
                message=f"Dry run: Would create {len(plan)} files for entity {entity_spec.name}",
            )

        # Create files
        created_files: List[Path] = []

        for file_op in plan:
            # Build full path
            full_path = target_dir / file_op.path

            # Ensure parent directory exists
            self.filesystem.ensure_directory(full_path.parent)

            # Render template
            try:
                content = self.template_repo.render(
                    file_op.template_name,
                    context={"entity_spec": entity_spec, "config": config},
                )

                # Write file
                self.filesystem.write_file(full_path, content)
                created_files.append(file_op.path)

            except Exception as e:
                raise ValueError(
                    f"Failed to generate {file_op.description}: {e}"
                ) from e

        return GenerationResult(
            success=True,
            files_created=created_files,
            message=(
                f"Successfully created {len(created_files)} files "
                f"for entity {entity_spec.name}"
            ),
        )
