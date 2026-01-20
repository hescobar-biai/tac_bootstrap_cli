# DetectService - Project Technology Stack Auto-Detection

**ADW ID:** 3b39c634
**Date:** 2026-01-20
**Specification:** specs/issue-34-adw-3b39c634-sdlc_planner-detect-service.md

## Overview

DetectService is an intelligent service that automatically analyzes existing repositories to identify their technology stack. It detects programming language, web framework, package manager, application root directory, and common project commands by inspecting project files and dependencies. This enables the `add-agentic` command to pre-populate the wizard with smart suggestions, minimizing manual user input and reducing configuration errors.

## What Was Built

- `DetectedProject` dataclass for structured detection results
- `DetectService` class with comprehensive detection methods
- Language detection for Python, TypeScript, JavaScript, Go, Rust, and Java
- Package manager detection across 11+ different managers (uv, pip, poetry, npm, pnpm, yarn, bun, cargo, maven, gradle, etc.)
- Framework detection for major frameworks (FastAPI, Django, Flask, Next.js, NestJS, Express, React, Vue, Gin, Echo, Axum, Actix, Spring)
- Application root directory identification
- Project command extraction from package.json and pyproject.toml
- Defensive parsing with error handling for malformed files
- Cross-Python-version compatibility (3.10+ using tomllib/tomli)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/detect_service.py`: **New file** containing all detection logic (403 lines)
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`: Minor update (13 lines changed)
- `specs/issue-34-adw-3b39c634-sdlc_planner-detect-service.md`: **New specification** (336 lines)

### Key Changes

#### DetectedProject Dataclass

The `DetectedProject` dataclass (lines 34-52 in detect_service.py) provides a structured result container:

```python
@dataclass
class DetectedProject:
    language: Language                           # Primary programming language
    framework: Optional[Framework] = None        # Web framework (if detected)
    package_manager: PackageManager = PIP        # Package/dependency manager
    app_root: Optional[str] = None               # Application root directory
    commands: Dict[str, str] = field(default_factory=dict)  # Project commands
    confidence: float = 0.0                      # Detection confidence score (0-1)
```

#### Detection Methods

The service implements a hierarchical detection strategy:

1. **Language Detection** (`_detect_language`, lines 95-139):
   - Checks for language-specific files in priority order
   - Python: `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile`, `poetry.lock`, `uv.lock`
   - TypeScript: `tsconfig.json` or TypeScript in `package.json` dependencies
   - JavaScript: `package.json` without TypeScript
   - Go: `go.mod`
   - Rust: `Cargo.toml`
   - Java: `pom.xml`, `build.gradle`, `build.gradle.kts`
   - Default: Returns `Language.PYTHON`

2. **Package Manager Detection** (`_detect_package_manager`, lines 141-181):
   - Python: uv.lock > poetry.lock > Pipfile.lock > pip (default)
   - JavaScript/TypeScript: pnpm-lock.yaml > yarn.lock > bun.lockb > npm (default)
   - Go: go mod
   - Rust: cargo
   - Java: pom.xml (maven) or gradle (default)

3. **Framework Detection** (`_detect_framework`, lines 183-251):
   - Python: Parses dependencies from pyproject.toml/requirements.txt
   - JavaScript/TypeScript: Parses package.json dependencies and devDependencies
   - Go: Searches go.mod content for framework imports
   - Rust: Searches Cargo.toml content for framework dependencies
   - Java: Searches pom.xml content for "spring"
   - Returns `Framework.NONE` if no framework detected

4. **App Root Detection** (`_detect_app_root`, lines 253-279):
   - Checks common directories: `src`, `app`, `lib`
   - For Python: Searches for directories containing `__init__.py`
   - Default: Returns `"."` (current directory)

5. **Command Detection** (`_detect_commands`, lines 281-338):
   - JavaScript/TypeScript: Extracts scripts from package.json (start/dev, test, lint, build)
   - Python: Limited support for pyproject.toml scripts (entry points)
   - Constructs command strings with appropriate package manager prefix

#### Helper Methods

- `_read_package_json` (lines 340-358): Safely parses package.json with error handling
- `_get_python_deps` (lines 360-403): Extracts Python dependencies from pyproject.toml and requirements.txt, handling various version specifiers

#### Python Version Compatibility

Lines 24-31 handle conditional import of TOML parser:
- Python 3.11+: Uses built-in `tomllib`
- Python 3.10: Falls back to `tomli` library
- Gracefully handles missing tomli by setting to `None`

## How to Use

### Basic Usage

