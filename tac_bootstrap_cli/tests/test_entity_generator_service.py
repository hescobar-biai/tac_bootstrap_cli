"""Tests for EntityGeneratorService."""

import tempfile
from pathlib import Path

import pytest
import yaml

from tac_bootstrap.application.entity_generator_service import EntityGeneratorService
from tac_bootstrap.domain.entity_config import EntitySpec, FieldSpec, FieldType
from tac_bootstrap.domain.models import (
    Architecture,
)


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with config.yml."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)

        # Create a minimal valid config.yml as plain dict
        config_dict = {
            "version": "0.9.6",
            "schema_version": 1,
            "project": {
                "name": "test-project",
                "language": "python",
                "package_manager": "uv",
                "architecture": "ddd",
            },
            "paths": {
                "app_root": "src",
            },
            "commands": {
                "start": "python -m app",
                "test": "pytest",
            },
            "claude": {
                "settings": {
                    "project_name": "test-project",
                },
            },
        }

        config_path = project_dir / "config.yml"
        with open(config_path, "w") as f:
            yaml.dump(config_dict, f)

        yield project_dir


@pytest.fixture
def sample_entity_spec():
    """Create a sample entity specification."""
    return EntitySpec(
        name="Product",
        capability="catalog",
        fields=[
            FieldSpec(name="name", field_type=FieldType.STRING, required=True),
            FieldSpec(name="price", field_type=FieldType.FLOAT, required=True),
            FieldSpec(name="description", field_type=FieldType.TEXT, required=False),
        ],
        authorized=False,
        async_mode=False,
        with_events=False,
    )


class TestValidateProject:
    """Test validate_project method."""

    def test_valid_project(self, temp_project_dir):
        """Test validation succeeds with valid config.yml."""
        service = EntityGeneratorService()
        config = service.validate_project(temp_project_dir)

        assert config.project.name == "test-project"
        assert config.project.architecture == Architecture.DDD

    def test_missing_config(self):
        """Test validation fails with missing config.yml."""
        service = EntityGeneratorService()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            with pytest.raises(ValueError, match="No config.yml found"):
                service.validate_project(project_dir)

    def test_invalid_yaml(self):
        """Test validation fails with invalid YAML."""
        service = EntityGeneratorService()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            config_path = project_dir / "config.yml"

            # Write invalid YAML
            with open(config_path, "w") as f:
                f.write("invalid: yaml: content: [")

            with pytest.raises(ValueError, match="Failed to parse config.yml"):
                service.validate_project(project_dir)

    def test_wrong_architecture(self):
        """Test validation fails with non-DDD architecture."""
        service = EntityGeneratorService()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create config with SIMPLE architecture as plain dict
            config_dict = {
                "version": "0.9.6",
                "schema_version": 1,
                "project": {
                    "name": "test-project",
                    "language": "python",
                    "package_manager": "uv",
                    "architecture": "simple",  # SIMPLE instead of DDD
                },
                "paths": {
                    "app_root": "src",
                },
                "commands": {
                    "start": "python -m app",
                    "test": "pytest",
                },
                "claude": {
                    "settings": {
                        "project_name": "test-project",
                    },
                },
            }

            config_path = project_dir / "config.yml"
            with open(config_path, "w") as f:
                yaml.dump(config_dict, f)

            with pytest.raises(ValueError, match="Entity generation requires architecture"):
                service.validate_project(project_dir)


class TestCheckConflicts:
    """Test check_conflicts method."""

    def test_no_conflict(self, temp_project_dir, sample_entity_spec):
        """Test no conflict when entity doesn't exist."""
        service = EntityGeneratorService()

        # Should not raise
        service.check_conflicts(temp_project_dir, sample_entity_spec, force=False)

    def test_conflict_without_force(self, temp_project_dir, sample_entity_spec):
        """Test conflict detection when entity exists and force=False."""
        service = EntityGeneratorService()

        # Create the entity file
        entity_path = (
            temp_project_dir
            / "domain"
            / "catalog"
            / "entities"
            / "product.py"
        )
        entity_path.parent.mkdir(parents=True, exist_ok=True)
        entity_path.write_text("# existing entity")

        with pytest.raises(ValueError, match="already exists"):
            service.check_conflicts(temp_project_dir, sample_entity_spec, force=False)

    def test_conflict_with_force(self, temp_project_dir, sample_entity_spec):
        """Test no error when entity exists and force=True."""
        service = EntityGeneratorService()

        # Create the entity file
        entity_path = (
            temp_project_dir
            / "domain"
            / "catalog"
            / "entities"
            / "product.py"
        )
        entity_path.parent.mkdir(parents=True, exist_ok=True)
        entity_path.write_text("# existing entity")

        # Should not raise
        service.check_conflicts(temp_project_dir, sample_entity_spec, force=True)


