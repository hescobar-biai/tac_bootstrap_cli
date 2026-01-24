"""Tests for GenerateService - Entity Generation Orchestration.

This module tests the GenerateService application service that orchestrates
entity generation following vertical slice architecture. Tests cover:
- EntitySpec validation (name format, capability format)
- Precondition checking (base classes existence)
- File conflict detection (all-or-nothing approach)
- Template rendering and filesystem operations
- Force overwrite behavior
- Error handling and messaging
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest

from tac_bootstrap.application.generate_service import (
    FileSystemError,
    GenerateResult,
    GenerateService,
    PreconditionError,
    ValidationError,
)
from tac_bootstrap.domain.entity_config import EntitySpec, FieldSpec, FieldType
from tac_bootstrap.domain.models import TACConfig
from tac_bootstrap.infrastructure.fs import FileSystem
from tac_bootstrap.infrastructure.template_repo import TemplateRepository

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_fs():
    """Create a mock FileSystem."""
    return Mock(spec=FileSystem)


@pytest.fixture
def mock_template_repo():
    """Create a mock TemplateRepository."""
    return Mock(spec=TemplateRepository)


@pytest.fixture
def generate_service(mock_template_repo, mock_fs):
    """Create a GenerateService with mocked dependencies."""
    return GenerateService(template_repo=mock_template_repo, fs=mock_fs)


@pytest.fixture
def sample_entity_spec():
    """Create a sample EntitySpec for testing."""
    return EntitySpec(
        name="Product",
        capability="catalog",
        fields=[
            FieldSpec(name="title", field_type=FieldType.STRING, max_length=200, required=True),
            FieldSpec(name="price", field_type=FieldType.DECIMAL, required=True),
            FieldSpec(name="description", field_type=FieldType.TEXT, required=False),
        ],
        authorized=False,
        async_mode=False,
    )


@pytest.fixture
def authorized_entity_spec():
    """Create an authorized EntitySpec for testing."""
    return EntitySpec(
        name="Order",
        capability="orders",
        fields=[
            FieldSpec(name="total", field_type=FieldType.DECIMAL, required=True),
            FieldSpec(name="status", field_type=FieldType.STRING, max_length=50, required=True),
        ],
        authorized=True,
        async_mode=True,
    )


@pytest.fixture
def mock_config():
    """Create a mock TACConfig."""
    config = Mock(spec=TACConfig)
    config.paths = Mock()
    config.paths.app_root = "src"
    return config


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# ============================================================================
# TEST ENTITY SPEC VALIDATION
# ============================================================================


class TestValidateEntitySpec:
    """Tests for _validate_entity_spec method.

    Note: Many invalid EntitySpec cases are caught by Pydantic validators
    in the EntitySpec model itself, so we only test cases that reach
    GenerateService._validate_entity_spec.
    """

    def test_valid_entity_spec(self, generate_service, sample_entity_spec):
        """Valid EntitySpec should pass validation."""
        # Should not raise
        generate_service._validate_entity_spec(sample_entity_spec)

    def test_invalid_capability_format(self, generate_service):
        """Capability with invalid format should raise ValidationError.

        Note: EntitySpec accepts kebab-case but GenerateService requires snake_case.
        This test verifies that GenerateService rejects kebab-case capabilities.
        """
        # EntitySpec will accept kebab-case, but GenerateService will reject it
        entity = EntitySpec(
            name="Product",
            capability="product-catalog",  # kebab-case
            fields=[FieldSpec(name="name", field_type=FieldType.STRING)],
        )

        with pytest.raises(
            ValidationError, match="must be lowercase, start with a letter"
        ):
            generate_service._validate_entity_spec(entity)


# ============================================================================
# TEST BASE CLASSES PRECONDITION
# ============================================================================


class TestCheckBaseClasses:
    """Tests for _check_base_classes method."""

    def test_all_base_classes_exist(
        self, generate_service, mock_fs, temp_project_dir, mock_config
    ):
        """All base classes exist - should not raise."""
        # Mock all base class files as existing
        mock_fs.file_exists.return_value = True

        # Should not raise
        generate_service._check_base_classes(temp_project_dir, mock_config)

        # Verify file_exists was called for each base class
        assert mock_fs.file_exists.call_count == 4

    def test_missing_base_entity(
        self, generate_service, mock_fs, temp_project_dir, mock_config
    ):
        """Missing base_entity.py should raise PreconditionError."""

        def side_effect(path):
            return "base_entity.py" not in str(path)

        mock_fs.file_exists.side_effect = side_effect

        with pytest.raises(PreconditionError, match="Required base classes are missing"):
            generate_service._check_base_classes(temp_project_dir, mock_config)

    def test_missing_base_repository(
        self, generate_service, mock_fs, temp_project_dir, mock_config
    ):
        """Missing base_repository.py should raise PreconditionError."""

        def side_effect(path):
            return "base_repository.py" not in str(path)

        mock_fs.file_exists.side_effect = side_effect

        with pytest.raises(PreconditionError, match="Required base classes are missing"):
            generate_service._check_base_classes(temp_project_dir, mock_config)

    def test_missing_base_schema(
        self, generate_service, mock_fs, temp_project_dir, mock_config
    ):
        """Missing base_schema.py should raise PreconditionError."""

        def side_effect(path):
            return "base_schema.py" not in str(path)

        mock_fs.file_exists.side_effect = side_effect

        with pytest.raises(PreconditionError, match="Required base classes are missing"):
            generate_service._check_base_classes(temp_project_dir, mock_config)

    def test_missing_base_service(
        self, generate_service, mock_fs, temp_project_dir, mock_config
    ):
        """Missing base_service.py should raise PreconditionError."""

        def side_effect(path):
            return "base_service.py" not in str(path)

        mock_fs.file_exists.side_effect = side_effect

        with pytest.raises(PreconditionError, match="Required base classes are missing"):
            generate_service._check_base_classes(temp_project_dir, mock_config)

    def test_missing_multiple_base_classes(
        self, generate_service, mock_fs, temp_project_dir, mock_config
    ):
        """Missing multiple base classes should list all missing files."""

        def side_effect(path):
            # Only base_entity.py exists
            return "base_entity.py" in str(path)

        mock_fs.file_exists.side_effect = side_effect

        with pytest.raises(PreconditionError) as exc_info:
            generate_service._check_base_classes(temp_project_dir, mock_config)

        # Error message should mention multiple missing files
        error_message = str(exc_info.value)
        assert "base_repository.py" in error_message
        assert "base_schema.py" in error_message
        assert "base_service.py" in error_message


# ============================================================================
# TEST EXISTING FILES CHECK
# ============================================================================


class TestCheckExistingFiles:
    """Tests for _check_existing_files method."""

    def test_no_existing_files_force_false(
        self, generate_service, mock_fs, sample_entity_spec, temp_project_dir
    ):
        """No existing files with force=False should not raise."""
        mock_fs.file_exists.return_value = False

        output_dir = temp_project_dir / "src" / "catalog"

        # Should not raise
        generate_service._check_existing_files(output_dir, sample_entity_spec, force=False)

    def test_existing_domain_file_force_false(
        self, generate_service, mock_fs, sample_entity_spec, temp_project_dir
    ):
        """Existing domain file with force=False should raise FileExistsError."""

        def side_effect(path):
            # Only domain/product.py exists
            return "domain/product.py" in str(path)

        mock_fs.file_exists.side_effect = side_effect

        output_dir = temp_project_dir / "src" / "catalog"

        with pytest.raises(FileExistsError, match="already exist"):
            generate_service._check_existing_files(output_dir, sample_entity_spec, force=False)

    def test_existing_schemas_file_force_false(
        self, generate_service, mock_fs, sample_entity_spec, temp_project_dir
    ):
        """Existing schemas file with force=False should raise FileExistsError."""

        def side_effect(path):
            return "application/schemas.py" in str(path)

        mock_fs.file_exists.side_effect = side_effect

        output_dir = temp_project_dir / "src" / "catalog"

        with pytest.raises(FileExistsError, match="already exist"):
            generate_service._check_existing_files(output_dir, sample_entity_spec, force=False)

    def test_multiple_existing_files_force_false(
        self, generate_service, mock_fs, sample_entity_spec, temp_project_dir
    ):
        """Multiple existing files with force=False should list all conflicts."""

        def side_effect(path):
            # Multiple files exist
            return any(
                pattern in str(path)
                for pattern in ["domain/product.py", "application/schemas.py", "api/routes.py"]
            )

        mock_fs.file_exists.side_effect = side_effect

        output_dir = temp_project_dir / "src" / "catalog"

        with pytest.raises(FileExistsError) as exc_info:
            generate_service._check_existing_files(output_dir, sample_entity_spec, force=False)

        error_message = str(exc_info.value)
        assert "domain/product.py" in error_message
        assert "application/schemas.py" in error_message
        assert "api/routes.py" in error_message

    def test_existing_files_force_true(
        self, generate_service, mock_fs, sample_entity_spec, temp_project_dir
    ):
        """Existing files with force=True should not raise."""
        # All files exist
        mock_fs.file_exists.return_value = True

        output_dir = temp_project_dir / "src" / "catalog"

        # Should not raise
        generate_service._check_existing_files(output_dir, sample_entity_spec, force=True)

        # file_exists should not have been called when force=True
        mock_fs.file_exists.assert_not_called()

    def test_error_message_includes_force_hint(
        self, generate_service, mock_fs, sample_entity_spec, temp_project_dir
    ):
        """Error message should suggest using force=True."""
        mock_fs.file_exists.return_value = True

        output_dir = temp_project_dir / "src" / "catalog"

        with pytest.raises(FileExistsError) as exc_info:
            generate_service._check_existing_files(output_dir, sample_entity_spec, force=False)

        assert "force=True" in str(exc_info.value)


# ============================================================================
# TEST TEMPLATE RENDERING
# ============================================================================


class TestRenderTemplates:
    """Tests for _render_templates method."""

    def test_render_all_templates(
        self, generate_service, mock_template_repo, sample_entity_spec, mock_config
    ):
        """All 6 templates should be rendered."""
        mock_template_repo.render.return_value = "# rendered content"

        result = generate_service._render_templates(sample_entity_spec, mock_config)

        # Should have 6 rendered templates
        assert len(result) == 6
        assert "domain/product.py" in result
        assert "application/schemas.py" in result
        assert "application/service.py" in result
        assert "infrastructure/repository.py" in result
        assert "infrastructure/models.py" in result
        assert "api/routes.py" in result

    def test_template_rendering_context(
        self, generate_service, mock_template_repo, sample_entity_spec, mock_config
    ):
        """Templates should be rendered with entity and config context."""
        mock_template_repo.render.return_value = "# rendered"

        generate_service._render_templates(sample_entity_spec, mock_config)

        # Check that render was called with correct context
        call_args = mock_template_repo.render.call_args
        context = call_args[0][1]  # Second argument
        assert context["entity"] == sample_entity_spec
        assert context["config"] == mock_config

    def test_template_rendering_error(
        self, generate_service, mock_template_repo, sample_entity_spec, mock_config
    ):
        """Template rendering error should raise FileSystemError."""
        mock_template_repo.render.side_effect = Exception("Template syntax error")

        with pytest.raises(FileSystemError, match="Failed to render template"):
            generate_service._render_templates(sample_entity_spec, mock_config)

    def test_domain_template_uses_snake_name(
        self, generate_service, mock_template_repo, sample_entity_spec, mock_config
    ):
        """Domain template should use entity's snake_name in path."""
        mock_template_repo.render.return_value = "# rendered"

        result = generate_service._render_templates(sample_entity_spec, mock_config)

        # Domain file should use snake_name
        assert "domain/product.py" in result

    def test_template_names_mapped_correctly(
        self, generate_service, mock_template_repo, sample_entity_spec, mock_config
    ):
        """Template names should be mapped to correct Jinja2 template files."""
        mock_template_repo.render.return_value = "# rendered"

        generate_service._render_templates(sample_entity_spec, mock_config)

        # Extract all template names that were requested
        template_names = [call[0][0] for call in mock_template_repo.render.call_args_list]

        assert "entity/domain.py.j2" in template_names
        assert "entity/schemas.py.j2" in template_names
        assert "entity/service.py.j2" in template_names
        assert "entity/repository.py.j2" in template_names
        assert "entity/models.py.j2" in template_names
        assert "entity/routes.py.j2" in template_names