```python
from pathlib import Path
from tac_bootstrap.application.detect_service import DetectService

# Initialize service
detector = DetectService()

# Detect project at path
detected = detector.detect(Path("/path/to/project"))

# Access results
print(f"Language: {detected.language}")
print(f"Package Manager: {detected.package_manager}")
print(f"Framework: {detected.framework}")
print(f"App Root: {detected.app_root}")
print(f"Commands: {detected.commands}")
print(f"Confidence: {detected.confidence}")
```

### Integration with Wizard

The service is designed to be integrated with the `add-agentic` wizard:

```python
from tac_bootstrap.application.detect_service import DetectService
from pathlib import Path

# Detect existing project
detector = DetectService()
detected = detector.detect(Path.cwd())

# Use detected values as wizard defaults
default_language = detected.language
default_package_manager = detected.package_manager
default_framework = detected.framework or Framework.NONE
suggested_commands = detected.commands

# User can override any detected value in wizard
```

### Example Detection Results

For the tac_bootstrap_cli project itself:
- Language: `PYTHON`
- Package Manager: `UV`
- Framework: `NONE` (CLI tool, not a web framework)
- App Root: `tac_bootstrap` (directory with `__init__.py`)
- Commands: `{}` (empty, as pyproject.toml scripts are entry points)

For a Next.js project:
- Language: `TYPESCRIPT`
- Package Manager: `NPM` or `PNPM` (based on lock file)
- Framework: `NEXTJS`
- App Root: `src` or `app`
- Commands: `{"start": "npm run dev", "build": "npm run build", "test": "npm test"}`

## Configuration

No configuration required. The service operates by analyzing files in the target repository.

## Testing

### Manual Testing

Test the service on the tac_bootstrap_cli repository:

```bash
cd tac_bootstrap_cli
uv run python -c "
from pathlib import Path
from tac_bootstrap.application.detect_service import DetectService

detector = DetectService()
detected = detector.detect(Path('.'))
print(f'Language: {detected.language}')
print(f'Package Manager: {detected.package_manager}')
print(f'Framework: {detected.framework}')
print(f'App Root: {detected.app_root}')
print(f'Confidence: {detected.confidence}')
"
```

### Validation Commands

All validation commands pass with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short    # Unit tests
cd tac_bootstrap_cli && uv run ruff check .                   # Linting
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/            # Type check
cd tac_bootstrap_cli && uv run tac-bootstrap --help           # Smoke test
```

## Notes

### Design Decisions

- **No external APIs**: All detection is performed locally by analyzing files
- **Defensive parsing**: All file parsing wrapped in try/except to handle malformed files gracefully
- **Priority-based detection**: When multiple indicators exist, uses well-defined priority order
- **Optional returns**: Uses `Optional[Framework]` and `Optional[str]` for values that may not be detected
- **Reasonable defaults**: Falls back to sensible defaults (Python language, pip package manager) when detection fails

### Known Limitations

- **Confidence score hardcoded**: Currently returns 0.8 for all detections; TODO: implement real confidence calculation based on number of indicators found
- **No monorepo support**: Returns the most prominent language; doesn't handle multi-language projects
- **Framework priority**: If multiple frameworks detected, returns first match (e.g., FastAPI before Django for Python)
- **Limited Python command detection**: pyproject.toml scripts are entry points, not shell commands, so command detection is limited for Python projects
- **No deep analysis**: Only analyzes dependency declarations, not actual code imports or usage

### Future Enhancements

- Calculate real confidence score based on quantity and quality of indicators
- Support monorepo detection with multiple sub-projects
- Detect multiple frameworks and let user choose
- Enhanced Python command detection from common patterns (Makefile, scripts/, etc.)
- Cache detection results to avoid re-scanning on repeated calls
- Detect testing frameworks (pytest, jest, etc.) separately from web frameworks
- Detect additional tools (docker, kubernetes, CI/CD configs)

### Integration Points

This service will be consumed by:
- `WizardService` in the `add-agentic` command to pre-populate wizard defaults
- `DoctorService` (future) to validate detected stack against installed tools
- `ScaffoldService` (future) to customize template selection based on detected framework

### Edge Cases Handled

1. **Empty repository**: Returns Python with pip as defaults
2. **Malformed package.json**: Returns `None` without crashing
3. **Missing pyproject.toml dependencies**: Returns empty list
4. **Multiple lock files**: Uses priority order (uv > poetry > pipenv for Python)
5. **No app_root found**: Returns `"."` as default
6. **Missing scripts in package.json**: Returns empty commands dict
7. **TypeScript as JS dependency**: Correctly identifies as TypeScript project
8. **Missing tomli on Python 3.10**: Gracefully skips TOML parsing
