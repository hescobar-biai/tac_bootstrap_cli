"""Tests for generate CLI command."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import yaml
from typer.testing import CliRunner

from tac_bootstrap.domain.entity_config import FieldSpec, FieldType
from tac_bootstrap.interfaces.cli import app

runner = CliRunner()


def create_test_project(tmpdir: Path) -> Path:
    """
    Create a test project with config.yml.

    Responsibility: Create isolated test project structure with standardized
    config.yml for CLI generate command test fixtures

    Tags: expert:backend, level:L1, topic:api

    Ownership: Test fixture creation, temporary directory setup, test project
    configuration, YAML config generation

    Invariants: Must create valid config.yml at tmpdir root; config must
    include all required sections (version, schema_version, project, paths,
    commands, claude); returned path must point to directory containing
    config.yml; config values must match test-project defaults

    Side effects: Writes config.yml to temporary directory; creates test
    project structure; initializes YAML configuration file

    Inputs: Temporary directory path (tmpdir)

    Outputs: Path to test project directory containing config.yml

    Failure modes: YAML serialization failure; file write permission denied;
    invalid tmpdir path; config.yml creation failure

    IDK: test-fixture, yaml-config, tmpdir, test-project-setup,
    config-generation, isolated-filesystem, cli-testing, pytest-fixture,
    test-data
    """
    config_dict = {
        "version": "0.9.0",
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

    config_path = tmpdir / "config.yml"
    with open(config_path, "w") as f:
        yaml.dump(config_dict, f)

    return tmpdir


class TestGenerateCommand:
    """
    Test generate command.

    Responsibility: Verify CLI generate command behavior across valid/invalid
    subcommands, non-interactive modes, field parsing, dry-run, and
    configuration validation scenarios

    Tags: expert:backend, level:L2, topic:api

    Ownership: CLI generate command test suite, subcommand validation testing,
    non-interactive mode verification, field parsing validation, dry-run mode
    testing, configuration validation, entity generation workflow testing

    Invariants: All test methods must execute in isolated temporary directories;
    working directory must be restored after each test; test suite must not
    persist filesystem changes; each test verifies specific CLI behavior with
    expected exit codes and output messages

    Side effects: Creates temporary test directories; invokes CLI generate
    commands; creates test project structures; modifies working directory during
    tests; restores original working directory; cleans up temporary resources

    Inputs: CLI generate command invocations with various arguments and flags;
    temporary test directories; test project structures; entity names; field
    definitions; capability identifiers

    Outputs: CLI exit codes; stdout messages; generated entity files; validation
    error messages; dry-run preview output

    Failure modes: Temporary directory cleanup failure; working directory not
    restored; test isolation breach; CLI behavior regression; validation logic
    bypass; incorrect exit codes; missing error messages

    IDK: cli-testing, generate-command, typer-cli, test-suite,
    entity-generation, field-parsing, dry-run, config-validation,
    non-interactive-mode, tempfile, isolated-filesystem, exit-codes
    """

    def test_invalid_subcommand(self):
        """
        Test error on invalid subcommand.

        Responsibility: Verify CLI rejects invalid generate subcommands with appropriate error code
        and message

        Tags: expert:backend, level:L1, topic:api

        Ownership: CLI subcommand validation, generate command routing, error message generation
        for unknown subcommands

        Invariants: CLI must exit with code 1 on invalid subcommand; error message must contain
        "Unknown subcommand 'invalid'"; no file generation or side effects on validation failure

        Side effects: Invokes CLI generate command with invalid subcommand; no filesystem
        modifications; no persistent changes

        Inputs: CLI command "generate" with invalid subcommand "invalid"; entity argument "Product"

        Outputs: CLI exit code 1; error message containing unknown subcommand text

        Failure modes: Wrong exit code returned; missing error message; CLI accepts invalid
        subcommand; unexpected file generation; validation bypassed

        IDK: cli-validation, subcommand-routing, typer-cli, exit-codes, error-messages,
        generate-command, invalid-input
        """
        result = runner.invoke(app, ["generate", "invalid", "Product"])

        assert result.exit_code == 1
        assert "Unknown subcommand 'invalid'" in result.stdout

    def test_non_interactive_with_fields(self):
        """
        Test non-interactive mode with --fields.

        Responsibility: Verify CLI executes entity generation in non-interactive mode with parsed
        field definitions, ensuring all specified fields are created in generated entity without
        user prompts

        Tags: expert:backend, level:L2, topic:api

        Ownership: CLI non-interactive mode execution, field parsing from command-line arguments,
        entity generation with predefined fields, output validation

        Invariants: CLI must exit with code 0 on successful entity generation; output must contain
        "Entity generated successfully"; entity file must exist at expected domain path; all fields
        from --fields argument parsed and applied; no interactive prompts during execution

        Side effects: Creates temporary project structure; writes entity files to domain directory;
        modifies working directory during test; invokes CLI generate command; restores original
        working directory; generates capability-based directory structure with entity files

        Inputs: Temporary directory path; test project structure; entity name "Product"; capability
        identifier "catalog"; field definitions
        "name:str:required,price:float:required,description:text"; --no-interactive flag; --fields
        argument

        Outputs: CLI exit code 0; stdout containing success confirmation; entity file created at
        domain/catalog/entities/product.py; entity with parsed fields from CLI arguments

        Failure modes: Temporary directory cleanup failure; working directory not restored; field
        parsing failure; exit code mismatch; entity files not created; missing success message;
        field definitions not applied; interactive prompt triggered despite flag

        IDK: non-interactive-mode, field-parsing, cli-arguments, entity-generation, typer-cli,
        tempfile, working-directory, domain-structure, catalog-capability, comma-separated-fields,
        field-definitions
        """
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = create_test_project(Path(tmpdir))
            original_cwd = os.getcwd()

            try:
                # Change to project directory
                os.chdir(project_dir)

                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "-c",
                        "catalog",
                        "--no-interactive",
                        "--fields",
                        "name:str:required,price:float:required,description:text",
                    ],
                )

                assert result.exit_code == 0
                assert "Entity generated successfully" in result.stdout

                # Verify files were created
                entity_path = project_dir / "domain" / "catalog" / "entities" / "product.py"
                assert entity_path.exists()
            finally:
                os.chdir(original_cwd)

    def test_auto_capability_generation(self):
        """
        Test automatic capability generation from entity name.

        Responsibility: Verify CLI auto-generates capability identifier from PascalCase entity
        name, ensuring capability naming follows kebab-case convention derived from entity name

        Tags: expert:backend, level:L2, topic:api

        Ownership: CLI capability auto-generation, entity-to-capability name transformation,
        capability identifier creation from entity names

        Invariants: CLI must exit with code 0 on successful entity generation; output must contain
        "Auto-generated capability: product-category"; capability name must be kebab-case
        transformation of entity name; single field entity generation succeeds with
        auto-capability; entity files created at expected domain paths

        Side effects: Creates temporary project structure; writes entity files to domain directory;
        modifies working directory during test; invokes CLI generate command; restores original
        working directory; generates capability-based directory structure

        Inputs: Temporary directory path; test project structure; entity name "ProductCategory";
        field definition "name:str"; --no-interactive flag

        Outputs: CLI exit code 0; stdout containing auto-generated capability confirmation; entity
        files created at capability-based paths; kebab-case capability identifier derived from
        PascalCase input

        Failure modes: Temporary directory cleanup failure; working directory not restored;
        capability name transformation incorrect; missing auto-generation output message; exit code
        mismatch; entity files not created; case conversion failure

        IDK: auto-capability-generation, entity-name-transformation, kebab-case,
        pascal-case-conversion, cli-testing, capability-identifier, entity-generation, typer-cli,
        tempfile, working-directory, domain-structure
        """
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = create_test_project(Path(tmpdir))
            original_cwd = os.getcwd()

            try:
                os.chdir(project_dir)

                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "ProductCategory",
                        "--no-interactive",
                        "--fields",
                        "name:str",
                    ],
                )

                assert result.exit_code == 0
                assert "Auto-generated capability: product-category" in result.stdout
            finally:
                os.chdir(original_cwd)

    def test_dry_run_mode(self):
        """
        Test --dry-run doesn't create files.

        Responsibility: Verify CLI rejects entity generation in dry-run mode, ensuring no files are
        created on filesystem when --dry-run flag is provided

        Tags: expert:backend, level:L2, topic:api

        Ownership: CLI dry-run mode validation, file system isolation in preview mode, entity
        generation output control

        Invariants: CLI must exit with code 0 in dry-run mode; output must contain "Dry Run -
        Preview" and "Would create:"; no entity files created on filesystem when --dry-run flag
        present; preview output shows intended file paths without executing write operations

        Side effects: Creates temporary project structure; modifies working directory during test;
        invokes CLI generate command with --dry-run flag; restores original working directory;
        verifies filesystem remains unchanged; no persistent changes to filesystem

        Inputs: Temporary directory path; test project structure; entity name "Product"; catalog
        context "catalog"; field definition "name:str"; --no-interactive flag; --dry-run flag

        Outputs: CLI exit code 0; preview output containing dry-run indicators; no entity files
        created at expected paths; filesystem verification confirming file non-existence

        Failure modes: Temporary directory cleanup failure; working directory not restored; files
        created despite dry-run flag; missing dry-run output indicators; exit code mismatch; file
        existence check failure; preview output incomplete

        IDK: dry-run, preview-mode, filesystem-isolation, entity-generation, cli-testing, no-write,
        tempfile, working-directory, typer-cli, file-creation-prevention, output-validation
        """
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = create_test_project(Path(tmpdir))
            original_cwd = os.getcwd()

            try:
                os.chdir(project_dir)

                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "-c",
                        "catalog",
                        "--no-interactive",
                        "--fields",
                        "name:str",
                        "--dry-run",
                    ],
                )

                assert result.exit_code == 0
                assert "Dry Run - Preview" in result.stdout
                assert "Would create:" in result.stdout

                # Verify no files were created
                entity_path = project_dir / "domain" / "catalog" / "entities" / "product.py"
                assert not entity_path.exists()
            finally:
                os.chdir(original_cwd)

    def test_missing_config_yml(self):
        """
        Test error when config.yml is missing.

        Responsibility: Verify CLI rejects entity generation in non-interactive mode when
        config.yml is missing from project directory

        Tags: expert:backend, level:L2, topic:api

        Ownership: CLI configuration validation, config.yml presence check, entity generation
        prerequisites

        Invariants: CLI must exit with code 1 when config.yml is missing; error message must
        contain "No config.yml found"; no entity files generated when config validation fails;
        validation occurs before any generation logic

        Side effects: Creates temporary directory; invokes CLI generate command; attempts file
        system operations in temporary isolated environment; no persistent changes to filesystem

        Inputs: Temporary directory path without config.yml; entity name "Product"; field
        definition "name:str"; --no-interactive flag

        Outputs: CLI exit code 1; error message containing config.yml validation text; no entity
        files created

        Failure modes: Temporary directory cleanup failure; CLI accepts missing config; wrong exit
        code; missing validation error message; unintended file generation; config check bypassed

        IDK: config-yml, cli-validation, missing-config, exit-codes, entity-generation, typer-cli,
        tempfile, isolated-filesystem, prerequisites, configuration-validation
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            with runner.isolated_filesystem(temp_dir=tmpdir):
                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "--no-interactive",
                        "--fields",
                        "name:str",
                    ],
                )

                assert result.exit_code == 1
                assert "No config.yml found" in result.stdout

    def test_wrong_architecture(self):
        """
        Test error with non-DDD architecture.

        Responsibility: Verify CLI rejects entity generation with non-DDD architecture, ensuring
        DDD-only commands fail gracefully on incompatible architectures

        Tags: expert:backend, level:L2, topic:api

        Ownership: CLI architecture validation, entity generation command restrictions,
        configuration-based architecture enforcement

        Invariants: CLI must exit with code 1 when architecture is not DDD (e.g., "simple"); error
        message must contain "Entity generation requires architecture"; no entity files generated
        when architecture validation fails; validation occurs before any file generation

        Side effects: Creates temporary project structure with SIMPLE architecture; writes
        config.yml to temporary directory; modifies working directory during test; invokes CLI
        generate command; restores original working directory; no persistent changes to filesystem
        on validation failure

        Inputs: Temporary directory path; config.yml with architecture "simple"; entity name
        "Product"; field definition "name:str"; --no-interactive flag

        Outputs: CLI exit code 1; error message containing architecture requirement validation
        text; no entity files created

        Failure modes: Temporary directory cleanup failure; working directory not restored; CLI
        accepts invalid architecture; wrong exit code; missing validation error message; unintended
        file generation; config validation bypassed

        IDK: architecture-validation, ddd-architecture, cli-validation, config-yml, exit-codes,
        entity-generation, non-ddd-architecture, typer-cli, tempfile, working-directory,
        architecture-simple
        """
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create config with SIMPLE architecture
            config_dict = {
                "version": "0.9.0",
                "schema_version": 1,
                "project": {
                    "name": "test-project",
                    "language": "python",
                    "package_manager": "uv",
                    "architecture": "simple",
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
            original_cwd = os.getcwd()

            try:
                os.chdir(project_dir)

                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "--no-interactive",
                        "--fields",
                        "name:str",
                    ],
                )

                assert result.exit_code == 1
                assert "Entity generation requires architecture" in result.stdout

            finally:
                os.chdir(original_cwd)
    def test_non_interactive_without_fields(self):
        """
        Test error in non-interactive mode without --fields.

        Responsibility: Verify CLI rejects entity generation in non-interactive mode when --fields
        flag is missing

        Tags: expert:backend, level:L2, topic:api

        Ownership: CLI validation for non-interactive mode, required fields parameter enforcement

        Invariants: CLI must exit with code 1 when --no-interactive flag present without --fields;
        error message must contain "--fields is required in non-interactive mode"; no entity files
        generated on validation failure

        Side effects: Creates temporary project structure; modifies working directory during test;
        invokes CLI generate command; restores original working directory; no persistent changes to
        filesystem on validation failure

        Inputs: Temporary directory path; test project structure; entity name "Product";
        --no-interactive flag without --fields parameter

        Outputs: CLI exit code 1; error message containing required fields validation text; no
        entity files created

        Failure modes: Temporary directory cleanup failure; working directory not restored; CLI
        accepts invalid input; wrong exit code; missing validation error message; unintended file
        generation

        IDK: cli-validation, non-interactive-mode, required-parameters, error-handling, exit-codes,
        typer-cli, tempfile, field-validation, entity-generation, no-interactive-flag
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            create_test_project(Path(tmpdir))

            with runner.isolated_filesystem(temp_dir=tmpdir):
                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "--no-interactive",
                    ],
                )

                assert result.exit_code == 1
                assert "--fields is required in non-interactive mode" in result.stdout

    def test_invalid_field_type(self):
        """
        Test error with invalid field type.

        Responsibility: Verify CLI interactive mode invokes entity field wizard when
        --no-interactive flag is absent

        Tags: expert:backend, level:L2, topic:api

        Ownership: CLI interactive mode, entity field wizard invocation

        Invariants: Entity field wizard must be called when --no-interactive flag not present;
        wizard must receive correct entity and context parameters; CLI must process wizard output
        for entity generation

        Side effects: Creates temporary project structure; modifies working directory during test;
        invokes CLI generate command without --no-interactive flag; mocks wizard execution;
        restores original working directory

        Inputs: Temporary directory path; test project structure; entity name "Product"; catalog
        context "catalog"; mocked wizard function

        Outputs: CLI exit code 0 on success; wizard function called with expected parameters;
        entity generation proceeds with wizard-provided field definitions

        Failure modes: Temporary directory cleanup failure; working directory not restored; CLI
        invocation fails; wizard not invoked; wizard mock not applied; incorrect parameters passed
        to wizard

        IDK: cli-testing, interactive-mode, entity-wizard, field-wizard, mock-patch, typer-cli,
        wizard-invocation, tempfile, working-directory, no-interactive-flag, entity-generation
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            create_test_project(Path(tmpdir))

            with runner.isolated_filesystem(temp_dir=tmpdir):
                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "--no-interactive",
                        "--fields",
                        "name:invalid_type",
                    ],
                )

                assert result.exit_code == 1
                assert "Unknown field type" in result.stdout

    def test_async_mode(self):
        """
        Test --async flag generates async repository.

        Responsibility: Verify CLI --async flag correctly generates async repository implementation
        for entity

        Tags: expert:backend, level:L2, topic:db

        Ownership: CLI generation with async flag, async repository template generation

        Invariants: BaseRepositoryAsync must be used when --async flag present; repository file
        must be created at infrastructure/{context}/repositories/{entity}_repository.py; async
        repository must inherit from BaseRepositoryAsync class

        Side effects: Creates temporary project structure; modifies working directory during test;
        invokes CLI generate command with --async flag; generates repository file with async base
        class; restores original working directory

        Inputs: Temporary directory path; test project structure; entity name "Product"; catalog
        context "catalog"; field definition "name:str"; --async flag; --no-interactive flag

        Outputs: CLI exit code 0 on success; generated repository file containing
        BaseRepositoryAsync import and inheritance

        Failure modes: Temporary directory cleanup failure; working directory not restored; CLI
        invocation fails; repository file not generated; BaseRepositoryAsync not present in
        generated code; file path incorrect

        IDK: cli-testing, async-repository, async-await, repository-pattern, ddd-repository,
        entity-generation, base-repository-async, tempfile, working-directory, typer-cli,
        database-async
        """
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = create_test_project(Path(tmpdir))
            original_cwd = os.getcwd()

            try:
                os.chdir(project_dir)

                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "-c",
                        "catalog",
                        "--no-interactive",
                        "--fields",
                        "name:str",
                        "--async",
                    ],
                )

                assert result.exit_code == 0

                # Verify async repository was created
                repo_path = (
                    project_dir
                    / "infrastructure"
                    / "catalog"
                    / "repositories"
                    / "product_repository.py"
                )
                assert repo_path.exists()

                content = repo_path.read_text()
                assert "BaseRepositoryAsync" in content

            finally:
                os.chdir(original_cwd)
    def test_with_events_flag(self):
        """
        Test --with-events flag generates events file.

        Responsibility: Verify CLI --with-events flag correctly generates domain events file for
        entity

        Tags: expert:backend, level:L2, topic:api

        Ownership: CLI generation with events flag, domain event file generation

        Invariants: Events file must be created at domain/{context}/events/{entity}_events.py when
        --with-events flag present; generated events must include Created, Updated, and Deleted
        event classes

        Side effects: Creates temporary project structure; modifies working directory; invokes CLI
        generate command with --with-events flag; generates events file with domain event classes;
        restores original working directory

        Inputs: Temporary directory path; test project structure; entity name "Product"; catalog
        context "catalog"; field definition "name:str"; --with-events flag; --no-interactive flag

        Outputs: CLI exit code 0 on success; generated events file containing ProductCreated,
        ProductUpdated, and ProductDeleted event classes

        Failure modes: Temporary directory cleanup failure; working directory not restored; CLI
        invocation fails; events file not generated; event classes missing from generated file;
        file path incorrect

        IDK: cli-testing, domain-events, event-sourcing, ddd-events, entity-generation,
        event-file-generation, tempfile, working-directory, typer-cli, event-classes,
        product-created, product-updated, product-deleted
        """
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = create_test_project(Path(tmpdir))
            original_cwd = os.getcwd()

            try:
                os.chdir(project_dir)

                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "-c",
                        "catalog",
                        "--no-interactive",
                        "--fields",
                        "name:str",
                        "--with-events",
                    ],
                )

                assert result.exit_code == 0

                # Verify events file was created
                events_path = (
                    project_dir
                    / "domain"
                    / "catalog"
                    / "events"
                    / "product_events.py"
                )
                assert events_path.exists()

                content = events_path.read_text()
                assert "ProductCreated" in content
                assert "ProductUpdated" in content
                assert "ProductDeleted" in content

            finally:
                os.chdir(original_cwd)
    def test_authorized_flag(self):
        """
        Test --authorized flag adds auth decorators.

        Responsibility: Verify CLI --authorized flag correctly adds authentication decorators to
        generated entity routes

        Tags: expert:backend, level:L2, topic:auth, topic:api

        Ownership: CLI generation with authentication, entity route generation with JWT decorators

        Invariants: Auth decorators must be added when --authorized flag present; generated routes
        must include get_current_user dependency; CurrentUser type must be imported;
        organization_id must be present in route signatures

        Side effects: Creates temporary project structure; modifies working directory; invokes CLI
        generate command with --authorized flag; generates routes file with auth decorators;
        restores original working directory

        Inputs: Temporary directory path; test project structure; entity name "Product"; catalog
        context "catalog"; field definition "name:str"; --authorized flag; --no-interactive flag

        Outputs: CLI exit code 0 on success; generated routes file containing get_current_user
        dependency; CurrentUser type references; organization_id parameter in route functions

        Failure modes: Temporary directory cleanup failure; working directory not restored; CLI
        invocation fails; routes file missing auth decorators; get_current_user not imported;
        CurrentUser type missing; organization_id not added to routes

        IDK: cli-testing, auth-decorators, jwt-authentication, get-current-user, route-generation,
        entity-generation, ddd-routes, tempfile, working-directory, typer-cli, authorization,
        organization-id
        """
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = create_test_project(Path(tmpdir))
            original_cwd = os.getcwd()

            try:
                os.chdir(project_dir)

                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "-c",
                        "catalog",
                        "--no-interactive",
                        "--fields",
                        "name:str",
                        "--authorized",
                    ],
                )

                assert result.exit_code == 0

                # Verify routes have auth decorator
                routes_path = (
                    project_dir
                    / "interfaces"
                    / "api"
                    / "catalog"
                    / "product_routes.py"
                )
                assert routes_path.exists()

                content = routes_path.read_text()
                # Check for get_current_user dependency (JWT auth)
                assert "get_current_user" in content
                assert "CurrentUser" in content
                assert "organization_id" in content

            finally:
                os.chdir(original_cwd)

    @patch("tac_bootstrap.interfaces.entity_wizard.run_entity_field_wizard")
    def test_interactive_mode(self, mock_wizard):
        """
        Test interactive mode calls wizard.

        Responsibility: Verify CLI interactive mode invokes wizard to collect entity field
        specifications

        Tags: expert:backend, level:L2, topic:api

        Ownership: CLI generation interactive workflow, wizard integration for field collection

        Invariants: Wizard must be called when interactive mode enabled (default); mock must return
        valid FieldSpec list; generated entity must include wizard-provided fields

        Side effects: Creates temporary project structure; mocks wizard function; changes working
        directory during test; invokes CLI generate command; restores original working directory

        Inputs: Mocked wizard returning two FieldSpecs (name:STRING, price:FLOAT); temporary
        project directory; entity name "Product"; catalog context "catalog"; interactive mode
        enabled by default

        Outputs: CLI exit code 0 on success; wizard called assertion success; generated entity file
        with fields from wizard

        Failure modes: Wizard mock not called; temporary directory cleanup failure; working
        directory not restored; CLI invocation fails; exit code non-zero; wizard returns invalid
        FieldSpec data

        IDK: cli-testing, wizard-interaction, interactive-mode, field-collection, mock-testing,
        typer-cli, entity-generation, ddd-entity, test-isolation, tempfile, working-directory,
        fieldspec
        """
        import os

        # Mock wizard to return fields
        mock_wizard.return_value = [
            FieldSpec(name="name", field_type=FieldType.STRING, required=True),
            FieldSpec(name="price", field_type=FieldType.FLOAT, required=True),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = create_test_project(Path(tmpdir))
            original_cwd = os.getcwd()

            try:
                os.chdir(project_dir)

                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "-c",
                        "catalog",
                        # interactive is True by default
                    ],
                )

                assert result.exit_code == 0
                assert mock_wizard.called
            finally:
                os.chdir(original_cwd)

    def test_force_mode(self):
        """
        Test --force overwrites existing files.

        Responsibility: Verify CLI --force flag correctly overwrites existing generated entity files

        Tags: expert:backend, level:L2, topic:api

        Ownership: CLI generation infrastructure, file overwrite handling

        Invariants: Entity file must exist before --force test; original content must be replaced;
        without --force must fail with "already exists"

        Side effects: Creates temporary project structure; writes test entity file; modifies
        working directory; invokes CLI commands twice; overwrites entity file on second invocation

        Inputs: Temporary directory path; test project structure; entity name "Product"; catalog
        context "catalog"; field definition "name:str"; --force flag

        Outputs: CLI exit codes (1 for collision, 0 for success); stdout messages indicating
        collision or success; overwritten entity file with new class definition

        Failure modes: Temporary directory cleanup failure; working directory not restored; entity
        file creation fails; CLI invocation returns unexpected exit code; file content not properly
        overwritten; assertion failures on missing text

        IDK: cli-testing, file-overwrite, force-flag, tempfile, typer-cli, entity-generation,
        ddd-entity, test-isolation, filesystem-operations, exit-codes, collision-detection,
        working-directory
        """
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = create_test_project(Path(tmpdir))

            # Create existing entity
            entity_path = project_dir / "domain" / "catalog" / "entities" / "product.py"
            entity_path.parent.mkdir(parents=True, exist_ok=True)
            entity_path.write_text("# OLD CONTENT")
            original_cwd = os.getcwd()

            try:
                os.chdir(project_dir)

                # First attempt without --force should fail
                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "-c",
                        "catalog",
                        "--no-interactive",
                        "--fields",
                        "name:str",
                    ],
                )

                assert result.exit_code == 1
                assert "already exists" in result.stdout

                # Second attempt with --force should succeed
                result = runner.invoke(
                    app,
                    [
                        "generate",
                        "entity",
                        "Product",
                        "-c",
                        "catalog",
                        "--no-interactive",
                        "--fields",
                        "name:str",
                        "--force",
                    ],
                )

                assert result.exit_code == 0

                # Verify file was overwritten
                content = entity_path.read_text()
                assert "# OLD CONTENT" not in content
                assert "class Product" in content
            finally:
                os.chdir(original_cwd)