# ============================================================================
# TEST FILE WRITING
# ============================================================================


class TestWriteFiles:
    """Tests for _write_files method."""

    def test_write_all_templates(
        self, generate_service, mock_fs, temp_project_dir
    ):
        """All rendered templates should be written to filesystem."""
        output_dir = temp_project_dir / "src" / "catalog"
        rendered_templates = {
            "domain/product.py": "# domain content",
            "application/schemas.py": "# schemas content",
            "application/service.py": "# service content",
            "infrastructure/repository.py": "# repository content",
            "infrastructure/models.py": "# models content",
            "api/routes.py": "# routes content",
        }

        files_created = generate_service._write_files(
            output_dir, rendered_templates, temp_project_dir
        )

        # Should write 6 templates + 4 __init__.py files = 10 files
        assert mock_fs.write_file.call_count == 10
        assert len(files_created) == 10

    def test_create_init_files(
        self, generate_service, mock_fs, temp_project_dir
    ):
        """__init__.py files should be created in each subdirectory."""
        output_dir = temp_project_dir / "src" / "catalog"
        rendered_templates = {
            "domain/product.py": "# content",
            "application/schemas.py": "# content",
            "application/service.py": "# content",
            "infrastructure/repository.py": "# content",
            "infrastructure/models.py": "# content",
            "api/routes.py": "# content",
        }

        generate_service._write_files(output_dir, rendered_templates, temp_project_dir)

        # Check that __init__.py files were written
        init_calls = [
            call for call in mock_fs.write_file.call_args_list
            if "__init__.py" in str(call[0][0])
        ]
        assert len(init_calls) == 4  # domain, application, infrastructure, api

    def test_return_relative_paths(
        self, generate_service, mock_fs, temp_project_dir
    ):
        """Returned paths should be relative to project_root."""
        output_dir = temp_project_dir / "src" / "catalog"
        rendered_templates = {
            "domain/product.py": "# content",
        }

        files_created = generate_service._write_files(
            output_dir, rendered_templates, temp_project_dir
        )

        # Paths should be relative to project_root
        assert all(not path.startswith("/") for path in files_created)
        assert any("src/catalog/domain/product.py" in path for path in files_created)

    def test_filesystem_write_error(
        self, generate_service, mock_fs, temp_project_dir
    ):
        """Filesystem I/O error should raise FileSystemError."""
        output_dir = temp_project_dir / "src" / "catalog"
        rendered_templates = {"domain/product.py": "# content"}

        mock_fs.write_file.side_effect = IOError("Permission denied")

        with pytest.raises(FileSystemError, match="Failed to write files"):
            generate_service._write_files(output_dir, rendered_templates, temp_project_dir)


