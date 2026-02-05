"""Tests for wizard module.

Comprehensive tests for interactive wizard functions using mocked
Rich components to avoid manual interaction during testing.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tac_bootstrap.domain.models import (
    Architecture,
    Framework,
    Language,
    PackageManager,
    ProjectMode,
)
from tac_bootstrap.interfaces.wizard import (
    run_add_agentic_wizard,
    run_init_wizard,
    select_from_enum,
)

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_console():
    """
    Mock Rich console to prevent output during tests.
    
    Responsibility: Stub Rich console print/error methods to capture console output for test verification without rendering visual terminal elements during pytest execution
    
    Tags: level:L3, topic:api
    
    Ownership: Test utilities fixture providing Rich console mock for wizard and CLI interface tests requiring output interception and verification
    
    Invariants: Patch target must match "tac_bootstrap.interfaces.wizard.console" import path; context manager must yield mock object enabling assertion methods; patch scope limited to fixture lifecycle; no actual terminal rendering occurs; mock captures print/error invocations for test verification
    
    Side effects: Patches Rich console import in wizard module; instantiates MagicMock for console methods; yields mock to test function; restores original console on context exit; enables assert_called/assert_called_once test validations
    
    Inputs: Patch decorator targeting "tac_bootstrap.interfaces.wizard.console" module path; context manager yielding mock object to test functions
    
    Outputs: MagicMock instance with callable print/error methods; captured invocation records for assertion verification; pytest fixture available via dependency injection
    
    Failure modes: Import path mismatch preventing patch application; console references cached before patch activation; nested patching conflicts; mock not properly restored on exception; assertion methods unavailable from incorrect mock type
    
    IDK: Rich-console, pytest-fixture, mock-output, console-patching, test-isolation, wizard-testing, MagicMock, context-manager-patch, output-verification, terminal-rendering-suppression
    """
    with patch("tac_bootstrap.interfaces.wizard.console") as mock:
        yield mock


@pytest.fixture
def mock_prompt():
    """
    Mock Prompt.ask to simulate user input.
    
    Responsibility: Validate wizard error handling when filter function eliminates all enumeration options by asserting ValueError raised with "No valid options available" message
    
    Tags: level:L3, topic:api
    
    Ownership: Application layer select_from_enum filtering validation test coverage for complete option elimination edge case
    
    Invariants: Filter function lambda returning False must eliminate all Framework enum options; ValueError must be raised with exact match on "No valid options available" message; no mock_prompt invocation when zero valid options exist; no default fallback behavior when filter eliminates all choices
    
    Side effects: Invokes select_from_enum with Framework enum and reject-all filter lambda; pytest.raises context manager captures ValueError; no user interaction or configuration creation due to early validation failure
    
    Inputs: Prompt string "What framework?"; Framework enum type; default=Framework.NONE; filter_fn lambda always returning False to simulate zero-valid-options scenario
    
    Outputs: ValueError exception with message "No valid options available"; pytest assertion validating exception raised when all enum values filtered out
    
    Failure modes: Filter validation bypassed allowing empty option set to proceed; ValueError not raised for zero valid options; incorrect exception type raised; fallback behavior executes instead of validation failure; default value returned despite being filtered out
    
    IDK: zero-valid-options, filter-eliminates-all, ValueError-no-options, empty-enumeration, reject-all-filter, wizard-error-handling, edge-case-validation, pytest-raises, filter-validation, select-from-enum
    """
    with patch("tac_bootstrap.interfaces.wizard.Prompt.ask") as mock:
        yield mock


@pytest.fixture
def mock_confirm():
    """
    Mock Confirm.ask to simulate yes/no confirmations.
    
    Responsibility: Verify select_from_enum raises ValueError when default value fails filter function predicate validation, ensuring filtered enumeration options exclude invalid defaults
    
    Tags: level:L3, topic:api
    
    Ownership: Application layer select_from_enum default-filter conflict validation test coverage for invalid default value edge case
    
    Invariants: Filter function must reject Framework.FASTAPI default value; ValueError must be raised with message containing "default" and "filtered"; no mock_prompt invocation when default fails filter validation; filter_fn predicate must eliminate default from valid options
    
    Side effects: Invokes select_from_enum with Framework enum, default=Framework.FASTAPI, reject-fastapi filter lambda; pytest.raises context manager captures ValueError; no user interaction due to early validation failure
    
    Inputs: Prompt string "What framework?"; Framework enum type; default=Framework.FASTAPI; filter_fn lambda returning False for FASTAPI to simulate default-filter mismatch
    
    Outputs: ValueError exception with message matching "default.*filtered" regex; pytest assertion validating exception raised when default fails filter validation
    
    Failure modes: Default-filter validation bypassed allowing invalid default; ValueError not raised for filtered-out default; incorrect exception type raised; error message missing "default" or "filtered" keywords; fallback behavior executes instead of validation failure
    
    IDK: default-filter-conflict, invalid-default, filter-validation, ValueError-assertion, enum-default-validation, reject-default-filter, wizard-error-handling, pytest-raises, early-validation, select-from-enum
    """
    with patch("tac_bootstrap.interfaces.wizard.Confirm.ask") as mock:
        yield mock


@pytest.fixture
def sample_detected_project():
    """
    Create a mock detected project with typical attributes.
    
    Responsibility: Generate test fixture returning mock DetectedProject object with Python/FastAPI/UV configuration including standard commands for start/test/lint/build and src app root for wizard testing dependencies
    
    Tags: level:L3, topic:api
    
    Ownership: Test utilities fixture providing sample DetectedProject mock instance for application layer wizard and detection test scenarios requiring typical project detection attributes
    
    Invariants: Returns MagicMock instance with language=Language.PYTHON; framework=Framework.FASTAPI; package_manager=PackageManager.UV; commands dict with exactly 4 keys (start, test, lint, build) containing uv-prefixed command strings; app_root="src"; all enum values must be valid domain model constants; no side effects on invocation
    
    Side effects: Instantiates MagicMock object; assigns Language/Framework/PackageManager enum attributes; constructs commands dictionary with UV-based CLI strings; returns configured mock with no filesystem or network I/O
    
    Inputs: None (parameterless fixture function)
    
    Outputs: MagicMock object configured with DetectedProject-compatible attributes including Language.PYTHON, Framework.FASTAPI, PackageManager.UV, commands dict {"start": "uv run fastapi dev", "test": "uv run pytest", "lint": "uv run ruff check .", "build": "uv build"}, app_root="src"
    
    Failure modes: Enum constants undefined from missing domain model imports; MagicMock attribute assignment fails from incorrect patching; commands dictionary missing required keys breaking wizard command validation; app_root path format incompatible with filesystem operations; enum value changes invalidating hardcoded Language.PYTHON/Framework.FASTAPI/PackageManager.UV references
    
    IDK: test-fixture, mock-DetectedProject, sample-data, Language-enum, Framework-enum, PackageManager-enum, uv-commands, fastapi-configuration, wizard-testing-dependencies, python-project-mock, app-root-src, MagicMock-fixture
    """
    detected = MagicMock()
    detected.language = Language.PYTHON
    detected.framework = Framework.FASTAPI
    detected.package_manager = PackageManager.UV
    detected.commands = {
        "start": "uv run fastapi dev",
        "test": "uv run pytest",
        "lint": "uv run ruff check .",
        "build": "uv build",
    }
    detected.app_root = "src"
    return detected


# ============================================================================
# TEST SELECT FROM ENUM
# ============================================================================


class TestSelectFromEnum:
    """
    Tests for select_from_enum function.
    
    Responsibility: Verify TestSelectFromEnum class provides comprehensive test coverage for select_from_enum function including default value selection, non-default option selection, filter function validation, empty-option edge cases, and default-filter conflict scenarios
    
    Tags: level:L3, topic:api
    
    Ownership: Test suite for application layer select_from_enum wizard utility function covering default acceptance, user selection, filtering behavior, and error handling edge cases
    
    Invariants: Each test method mocks mock_console and mock_prompt fixtures; mock_prompt.return_value simulates user selection index; all tests verify result matches expected enum value; filter tests validate predicate application; error tests use pytest.raises for exception validation; no actual user interaction occurs
    
    Side effects: Instantiates TestSelectFromEnum test class; executes pytest test methods with mock fixtures; validates select_from_enum behavior via assertions; no filesystem or network I/O; no configuration persistence
    
    Inputs: Mock_console fixture for output verification; mock_prompt fixture for simulating user input; Language and Framework enum types; filter_fn predicates for option subsetting; default enum values for acceptance testing
    
    Outputs: Pytest test execution results; assertion validations for enum value selection, filter application, error raising; mock call count verifications; test coverage for select_from_enum utility function
    
    Failure modes: Mock fixtures not properly injected breaking test isolation; enum ordering changes invalidating hardcoded index assumptions; filter validation bypassed allowing invalid options; error cases not raising expected exceptions; mock call count assertions failing from invocation mismatches
    
    IDK: select-from-enum, test-coverage, enum-selection-testing, mock-fixtures, filter-validation, default-value-testing, pytest-test-suite, Language-enum, Framework-enum, wizard-utility-testing, error-edge-cases, predicate-filtering
    """

    def test_select_with_default(self, mock_console, mock_prompt):
        """
        Test selection with default value.
        
        Responsibility: Validate select_from_enum default value selection by simulating user accepting first enum option via mock_prompt "1" and verifying result matches Language.PYTHON default value with console output verification
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer select_from_enum default value acceptance and enum first-option selection path test coverage
        
        Invariants: Mock_prompt must receive exactly 1 call returning "1" for first enum option; select_from_enum receives Language enum type with PYTHON default; user selection "1" must map to Language.PYTHON enum value matching provided default; mock_console.print must be invoked at least once; result must equal default value
        
        Side effects: Invokes select_from_enum with prompt "What programming language?", Language enum, default=Language.PYTHON; mock_prompt returns "1" simulating user selecting first option; validates result equals Language.PYTHON; asserts mock_console.print called verifying user-facing output displayed
        
        Inputs: Prompt string "What programming language?"; Language enum type; default=Language.PYTHON; mocked user selection "1" for first enumeration option
        
        Outputs: Language.PYTHON enum value; assertion validating result matches default Python language option; console output verification via mock_console.print.assert_called
        
        Failure modes: First option index "1" maps to incorrect enum value instead of Language.PYTHON; default value not returned despite matching user selection; mock_prompt not invoked or receives wrong prompt text; console output not displayed; enum ordering changes breaking first-position assumption
        
        IDK: select-from-enum, default-value-selection, enum-first-option, Language-enum, mock-prompt, wizard-default-acceptance, console-output-verification, python-default, interactive-cli-testing
        """
        # Simulate user pressing Enter (accepts default)
        mock_prompt.return_value = "1"  # First option (Python)

        result = select_from_enum(
            "What programming language?",
            Language,
            default=Language.PYTHON,
        )

        assert result == Language.PYTHON
        mock_console.print.assert_called()  # Verify output was shown

    def test_select_different_option(self, mock_console, mock_prompt):
        """
        Test selecting non-default option.
        
        Responsibility: Validate select_from_enum user selection of non-default enum option, verifying mock_prompt returns option index "2" for TypeScript selection and result matches Language.TYPESCRIPT enum value
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer select_from_enum non-default option selection and enum index-to-value mapping test coverage
        
        Invariants: Mock_prompt must receive exactly 1 call returning "2" for second enum option; select_from_enum receives Language enum type with PYTHON default; user selection "2" must map to Language.TYPESCRIPT enum value; selected result must not equal default value; enum ordering must be deterministic
        
        Side effects: Invokes select_from_enum with prompt "What programming language?", Language enum, default=Language.PYTHON; mock_prompt returns "2" simulating user selecting second option; validates result equals Language.TYPESCRIPT asserting correct enum index mapping
        
        Inputs: Prompt string "What programming language?"; Language enum type; default=Language.PYTHON; mocked user selection "2" for second enumeration option
        
        Outputs: Language.TYPESCRIPT enum value; assertion validating result matches TypeScript language option from second enum position
        
        Failure modes: Option index "2" maps to incorrect enum value; enum ordering changes breaking deterministic second-position assumption; mock_prompt not invoked or receives wrong prompt text; default value returned instead of user selection; enum index out of bounds
        
        IDK: select-from-enum, non-default-selection, enum-index-mapping, Language-enum, user-selection, option-index, typescript-selection, wizard-enum-selection, mock-prompt, enum-ordering
        """
        # Simulate user selecting option 2 (TypeScript)
        mock_prompt.return_value = "2"

        result = select_from_enum(
            "What programming language?",
            Language,
            default=Language.PYTHON,
        )

        # TypeScript should be second in the Language enum
        assert result == Language.TYPESCRIPT

    def test_select_with_filter(self, mock_console, mock_prompt):
        """
        Test selection with filter function.
        
        Responsibility: Validate select_from_enum filtering behavior when filter function preserves subset of Framework enumeration options, verifying filtered selection returns only Python-compatible frameworks and user prompt displays only valid options
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer select_from_enum filter function validation test coverage for language-framework compatibility filtering use case
        
        Invariants: Filter function must eliminate non-Python Framework enum values; get_frameworks_for_language(Language.PYTHON) return value defines valid options subset; selected result must exist in valid_frameworks set; mock_prompt receives exactly 1 call with "1" selection; filtered enumeration options displayed to user must match filter_fn predicate; no invalid framework options presented
        
        Side effects: Invokes get_frameworks_for_language(Language.PYTHON) to retrieve authoritative valid frameworks; invokes select_from_enum with Framework enum and language-compatibility filter lambda; mock_prompt returns "1" selecting first valid option; validates result membership in valid_frameworks set
        
        Inputs: Prompt string "What framework?"; Framework enum type; default=Framework.NONE; filter_fn lambda checking membership in get_frameworks_for_language(Language.PYTHON) result; mocked user selection "1" for first valid option
        
        Outputs: Framework enum value from valid_frameworks set matching Python language compatibility; assertion validating result in valid_frameworks; filtered option list presented to user via mock_prompt
        
        Failure modes: Filter function incorrectly includes non-Python frameworks; filter bypassed showing all Framework options; selected result not validated against filter_fn predicate; get_frameworks_for_language returns stale or incorrect framework set; default value selected despite being filtered out; mock_prompt receives invalid option index
        
        IDK: filter-fn, select-from-enum, framework-filtering, language-compatibility, get-frameworks-for-language, enum-subset-validation, filtered-options, python-framework-compatibility, wizard-filtering, predicate-validation
        """
        # Only allow frameworks that work with Python
        from tac_bootstrap.domain.models import get_frameworks_for_language

        valid_frameworks = get_frameworks_for_language(Language.PYTHON)

        # Select first valid option
        mock_prompt.return_value = "1"

        result = select_from_enum(
            "What framework?",
            Framework,
            default=Framework.NONE,
            filter_fn=lambda f: f in valid_frameworks,
        )

        # Should be a Python-compatible framework
        assert result in valid_frameworks

    def test_select_no_valid_options(self, mock_console, mock_prompt):
        """
        Test error when filter removes all options.
        
        Responsibility: Validate wizard error handling when filter function eliminates all enumeration options by asserting ValueError raised with "No valid options available" message
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer select_from_enum filtering validation test coverage for complete option elimination edge case
        
        Invariants: Filter function lambda returning False must eliminate all Framework enum options; ValueError must be raised with exact match on "No valid options available" message; no mock_prompt invocation when zero valid options exist; no default fallback behavior when filter eliminates all choices
        
        Side effects: Invokes select_from_enum with Framework enum and reject-all filter lambda; pytest.raises context manager captures ValueError; no user interaction or configuration creation due to early validation failure
        
        Inputs: Prompt string "What framework?"; Framework enum type; filter_fn lambda function returning False for all inputs to simulate zero valid options scenario
        
        Outputs: ValueError exception with message matching "No valid options available"; pytest assertion validating exception raised with correct error message
        
        Failure modes: Filter validation bypassed allowing empty options list; ValueError not raised for zero valid options; incorrect exception type raised; error message mismatch breaking pytest.raises match assertion; fallback behavior executes instead of failing fast
        
        IDK: filter-validation, empty-options-edge-case, select-from-enum, ValueError-assertion, reject-all-filter, zero-valid-options, pytest-raises, wizard-error-handling, enum-filtering, early-validation-failure
        """
        # Filter that rejects everything
        with pytest.raises(ValueError, match="No valid options available"):
            select_from_enum(
                "What framework?",
                Framework,
                filter_fn=lambda f: False,  # Reject all
            )

    def test_default_not_in_filtered_options(self, mock_console, mock_prompt):
        """
        Test when default is filtered out.
        
        Responsibility: Validate wizard cancellation flow during initialization by verifying SystemExit(0) raised when user cancels at final confirmation prompt with correct abort message display
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer initialization wizard cancellation flow and user-abort exit handling test coverage
        
        Invariants: Mock_prompt receives exactly 8 calls for language/framework/package_manager/commands/target_branch selections; mock_confirm receives exactly 2 calls (worktrees=True, final=False); cancellation at final confirmation must raise SystemExit with code 0; abort message must be printed to console; no configuration or filesystem side effects after cancellation
        
        Side effects: Invokes mock_prompt 8 times with user selecting option "1" for enums and empty strings for optional commands; invokes mock_confirm 2 times (worktrees=True, final=False); raises SystemExit(0); prints "[yellow]Aborted.[/yellow]" to console; no ProjectConfig creation or file modifications
        
        Inputs: Project name string "cancelled-project"; mocked user selections via mock_prompt.side_effect ["1", "1", "1", "1", "", "", "", "main"] for language/framework/package_manager/commands/target_branch; mock_confirm.side_effect [True, False] simulating worktrees enabled then cancellation at final confirmation
        
        Outputs: SystemExit exception with exit code 0; console print assertion validating abort message "[yellow]Aborted.[/yellow]" displayed to user
        
        Failure modes: SystemExit not raised on cancellation; incorrect exit code (non-zero or None); abort message not displayed or incorrectly formatted; mock side_effect exhaustion from mismatched prompt sequence length; wizard continues execution after user cancellation; configuration persisted despite abort
        
        IDK: cancellation-flow, SystemExit-validation, abort-message, user-cancellation, wizard-abort, final-confirmation, mock-confirm, interactive-cli-testing, exit-code-zero, no-side-effects, init-wizard
        """
        # Filter to only TypeScript frameworks
        from tac_bootstrap.domain.models import get_frameworks_for_language

        valid_frameworks = get_frameworks_for_language(Language.TYPESCRIPT)

        # Default is a Python framework, but we're filtering to TS
        mock_prompt.return_value = "1"  # Select first valid option

        result = select_from_enum(
            "What framework?",
            Framework,
            default=Framework.FASTAPI,  # Python framework
            filter_fn=lambda f: f in valid_frameworks,
        )

        # Should select a TypeScript-compatible framework
        assert result in valid_frameworks


# ============================================================================
# TEST RUN INIT WIZARD
# ============================================================================


class TestRunInitWizard:
    """
    Tests for run_init_wizard function.
    
    Responsibility: Validate add-agentic wizard acceptance testing for detected-value persistence, override flows, and cancellation flows across existing project scenarios
    
    Tags: level:L3, topic:api
    
    Ownership: Test suite application layer add-agentic wizard covering detected-value acceptance, language-override cascades, and user-abort scenarios
    
    Invariants: Mock_prompt call count matches wizard sequence length; mock_confirm receives exactly 2 calls per test; detected values persist when user accepts defaults; language override triggers framework/package_manager reselection; cancellation raises SystemExit(0); no configuration instantiation errors for valid inputs
    
    Side effects: Executes run_add_agentic_wizard with mocked fixtures; validates ProjectConfig output against expected detected/overridden values; asserts mock invocation counts; no file I/O or network calls
    
    Inputs: Mock_console, mock_prompt, mock_confirm fixtures; sample_detected_project fixture with pre-detected Python/FastAPI/UV configuration; repository path for existing project; test-specific mock_prompt.side_effect sequences; mock_confirm boolean sequences
    
    Outputs: Test assertions validating detected-value persistence, override flows, cancellation behavior; ProjectConfig instances with expected values; mock call count validations; SystemExit(0) on cancellation
    
    Failure modes: Detected values overridden when user accepts defaults; language override fails to trigger dependent field reselection; cancellation doesn't raise SystemExit(0); mock side_effect exhaustion from prompt sequence length mismatch; detected commands lost during wizard flow; project mode incorrectly set to NEW instead of EXISTING
    
    IDK: add-agentic-wizard, detected-values-persistence, override-cascades, cancellation-flow, existing-project-mode, mock-fixtures, pytest-test-coverage, language-override-reselection, wizard-acceptance-testing, interactive-cli-testing, SystemExit-validation, sample-detected-project
    """

    def test_wizard_with_all_defaults(self, mock_console, mock_prompt, mock_confirm):
        """
        Test wizard accepting all default values.
        
        Responsibility: Validate wizard accepting all default enumeration selections and default command values, verifying first-option selection for language/framework/package_manager/architecture and get_default_commands return values persist to final ProjectConfig with worktrees enabled and main branch
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer init wizard default-value acceptance flow and first-option enumeration selection path test coverage
        
        Invariants: Mock_prompt receives exactly 8 calls for language/framework/package_manager/architecture/commands/target_branch; mock_confirm receives exactly 2 calls with both True; first option "1" for all enum prompts must select Language.PYTHON, Framework.FASTAPI, PackageManager.UV, Architecture.SIMPLE; returned default command strings must match get_default_commands(Language.PYTHON, PackageManager.UV) output exactly; worktrees must be enabled; target_branch must equal "main"
        
        Side effects: Invokes get_default_commands(Language.PYTHON, PackageManager.UV) to retrieve authoritative defaults; invokes mock_prompt 8 times with user selecting "1" for enums and returning default_cmds strings for commands; invokes mock_confirm 2 times with both True; creates ProjectConfig with name="myproject", mode=NEW, language=PYTHON, framework=FASTAPI, architecture=SIMPLE, commands matching default_cmds, worktrees.enabled=True, target_branch="main"
        
        Inputs: Project name string "myproject"; mocked user selections via mock_prompt.side_effect ["1", "1", "1", "1", default_cmds.start, default_cmds.test, default_cmds.lint, "main"]; mock_confirm.side_effect [True, True] for worktrees and final confirmation; get_default_commands return value for Python/UV
        
        Outputs: ProjectConfig instance with project.name="myproject", mode=NEW, language=PYTHON, framework=FASTAPI, architecture=SIMPLE, commands.start/test matching get_default_commands output, worktrees.enabled=True, target_branch="main"; assertions validating default value persistence
        
        Failure modes: First enum option doesn't map to expected Language.PYTHON/Framework.FASTAPI; get_default_commands return values modified during wizard flow; empty string interpreted as "use default" instead of "no input"; default commands not persisted to config.commands; mock side_effect exhaustion from prompt sequence mismatch; worktrees incorrectly disabled; target_branch overridden
        
        IDK: default-values, first-option-selection, get_default_commands, init-wizard, enum-defaults, mock-side-effects, python-fastapi-uv, worktrees-enabled, wizard-acceptance, command-defaults, new-project-mode, pytest-fixtures
        """
        # Mock all prompts to accept defaults (option 1 for selects)
        # For commands, we need to return the actual default values since
        # empty string means "no input" not "use default"
        from tac_bootstrap.domain.models import get_default_commands
        default_cmds = get_default_commands(Language.PYTHON, PackageManager.UV)

        mock_prompt.side_effect = [
            "1",  # Language: Python (default)
            "1",  # Framework: FASTAPI (first option for Python)
            "1",  # Package Manager: UV (default for Python)
            "1",  # Architecture: Simple (default)
            default_cmds.get("start", ""),  # Start command (return default)
            default_cmds.get("test", ""),  # Test command (return default)
            default_cmds.get("lint", ""),  # Lint command (return default)
            "main",  # Target branch (default)
        ]
        mock_confirm.side_effect = [
            True,  # Enable worktrees
            True,  # Confirm configuration
        ]

        config = run_init_wizard("myproject")

        # Verify project configuration
        assert config.project.name == "myproject"
        assert config.project.mode == ProjectMode.NEW
        assert config.project.language == Language.PYTHON
        assert config.project.framework == Framework.FASTAPI  # First option for Python
        assert config.project.architecture == Architecture.SIMPLE

        # Verify default commands were set (should match what get_default_commands returns)
        assert config.commands.start == default_cmds.get("start", "")
        assert config.commands.test == default_cmds.get("test", "")

        # Verify worktrees enabled
        assert config.agentic.worktrees.enabled is True

        # Verify target branch
        assert config.agentic.target_branch == "main"

    def test_wizard_with_custom_values(self, mock_console, mock_prompt, mock_confirm):
        """
        Test wizard with custom user selections.
        
        Responsibility: Validate wizard behavior with user overriding all detected project values, verifying language override triggers dependent framework/package-manager reselection and custom command strings persist to final configuration
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer add-agentic wizard value override flow and language-dependent cascade revalidation test coverage
        
        Invariants: Language override must trigger fresh framework/package_manager selection prompts for new language; mock_prompt receives exactly 8 calls; mock_confirm receives exactly 2 calls; custom command strings must persist unchanged; worktrees setting independent of override flow; final config must contain zero detected values; all overridden selections must persist to ProjectConfig
        
        Side effects: Invokes mock_prompt 8 times for language/framework/package_manager/architecture/commands/target_branch override selections; invokes mock_confirm 2 times [False, True] for worktrees disabled and final confirmation; creates ProjectConfig with language=Language.TYPESCRIPT and custom pnpm commands; validates override values differ from sample_detected_project fixture
        
        Inputs: Repository path Path("/path/to/existing-repo"); sample_detected_project fixture containing detected Python/FastAPI/UV configuration; mocked user selections ["2", "1", "1", "pnpm dev", "pnpm test", "pnpm lint", "pnpm build", "master"] overriding to TypeScript with custom commands; mock_confirm sequence [False, True] disabling worktrees
        
        Outputs: ProjectConfig instance with project.language=Language.TYPESCRIPT, custom pnpm command strings, agentic.worktrees.enabled=False, agentic.target_branch="master"; assertions validating complete override of detected values
        
        Failure modes: Language override fails to cascade framework/package_manager reselection; custom commands reverted to detected values; override selections ignored or partially applied; worktrees toggle incorrectly coupled to language override; mock side_effect exhaustion from unexpected prompt sequence; detected values bleed into final configuration despite overrides
        
        IDK: detected-values-override, language-cascade, framework-reselection, package-manager-reselection, custom-command-persistence, typescript-override, worktrees-disabled, add-agentic-wizard, override-flow, mock-side-effects, configuration-override, interactive-cli
        """
        # Mock prompts for TypeScript + React + npm + LAYERED
        mock_prompt.side_effect = [
            "2",  # Language: TypeScript
            "4",  # Framework: React (4th option for TS: NEXTJS, EXPRESS, NESTJS, REACT)
            "2",  # Package Manager: npm (2nd for TS: PNPM, NPM)
            "2",  # Architecture: LAYERED (2nd option)
            "npm run dev",  # Custom start command
            "npm test",  # Custom test command
            "npm run lint",  # Custom lint command
            "develop",  # Custom target branch
        ]
        mock_confirm.side_effect = [
            False,  # Disable worktrees
            True,  # Confirm configuration
        ]

        config = run_init_wizard("custom-app")

        # Verify custom selections
        assert config.project.name == "custom-app"
        assert config.project.language == Language.TYPESCRIPT
        assert config.project.architecture == Architecture.LAYERED
        assert config.commands.start == "npm run dev"
        assert config.commands.test == "npm test"
        assert config.commands.lint == "npm run lint"
        assert config.agentic.worktrees.enabled is False
        assert config.agentic.target_branch == "develop"

    def test_wizard_with_preset_language(self, mock_console, mock_prompt, mock_confirm):
        """
        Test wizard when language is already provided.
        
        Responsibility: Validate wizard behavior when language parameter is preset, verifying language selection step is skipped and remaining initialization prompts execute normally with preset value persisted to final configuration
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer init wizard preset-language flow and partial wizard execution path test coverage
        
        Invariants: Preset language must skip language selection prompt; mock_prompt receives exactly 7 calls (excluding language); mock_confirm receives exactly 2 calls; preset Language.GO must persist unchanged to final config; framework/package_manager selection must occur normally despite preset language; all non-language wizard steps must execute in standard sequence
        
        Side effects: Invokes mock_prompt 7 times for framework/package_manager/architecture/commands/target_branch; invokes mock_confirm 2 times with both True; creates ProjectConfig with language=Language.GO; validates preset parameter bypasses language selection step
        
        Inputs: Project name string "preset-project"; preset language parameter Language.GO; mocked user selections ["1", "1", "1", "", "", "", "main"] for framework/package_manager/architecture/commands/target_branch; mock_confirm sequence [True, True]
        
        Outputs: ProjectConfig instance with project.language=Language.GO matching preset parameter; assertion validating preset language persistence
        
        Failure modes: Preset language overridden by wizard flow; language selection prompt executed despite preset; mock side_effect exhaustion from incorrect reduced prompt count; preset parameter ignored causing language to default or prompt user; framework/package_manager selection incompatible with preset language
        
        IDK: preset-language, partial-wizard-flow, init-wizard, parameter-bypass, language-preset, mock-side-effects, reduced-prompts, wizard-testing, go-language, configuration-preset, pytest-fixtures, interactive-cli
        """
        # Language preset, so wizard skips that step
        mock_prompt.side_effect = [
            "1",  # Framework
            "1",  # Package Manager
            "1",  # Architecture
            "",  # Start command
            "",  # Test command
            "",  # Lint command
            "main",  # Target branch
        ]
        mock_confirm.side_effect = [True, True]

        config = run_init_wizard("preset-project", language=Language.GO)

        # Verify preset language was used
        assert config.project.language == Language.GO

    def test_wizard_cancellation(self, mock_console, mock_prompt, mock_confirm):
        """
        Test wizard when user cancels at confirmation.
        
        Responsibility: Validate wizard cancellation flow during initialization by verifying SystemExit(0) raised when user cancels at final confirmation prompt with correct abort message display
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer initialization wizard cancellation flow and user-abort exit handling test coverage
        
        Invariants: Mock_prompt receives exactly 8 calls for language/framework/package_manager/commands/target_branch selections; mock_confirm receives exactly 2 calls (worktrees=True, final=False); cancellation at final confirmation must raise SystemExit with code 0; abort message must be printed to console; no configuration or filesystem side effects after cancellation
        
        Side effects: Invokes mock_prompt 8 times with user selecting option "1" for enums and empty strings for optional commands; invokes mock_confirm 2 times (worktrees=True, final=False); raises SystemExit(0); prints "[yellow]Aborted.[/yellow]" to console; no ProjectConfig creation or file modifications
        
        Inputs: Project name string "cancelled-project"; mocked user selections via mock_prompt.side_effect ["1", "1", "1", "1", "", "", "", "main"] for language/framework/package_manager/commands/target_branch; mock_confirm.side_effect [True, False] simulating worktrees enabled then cancellation at final confirmation
        
        Outputs: SystemExit exception with exit code 0; console print assertion validating abort message "[yellow]Aborted.[/yellow]" displayed to user
        
        Failure modes: SystemExit not raised on cancellation; incorrect exit code (non-zero or None); abort message not displayed or incorrectly formatted; mock side_effect exhaustion from mismatched prompt sequence length; wizard continues execution after user cancellation; configuration persisted despite abort
        
        IDK: init-wizard, user-cancellation, systemExit, abort-flow, mock-side-effects, pytest-raises, confirmation-prompt, wizard-testing, exit-code-validation, rich-console, interactive-cli, cancellation-handling
        """
        mock_prompt.side_effect = ["1", "1", "1", "1", "", "", "", "main"]
        mock_confirm.side_effect = [
            True,  # Enable worktrees
            False,  # Cancel at final confirmation
        ]

        # Should raise SystemExit when user cancels
        with pytest.raises(SystemExit) as exc_info:
            run_init_wizard("cancelled-project")

        assert exc_info.value.code == 0
        mock_console.print.assert_any_call("[yellow]Aborted.[/yellow]")


# ============================================================================
# TEST RUN ADD AGENTIC WIZARD
# ============================================================================


class TestRunAddAgenticWizard:
    """
    Tests for run_add_agentic_wizard function.
    
    Responsibility: Validate TestRunAddAgenticWizard class behavior for add-agentic wizard acceptance testing covering detected value persistence, user override flows, and cancellation scenarios
    
    Tags: level:L3, topic:api
    
    Ownership: Test suite for application layer add-agentic wizard covering detected-value acceptance, override flows, and cancellation handling
    
    Invariants: All tests isolate wizard behavior through mocks; each test validates specific add-agentic scenario independently; mock call counts must match expected interaction patterns (8 prompts, 2 confirms); configuration validation must not raise exceptions for valid inputs; detected values must persist when accepted; overrides must trigger dependent field reselection
    
    Side effects: Executes add-agentic wizard with mocked user interactions; validates configuration output against expected detected/overridden values; asserts mock invocation counts; no filesystem or network operations
    
    Inputs: Mocked console, prompt, and confirm fixtures; sample_detected_project fixture containing pre-detected language/framework/package_manager/commands/app_root; repository path for existing project; test-specific user selection sequences
    
    Outputs: Test assertions validating correct add-agentic wizard behavior; ProjectConfig instances with expected detected or overridden values; mock call count validations; SystemExit(0) on cancellation
    
    Failure modes: Detected values lost or overridden incorrectly; override flow fails to trigger dependent reselection; cancellation doesn't raise SystemExit; mock side_effect exhaustion from incorrect prompt sequences; detected commands not persisted; project mode incorrectly set
    
    IDK: add-agentic-wizard, detected-values, test-coverage, override-flows, cancellation-testing, mock-fixtures, pytest-parametrization, wizard-acceptance, existing-project-mode, configuration-persistence, interactive-cli-testing, SystemExit-testing
    """

    def test_wizard_with_detected_values(
        self, mock_console, mock_prompt, mock_confirm, sample_detected_project
    ):
        """
        Test wizard using detected project values.
        
        Responsibility: Verify wizard accepts all detected project values without user override, persisting detected language, framework, package_manager, commands, and app_root path to final configuration
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer add-agentic wizard detection acceptance flow and detected-value persistence logic
        
        Invariants: Mock_prompt receives exactly 8 calls for selection/command inputs; mock_confirm receives exactly 2 calls for worktrees and final confirmation; detected values must persist unmodified in final ProjectConfig; project mode must be EXISTING; repo_root must match input path; all detected commands must appear in config.commands exactly as provided
        
        Side effects: Creates ProjectConfig with detected values (Language.PYTHON, Framework.FASTAPI, PackageManager.UV, app_root="src"); invokes mock_prompt 8 times with user selecting option "1" for detected enums and accepting detected command strings; invokes mock_confirm 2 times with both True; validates detected project fixture values match final configuration
        
        Inputs: Repository path Path("/path/to/existing-repo"); sample_detected_project fixture containing detected language/framework/package_manager/commands/app_root; mocked user selections accepting all detected values via "1" choices and returning detected command strings; mock_confirm sequence [True, True]
        
        Outputs: ProjectConfig instance with project.name="existing-repo", project.mode=EXISTING, language=PYTHON, framework=FASTAPI, package_manager=UV, commands matching detected values, paths.app_root="src"; assertions validating detected value persistence
        
        Failure modes: Detected values overridden despite user accepting defaults; mock side_effect exhaustion from incorrect prompt sequence; detected commands modified or lost during wizard flow; app_root path not persisted; project mode incorrectly set to INIT instead of EXISTING
        
        IDK: detected-values, add-agentic-flow, value-persistence, project-detection, interactive-wizard, detected-commands, app-root-detection, existing-project-mode, mock-side-effects, wizard-acceptance, pytest-fixtures, configuration-detection
        """
        # Accept all detected values (option 1 for each select)
        # When Prompt.ask is called with a default, returning empty string means accept default
        mock_prompt.side_effect = [
            "1",  # Language: PYTHON (detected)
            "1",  # Framework: FASTAPI (detected)
            "1",  # Package Manager: UV (detected)
            "uv run fastapi dev",  # Start command (return detected value)
            "uv run pytest",  # Test command (return detected value)
            "uv run ruff check .",  # Lint command (return detected value)
            "uv build",  # Build command (return detected value)
            "main",  # Target branch
        ]
        mock_confirm.side_effect = [
            True,  # Enable worktrees
            True,  # Confirm configuration
        ]

        repo_path = Path("/path/to/existing-repo")
        config = run_add_agentic_wizard(repo_path, sample_detected_project)

        # Verify detected values were used
        assert config.project.name == "existing-repo"
        assert config.project.mode == ProjectMode.EXISTING
        assert config.project.repo_root == str(repo_path)
        assert config.project.language == Language.PYTHON
        assert config.project.framework == Framework.FASTAPI
        assert config.project.package_manager == PackageManager.UV

        # Verify detected commands
        assert config.commands.start == "uv run fastapi dev"
        assert config.commands.test == "uv run pytest"
        assert config.commands.lint == "uv run ruff check ."
        assert config.commands.build == "uv build"

        # Verify detected app_root
        assert config.paths.app_root == "src"

    def test_wizard_overriding_detected_values(
        self, mock_console, mock_prompt, mock_confirm, sample_detected_project
    ):
        """
        Test wizard when user overrides detected values.
        
        Responsibility: Verify wizard correctly handles user override of detected project values when changing language triggers framework/package-manager reselection and custom command configuration
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer add-agentic wizard override flow and language-dependent configuration revalidation
        
        Invariants: Changing detected language must trigger fresh framework/package-manager selection prompts; custom command strings must persist exactly as entered; worktrees toggle must be independent of override flow; mock_prompt receives exactly 8 calls for override scenario; mock_confirm receives exactly 2 calls; final config must reflect all user overrides not detected values
        
        Side effects: Creates ProjectConfig with overridden language (TypeScript), framework, package_manager, and custom commands; invokes mock_prompt 8 times; invokes mock_confirm 2 times; disables worktrees via first confirm=False
        
        Inputs: Repository path Path("/path/to/existing-repo"); sample_detected_project fixture with detected values; mocked user selections overriding language to TypeScript (2), selecting first valid framework/package-manager for TS, custom pnpm commands, master target branch; mock_confirm sequence [False, True]
        
        Outputs: ProjectConfig instance with language=Language.TYPESCRIPT, commands matching custom pnpm values, agentic.worktrees.enabled=False; assertions validating overridden values differ from detected project
        
        Failure modes: Override fails to trigger framework/package-manager reselection; custom commands ignored or reverted to detected values; language change rejected or not persisted; worktrees setting incorrectly coupled to override flow; mock side_effect exhaustion from incorrect prompt sequence
        
        IDK: override-detection, language-switching, detected-values, add-agentic-flow, framework-reselection, custom-commands, worktrees-toggle, interactive-wizard, configuration-override, mock-side-effects, typescript-migration, pytest-fixtures
        """
        # Change language to TypeScript
        mock_prompt.side_effect = [
            "2",  # Language: TypeScript (override detected)
            "1",  # Framework: First valid for TS
            "1",  # Package Manager: First valid for TS
            "pnpm dev",  # Custom start command
            "pnpm test",  # Custom test command
            "pnpm lint",  # Custom lint command
            "pnpm build",  # Custom build command
            "master",  # Custom target branch
        ]
        mock_confirm.side_effect = [False, True]

        repo_path = Path("/path/to/existing-repo")
        config = run_add_agentic_wizard(repo_path, sample_detected_project)

        # Verify overrides
        assert config.project.language == Language.TYPESCRIPT
        assert config.commands.start == "pnpm dev"
        assert config.agentic.worktrees.enabled is False

    def test_add_agentic_cancellation(
        self, mock_console, mock_prompt, mock_confirm, sample_detected_project
    ):
        """
        Test add agentic wizard when user cancels.
        
        Responsibility: Verify wizard correctly handles user cancellation during add-agentic flow by raising SystemExit(0) and displaying abort message
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer add-agentic wizard cancellation flow and exit handling
        
        Invariants: User cancellation at final confirmation must raise SystemExit with code 0; wizard must display abort message; mock_prompt receives exactly 8 calls before cancellation; mock_confirm receives exactly 2 calls with final False triggering exit
        
        Side effects: Invokes mock_prompt 8 times for user selections; invokes mock_confirm 2 times (worktrees=True, final=False); raises SystemExit(0); prints abort message to console; no configuration or filesystem modifications
        
        Inputs: Repository path Path("/path/to/repo"); sample_detected_project fixture; mocked user selections (language=1, framework=1, package_manager=1, empty commands, target_branch="main"); mock_confirm sequence [True, False] simulating cancellation
        
        Outputs: SystemExit exception with code 0; console print call with "[yellow]Aborted.[/yellow]" message
        
        Failure modes: SystemExit not raised on cancellation; incorrect exit code (non-zero); abort message not displayed; mock side_effect exhaustion from incorrect prompt sequence; wizard continues execution after cancellation
        
        IDK: wizard-cancellation, exit-handling, user-abort, interactive-wizard, add-agentic-flow, systemExit, abort-messaging, mock-side-effects, confirmation-sequence, cancellation-testing, pytest-raises, rich-console
        """
        mock_prompt.side_effect = ["1", "1", "1", "", "", "", "", "main"]
        mock_confirm.side_effect = [
            True,  # Enable worktrees
            False,  # Cancel at final confirmation
        ]

        repo_path = Path("/path/to/repo")

        # Should raise SystemExit when user cancels
        with pytest.raises(SystemExit) as exc_info:
            run_add_agentic_wizard(repo_path, sample_detected_project)

        assert exc_info.value.code == 0
        mock_console.print.assert_any_call("[yellow]Aborted.[/yellow]")


# ============================================================================
# TEST EDGE CASES
# ============================================================================


class TestWizardEdgeCases:
    """
    Tests for edge cases and error conditions.
    
    Responsibility: Validate wizard behavior under boundary conditions, empty inputs, and preset configuration scenarios
    
    Tags: level:L3, topic:api
    
    Ownership: Application layer initialization wizard edge case validation and error handling test coverage
    
    Invariants: All tests isolate wizard behavior through mocks; each test validates specific edge case independently; mock call counts must match expected interaction patterns; configuration validation must not raise exceptions for valid edge cases
    
    Side effects: Executes wizard with mocked user interactions; validates configuration output; asserts mock invocation counts; no filesystem or network operations
    
    Inputs: Mocked console, prompt, and confirm fixtures; various edge case scenarios (empty strings, preset values); test-specific project names and configuration parameters
    
    Outputs: Test assertions validating correct wizard behavior; configuration instances with expected values; mock call count validations
    
    Failure modes: Wizard rejects valid edge case inputs; preset bypass logic fails; type coercion breaks empty string handling; mock exhaustion from incorrect prompt sequences; configuration validation errors on valid inputs
    
    IDK: edge-case-testing, wizard-validation, init-wizard, test-fixtures, mock-assertions, boundary-conditions, preset-configuration, optional-inputs, typer-cli-testing, interactive-wizard, pytest-mocking, validation-testing
    """

    def test_empty_command_strings_allowed(
        self, mock_console, mock_prompt, mock_confirm
    ):
        """
        Test that empty strings are acceptable for optional commands.
        
        Responsibility: Verify that init wizard accepts empty strings for optional command configuration fields (start, test, lint) without converting to None or raising validation errors
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer initialization wizard input validation and optional field handling
        
        Invariants: Empty string inputs for start/test/lint commands must remain as empty strings (str type); project name and target branch remain required; all command fields must be str type (never None); Language/Framework/PackageManager selections still prompted; mock_prompt receives exactly 8 calls; mock_confirm receives exactly 2 calls
        
        Side effects: Creates ProjectConfig with empty string command values; invokes mock_prompt 8 times; invokes mock_confirm 2 times; validates type preservation of empty strings
        
        Inputs: Project name "minimal-project"; mocked user selections for language (1), framework (1), package_manager (1), architecture (1), empty strings for start/test/lint commands, target branch "main"
        
        Outputs: ProjectConfig instance with commands.start/test/lint as empty strings (not None); type assertions confirming str type for all command fields
        
        Failure modes: Empty strings converted to None indicating incorrect optional field handling; type validation failure if commands become NoneType; mock side_effect exhaustion from incorrect prompt count; wizard rejection of empty command inputs
        
        IDK: optional-fields, empty-string-validation, init-wizard, command-configuration, type-preservation, nullable-vs-empty, wizard-validation, interactive-cli, minimal-configuration, typer-prompts, test-mocking, edge-case-testing
        """
        mock_prompt.side_effect = [
            "1",  # Language
            "1",  # Framework
            "1",  # Package Manager
            "1",  # Architecture
            "",  # Start command (empty)
            "",  # Test command (empty)
            "",  # Lint command (empty)
            "main",  # Target branch
        ]
        mock_confirm.side_effect = [True, True]

        config = run_init_wizard("minimal-project")

        # Empty strings should be preserved (not None)
        assert isinstance(config.commands.start, str)
        assert isinstance(config.commands.test, str)
        assert isinstance(config.commands.lint, str)

    def test_preset_values_skip_prompts(
        self, mock_console, mock_prompt, mock_confirm
    ):
        """
        Test that preset values reduce number of prompts.
        
        Responsibility: Verify that supplying preset configuration values to init wizard bypasses corresponding interactive prompts and reduces total prompt count
        
        Tags: level:L3, topic:api
        
        Ownership: Application layer initialization wizard flow control
        
        Invariants: Preset language, framework, package_manager parameters skip selection prompts; architecture and command prompts still required; preset values persist in final configuration; mock_prompt call count equals non-preset prompt count only
        
        Side effects: Creates ProjectConfig with preset values; invokes mock_prompt 5 times; invokes mock_confirm 2 times
        
        Inputs: Project name "preset-all"; Language.RUST; Framework.NONE; PackageManager.CARGO; mocked user selections for architecture, commands, target branch
        
        Outputs: ProjectConfig instance with preset language/framework/package_manager values and user-selected architecture/commands; assertion validations on configuration fields and prompt call counts
        
        Failure modes: Preset values not respected in final config; incorrect prompt count indicates preset bypass logic failure; mock side_effect exhaustion from unexpected prompt calls
        
        IDK: wizard-presets, prompt-reduction, configuration-override, init-wizard, mock-assertion, call-count-validation, preset-bypass, interactive-cli, typer-prompts, configuration-presets, test-mocking
        """
        # When language, framework, and package_manager are preset
        mock_prompt.side_effect = [
            "1",  # Architecture (only remaining selection)
            "",  # Start command
            "",  # Test command
            "",  # Lint command
            "main",  # Target branch
        ]
        mock_confirm.side_effect = [True, True]

        config = run_init_wizard(
            "preset-all",
            language=Language.RUST,
            framework=Framework.NONE,
            package_manager=PackageManager.CARGO,
        )

        # Verify presets were used
        assert config.project.language == Language.RUST
        assert config.project.framework == Framework.NONE
        assert config.project.package_manager == PackageManager.CARGO

        # Verify fewer prompts were called (no language/framework/pm selection)
        assert mock_prompt.call_count == 5  # Only arch + 3 commands + target_branch