class TestBuildGenerationPlan:
    """Test build_generation_plan method."""

    def test_basic_plan(self, temp_project_dir, sample_entity_spec):
        """Test plan includes all basic files."""
        service = EntityGeneratorService()
        config = service.validate_project(temp_project_dir)
        plan = service.build_generation_plan(sample_entity_spec, config)

        # Should have 6 files: domain entity, schemas, orm_model, repository, service, routes
        assert len(plan) == 6

        file_names = [op.path.name for op in plan]
        assert "product.py" in file_names  # domain entity
        assert "product_schemas.py" in file_names
        assert "product_model.py" in file_names  # ORM model
        assert "product_repository.py" in file_names
        assert "product_service.py" in file_names
        assert "product_routes.py" in file_names

    def test_async_plan(self, temp_project_dir):
        """Test plan uses async repository when async_mode=True."""
        service = EntityGeneratorService()
        config = service.validate_project(temp_project_dir)

        entity_spec = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="name", field_type=FieldType.STRING)],
            async_mode=True,
        )

        plan = service.build_generation_plan(entity_spec, config)

        # Check that async repository template is used
        repo_op = next(op for op in plan if "repository" in str(op.path))
        assert repo_op.template_name == "entity/repository_async.py.j2"

    def test_with_events_plan(self, temp_project_dir):
        """Test plan includes events when with_events=True."""
        service = EntityGeneratorService()
        config = service.validate_project(temp_project_dir)

        entity_spec = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[FieldSpec(name="name", field_type=FieldType.STRING)],
            with_events=True,
        )

        plan = service.build_generation_plan(entity_spec, config)

        # Should have 7 files (6 basic + events)
        assert len(plan) == 7

        file_names = [op.path.name for op in plan]
        assert "product_events.py" in file_names


class TestGenerate:
    """Test generate method."""

    def test_dry_run(self, temp_project_dir, sample_entity_spec):
        """Test dry run doesn't create files."""
        service = EntityGeneratorService()

        result = service.generate(
            entity_spec=sample_entity_spec,
            target_dir=temp_project_dir,
            dry_run=True,
            force=False,
        )

        assert result.success is True
        # domain, schemas, orm_model, repository, service, routes
        assert len(result.files_created) == 6

        # Verify no files were actually created
        entity_path = (
            temp_project_dir
            / "domain"
            / "catalog"
            / "entities"
            / "product.py"
        )
        assert not entity_path.exists()

    def test_real_generation(self, temp_project_dir, sample_entity_spec):
        """Test real generation creates all files."""
        service = EntityGeneratorService()

        result = service.generate(
            entity_spec=sample_entity_spec,
            target_dir=temp_project_dir,
            dry_run=False,
            force=False,
        )

        # domain, schemas, orm_model, repository, service, routes
        assert len(result.files_created) == 6

        # Verify files were created
        entity_path = (
            temp_project_dir
            / "domain"
            / "catalog"
            / "entities"
            / "product.py"
        )
        assert entity_path.exists()

        schemas_path = (
            temp_project_dir
            / "domain"
            / "catalog"
            / "schemas"
            / "product_schemas.py"
        )
        assert schemas_path.exists()

        # Verify content contains expected elements
        entity_content = entity_path.read_text()
        assert "class Product(Entity):" in entity_content
        assert "name: str" in entity_content
        assert "price: float" in entity_content

    def test_force_overwrite(self, temp_project_dir, sample_entity_spec):
        """Test force flag overwrites existing files."""
        service = EntityGeneratorService()

        # Create existing entity
        entity_path = (
            temp_project_dir
            / "domain"
            / "catalog"
            / "entities"
            / "product.py"
        )
        entity_path.parent.mkdir(parents=True, exist_ok=True)
        entity_path.write_text("# OLD CONTENT")

        # Generate with force=True
        result = service.generate(
            entity_spec=sample_entity_spec,
            target_dir=temp_project_dir,
            dry_run=False,
            force=True,
        )

        assert result.success is True

        # Verify file was overwritten
        new_content = entity_path.read_text()
        assert "# OLD CONTENT" not in new_content
        assert "class Product(Entity):" in new_content