# ============================================================================
# TEST GENERATE ENTITY (INTEGRATION)
# ============================================================================


class TestGenerateEntity:
    """Integration tests for generate_entity method."""

    def test_successful_generation(
        self,
        generate_service,
        mock_fs,
        mock_template_repo,
        sample_entity_spec,
        mock_config,
        temp_project_dir,
    ):
        """Complete successful entity generation flow."""
        # Setup mocks - base classes exist, entity files don't exist
        def file_exists_side_effect(path):
            # Base classes exist
            base_classes = [
                "base_entity.py",
                "base_repository.py",
                "base_schema.py",
                "base_service.py",
            ]
            if any(base in str(path) for base in base_classes):
                return True
            # Entity files don't exist yet
            return False

        mock_fs.file_exists.side_effect = file_exists_side_effect
        mock_template_repo.render.return_value = "# rendered content"

        result = generate_service.generate_entity(
            entity=sample_entity_spec,
            project_root=temp_project_dir,
            config=mock_config,
            force=False,
        )

        # Verify result
        assert isinstance(result, GenerateResult)
        assert result.entity_name == "Product"
        assert result.capability == "catalog"
        assert len(result.files_created) == 10  # 6 templates + 4 __init__.py
        assert "src/catalog" in result.directory

    def test_generation_with_force(
        self,
        generate_service,
        mock_fs,
        mock_template_repo,
        sample_entity_spec,
        mock_config,
        temp_project_dir,
    ):
        """Generation with force=True should overwrite existing files."""
        # Setup mocks - base classes exist, but entity files also exist
        def file_exists_side_effect(path):
            # Base classes exist
            base_classes = [
                "base_entity.py",
                "base_repository.py",
                "base_schema.py",
                "base_service.py",
            ]
            if any(base in str(path) for base in base_classes):
                return True
            # Entity files also exist
            return "catalog" in str(path)

        mock_fs.file_exists.side_effect = file_exists_side_effect
        mock_template_repo.render.return_value = "# rendered content"

        result = generate_service.generate_entity(
            entity=sample_entity_spec,
            project_root=temp_project_dir,
            config=mock_config,
            force=True,
        )

        # Should succeed despite existing files
        assert result.entity_name == "Product"
        assert len(result.files_created) == 10

    def test_generation_fails_validation(
        self,
        generate_service,
        mock_config,
        temp_project_dir,
    ):
        """Generation with invalid EntitySpec should fail validation phase."""
        # Pydantic will catch invalid specs at construction time
        from pydantic import ValidationError as PydanticValidationError

        with pytest.raises(PydanticValidationError):
            EntitySpec(
                name="",  # Invalid empty name
                capability="catalog",
                fields=[],
            )

    def test_generation_fails_precondition(
        self,
        generate_service,
        mock_fs,
        sample_entity_spec,
        mock_config,
        temp_project_dir,
    ):
        """Generation should fail if base classes don't exist."""
        # No base classes exist
        mock_fs.file_exists.return_value = False

        with pytest.raises(PreconditionError):
            generate_service.generate_entity(
                entity=sample_entity_spec,
                project_root=temp_project_dir,
                config=mock_config,
                force=False,
            )

    def test_generation_fails_file_exists(
        self,
        generate_service,
        mock_fs,
        sample_entity_spec,
        mock_config,
        temp_project_dir,
    ):
        """Generation should fail if entity files exist and force=False."""

        def file_exists_side_effect(path):
            # Base classes exist
            base_classes = [
                "base_entity.py",
                "base_repository.py",
                "base_schema.py",
                "base_service.py",
            ]
            if any(base in str(path) for base in base_classes):
                return True
            # Entity files also exist
            return "catalog/domain/product.py" in str(path)

        mock_fs.file_exists.side_effect = file_exists_side_effect

        with pytest.raises(FileExistsError):
            generate_service.generate_entity(
                entity=sample_entity_spec,
                project_root=temp_project_dir,
                config=mock_config,
                force=False,
            )

    def test_generation_creates_directories(
        self,
        generate_service,
        mock_fs,
        mock_template_repo,
        sample_entity_spec,
        mock_config,
        temp_project_dir,
    ):
        """Generation should create app_root, capability, and subdirectories."""
        # Base classes exist, entity files don't
        def file_exists_side_effect(path):
            base_classes = [
                "base_entity.py",
                "base_repository.py",
                "base_schema.py",
                "base_service.py",
            ]
            if any(base in str(path) for base in base_classes):
                return True
            return False

        mock_fs.file_exists.side_effect = file_exists_side_effect
        mock_template_repo.render.return_value = "# content"

        generate_service.generate_entity(
            entity=sample_entity_spec,
            project_root=temp_project_dir,
            config=mock_config,
            force=False,
        )

        # Verify directory creation
        ensure_dir_calls = mock_fs.ensure_directory.call_args_list
        assert len(ensure_dir_calls) >= 6  # app_root + capability + 4 subdirs

        # Check specific directories
        created_dirs = [str(call[0][0]) for call in ensure_dir_calls]
        assert any("src" in d for d in created_dirs)  # app_root
        assert any("catalog" in d for d in created_dirs)  # capability
        assert any("domain" in d for d in created_dirs)
        assert any("application" in d for d in created_dirs)
        assert any("infrastructure" in d for d in created_dirs)
        assert any("api" in d for d in created_dirs)

    def test_generation_with_authorized_entity(
        self,
        generate_service,
        mock_fs,
        mock_template_repo,
        authorized_entity_spec,
        mock_config,
        temp_project_dir,
    ):
        """Generation with authorized=True should include tenant_id in context."""
        # Base classes exist, entity files don't
        def file_exists_side_effect(path):
            base_classes = [
                "base_entity.py",
                "base_repository.py",
                "base_schema.py",
                "base_service.py",
            ]
            if any(base in str(path) for base in base_classes):
                return True
            return False

        mock_fs.file_exists.side_effect = file_exists_side_effect
        mock_template_repo.render.return_value = "# content"

        result = generate_service.generate_entity(
            entity=authorized_entity_spec,
            project_root=temp_project_dir,
            config=mock_config,
            force=False,
        )

        # Verify generation succeeded
        assert result.entity_name == "Order"
        assert result.capability == "orders"

        # Verify template was called with authorized entity
        render_calls = mock_template_repo.render.call_args_list
        contexts = [call[0][1] for call in render_calls]
        assert all(ctx["entity"].authorized is True for ctx in contexts)

    def test_generation_phases_order(
        self,
        generate_service,
        mock_fs,
        mock_template_repo,
        sample_entity_spec,
        mock_config,
        temp_project_dir,
    ):
        """Validation should happen before any filesystem writes."""
        mock_template_repo.render.return_value = "# content"

        # Track order of operations
        operation_order = []

        def track_file_exists(path):
            operation_order.append("file_exists")
            # Base classes exist, entity files don't
            base_classes = [
                "base_entity.py",
                "base_repository.py",
                "base_schema.py",
                "base_service.py",
            ]
            if any(base in str(path) for base in base_classes):
                return True
            return False

        def track_ensure_directory(path):
            operation_order.append("ensure_directory")

        def track_write_file(path, content):
            operation_order.append("write_file")

        mock_fs.file_exists.side_effect = track_file_exists
        mock_fs.ensure_directory.side_effect = track_ensure_directory
        mock_fs.write_file.side_effect = track_write_file

        generate_service.generate_entity(
            entity=sample_entity_spec,
            project_root=temp_project_dir,
            config=mock_config,
            force=False,
        )

        # Validation (file_exists checks) should happen before writes
        first_write_index = operation_order.index("write_file")
        file_exists_checks = [
            i for i, op in enumerate(operation_order) if op == "file_exists"
        ]
        assert all(i < first_write_index for i in file_exists_checks)
